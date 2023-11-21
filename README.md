# Получение курса валют с сайта https://www.nbrb.by/

## Endpoints

>> http://127.0.0.1:8000/currency_rate_app/load_data/?date=2023-01-10

>> http://127.0.0.1:8000/currency_rate_app/get_rate/?cur_code=460&date=2023-01-10

## Деплой приложения

### Клонируйте данный репозиторий и перейдите в директорию с приложением
```
git clone https://github.com/heywhereismymind/currency.git
cd currency
 ```
### Создайте и активируйте виртуальное окружение
```
python -m venv .venv
source ./.venv/Scripts/Activate.ps1  #для Windows
source ./.venv/bin/activate      #для Linux и macOS
```
### Установите требуемые зависимости
```
pip install -r requirements.txt
```
### Запустите проект
```
python manage.py runserver
```
