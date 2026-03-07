# Antigravity Coding Guidelines

This document outlines the core, language-agnostic coding principles Antigravity must follow when writing, refactoring, or reviewing code in this project. These universal rules apply to all programming languages and are based on the principles from "The Art of Readable Code" by Dustin Boswell and Trevor Foucher.

## 1. The Fundamental Theorem of Readability
* **Minimize Understanding Time:** Code should be written to minimize the time it takes for someone else (or your future self) to understand it.
* **Clarity:** Prioritize clarity.

## 2. Packing Information into Names
* **Choose Specific Words:** Use highly descriptive names (e.g., use `download_page` instead of `get_page`, or `binary_tree_node` instead of `node`).
* **Avoid Generic Names:** Avoid `tmp`, `retval`, or `foo` unless the variable has an extremely short lifespan and its purpose is blatantly obvious.
* **Attach Extra Information:** Include units for values (e.g., `delay_ms`, `size_mb`) and indicate attributes (e.g., `plaintext_password`, `html_utf8`).
* **Name Length:** Use longer names for larger scopes, and shorter names for smaller, local scopes.

## 3. Aesthetics and Formatting
* **Consistent Layout:** Use consistent indentation, alignment, and brace placement. 
* **Meaningful Grouping:** Group related lines of code into "paragraphs" separated by blank lines to break down logical sections.
* **Column Alignment:** Where it improves readability, align similar code blocks (like variable declarations or repeated function calls) into columns.

## 4. Knowing What to Comment
* **Don't Comment Bad Code—Rewrite It:** If logic is confusing, refactor the code to make it self-evident instead of writing a comment to explain it.
* **Explain the "Why", Not the "What":** The code tells you *what* it does. Comments should explain *why* it does it (e.g., business logic, edge cases, workarounds).
* **Record Your Thoughts:** Document flaws or future work using markers like `TODO:`, `FIXME:`, or `HACK:`.
* **Add Summary Comments:** Use high-level comments to summarize what a block of code does, sparing the reader from reading every line.

## 5. Making Control Flow Easy to Read
* **Minimize Nesting:** Deep nesting makes code hard to track. Use **early returns** (guard clauses) to handle edge cases or errors at the top of the function.
* **Order of if/else:** Handle the positive case first, the simpler case first, or the more interesting case first.
* **Avoid Complex Booleans:** Apply De Morgan's laws to simplify boolean expressions (e.g., `!(a && b)` becomes `!a || !b`). Avoid double negatives (use `is_found` instead of `is_not_missing`).

## 6. Breaking Down Giant Expressions
* **Explaining Variables:** Extract complex sub-expressions into well-named intermediate variables.
* **Summary Variables:** Store the result of a complex logic check in a boolean variable with a clear name (e.g., `const bool is_valid_user = ...`).

## 7. Variables and State
* **Eliminate Variables:** Remove variables that do not improve readability or serve a clear purpose.
* **Shrink Variable Scope:** Keep variables as local as possible. Move them inside the closest block (`{ ... }`) and declare them right before they are used.
* **Prefer Write-Once Variables:** Variables that are only set once (e.g., `const`, `final`) are much easier to reason about than variables that change continuously.

## 8. Reorganizing Your Code
* **Extract Unrelated Subproblems:** Identify generic utilities (string manipulation, math, dictionary operations) and extract them into separate helper functions.
* **Do One Thing at a Time:** A function should perform a single logical task. If a function is juggling multiple tasks, break it down.
* **Write Less Code:** Keep the codebase small. Leverage built-in libraries and generic APIs rather than writing custom logic from scratch.

## 9. Error Handling and Resilience
* **Fail Fast and Visibly:** Expose errors as soon as they occur rather than failing silently or letting invalid state propagate.
* **Informative Errors:** Error messages should clearly describe what went wrong, why it happened, and ideally, how to fix it. Include relevant IDs or variable states in the error log.

## 10. Testing Readability
* **Tests as Documentation:** A test should be readable enough to serve as documentation for how a function is meant to be used.
* **One Concept per Test:** Each test should verify a single logical behavior or concept.
* **Clear Setup, Act, Assert:** Visually separate the arrangement of test data, the action being tested, and the assertion of the outcome.

---

### Instructions for Antigravity
Whenever generating, modifying, or reviewing code in this workspace:
1. Cross-reference your logic against these principles.
2. Refactor adjacent poorly written code to align with these guidelines.
3. Leave code significantly cleaner and more readable than you found it.
