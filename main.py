# Импорт необходимых библиотек
import requests  # Для отправки HTTP-запросов
from bs4 import BeautifulSoup  # Для парсинга HTML
import json  # Для работы с JSON-данными

# Основная функция для парсинга данных
def parse_vet_clinic_data():
    # URL главной страницы энциклопедии
    url = 'https://dar-vetclinic.ru/encziklopediya/'  # Устанавливаем URL-адрес страницы для извлечения данных

    # Отправляем GET-запрос для получения содержимого страницы
    response = requests.get(url)  # Отправляем GET-запрос на указанный URL-адрес и получаем ответ

    # Парсим HTML-содержимое с помощью BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')  # Создаем объект BeautifulSoup для парсинга HTML-кода страницы

    # Находим все ссылки на странице
    links = soup.find_all('a')  # Ищем все ссылки на странице

    # Множество для отслеживания уже обработанных ссылок
    visited_links = set()  # Создаем множество для отслеживания посещенных ссылок

    # Словарь для хранения извлеченных данных
    dataframe = {}  # Создаем пустой словарь для хранения данных

    # Проходим по каждой найденной ссылке
    for link in links:  # Проходимся по каждой ссылке на странице
        href = link.get('href')  # Получаем URL-адрес из ссылки
        if href and '/sobaki/' in href and href not in visited_links:  # Проверяем, что ссылка содержит "/sobaki/" и еще не была посещена
            visited_links.add(href)  # Добавляем ссылку в множество посещенных ссылок
            try:
                # Загружаем страницу подраздела
                response = requests.get(href)  # Отправляем GET-запрос на ссылку и получаем ответ
                subpage_soup = BeautifulSoup(response.text, 'html.parser')  # Создаем объект BeautifulSoup для парсинга HTML-кода подстраницы

                # Извлекаем заголовок статьи
                entry_title = subpage_soup.find('h1', class_='entry-title')  # Ищем заголовок записи
                if entry_title:  # Проверяем, что заголовок найден
                    entry_title_text = entry_title.get_text().strip()  # Получаем текст заголовка и удаляем лишние пробелы

                    # Извлекаем текст статьи
                    article_body_container = subpage_soup.find('div', class_='article-body-container')  # Ищем контейнер с текстом статьи
                    if article_body_container:  # Проверяем, что контейнер найден
                        article_text = article_body_container.get_text(separator='\n')  # Получаем текст статьи
                        article_text_list = article_text.split("\n")  # Разделяем текст статьи на список по символу новой строки

                        # Очищаем текст от лишних элементов
                        article_text_list2 = article_text_list[:-2]  # Обрезаем последние две строки
                        if 'ДАР»' in article_text_list2:  # Проверяем наличие определенной строки в списке
                            first_index = article_text_list2.index('ДАР»')  # Находим индекс этой строки
                            trimmed_list = article_text_list2[:first_index]  # Обрезаем список до указанного индекса
                            trimmed_list1 = trimmed_list[:-4]  # Дополнительное обрезание списка

                            # Извлекаем данные из таблицы цен
                            table = subpage_soup.find('table', class_='prices-table__services')  # Ищем таблицу с ценами
                            if table:
                                headers = [header.text.strip() for header in table.find_all('td', class_='prices-table-title-sec')]  # Получаем заголовки таблицы
                                tabl = []  # Создаем пустой список для хранения данных таблицы
                                for row in table.find_all('tr'):  # Проходимся по каждой строке таблицы
                                    cells = row.find_all('td')  # Ищем все ячейки в строке
                                    if len(cells) == len(headers):  # Проверяем, что количество ячеек равно количеству заголовков
                                        tabl.append([cell.text.strip() for cell in cells])  # Добавляем данные ячеек в список

                                # Сохраняем данные в словарь
                                dataframe[entry_title_text] = [trimmed_list1, tabl]  # Добавляем данные в словарь
            except Exception as e:
                print(f"Ошибка при обработке {href}: {e}")

    return dataframe

# Основной блок выполнения
if __name__ == "__main__":
    # Вызываем функцию парсинга
    data = parse_vet_clinic_data()

    # Записываем данные в JSON-файл
    with open('dataframe.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
