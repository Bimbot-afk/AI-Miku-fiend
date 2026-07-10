TRANSLATIONS = {
    "Español": {
        "thinking": "Miku está pensando",
        "error_api": "Error: API_KEY o Server URL no encontrado",
        "chat_restarted": "Chat reiniciado",
        "btn_send": "Enviar",
        "btn_restart": "Reiniciar",
        "placeholder": "Escríbele a Miku aquí...",
        "popup_title": "Miku dice:"
    },
    "English": {
        "thinking": "Miku is thinking",
        "error_api": "Error: API_KEY or Server URL not found",
        "chat_restarted": "Chat restarted",
        "btn_send": "Send",
        "btn_restart": "Restart",
        "placeholder": "Text Miku here...",
        "popup_title": "Miku says:"
    },
    "日本語": {
        "thinking": "ミクは考えています",
        "error_api": "エラー：API_KEYまたはサーバーURLが見つかりません",
        "chat_restarted": "チャットを再起動しました",
        "btn_send": "送信",
        "btn_restart": "再起動",
        "placeholder": "ここにメッセージを入力...",
        "popup_title": "ミク："
    }
}

def get_text(idiom, key):
    lang_dict = TRANSLATIONS.get(idiom, TRANSLATIONS["Español"]) 
    return lang_dict.get(key, key) 
