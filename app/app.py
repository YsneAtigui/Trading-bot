import threading
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

from strategies import RSI_Strategy, SMA_Strategy  # For handling CORS (if needed)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app)


@app.route("/", methods=["GET"])
def index():
    return render_template("base.html")


@app.route("/strategy", methods=["POST"])
def handle_strategy():
    # Get JSON data from the request
    data = request.get_json()

    # Validate required fields
    required_fields = ["symbol", "qty", "api_key", "secret_key"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    # Additional validation for SMA strategy
    # if data["strategy_type"].lower() == "sma":

    sma_strategy = SMA_Strategy(
        data["api_key"], data["secret_key"], int(data["sma_fast"]), int(data["sma_slow"])
    )
    # sma_strategy.api_crypto_SMA()
    threading.Thread(target=sma_strategy.api_crypto_SMA, args=(data["symbol"], data["qty"], socketio)).start()

    if "sma_fast" not in data or "sma_slow" not in data:
        return jsonify({"error": "Missing SMA fast or slow period"}), 400
    if int(data["sma_fast"]) >= int(data["sma_slow"]):
        return (
            jsonify({"error": "SMA fast period must be less than SMA slow period"}),
            400,
        )

    response = {"message": "Strategy data received successfully", "data": data}
    return jsonify(response), 200

    # else:
    #     rsi_strategy = RSI_Strategy(data["api_key"], data["secret_key"])
    #     # sma_strategy.api_crypto_SMA()
    #     threading.Thread(target=rsi_strategy.trade, args=(data["symbol"], data["qty"], socketio)).start()

    #     if "sma_fast" not in data or "sma_slow" not in data:
    #         return jsonify({"error": "Missing SMA fast or slow period"}), 400
    #     if int(data["sma_fast"]) >= int(data["sma_slow"]):
    #         return (
    #             jsonify({"error": "SMA fast period must be less than SMA slow period"}),
    #             400,
    #         )
    
    #     response = {"message": "Strategy data received successfully", "data": data}
    #     return jsonify(response), 200



if __name__ == "__main__":
    app.run(debug=True)
