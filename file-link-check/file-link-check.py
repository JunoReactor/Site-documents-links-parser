import requests
from colorama import Fore, Style, init

init()  # Инициализация colorama

# Чтение списка ссылок из текстового файла
def read_links_from_file(file_name):
    with open(file_name, 'r') as file:
        links = file.readlines()
    return [link.strip() for link in links]

# Проверка кодов ответов каждой ссылки и вывод в консоль с подсветкой
def check_response_codes(links):
    results = []
    for link in links:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                result = f'{link};{response.status_code}'
                results.append(result)
                print(f'{link} - Код ответа: {Fore.GREEN}{response.status_code}{Style.RESET_ALL}')
            elif response.status_code == 404:
                result = f'{link};{response.status_code}'
                results.append(result)
                print(f'{link} - Код ответа: {Fore.RED}{response.status_code}{Style.RESET_ALL}')
            else:
                result = f'{link};{response.status_code}'
                results.append(result)
                print(f'{link} - Код ответа: {response.status_code}')
        except requests.exceptions.RequestException as e:
            result = f'{link};Ошибка при запросе: {e}'
            results.append(result)
            print(result)
    return results

# Сохранение результатов в файлы
def save_results_to_file(file_name, results):
    with open(file_name, 'w') as file:
        for result in results:
            file.write(result + '\n')

if __name__ == "__main__":
    file_name = 'file_urls.txt'  # Замените на имя вашего файла
    links = read_links_from_file(file_name)
    results = check_response_codes(links)
    save_results_to_file('log.txt', results)
