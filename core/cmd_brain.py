class Brain_cmd:
    def __init__(self):
        self.response = ""
    
    def decide_comand(self, comand):
        parts = comand.strip().split(maxsplit=2)
        if len(parts) < 2:
            self.response = "invalid command format. Use: /save <arg> <text> or /read <arg>"
            return self.response
            
        cmd = parts[0].lower()
        argument = parts[1].lower()
        text = parts[2] if len(parts) > 2 else ""
        self.were_web_search = False
        
        if cmd == "/save":
            if not text:
                self.response = "please specify the text to save."
                return self.response
                
            if argument == "soul":
                from tools import open_txt_file
                open_txt_file.save_soul(text)
                self.response = f"miku has saved the soul info: '{text}'"
            elif argument == "memory":
                from tools import open_txt_file
                open_txt_file.save_general_memorie(text)
                self.response = f"miku has saved the memory info: '{text}'"
            elif argument == "session":
                from tools import open_txt_file
                open_txt_file.save_memory_session(text)
                self.response = f"miku has saved the session info: '{text}'"
            else:
                self.response = f"unknown save argument: '{argument}'"
                
            return self.response

        elif cmd == "/read":
            from tools import read_memory, music_listener
            if argument == "soul":
                text_to_read = read_memory.read_soul()
                self.response = text_to_read if text_to_read else "(empty soul)"
            elif argument == "memory":
                text_to_read = read_memory.read_memory()
                self.response = text_to_read if text_to_read else "(empty memory)"
            elif argument == "session":
                text_to_read = read_memory.read_session()
                self.response = text_to_read if text_to_read else "(empty session)"
            elif argument == "music":
                text_to_read = music_listener.read_music_info_wrapper()
                self.response = text_to_read if text_to_read else "(empty music)"
            else:
                self.response = f"unknown read argument: '{argument}'"
                
            return self.response

        elif cmd == "/web_search":
            if not text:
                self.response = "please specify the text to search."
                return self.response
                
            from tools import web_search
            web_search.web_search(text)
            self.response = "web search completed"
            self.were_web_search = True

            return self.response
            
        else:
            self.response = "unknown command"
            return self.response

    def return_miku_cmd(self):
        return self.response
