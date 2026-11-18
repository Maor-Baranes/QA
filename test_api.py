import pytest
import requests


@pytest.fixture
def created_booking():


    booking =  {
        "firstname": "Maor",
        "lastname": "Baranes",
        "totalprice": 444,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-12-10",
            "checkout": "2026-12-30"
        },
        "additionalneeds": "Breakfast"
    }


    r = requests.post(
        'https://restful-booker.herokuapp.com/booking', json=booking)

    assert r.status_code == 200, r.text

    booking_id = r.json()['bookingid']
    return booking, booking_id


def test_booking():

    booking =  {
        "firstname": "Maor",
        "lastname": "Baranes",
        "totalprice": 444,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-12-10",
            "checkout": "2026-12-30"
        },
        "additionalneeds": "Breakfast"
    }

    r = requests.post(
        'https://restful-booker.herokuapp.com/booking', json=booking)

    assert r.status_code == 200, r.text

    booking_id = r.json()['bookingid']
    assert booking_id is not None
    assert r.json()["booking"] == booking

def test_read(created_booking):
    booking, booking_id = created_booking

    r = requests.get(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}")

    assert r.status_code == 200
    assert r.json() == booking

def test_update(created_booking):

    booking, booking_id = created_booking
    updated_booking = {**booking, "totalprice":999}

    r = requests.post(
        "https://restful-booker.herokuapp.com/auth",
        json={"username":'admin', "password": 'password123'})
    assert r.status_code == 200, r.text

    token = r.json()["token"]
    r = requests.put(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        json=updated_booking,
        cookies={"token":token}
    )
    assert r.status_code == 200, r.text
    r = requests.get(
            f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        )
    
    assert r.status_code == 200
    assert r.json() == updated_booking

def test_delete(created_booking):
    booking, booking_id = created_booking
    r = requests.post(
            "https://restful-booker.herokuapp.com/auth",
            json={"username":'admin', "password": 'password123'})
    assert r.status_code == 200, r.text
    
    token = r.json()["token"]

    r = requests.delete(f"https://restful-booker.herokuapp.com/booking/{booking_id}",
            cookies={"token":token}
        )
    assert r.status_code == 201
    r = requests.get(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    assert r.status_code == 404

def test_negative_id(): 
    r = requests.get(
        "https://restful-booker.herokuapp.com/booking/99999999999999")
    assert r.status_code == 404
def test_missing_data():

    incomplete_booking = {
        "firstname": "Maor",
        "totalprice": 444,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-12-10",
            "checkout": "2026-12-30"
            },
        "additionalneeds": "Breakfast"
        }

    r = requests.post(
        "https://restful-booker.herokuapp.com/booking/",
        json=incomplete_booking)
    assert r.status_code == 500
    # API returns 500 Internal Server Error for missing required fields.

def test_delete_without_auth(created_booking):
    _, booking_id = created_booking
    r = requests.delete(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    assert r.status_code == 403
    r = requests.get(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    assert r.status_code == 200, r.text