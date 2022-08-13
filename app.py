from flask import Flask, request, make_response
app = Flask(__name__)


@app.route("/")
def index():
    response = make_response("<h1>Hello, world</h1>")
    return response


@app.route("/profile/<name>")
def profile(name):
    response = make_response(f"<h1>Hello, {name}</h1>")
    return response


@app.route("/user-agent/")
def user_agent():
    response = make_response("test")
    return response.status


### Hooks ###
# @app.before_request
# def before_request():
#     print(request.headers.get("User-Agent"))


if __name__ == "__main__":
    app.run()
