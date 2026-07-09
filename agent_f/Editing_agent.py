import os
import core.brain

WIP_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "WIP.md")

editor_notes_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "editor_notes.md")

def edit_the_essay():
    with open(WIP_file, "r", encoding="utf-8") as f:
        essay = f.read()
    
    prompt = f"""
    You are an expert editing agent tasked with reviewing the following essay:

    Your task is to read the essay and provide ONLY a bulleted list of corrections and suggestions to improve its clarity, logic, and overall quality.
    DO NOT rewrite the entire essay. Just output the feedback notes.

    If the essay is already very good and requires no changes, simply respond with: "The essay is good, no corrections needed."
    """
    history = [{'role': 'user', 'content': prompt + "\n\nEssay to review:\n" + str(essay)}]
    from agent_functions.essay_agent_brain import sync_llm_call
    print("[SYSTEM] Editing agent is reviewing...")
    response_editor = sync_llm_call(history)
    
    with open(editor_notes_file, "w", encoding="utf-8") as f:
        f.write(response_editor)
