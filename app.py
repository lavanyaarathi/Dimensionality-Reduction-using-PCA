from flask import Flask
from routes.preprocessing_routes import preprocess_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.register_blueprint(preprocess_bp)

if __name__ == "__main__":
    app.run(debug=True)
