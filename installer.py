'''
This is the main installer script for the Alpha 1.0 Beta 1.0 version of the software.
'''

import customtkinter as ctk
import tkinter as tk
import pywinstyles

class InstallerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alpha 1.0 Beta 1.0 Installer")
        self.resizable(False, False)
        self.center_window()
        self.overrideredirect(True) # Remove window decorations

        self.step1 = ctk.CTkFrame(self, width=700, height=500)
        self.step1.place(x=0, y=0)
        ctk.CTkLabel(self.step1, 
                     text="配置和安装程序", font=("黑体", 16)).place(x=5, y=5)
        ctk.CTkButton(self.step1, text="取消", command=self.destroy, width=40).place(x=610, y=470)
        ctk.CTkButton(self.step1, text="确定", command=self.step2, width=40).place(x=655, y=470)

        # Corrected image loading
        self.progress_image1 = tk.PhotoImage(file=r"alpha1.0-bata1.0\assets\install_progress1.png")
        self.progress_image2 = tk.PhotoImage(file=r"alpha1.0-bata1.0\assets\install_progress2.png")
        self.progress_bar = tk.Label(self.step1, image=self.progress_image1).place(x=0, y=380)

    def center_window(self):
        """Centers the window on the screen."""
        self.update_idletasks()  # Ensure the window dimensions are calculated
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (700 // 2)
        y = (screen_height // 2) - (500 // 2)

        self.geometry(f"{700}x{500}+{x}+{y}")
    
    def step2(self):
        """Switch to step 2 of the installation."""
        self.step1.place_forget()
        self.step2_frame = ctk.CTkFrame(self, width=700, height=500)
        self.step2_frame.place(x=0, y=0)
        self.progress_bar = tk.Label(self.step1, image=self.progress_image2).place(x=0, y=380)

if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()