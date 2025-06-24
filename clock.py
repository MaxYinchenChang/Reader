'''
闹铃提醒阅读开始与结束。
'''

import tkinter as tk
import json
import companion


with open(r'alpha1.0-bata1.0\data\settings\clock.json') as f:
    settings = json.loads(f.read())

class Clock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        

        # 获取屏幕宽高
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 根据设置放置窗口
        window_place = settings.get('window place', 'top')
        if window_place == 'top':
            self.geometry(f'{screen_width}x70+0+0')
            width, height = screen_width, 70
        elif window_place == 'bottom':
            self.geometry(f'{screen_width}x70+0+{screen_height - 120}')
            # 尝试适配不同任务栏，保证不被遮挡。
            width, height = screen_width, 70

        # 创建背景画布
        tk.Canvas(self, width=width, height=height, bg=settings['background']).pack(fill=tk.BOTH, expand=True)

        # 确保图标路径正确并加载
        self.alarms = tk.PhotoImage(file=r'alpha1.0-bata1.0\assets\round_access_alarms_black_48.png')
        # 布置控件
        tk.Label(self, image=self.alarms, bg=settings['background']).place(x=0, y=-3)
        tk.Label(self, text='准备开始进行阅读计划', font=('黑体', 16), bg=settings['background']).place(x=80, y=10)
        tk.Label(self, text='请按回车键开始阅读，按ESC键拒绝', font=('黑体', 12), bg=settings['background']).place(x=80, y=40)

        # 绑定事件
        self.bind('<Return>', func=self.reading_start)
        self.bind('<Escape>', func=self.reading_refuse)

    def reading_start(self, event=None):
        self.destroy()
        _companion = companion.Conpanion()
        _companion.mainloop()
        
    def reading_refuse(self, event=None):
        # 这里还需要完善功能：取消后记录计划未完成。
        self.destroy()


if __name__ == '__main__':
    clock = Clock()
    clock.mainloop()

