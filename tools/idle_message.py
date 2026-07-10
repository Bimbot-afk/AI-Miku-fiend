from core.brain import consultar_miku
from tools.read_memory import read_notifications, read_session
from UI.configuration import configurationMiku
from tools.music_listener import read_music_info_wrapper

def read_session_data():
    return {
        "notificationes del usuario": read_notifications(),
        "sess actual del user": read_session(),
        "ultima canción escuchada": read_music_info_wrapper()
    }


def create_idle_message(main_window):
    from UI.MainWindow import MainWindow
    ms_to_seconds = main_window.miku_idle_timer
    main_window.idle_timer.start(ms_to_seconds)
    print(f"miku idle time {ms_to_seconds/60000} minutes")

    from core.miku_config_manager import load_memory_data
    idiom = load_memory_data().get("soul", {}).get("idiom", "Español")

    prompt = f"[SISTEMA]: El usuario no te ha hablado en un buen rato. Inicia tú la conversación. Escribe un mensaje natural y corto como si le estuvieras hablando por chat, usa esta information, se lo mas personal posible: [CRITICAL: Escribe tu respuesta obligatoriamente en este idioma: {idiom}]"
    history = [{'role': 'user', 'content': prompt + str(read_session_data())}]
    
    worker = consultar_miku(history, [])
    main_window.active_agent_workers.append(worker)
    
    if main_window.config_window is None:
        main_window.config_window = configurationMiku(main_window)
    worker.miku_config()

    worker.finished_response.connect(main_window.show_miku_reaction)
    worker.finished.connect(lambda: main_window.cleanup_worker(worker))
    worker.start()
