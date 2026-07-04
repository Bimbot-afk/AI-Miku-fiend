from tavily import TavilyClient
import os

api_key = os.getenv("research_api_key")
tavily = TavilyClient(api_key=api_key)

#Documento donde se almacena la info
research_md = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent")
research_file = os.path.join(research_md, "research.md")

def research(query):
    response = tavily.search(query=query, language="en", include_answer=True)
    os.makedirs(research_md, exist_ok=True)
    with open(research_file, "w", encoding="utf-8") as f:
        # Convert dictionary to string for saving
        import json
        f.write(json.dumps(response, indent=2, ensure_ascii=False))

    