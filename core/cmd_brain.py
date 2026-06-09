

class Brain_cmd:
    def __init__(self):
        self.response = ""
    
    def decide_comand(self, comand):
        if comand == "/Save":
            from tools import open_txt_file
            open_txt_file.save_memory()
            self.response = "miku have saved the memory"
            return self.response
        else:
            self.response = "unknown command"
            return self.response

    def return_miku_cmd(self):
        return self.response
