import os
from ddgs import DDGS
import json

#Documento donde se almacena la info
research_md = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent")
research_file = os.path.join(research_md, "research.md")

def research(query, max_results=20):
    os.makedirs(research_md, exist_ok=True)
    try:
        resultados = []
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            for r in results:
                resultados.append(r)
        
        with open(research_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(resultados, indent=2, ensure_ascii=False))
    except Exception as e:
        with open(research_file, "w", encoding="utf-8") as f:
            f.write(f"Error en la investigación: {e}")

    