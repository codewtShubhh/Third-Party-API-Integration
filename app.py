from flask import Flask, jsonify, request
from dotenv import load_dotenv

from services.weather_services import get_weather

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Third-Party API Integration API is running"
    })


@app.route("/api/weather", methods=["GET"])
async def weather():
    city = request.args.get("city")

    if not city:
        return jsonify({
            "success": False,
            "message": "City is required"
        }), 400

    result = await get_weather(city)

    status_code = result.get("status_code", 200)

    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)