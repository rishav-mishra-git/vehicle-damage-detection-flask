from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)


# ROBOFLOW CONFIG


API_KEY = "9PU75Z9tiNgXhZlgx5cW"

MODEL_URL = "https://detect.roboflow.com/car_dent_scratch_detection-1-mczqd/1"

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# DAMAGE COST DATABASE


damage_costs = {

    "bonnet-dent": 4500,
    "boot-dent": 4000,
    "doorouter-dent": 5000,
    "fender-dent": 3500,
    "front-bumper-dent": 6000,
    "rear-bumper-dent": 5500,
    "quarterpanel-dent": 6500,
    "roof-dent": 7000,
    "pillar-dent": 4500,
    "RunningBoard-Dent": 3000,

    "Front-Windscreen-Damage": 15000,
    "Rear-windscreen-Damage": 12000,

    "Headlight-Damage": 8000,
    "Signlight-Damage": 3000,
    "Taillight-Damage": 5000,
    "Sidemirror-Damage": 3500,
}


# HOME PAGE


@app.route("/")
def home():
    return render_template("index.html")


# PREDICT API


@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})

    file = request.files["image"]

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(file_path)

    with open(file_path, "rb") as image_file:

        response = requests.post(
            f"{MODEL_URL}?api_key={API_KEY}",
            files={"file": image_file}
        )

    result = response.json()

    predictions = result.get("predictions", [])

    total_cost = 0

    damage_report = []

    for p in predictions:

        confidence = p["confidence"]

        if confidence < 0.40:
            continue

        damage_class = p["class"]

        cost = damage_costs.get(
            damage_class,
            4000
        )

        total_cost += cost

        damage_report.append({

            "damage": damage_class,
            "confidence": round(confidence, 2),
            "cost": cost
        })

    return jsonify({

        "damages": damage_report,
        "total_cost": total_cost
    })


# RUN APP


if __name__ == "__main__":
    app.run(debug=True)
