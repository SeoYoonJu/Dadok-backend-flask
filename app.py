from flask import Flask
from chat import generate_text_bp
from gyobo import scrape_bp

app = Flask(__name__)

app.register_blueprint(generate_text_bp)
app.register_blueprint(scrape_bp)



if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
