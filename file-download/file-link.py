import requests
import os
from urllib.parse import urlparse

# Создаем папку для сохранения файлов, если она не существует
output_folder = 'downloaded_files'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Читаем список ссылок из текстового файла
file_urls_file = 'file_urls.txt'
with open(file_urls_file, 'r') as f:
    file_urls = f.read().splitlines()

# Загружаем файлы
for url in file_urls:
    file_name = os.path.join(output_folder, urlparse(url).path.lstrip('/'))
    file_dir = os.path.dirname(file_name)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    response = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(response.content)
    print(f"Файл {file_name} успешно сохранен.")
