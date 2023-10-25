from flask import Flask

from routes.raw_data import raw_blueprint
from routes.leagues import leagues_blueprint

app = Flask(__name__)

app.register_blueprint(raw_blueprint, url_prefix='/api/training/data')
app.register_blueprint(leagues_blueprint, url_prefix='/api/leagues')

if __name__ == '__main__':
    app.run()