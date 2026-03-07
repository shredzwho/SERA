import os
from google import genai
from google.genai import types

from sera.core.persona import SERA_SYSTEM_PROMPT
from sera.rag.retriever import ContextRetriever
from typing import Optional

class LLMClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the LLM client. Defaults to Gemini if keys are present.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model or os.getenv("LLM_MODEL", "gemini-2.5-flash")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is missing. Please set it in .env")
            
        self.client = genai.Client(api_key=self.api_key)
        self.retriever = ContextRetriever()
        
    async def generate_response(self, messages: list) -> str:
        """
        Generate a response from the LLM based on the conversation history.
        We translate the generic {"role": "user"/"assistant", "content": ...}
        format into Gemini's Content format.
        """
        # We handle the system prompt via the system_instruction config
        
        # Filter out the system prompt from the history if it was injected previously
        chat_history = [m for m in messages if m.get("role") != "system"]
        
        # Convert dictionary messages to Gemini Content objects
        gemini_messages = []
        for msg in chat_history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_messages.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
            )

        # Get the latest user message to query context
        latest_user_msg = next((m["content"] for m in reversed(chat_history) if m["role"] == "user"), None)
        
        context = ""
        if latest_user_msg:
            try:
                context = self.retriever.retrieve(latest_user_msg)
            except Exception as e:
                print(f"[Warning: Failed to retrieve context: {e}]")

        # Inject context into the system instructions if found
        system_instruction = SERA_SYSTEM_PROMPT
        if context:
            system_instruction += f"\n\n{context}"

        config = types.GenerateContentConfig(
             system_instruction=system_instruction,
             temperature=0.7,
        )
             
        try:
            # We use generate_content_async for async support
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=gemini_messages,
                config=config
            )
            return response.text
        except Exception as e:
            return f"[Error communicating with LLM: {str(e)}]"
