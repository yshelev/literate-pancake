# ad api
API-интерфейс 

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [Команда проекта](#команда-проекта)


## Технологии
DRF для создания API, создание тестов встроенными возможностями DRF, документация с помощью библиотеки DRF-YASG

## Использование
1. Склонируйте репозиторий:
   ```sh
   git clone https://github.com/yshelev/literate-pancake.git
   cd literate-pancake
   ```
2. Создайте и активируйте виртуальное окружение: 
   ```sh
   python3 -m venv .venv
   .venv/Scripts/activate
   ```
3. Установите необходимые зависимости:  	
   ```sh
   pip install -r requirements.txt
   ```
4. В директорию проекта поместите БД *.sqlite3
5. Настройте виртуальное окружение (.env.example заменить на .env, вставить ваши значения) 
6. Создайте миграции:
   ```sh
   python manage.py makemigrations 
   ```
7. Запустите миграции
   ```sh
   python manage.py migrate
   ```
8. Запустите приложение
   ```sh
   python manage.py runserver
   ```

Пример работы программы:
![image](https://github.com/user-attachments/assets/b86867bc-4c90-452e-b17f-24454d0c1596)


Для запуска тестов: 
1. Запустите тесты:
   ```sh
     python manage.py test --parallel
   ```

## Команда проекта

- [Шелевой Ярослав](https://github.com/yshelev) — Backend developer
