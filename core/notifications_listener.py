import asyncio
from winsdk.windows.ui.notifications.management import UserNotificationListener  # type: ignore
from winsdk.windows.ui.notifications import NotificationKinds  # type: ignore
from PySide6.QtCore import QThread, Signal
import os

class NotificationWorker(QThread):
    notification_received = Signal(dict)

    def __init__(self):
        super().__init__()
        self.running = True
        self.seen_ids = set()
        
        # Archivo para guardar el historial de notificaciones
        self.notifications_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "notifications.md")
        os.makedirs(os.path.dirname(self.notifications_file), exist_ok=True)

    def run(self):
        asyncio.run(self.listen_loop())

    async def listen_loop(self):
        listener = UserNotificationListener.current
        access_status = await listener.request_access_async()

        if access_status != 1:
            print("[SYSTEM] Access to User Notifications Denied")
            return

        # Para no procesar notificaciones viejas al abrir la app
        try:
            initial_notis = await listener.get_notifications_async(NotificationKinds.TOAST)
            for noti in initial_notis:
                self.seen_ids.add(noti.id)
        except Exception:
            pass

        while self.running:
            try:
                notifications = await listener.get_notifications_async(NotificationKinds.TOAST)
                
                for noti in notifications:
                    noti_id = noti.id
                    if noti_id in self.seen_ids:
                        continue
                        
                    self.seen_ids.add(noti_id)
                    
                    try:
                        app_name = noti.app_info.display_info.display_name
                        noti_time = noti.creation_time
                        
                        binding = noti.notification.visual.get_binding("ToastGeneric")
                        elements_text = binding.get_text_elements()

                        title = elements_text[0].text if len(elements_text) > 0 else "Sin título"
                        content = elements_text[1].text if len(elements_text) > 1 else ""

                        noti_dict = {
                            "app_name": app_name,
                            "notification_time": str(noti_time),
                            "title": title,
                            "content": content
                        }

                        self.upload_notification(noti_dict)
                        self.notification_received.emit(noti_dict)
                    except Exception as e:
                        print(f"Error procesando una notificación: {e}")

            except Exception as e:
                print(f"Error polling notifications: {e}")
                
            await asyncio.sleep(2)
            
    def upload_notification(self, noti_dict):
        try:
            with open(self.notifications_file, "a", encoding="utf-8") as f:
                f.write(f"- **[{noti_dict['app_name']}]** {noti_dict['title']}: {noti_dict['content']}\n")
        except Exception as e:
            print(f"Error saving notification: {e}")

    def stop(self):
        self.running = False

