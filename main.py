from flask import Flask
from api.controller import bp as api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    print("Hello world")
    app.run(host='0.0.0.0', port=8555, debug=True, threaded=False)