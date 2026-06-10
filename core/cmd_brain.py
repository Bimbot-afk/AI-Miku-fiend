class Brain_cmd:
    def __init__(self):
        self.response = ""
    
    def decide_comand(self, comand):
        cmd_lower = comand.strip().lower()
        comand, argument, text = comand.split(maxsplit=2)
        if comand == "/save":
            if argument == "soul":
                text_to_save = text    
                from tools import open_txt_file
                open_txt_file.save_soul(text_to_save)

            if argument == "memory":
                text_to_save = text    
                from tools import open_txt_file
                open_txt_file.save_general_memorie(text_to_save)

            if argument == "session":
                text_to_save = text    
                from tools import open_txt_file
                open_txt_file.save_memory_session(text_to_save)
            
            if text_to_save:
                self.response = f"miku have saved the memory: '{text_to_save}'"
            else:
                self.response = "miku have saved the memory (empty)"
            return self.response
        else:
            self.response = "unknown command"
            return self.response

    def return_miku_cmd(self):
        return self.response



