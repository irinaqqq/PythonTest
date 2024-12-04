from fastapi import FastAPI, HTTPException, Depends
from app.services.weather import fetch_weather
from app.database import save_weather_data, get_weather_data, update_weather_data, delete_weather_data
from app.models import *
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer
from app.auth import create_access_token, get_current_user

app = FastAPI(
    title="Weather API",
    description="API for fetching and managing weather data for cities. Includes weather data storage, updates, and protected access.",
    version="1.0.0"
)

@app.post("/token", response_model=Token, summary="Login to get access token", tags=["Authentication"])
def login_for_access_token(username: str, password: str):
    """
    Получение JWT токена для авторизации.
    Логин и пароль для разработки: `admin` (по умолчанию).
    
    Параметры:
    - `username`: Имя пользователя (строка). В настоящее время ожидается значение "admin".
    - `password`: Пароль (строка). В настоящее время ожидается значение "admin".
    
    Возвращает:
    - `access_token`: Токен для доступа.
    - `token_type`: Тип токена (по умолчанию "bearer").
    
    Ошибки:
    - 401: Неверное имя пользователя или пароль (если указано что-то отличное от "admin").
    """
    if username != "admin" or password != "admin":
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected-endpoint", summary="Access a protected endpoint", tags=["Protected Endpoints"])
def protected_endpoint(current_user: TokenData = Depends(get_current_user)):
    """
    Защищенный эндпоинт, доступный только для авторизованных пользователей.
    Для доступа требуется Bearer токен, который передается в заголовке `Authorization`.
    
    Параметры запроса:
    - Заголовок `Authorization`: Токен в формате `Bearer <token>`.
    
    Возвращает:
    - Приветственное сообщение с именем пользователя.
    
    Ошибки:
    - 403: Токен недействителен или не был предоставлен.
    """
    return {"message": f"Hello {current_user.username}, you have access!"}

