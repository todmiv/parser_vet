# parser_vet

Парсинг части сайта https://dar-vetclinic.ru/encziklopediya/ выполнен в рамках занятия "Парсинг HTML". Скаченные данные в дальнейшем будут использованы в боте "нейроветврач-консультант" по болезням собак.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/todmiv/parser_vet.git
   cd parser_vet
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Использование

Запустите скрипт:
```bash
python main.py
```

Результат будет сохранен в файл `dataframe.json`.

## Структура проекта

- `main.py`: Основной скрипт для парсинга данных.
- `requirements.txt`: Список зависимостей.
- `dataframe.json`: Выходной файл с данными.
- `README.md`: Описание проекта.
- `LICENSE`: Лицензия проекта.
- `CONTRIBUTING.md`: Инструкции по вкладу.

## Лицензия

Этот проект лицензирован под MIT License. См. файл [LICENSE](LICENSE) для деталей.
