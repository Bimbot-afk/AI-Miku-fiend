import sys
from PySide6.QtWidgets import QApplication
from UI.MainWindow import MainWindow
from UI.ChatbotWindowMiku import ChatbotWindowMiku
from PySide6.QtCore import QTimer

app = QApplication(sys.argv)
try:
    window = MainWindow()
    chat = ChatbotWindowMiku(window)
    chat.user_input.setText("Hola Miku!")
    chat.send_message()
    print("send_message executed successfully!")
    
    def on_finished(response):
        print("Miku responded:", response)
        app.quit()
        
    chat.active_workers[0].finished_response.connect(on_finished)
    QTimer.singleShot(30000, lambda: (print("Timeout!"), app.quit()))
    app.exec()
except Exception as e:
    import traceback
    traceback.print_exc()