@app.get("/test-weather/{city}", response_model=dict, summary="Test weather API", tags=["Weather"])
def test_weather(city: str):
    """
    Тестовый эндпоинт для проверки интеграции с внешним API.
    
    Параметры:
    - `city`: Название города (строка).
    
    Возвращает:
    - `status`: Статус ответа (например, "success").
    - `city`: Город.
    - `temperature`: Температура в городе.
    - `description`: Описание погоды.
    
    Ошибки:
    - 500: Ошибка на сервере (не удалось получить данные).
    """
    try:
        weather = fetch_weather(city)
        return {
            "status": "success",
            "city": weather["city"],
            "temperature": weather["temperature"],
            "description": weather["description"]
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/weather/", response_model=dict, summary="Save weather data", tags=["Protected Endpoints"])
def create_weather(weather: WeatherCreate, current_user: TokenData = Depends(get_current_user)):
    """
    Сохранение данных о погоде в базе.
    Для сохранения данных о погоде необходим токен и название города.
    Доступно только для авторизованных пользователей.
    
    Параметры запроса:
    - Заголовок `Authorization`: Токен в формате `Bearer <token>`.
    - `city`: Название города (строка).
    
    Возвращает:
    - `status`: Статус ответа (например, "success").
    - `message`: Сообщение о статусе операции.
    
    Ошибки:
    - 403: Токен недействителен или не был предоставлен.
    - 500: Ошибка на сервере (не удалось сохранить данные).
    """
    try:
        save_weather_data(weather.city)
        return {"status": "success", "message": f"Data for {weather.city} saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/{city}", response_model=list[WeatherResponse], summary="Get weather data for a city", tags=["Weather"])
def read_weather(city: str):
    """
    Получение данных о погоде для конкретного города из базы.
    
    Параметры:
    - `city`: Название города (строка).
    
    Возвращает:
    - Список объектов `WeatherResponse`:
        - `id`: ID записи (целое число).
        - `city`: Название города.
        - `temperature`: Температура.
        - `description`: Описание погоды.
        - `timestamp`: Время записи.
    
    Ошибки:
    - 404: Данные о погоде не найдены.
    - 500: Ошибка на сервере.
    """
    try:
        weather_data = get_weather_data(city)
        if not weather_data:
            raise HTTPException(status_code=404, detail="Weather data not found.")
        return [
            WeatherResponse(
                id=row[0],
                city=row[1],
                temperature=row[2],
                description=row[3],
                timestamp=row[4]
            ) for row in weather_data
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/weather/{city}", response_model=dict, summary="Update weather data", tags=["Weather"])
def update_weather(city: str):
    """
    Обновление данных о погоде для города из базы.
    
    Параметры:
    - `city`: Название города (строка), данные о погоде которого нужно обновить.
    
    Возвращает:
    - `status`: Статус ответа (например, "success").
    - `message`: Сообщение о статусе операции (например, "Weather data for {city} updated successfully.")
    
    Ошибки:
    - 404: Город не найден в базе данных.
    - 500: Ошибка на сервере (не удалось обновить данные).
    """
    try:
        # Проверяем наличие данных для города в базе
        weather_data = get_weather_data(city)
        if not weather_data:
            # Если данные о погоде для города отсутствуют, возвращаем ошибку 404
            raise HTTPException(status_code=404, detail=f"Weather data for {city} not found.")
        
        # Если данные есть, обновляем их
        update_weather_data(city)
        return {"status": "success", "message": f"Weather data for {city} updated successfully."}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/weather/{city}", response_model=dict, summary="Delete weather data", tags=["Weather"])
def delete_weather(city: str):
    """
    Удаление данных о погоде для указанного города из базы.
    
    Параметры:
    - `city`: Название города (строка), для которого необходимо удалить данные о погоде.
    
    Возвращает:
    - `status`: Статус ответа (например, "success").
    - `message`: Сообщение о статусе операции, например, "Weather data for {city} deleted successfully."
    
    Ошибки:
    - 404: Данные о погоде для города не найдены.
    - 500: Ошибка на сервере (не удалось удалить данные).
    """
    try:
        # Проверяем наличие данных о погоде для города
        weather_data = get_weather_data(city)
        if not weather_data:
            # Если данные для города не найдены, возвращаем ошибку 404
            raise HTTPException(status_code=404, detail=f"Weather data for {city} not found.")
        
        # Если данные найдены, удаляем их
        delete_weather_data(city)
        return {"status": "success", "message": f"Weather data for {city} deleted successfully."}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/weather-info/{city}", response_model=WeatherResponse, summary="Get weather information", tags=["Protected Endpoints"])
def get_weather_info(city: str, current_user: TokenData = Depends(get_current_user)):
    """
    Основной эндпоинт, демонстрирующий связку локального API и внешнего API.
    - Проверяет наличие данных в базе.
    - Если данных нет, запрашивает данные у внешнего API и сохраняет их.
        Для доступа требуется Bearer токен в заголовке `Authorization`.
    
    Параметры запроса:
    - Заголовок `Authorization`: Токен в формате `Bearer <token>`.
    - `city`: Название города (строка) в пути запроса.

    Возвращает:
    - Объект с информацией о погоде:
        - `id`: Идентификатор записи в базе данных (или `None`, если данные получены с внешнего API).
        - `city`: Название города.
        - `temperature`: Температура.
        - `description`: Описание погоды.
        - `timestamp`: Время получения данных.
    
    Ошибки:
    - 403: Токен недействителен или не был предоставлен.
    - 500: Ошибка на сервере.
    """
    try:
        weather_data = get_weather_data(city)
        if weather_data:
            row = weather_data[0]
            return WeatherResponse(
                id=row[0],
                city=row[1],
                temperature=row[2],
                description=row[3],
                timestamp=row[4]
            )
        
        # Если данных нет в базе, получаем их из внешнего API
        external_weather = fetch_weather(city)
        save_weather_data(city)

        return WeatherResponse(
            id=None,
            city=external_weather["city"],
            temperature=external_weather["temperature"],
            description=external_weather["description"],
            timestamp=datetime.now()
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    