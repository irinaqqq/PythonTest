# FastAPI Weather App

Это приложение на FastAPI, которое позволяет работать с данными о погоде. Оно включает функциональность для получения, создания, обновления и удаления данных о погоде для городов. Также интегрировано с внешним API для получения актуальных данных о погоде.

## Стек технологий

- **FastAPI** – для создания веб-приложений.
- **SQLAlchemy** – для работы с базой данных.
- **Uvicorn** – для запуска приложения на сервере.
- **Pydantic** – для валидации данных.
- **Requests** – для взаимодействия с внешним API (OpenWeatherMap).

## Локальный запуск

### Требования

Для запуска проекта необходимо установить следующие зависимости:

1. **Python** версии 3.8 или выше.
2. Установите виртуальное окружение:

      ```bash
   python -m venv venv
Активируйте виртуальное окружение:

Для Windows:

     .\venv\Scripts\activate

Для macOS/Linux:

     source venv/bin/activate
     
Установите зависимости:


      pip install -r requirements.txt
Запуск приложения
Чтобы запустить приложение, используйте команду:

      uvicorn app.main:app --reload
После этого приложение будет доступно по адресу http://127.0.0.1:8000.

Для доступа к документации API откройте http://127.0.0.1:8000/docs.

Эндпоинты
1. Получение JWT токена
POST /token

Получение JWT токена для авторизации.

Параметры:
username: Имя пользователя (строка).
password: Пароль (строка).
Пример запроса:
bash
Копировать код
curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin&password=admin'
Ответ:
json
Копировать код
{
  "access_token": "jwt_token_value",
  "token_type": "bearer"
}
2. Защищенный эндпоинт
GET /protected-endpoint

Защищенный эндпоинт, доступный только для авторизованных пользователей.

Пример запроса:
bash
Копировать код
curl -X 'GET' \
  'http://127.0.0.1:8000/protected-endpoint' \
  -H 'Authorization: Bearer jwt_token_value'
Ответ:
json
Копировать код
{
  "message": "Hello admin, you have access!"
}
3. Получение данных о погоде для города
GET /weather/{city}

Получение данных о погоде для указанного города.

Пример запроса:
bash
Копировать код
curl -X 'GET' \
  'http://127.0.0.1:8000/weather/London'
Ответ:
json
Копировать код
[
  {
    "id": 1,
    "city": "London",
    "temperature": 15.5,
    "description": "Clear sky",
    "timestamp": "2024-12-04T18:22:25"
  }
]
4. Создание данных о погоде
POST /weather/

Сохранение данных о погоде для города в базе данных. Требуется авторизация.

Пример запроса:
bash
Копировать код
curl -X 'POST' \
  'http://127.0.0.1:8000/weather/' \
  -H 'Authorization: Bearer jwt_token_value' \
  -H 'Content-Type: application/json' \
  -d '{
    "city": "New York",
    "temperature": 10,
    "description": "Cloudy"
}'
Ответ:
json
Копировать код
{
  "status": "success",
  "message": "Data for New York saved successfully."
}
5. Обновление данных о погоде
PUT /weather/{city}

Обновление данных о погоде для указанного города.

Пример запроса:
bash
Копировать код
curl -X 'PUT' \
  'http://127.0.0.1:8000/weather/London' \
  -H 'Authorization: Bearer jwt_token_value'
Ответ:
json
Копировать код
{
  "status": "success",
  "message": "Weather data for London updated successfully."
}
6. Удаление данных о погоде
DELETE /weather/{city}

Удаление данных о погоде для указанного города.

Пример запроса:
bash
Копировать код
curl -X 'DELETE' \
  'http://127.0.0.1:8000/weather/London' \
  -H 'Authorization: Bearer jwt_token_value'
Ответ:
json
Копировать код
{
  "status": "success",
  "message": "Weather data for London deleted successfully."
}
Развернутый сервис
Ваш сервис доступен по следующему URL: https://your-app-name.onrender.com.

Для получения дополнительной информации и обновлений следите за репозиторием на GitHub.
