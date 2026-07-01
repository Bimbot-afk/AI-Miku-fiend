from core.brain import consultar_miku
from tools.read_memory import read_notifications, read_session
from UI.configuration import configurationMiku

def read_session_data():
    return {
        "notificationes del usuario": read_notifications(),
        "sess actual del user": read_session()
    }


def create_idle_message(main_window):
    from UI.MainWindow import MainWindow
    from tools.get_weather import read_weather_result
    
    ms_to_seconds = main_window.miku_idle_timer
    main_window.idle_timer.start(ms_to_seconds)
    print(f"miku idle time {ms_to_seconds/60000} minutes")

    weather_info = read_weather_result()
    weather_context = f"\n\nContexto del clima actual:\n{weather_info}" if weather_info else ""

    prompt = f"[SISTEMA]: El usuario no te ha hablado en un buen rato. Inicia tú la conversación. Escribe un mensaje natural y corto como si le estuvieras hablando por chat.{weather_context}"
    history = [{'role': 'user', 'content': prompt}]
    
    worker = consultar_miku(history, [])
    main_window.active_agent_workers.append(worker)
    
    if main_window.config_window is None:
        main_window.config_window = configurationMiku(main_window)
    worker.miku_config()

    worker.finished_response.connect(main_window.show_miku_reaction)
    worker.finished.connect(lambda: main_window.cleanup_worker(worker))
    worker.start()
