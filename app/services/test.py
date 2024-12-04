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

@app.post("/token", response_model=Token)
def login_for_access_token(username: str, password: str):
    """
    Получение JWT токена для авторизации.
    - `username`: Имя пользователя.
    - `password`: Пароль.
    - при разработке `admin` используется в обоих полях.
    """
    if username != "admin" or password != "admin":
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected-endpoint")
def protected_endpoint(current_user: TokenData = Depends(get_current_user)):
    """
    Защищенный эндпоинт, доступный только для авторизованных пользователей.
    - Этот эндпоинт возвращает приветственное сообщение с именем пользователя.
    """
    return {"message": f"Hello {current_user.username}, you have access!"}


@app.get("/test-weather/{city}")
def test_weather(city: str):
    """Тестовый эндпоинт для проверки интеграции с внешним API."""
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

@app.post("/weather/", response_model=dict)
def create_weather(weather: WeatherCreate, current_user: TokenData = Depends(get_current_user)):
    """
    Сохранение данных о погоде в базе.
    Этот эндпоинт доступен только для авторизованных пользователей.
    """
    try:
        save_weather_data(weather.city)
        return {"status": "success", "message": f"Data for {weather.city} saved successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/weather/{city}", response_model=list[WeatherResponse])
def read_weather(city: str):
    """Получение данных о погоде для конкретного города."""
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

@app.put("/weather/{city}", response_model=dict)
def update_weather(city: str):
    """Обновление данных о погоде для города."""
    try:
        update_weather_data(city)
        return {"status": "success", "message": f"Weather data for {city} updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/weather/{city}", response_model=dict)
def delete_weather(city: str):
    """Удаление данных о погоде для города."""
    try:
        delete_weather_data(city)
        return {"status": "success", "message": f"Weather data for {city} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/weather-info/{city}", response_model=WeatherResponse)
def get_weather_info(city: str, current_user: TokenData = Depends(get_current_user)):
    """
    Основной эндпоинт, демонстрирующий связку локального API и внешнего API.
    - Проверяет наличие данных в базе.
    - Если данных нет, запрашивает данные у внешнего API и сохраняет их.
    - Этот эндпоинт доступен только для авторизованных пользователей.
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

