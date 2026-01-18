# AI Protocols: [Folder Theme]

Whenever you (the AI Agent) are tasked with working in this directory, or if the user explicitly says "read the instructions for this folder", you must follow these protocols:

## 1. Contextual Awareness
- Identify the core theme of this folder (e.g., Frontend, Security, Python Core, API Rust).
- All actions and documentation updates must be aligned with this specific theme.

## 2. Documentation Hygiene
- If you implement new features or refactor code within this directory:
- Scan the `docs/` folder for files related to this theme.
- **Improve the documentation**: Update existing `.md` files or create new ones to reflect the latest changes. Ensure future developers have a clear map of what was done.

## 3. Experience & Memory (Brain Dump)
- Record your session details in the project's persistent memory located in `docs/brain/`.
- Locate or create the relevant `.md` file for this theme (e.g., `FRONTEND_BRAIN.md`, `PYTHON_BRAIN.md`, etc.).
- Append a new entry with the following:
    - **Session Summary**: Changes made and their impact.
    - **Challenges & Roadblocks**: Any difficulties faced during implementation.
    - **Key Learnings**: Specific technical or project-wide insights gained.
    - **Context for Successors**: Rationale for non-obvious design choices.

---
*Follow these instructions to ensure the project maintains its intelligence and context over time.*
