from flask import Flask

from routes.training.raw_data import raw_blueprint

app = Flask(__name__)

app.register_blueprint(raw_blueprint, url_prefix='/api/training/data')

if __name__ == '__main__':
    app.run()