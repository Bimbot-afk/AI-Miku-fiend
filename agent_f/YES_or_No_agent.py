import os
from docx import Document

WIP_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "WIP.md")
essay_docx = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_creations", "essay.docx") 

def yes_or_no(query, cc):

    with open(WIP_file, "r", encoding="utf-8") as f:
        essay_wip = f.read()

    prompt = f"""
    Read the next essay and answer "YES" or "NO" if the essay meets this requeriments:

    - The essay is well-structured.
    - The essay is well-written.
    - The essay is well-organized.
    - The essay is well-researched.
    - The essay is well-cited.

    Do not write anything else, just "YES" or "NO".
    """
    history = [{'role': 'user', 'content': prompt + str(essay_wip)}]
    from agent_functions.essay_agent_brain import sync_llm_call
    print("[SYSTEM] Auditing agent is deciding...")
    veredict = sync_llm_call(history)
    
    is_approved = veredict_check(veredict)
    if is_approved or cc == 1:
        create_essay_docx(essay_wip)
        return True
    else:
        return False
   
def veredict_check(veredict):
    return "YES" in veredict.upper()

def create_essay_docx(essay_wip):
    doc = Document()
    doc.add_paragraph(essay_wip)
    doc.save(essay_docx)
    print(f"[SYSTEM] Essay created successfully: {essay_docx}")
