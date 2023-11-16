'''
Created by Han Xu
email:736946693@qq.com
'''
import os
import re
import requests
from urllib.parse import urlparse

def process_markdown_file(current_dir, md_file_name):
    os.chdir(current_dir)

    # 图片素材文件夹
    img_dir = 'imgRes'+md_file_name if len('imgRes'+md_file_name)<=200 else 'imgRes'+md_file_name[:200]

    # 重新创建目录
    if os.path.exists(img_dir)==True:
        os.removedirs(img_dir)
        os.makedirs(img_dir)
    elif os.path.exists(img_dir)==False:
        os.makedirs(img_dir)


    with open(md_file_name, 'r', encoding='utf-8') as f:
        md_content = f.read()

    img_pattern = re.compile('!\[.*?\]\((http.*?)\)', re.IGNORECASE)
    img_matches = img_pattern.findall(md_content)

    for img_url in img_matches:
        img_name = os.path.basename(urlparse(img_url).path)
        img_path = os.path.join(img_dir, img_name)

        response = requests.get(img_url)
        with open(img_path, 'wb') as img_file:
            img_file.write(response.content)

        md_content = md_content.replace(img_url, f'{img_dir}/{img_name}')

    with open(md_file_name, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f'处理完成：{md_file_name}')

def process_dir(directory):
    os.chdir(directory)
    obj_list=os.listdir(directory)


    for obj in obj_list:

        if obj==".git":continue

        elif obj.endswith('.md')==True:
            process_markdown_file(directory,obj)
        elif os.path.isdir(os.path.join(directory,obj))==True:
            process_dir(os.path.join(directory,obj))


if __name__ == '__main__':
    # replace the directory you want to rename
    target_directory = r"D:\Desktop\note_offline"
    process_dir(target_directory)

