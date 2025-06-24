from ebooklib import epub
from bs4 import BeautifulSoup
import os
import shutil

def epub2html_advanced(epub_path, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 读取EPUB文件
    book = epub.read_epub(epub_path)
    
    # 创建资源文件夹
    resources_dir = os.path.join(output_folder, "resources")
    if not os.path.exists(resources_dir):
        os.makedirs(resources_dir)
    
    # 处理所有项目
    for item in book.get_items():
        # 处理文档内容
        if item.get_type() == epub.ITEM_DOCUMENT:
            file_name = f"{item.get_id()}.html"
            output_path = os.path.join(output_folder, file_name)
            
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            
            # 写入文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            
            print(f"已保存HTML: {output_path}")
        
        # 处理图片和样式表等资源
        elif item.get_type() in [epub.ITEM_IMAGE, epub.ITEM_STYLE]:
            # 获取文件名
            if hasattr(item, 'file_name'):
                file_name = item.file_name
            else:
                file_name = item.get_id()
            
            # 确保文件名有效
            file_name = os.path.basename(file_name)
            output_path = os.path.join(resources_dir, file_name)
            
            # 写入文件
            with open(output_path, 'wb') as f:
                f.write(item.get_content())
            
            print(f"已保存资源: {output_path}")

# 使用示例
if __name__ == "__main__":
    epub_file = r"alpha1.0-bata1.0\example.epub"  # 替换为你的EPUB文件路径
    output_dir = r"alpha1.0-bata1.0\data\book"  # 输出文件夹
    
    epub2html_advanced(epub_file, output_dir)
    print("高级转换完成！")