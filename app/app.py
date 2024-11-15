from flask import Flask
from routes import init_blueprints


app = Flask(__name__)

init_blueprints(app)

def check_palindrome(word):
    return word == word[::-1]

app.jinja_env.globals['check_palindrome'] = check_palindrome
#app.jinja_env.globals.update(int=int, float=float, str=str)


if __name__ == '__main__':
    app.run(debug=True)

