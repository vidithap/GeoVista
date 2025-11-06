from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os
import requests

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'geovista.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table for storing search history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            country TEXT,
            searched_at DATETIME
        )
    """)

    # Table for storing contact form messages
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            submitted_at DATETIME
        )
    """)

    conn.commit()
    conn.close()

# Initialize the database tables when app starts
init_db()


def save_search(city, country):
    city = city.strip().capitalize()
    country = country.strip().capitalize() if country else None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO searches (city, country, searched_at) VALUES (?, ?, ?)",
        (city, country, datetime.now())
    )
    conn.commit()
    conn.close()


def get_recent_searches(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT city, country, searched_at
        FROM searches
        ORDER BY searched_at DESC
        LIMIT ?
    """, (limit,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")  # safely load key from environment

    if not api_key:
        print(" Missing OpenWeather API key.")
        return None

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temp": data['main']['temp'],
            "description": data['weather'][0]['description'],
            "icon": data['weather'][0]['icon']
        }
    return None

@app.route('/')
def home():
    city = request.args.get('city')
    country = request.args.get('country')
    weather = None

    # ✅ Capitalize if present
    if city:
        city = city.strip().capitalize()
    if country:
        country = country.strip().capitalize()

    if city:
        weather = get_weather(city)

    searches = get_recent_searches()
    return render_template('index.html', city=city, country=country, weather=weather, searches=searches)


@app.route('/search')
def search():
    city = request.args.get('city')
    country = request.args.get('country')

    if not city:
        return redirect(url_for('home'))

    # ✅ Capitalize before saving and displaying
    city = city.strip().capitalize()
    country = country.strip().capitalize() if country else None

    save_search(city, country)
    weather = get_weather(city)
    searches = get_recent_searches()

    return render_template('index.html', city=city, country=country, weather=weather, searches=searches)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contact_messages (name, email, message, submitted_at)
        VALUES (?, ?, ?, ?)
    """, (name, email, message, datetime.now()))
    conn.commit()
    conn.close()

    # Fetch recent searches again so home page loads correctly
    searches = get_recent_searches()
    return render_template('index.html', success=True, searches=searches)

@app.route('/api/weather')
def api_weather():
    city = request.args.get('city')
    country = request.args.get('country')
    if not city:
        return {"error": "City required"}, 400

    weather = get_weather(city)
    if not weather:
        return {"error": "Weather not found"}, 404

    return {
        "city": city,
        "country": country,
        "weather": weather
    }

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=8080, debug=False)
