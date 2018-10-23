"""Initializes app"""
import os

from app import create_app

app = create_app(os.getenv('APP_SETTINGS'))


@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    app.run()
