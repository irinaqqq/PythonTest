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

## Эндпоинты

### 1. **Главная страница**
- **Эндпоинт**: `/`
- **Метод**: `GET`
- **Описание**: Главная страница с ссылками на все доступные эндпоинты.
- **Пример запроса**:
  - **URL**: `http://127.0.0.1:8000/`
  - **Метод**: `GET`
  
  В ответе будет отображена страница с ссылками на другие эндпоинты и кратким описанием API.

### 2. **Получение токена (JWT)**
- **Эндпоинт**: `/token`
- **Метод**: `POST`
- **Описание**: Получение JWT токена для аутентификации.
- **Параметры**:
  - `username`: Имя пользователя (по умолчанию "admin").
  - `password`: Пароль (по умолчанию "admin").
- **Пример запроса** (Postman):
  - **URL**: `http://127.0.0.1:8000/token`
  - **Метод**: `POST`
  - **Тело запроса** (формат JSON):
    ```json
    {
      "username": "admin",
      "password": "admin"
    }
    ```
### 3. **Доступ к защищённому эндпоинту**
- **Эндпоинт**: `/protected-endpoint`
- **Метод**: `GET`
- **Описание**: Защищённый эндпоинт, доступный только для авторизованных пользователей.
- **Пример запроса** (Postman):
  - **URL**: `http://127.0.0.1:8000/protected-endpoint?token=<ваш_jwt_токен>`
  - **Метод**: `GET`

### 4. **Получение тестовых данных о погоде**
- **Эндпоинт**: `/test-weather/{city}`
- **Метод**: `GET`
- **Описание**: Получение данных о погоде для указанного города через внешний API.
- **Пример запроса** (Postman):
  - **URL**: `http://127.0.0.1:8000/test-weather/Almaty`
  - **Метод**: `GET`

### 5. **Сохранение данных о погоде**
- **Эндпоинт**: `/weather/`
- **Метод**: `POST`
- **Описание**: Сохранение данных о погоде для города в базе данных. Требуется авторизация.
- **Параметры**:
  - `city` (строка): Название города, для которого нужно сохранить данные о погоде.
  
- **Пример запроса** (Postman):
  - **URL**: `http://127.0.0.1:8000/weather/?token=<ваш_jwt_токен>`
  - **Метод**: `POST`
  - **Тело запроса** (формат JSON):
    ```json
    {
      "city": "Almaty"
    }
    ```

  Замените `<ваш_jwt_токен>` на действующий JWT токен, полученный при авторизации.

### 6. **Получение данных о погоде для города**
- **Эндпоинт**: `/weather/{city}`
- **Метод**: `GET`
- **Описание**: Получение данных о погоде для указанного города из базы данных.
- **Пример запроса** (Postman):
  - **URL**: `http://127.0.0.1:8000/weather/Almaty`
  - **Метод**: `GET`

### 7. **Обновление данных о погоде**
- **Эндпоинт**: `/weather/{city}`
- **Метод**: `PUT`
- **Описание**: Обновление данных о погоде для города в базе данных.
- **Пример запроса** (Postman):
  - **URL**: `http://127.0.0.1:8000/weather/Almaty`
  - **Метод**: `PUT`

### 8. **Удаление данных о погоде**
- **Эндпоинт**: `/weather/{city}`
- **Метод**: `DELETE`
- **Описание**: Удаление данных о погоде для указанного города из базы данных.
- **Пример запроса** (Postman):
  - **URL**: `http://127.0.0.1:8000/weather/Almaty`
  - **Метод**: `DELETE`

### 9. **Получение информации о погоде для города**
- **Эндпоинт**: `/weather-info/{city}`
- **Метод**: `GET`
- **Описание**: Получение информации о погоде для города из базы данных или внешнего API (если данных нет в базе). Требуется аутентификация.
- **Пример запроса** (Postman):
  - **URL**: `http://127.0.0.1:8000/weather-info/Almaty?token=<ваш_jwt_токен>`
  - **Метод**: `GET`
  
  Замените `<ваш_jwt_токен>` на действующий JWT токен, полученный при авторизации.

## Примечания

- Для аутентификации используется JWT токен, который необходимо получить через эндпоинт `/token`.

Развернутый сервис
Cервис доступен по следующему URL: https://pythontest-ievp.onrender.com/

