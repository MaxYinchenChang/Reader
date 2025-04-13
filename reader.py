import tkinter as tk
import customtkinter as ctk
from tkinterweb import HtmlFrame
from bs4 import BeautifulSoup
import re

class OptimizedHTMLEditor:
    def __init__(self, html_file):
        # 初始化主窗口
        self.root = ctk.CTk()
        self.root.title("HTML格式编辑器")
        self.root.geometry("1100x700")
        
        # 保存文件路径
        self.html_file = html_file
        
        # 加载并解析原始HTML
        self.original_html = self.load_html_file(html_file)
        self.current_html = self.original_html
        
        # 创建界面
        self.create_widgets()
        self.update_preview()
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def load_html_file(self, file_path):
        """加载HTML文件并处理转义字符"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # 处理常见的转义字符
                content = content.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
                return content
        except Exception as e:
            print(f"加载文件错误: {e}")
            return """<!DOCTYPE html>
<html>
<head><title>错误</title></head>
<body><h1>无法加载文件</h1></body>
</html>"""
    
    def create_widgets(self):
        """创建界面组件"""
        # 主布局 - 左侧预览区，右侧工具栏
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=5)  # 预览区占5份
        self.root.grid_columnconfigure(1, weight=1)  # 工具栏占1份
        
        # 预览区域（左侧）
        preview_container = ctk.CTkFrame(self.root)
        preview_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.tk_preview = tk.Frame(preview_container)
        self.tk_preview.pack(fill="both", expand=True)
        
        self.html_preview = HtmlFrame(self.tk_preview)
        self.html_preview.pack(fill="both", expand=True)
        
        # 工具栏区域（右侧）
        toolbar = ctk.CTkFrame(self.root)
        toolbar.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # 工具栏标题
        ctk.CTkLabel(toolbar, text="格式设置", font=("Arial", 14)).pack(pady=(10, 20))
        
        # 文字样式部分
        self.create_style_buttons(toolbar)
        
        # 颜色选择部分
        self.create_color_selector(toolbar)
        
        # 重置按钮
        ctk.CTkButton(toolbar, text="重置所有样式", 
                      command=self.reset_styles, 
                      width=100, height=30,
                      fg_color="#FF5555").pack(pady=20)
    
    def create_style_buttons(self, parent):
        """创建文字样式按钮"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(frame, text="文字样式").pack(anchor="w", padx=5)
        
        # 使用更小的按钮
        btn_params = {"width": 80, "height": 30, "corner_radius": 5}
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=5)
        
        ctk.CTkButton(btn_frame, text="粗体", 
                      command=lambda: self.toggle_style("font-weight", "bold", "normal"),
                      **btn_params).pack(pady=2)
        
        ctk.CTkButton(btn_frame, text="斜体", 
                      command=lambda: self.toggle_style("font-style", "italic", "normal"),
                      **btn_params).pack(pady=2)
        
        ctk.CTkButton(btn_frame, text="下划线", 
                      command=lambda: self.toggle_style("text-decoration", "underline", "none"),
                      **btn_params).pack(pady=2)
    
    def create_color_selector(self, parent):
        """创建颜色选择器"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(frame, text="文字颜色").pack(anchor="w", padx=5)
        
        # 颜色选项
        colors = [
            ("黑色", "#000000"),
            ("红色", "#FF0000"),
            ("绿色", "#00FF00"),
            ("蓝色", "#0000FF"),
            ("紫色", "#800080"),
            ("橙色", "#FFA500")
        ]
        
        for name, code in colors:
            btn = ctk.CTkButton(
                frame, 
                text=name, 
                fg_color=code,
                hover_color=code,
                text_color="#FFFFFF" if code != "#000000" else "#FFFFFF",
                command=lambda c=code: self.apply_style("color", c),
                width=80,
                height=30,
                corner_radius=5
            )
            btn.pack(pady=2)
    
    def toggle_style(self, property, value_on, value_off):
        """切换样式状态"""
        soup = BeautifulSoup(self.current_html, 'html.parser')
        protected_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'title']
        
        for tag in soup.find_all(['p', 'span', 'div', 'li', 'td']):
            if tag.name not in protected_tags:
                styles = {}
                if tag.get('style'):
                    styles = dict(s.split(":") for s in tag['style'].split(";") if s)
                
                # 切换样式
                current_value = styles.get(property, value_off)
                styles[property] = value_on if current_value == value_off else value_off
                tag['style'] = ";".join(f"{k}:{v}" for k, v in styles.items())
        
        self.current_html = str(soup)
        self.update_preview()
    
    def apply_style(self, property, value):
        """应用样式"""
        soup = BeautifulSoup(self.current_html, 'html.parser')
        protected_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'title']
        
        for tag in soup.find_all(['p', 'span', 'div', 'li', 'td']):
            if tag.name not in protected_tags:
                styles = {}
                if tag.get('style'):
                    styles = dict(s.split(":") for s in tag['style'].split(";") if s)
                
                styles[property] = value
                tag['style'] = ";".join(f"{k}:{v}" for k, v in styles.items())
        
        self.current_html = str(soup)
        self.update_preview()
    
    def reset_styles(self):
        """重置所有样式"""
        self.current_html = self.original_html
        self.update_preview()
    
    def update_preview(self):
        """更新HTML预览"""
        self.html_preview.load_html(self.current_html)
    
    def save_changes(self):
        """保存修改到文件"""
        try:
            with open(self.html_file, "w", encoding="utf-8") as f:
                f.write(self.current_html)
            print("修改已保存")
        except Exception as e:
            print(f"保存文件错误: {e}")
    
    def on_close(self):
        """窗口关闭事件处理"""
        self.save_changes()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

# 使用示例
if __name__ == "__main__":
    # 替换为你的HTML文件路径
    editor = OptimizedHTMLEditor(r"alpha1.0-bata1.0\assets\test_file\tkinterweb_test.html")
    editor.run()