import pytest
import requests_mock
from app.services.weather import fetch_weather 
from unittest.mock import patch

def test_fetch_weather_success():
    """
    Тест проверяет успешное получение данных о погоде от API.
    """
    city = "Almaty"
    mock_response = {
        "name": city,
        "main": {"temp": 25},
        "weather": [{"description": "clear sky"}]
    }

    with requests_mock.Mocker() as mocker:
        mocker.get(
            "https://api.openweathermap.org/data/2.5/weather",
            json=mock_response,
            status_code=200
        )

        result = fetch_weather(city)
        assert result["city"] == "Almaty"
        assert result["temperature"] == 25
        assert result["description"] == "clear sky"


def test_fetch_weather_server_error():
    """
    Тест проверяет обработку ситуации, когда API возвращает ошибку сервера (500).
    """
    city = "Astana"

    with requests_mock.Mocker() as mocker:
        mocker.get(
            "https://api.openweathermap.org/data/2.5/weather",
            status_code=500
        )

        with pytest.raises(Exception) as excinfo:
            fetch_weather(city)
        assert "500 Server Error" in str(excinfo.value)


def test_fetch_weather_invalid_response():
    mock_response = {
        "unexpected_key": "unexpected_value"
    }
    
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        with pytest.raises(ValueError, match="Missing 'main' or 'temp' in the response data."):
            fetch_weather("Almaty")


def test_fetch_weather_timeout():
    """
    Тест проверяет обработку таймаута запроса.
    """
    from requests.exceptions import Timeout

    city = "Shymkent"

    with requests_mock.Mocker() as mocker:
        mocker.get(
            "https://api.openweathermap.org/data/2.5/weather",
            exc=Timeout
        )

        with pytest.raises(Exception) as excinfo:
            fetch_weather(city)
        assert "Timeout" in str(excinfo.value)


def test_fetch_weather_not_found():
    """
    Тест проверяет обработку ситуации, когда город не найден (404).
    """
    city = "UnknownCity"

    with requests_mock.Mocker() as mocker:
        mocker.get(
            "https://api.openweathermap.org/data/2.5/weather",
            status_code=404,
            json={"cod": "404", "message": "city not found"}
        )

        with pytest.raises(Exception) as excinfo:
            fetch_weather(city)
        assert "404 Client Error" in str(excinfo.value)
