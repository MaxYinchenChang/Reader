import customtkinter as ctk
import pywinstyles

class Conpanion(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('既定阅读计划')
        self.geometry('1000x618')
        self.resizable(False, False)
        pywinstyles.apply_style(self, style='acrylic')
