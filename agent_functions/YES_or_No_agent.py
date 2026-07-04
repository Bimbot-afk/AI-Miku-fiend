import os
from docx import Document
import core.brain

WIP_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "WIP.md")
essay_docx = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "essay.docx")

def yes_or_no(query):

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
    
    worker = core.brain.consultar_miku(history, [])
    worker.miku_config()
    worker.start()
    veredict = worker.response
    
    is_approved = veredict_check(veredict)
    if is_approved:
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
    print(f"Essay created successfully: {essay_docx}")
