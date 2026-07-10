import os
from core.brain import consultar_miku

research_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "research.md")
WIP_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "WIP.md")

editor_notes_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "editor_notes.md")

def draft_the_information(query, is_correction_cycle=False):

    with open(research_file, "r", encoding="utf-8") as f:
        research = f.read()

    editor_notes = ""
    previous_essay = ""
    if is_correction_cycle:
        if os.path.exists(editor_notes_file):
            with open(editor_notes_file, "r", encoding="utf-8") as f:
                editor_notes = f.read()
        if os.path.exists(WIP_file):
            with open(WIP_file, "r", encoding="utf-8") as f:
                previous_essay = f.read()

    prompt = f"""
    You are an expert drafting agent tasked with writing a comprehensive essay on the following topic:
    {query}

    Another agent has conducted the necessary research on this topic and it is provided below. 

    Your task is to draft a well-structured, high-quality essay based on this research. Ensure that your writing is clear, logical, and worthy of an A+ grade. The final draft will be reviewed by an auditing agent.
    """
    
    if is_correction_cycle:
        prompt += f"""
        
    IMPORTANT: This is a correction cycle. The editing agent has reviewed your previous draft and left the following corrections/comments:
    ---
    {editor_notes}
    ---
    
    Here is your PREVIOUS DRAFT:
    ---
    {previous_essay}
    ---
    
    Please rewrite the essay applying these corrections. Output ONLY the new essay, no conversational text.

    No more than 1500 words.

    if reviewer says "abrupt cut" reduce in a 20% th length of the essay.
    """

    history = [{'role': 'user', 'content': prompt + "\nResearch:\n" + str(research)}]
    
    from agent_f.essay_agent_brain import sync_llm_call
    print("[SYSTEM] Drafting agent is writing...")
    response = sync_llm_call(history)
    
    with open(WIP_file, "w", encoding="utf-8") as f:
        f.write(response)

def audit_the_essay():
    pass