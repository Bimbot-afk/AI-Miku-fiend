import os
from core.brain import consultar_miku

research_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "research.md")
WIP_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "WIP.md")

def draft_the_information(query, is_correction_cycle=False):

    with open(research_file, "r", encoding="utf-8") as f:
        research = f.read()

    editor_notes = ""
    if is_correction_cycle and os.path.exists(WIP_file):
        with open(WIP_file, "r", encoding="utf-8") as f:
            editor_notes = f.read()

    prompt = f"""
    You are an expert drafting agent tasked with writing a comprehensive essay on the following topic:
    {query}

    Another agent has conducted the necessary research on this topic and it is provided below. 

    Your task is to draft a well-structured, high-quality essay based on this research. Ensure that your writing is clear, logical, and worthy of an A+ grade. The final draft will be reviewed by an auditing agent.
    """
    
    if is_correction_cycle:
        prompt += f"""
        
    IMPORTANT: This is a correction cycle. The editing agent has reviewed the previous draft and left the following corrections/comments:
    ---
    {editor_notes}
    ---
    Please rewrite the essay applying these corrections, and remove the editor's comments from the final text.
    """

    history = [{'role': 'user', 'content': prompt + "\nResearch:\n" + str(research)}]
    
    worker = consultar_miku(history, [])
    worker.miku_config()
    worker.start()
    create_the_essay(worker)

def create_the_essay(worker):
    response = worker.response
    with open(WIP_file, "w", encoding="utf-8") as f:
        f.write(response)

def audit_the_essay():
    pass