from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    news = []
    error = None

    if request.method == 'POST':
        city = request.form['city']
        weather = get_weather(city)

        if weather.get('cod') != 200:
            error = 'Город не найден. Попробуйте ещё раз.'
            weather = None
        else:
            news = get_news(city)

    return render_template('index.html', weather=weather, news=news, error=error)


def get_weather(city):
    api_key = 'c1569892fe7c201402fd0bb2547cb09c'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ru'
    return requests.get(url).json()


def get_news(city):
    api_key = '228595da0e7343f9a759b8ac9e6e1096'  # замените на свой ключ, если нужно
    url = f'https://newsapi.org/v2/everything?q={city}&language=ru&sortBy=publishedAt&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    return []


if __name__ == '__main__':
    app.run(debug=True)
