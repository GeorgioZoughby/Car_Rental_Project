from flask import Flask
from routes import init_blueprints


app = Flask(__name__)

init_blueprints(app)

app.jinja_env.globals.update(int=int, float=float, str=str)


if __name__ == '__main__':
    app.run(debug=True)

