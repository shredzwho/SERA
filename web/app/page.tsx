"use client";

import React, { useState, useEffect, useRef } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Neural link established. Shadow Dashboard initialized. How can I assist with your operation today?" }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg: Message = { role: "user", content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: [...messages, userMsg] }),
      });

      if (!response.ok) throw new Error("Failed to transmit to neural interface");

      const data = await response.json();
      setMessages(prev => [...prev, data]);
    } catch (error) {
      setMessages(prev => [...prev, { role: "assistant", content: `[CRITICAL ERROR]: ${error instanceof Error ? error.message : "Connection Lost"}` }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-full overflow-hidden p-4 gap-4 bg-background">
      {/* --- Sidebar (Navigation & Status) --- */}
      <aside className="w-16 flex flex-col items-center py-6 gap-8 glass rounded-2xl glow-border">
        <div className="w-10 h-10 rounded-lg bg-cyber-blue/20 flex items-center justify-center border border-cyber-blue shadow-[0_0_10px_rgba(0,242,255,0.5)]">
          <span className="text-cyber-blue font-bold">Ξ</span>
        </div>
        <nav className="flex flex-col gap-6 text-zinc-500">
          <button className="hover:text-cyber-blue transition-colors">◈</button>
          <button className="hover:text-cyber-blue transition-colors">▣</button>
          <button className="hover:text-cyber-blue transition-colors">⚙</button>
        </nav>
      </aside>

      {/* --- Main Dashboard Area --- */}
      <div className="flex-1 flex flex-col gap-4 overflow-hidden">
        
        {/* Top Section: Chat + Terminal */}
        <div className="flex-1 flex gap-4 min-h-0">
          
          {/* Main Chat Panel */}
          <section className="flex-[1.5] flex flex-col glass rounded-2xl glow-border overflow-hidden">
            <header className="p-4 border-b border-white/5 flex items-center justify-between">
              <h2 className="text-xs font-mono tracking-widest text-cyber-blue/80 uppercase">Sera // Neural Interface</h2>
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${isLoading ? 'bg-amber-500 animate-ping' : 'bg-matrix-green'} `}></span>
                <span className="text-[10px] font-mono text-zinc-400">{isLoading ? 'PROCESSING // LINK ACTIVE' : 'ENCRYPTED // ACTIVE'}</span>
              </div>
            </header>
            
            {/* Messages Area */}
            <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 flex flex-col gap-6 scroll-smooth">
              {messages.map((msg, idx) => (
                <div key={idx} className={`flex flex-col gap-1 max-w-[85%] ${msg.role === "user" ? "self-end items-end" : "self-start items-start"}`}>
                  <p className="text-[10px] uppercase font-mono text-cyber-blue/60 ml-1">{msg.role === "user" ? "Operator" : "Sera"}</p>
                  <div className={`p-4 rounded-2xl text-sm ${
                    msg.role === "user" 
                      ? "bg-white/5 border border-white/10 rounded-tr-none text-zinc-200" 
                      : "bg-cyber-blue/5 border border-cyber-blue/10 rounded-tl-none text-cyber-blue/90"
                  }`}>
                    {msg.content}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex flex-col gap-1 self-start items-start animate-pulse">
                  <p className="text-[10px] uppercase font-mono text-cyber-blue/60 ml-1">Sera</p>
                  <div className="bg-cyber-blue/5 border border-cyber-blue/10 p-4 rounded-2xl rounded-tl-none italic opacity-50">
                    Thinking...
                  </div>
                </div>
              )}
            </div>

            {/* Input Hook */}
            <footer className="p-4 bg-white/5 border-t border-white/5">
              <div className="relative">
                <input 
                  type="text" 
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSend()}
                  disabled={isLoading}
                  placeholder={isLoading ? "Sera is processing..." : "Transmit command to Sera..."}
                  className="w-full bg-[#0d0e11] border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-cyber-blue focus:ring-1 focus:ring-cyber-blue/50 transition-all font-mono"
                />
                <button 
                  onClick={handleSend}
                  disabled={isLoading}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-cyber-blue text-xs font-mono hover:glow-text disabled:opacity-30 disabled:hover:glow-none"
                >
                  SEND [ENTER]
                </button>
              </div>
            </footer>
          </section>

          {/* Right Panel: Tool Execution / Terminal */}
          <section className="flex-1 flex flex-col glass rounded-2xl glow-border overflow-hidden bg-black/40">
             <header className="p-4 border-b border-white/5">
              <h2 className="text-xs font-mono tracking-widest text-neon-crimson uppercase">Nexus // Execute Activity</h2>
            </header>
            <div className="flex-1 p-4 font-mono text-[11px] overflow-y-auto terminal-text">
              <p className="opacity-40">-- INCOMING LOGS --</p>
              <p className="mt-2">[SYSTEM] Dashboard v0.1.0 online</p>
              <p>[SYSTEM] WebSocket listener ready</p>
              <p className="text-white/20 mt-4 italic">Scanning for tool signatures...</p>
            </div>
          </section>
        </div>

        {/* Bottom Section: Knowledge Base / Assets */}
        <div className="h-48 flex gap-4 overflow-hidden">
          <section className="flex-1 glass rounded-2xl glow-border p-4 overflow-hidden flex flex-col">
            <h3 className="text-[10px] font-mono tracking-tighter text-zinc-500 uppercase mb-3">Retrieved Knowledge // RAG</h3>
            <div className="flex gap-4 overflow-x-auto pb-2 h-full">
              {[1, 2, 3].map((i) => (
                <div key={i} className="min-w-[240px] h-full bg-white/5 border border-white/5 rounded-xl p-3 flex flex-col justify-between hover:border-cyber-blue/30 transition-colors group">
                  <div>
                    <div className="text-[10px] text-cyber-blue mb-1 group-hover:glow-text transition-all">CVE-2026-X00{i}</div>
                    <div className="text-xs font-semibold line-clamp-2 text-zinc-300">Exploit analysis for high-priority target #{i}...</div>
                  </div>
                  <div className="text-[10px] text-zinc-600 font-mono">CONFIDENCE: {90 + i}%</div>
                </div>
              ))}
            </div>
          </section>
        </div>

      </div>
    </div>
  );
}


