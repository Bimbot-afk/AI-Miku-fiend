import os
import core.brain

WIP_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "WIP.md")

def edit_the_essay():
    with open(WIP_file, "r", encoding="utf-8") as f:
        essay = f.read()
    
    prompt = f"""
    You are an expert editing agent tasked with editing the following essay:

    Your task is to edit the essay to improve its clarity, logic, and overall quality, write in the essay the corrections to be made, do not replace.

    dont be a dictator, if the essay is good, do not make corrections, and then you should say in the essay "the essay is good, no corrections needed"
    """
    history = [{'role': 'user', 'content': prompt + str(essay)}]
    worker = core.brain.consultar_miku(history, [])
    worker.miku_config()
    response_editor = worker.response
    worker.start()
    create_review_(response_editor)

def create_review_(response_editor):
    with open(WIP_file, "w", encoding="utf-8") as f:
        f.write(response_editor)