import requests
from bot.config import FLASK_LOGIN_URL, FLASK_BOOKING_TODAY_URL


def login_to_flask(username: str, password: str) -> str:
    response = requests.post(FLASK_LOGIN_URL, json={"username": username, "password": password})
    
    if response.status_code == 200:
        data = response.json()
        return data.get("access_token")
    else:
        raise ValueError(f"Ошибка авторизации: {response.status_code} {response.text}")


def get_bookings_today(token: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(FLASK_BOOKING_TODAY_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()
        pick_ups = data.get("pick_ups", [])
        drop_offs = data.get("drop_offs", [])

        bookings_info = f"Бронирования на {data['selected_date']}:\n\n"

        if pick_ups:
            bookings_info += "Заборы:\n" + "\n".join(
                [f"- Машина: {b['car_brand']} {b['car_number']}\n, Статус: {b['status']}, Начало: {b['start_date']}, Конец: {b['end_date']}" for b in pick_ups]
            ) + "\n\n"
        else:
            bookings_info += "Нет заборов.\n\n"

        if drop_offs:
            bookings_info += "Возвраты:\n" + "\n".join(
                [f"- Машина: {b['car_brand']} {b['car_number']}\n, Статус: {b['status']}, Начало: {b['start_date']}, Конец: {b['end_date']}" for b in drop_offs]
            )
        else:
            bookings_info += "Нет возвратов."

        return bookings_info
    else:
        return f"Ошибка: {response.status_code} {response.text}"
    
def login_with_telegram_id(telegram_id: str) -> str:
    response = requests.post(FLASK_LOGIN_URL, json={"telegram_id": telegram_id})
    
    if response.status_code == 200:
        data = response.json()
        return data.get("access_token")
    else:
        raise ValueError(f"Ошибка авторизации: {response.status_code} {response.text}")