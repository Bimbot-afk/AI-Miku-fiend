from ddgs import DDGS
import os

path_results = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent")
path_results_file = os.path.join(path_results, "research_results.md")

def create_research_answer_file(results):
    os.makedirs(path_results, exist_ok=True)
    with open(path_results_file, "w", encoding="utf-8") as f:
        f.write(results)

def delete_research_file():
    if os.path.exists(path_results_file):
        os.remove(path_results_file)

def web_search(query, max_results=4):
    try:
        resultados_md = f"### Resultados de la búsqueda para: '{query}'\n\n"
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            for r in results:
                titulo = r.get("title", "Sin título")
                snippet = r.get("body", "Sin descripción")
                url = r.get("href", "#")
                resultados_md += f"**{titulo}**\n{snippet}\nFuente: {url}\n\n"
                
        create_research_answer_file(resultados_md)
    except Exception as e:
        create_research_answer_file(f"Error al buscar en internet: {e}")
