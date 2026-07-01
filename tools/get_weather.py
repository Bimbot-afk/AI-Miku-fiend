from duckduckgo_search import DDGS
from core.miku_config_manager import load_soul_data
import os

def get_weather():
    soul_data = load_soul_data()
    city_name = soul_data.get("city", "Bogotá")
    weather_text = ""
    try:
        with DDGS() as ddgs:
            results = ddgs.text(f"weather in {city_name}", max_results=2)
            for r in results:
                titulo = r.get("title", "Sin título")
                snippet = r.get("body", "Sin descripción")
                url = r.get("href", "#")
                weather_text += f"**{titulo}**\n{snippet}\nFuente: {url}\n\n"
    except Exception as e:
        print(f"Error al buscar el clima: {e}")
        return None
    
    path_results = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent")
    os.makedirs(path_results, exist_ok=True)
    file = os.path.join(path_results, "weather_result.md")
    
    with open(file, "w", encoding="utf-8") as f:
        f.write(weather_text)
    print(f"Clima guardado en {file}")
    return weather_text

def read_weather_result():
    path_results = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent")
    file = os.path.join(path_results, "weather_result.md")
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""
