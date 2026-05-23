from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory
)

import requests
import os

from PIL import Image, ImageDraw

app = Flask(__name__)

# ROBOFLOW CONFIG

API_KEY = "9PU75Z9tiNgXhZlgx5cW"

MODEL_URL = "https://detect.roboflow.com/car_dent_scratch_detection-1-mczqd/1"

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# DAMAGE COST DATABASE

damage_costs = {

    # DENTS
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
    "medium-Bodypanel-Dent": 5000,
    "Major-Rear-Bumper-Dent": 12000,

    # GLASS DAMAGES
    "Front-Windscreen-Damage": 15000,
    "Rear-windscreen-Damage": 12000,

    # LIGHT DAMAGES
    "Headlight-Damage": 8000,
    "Signlight-Damage": 3000,
    "Taillight-Damage": 5000,
    "Sidemirror-Damage": 3500,

    # DEFAULT
    "scratch": 2500
}


# HOME PAGE

@app.route("/")
def home():

    return render_template("index.html")

# IMAGE ROUTE

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )

# PREDICTION API

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:

        return jsonify({
            "error": "No image uploaded"
        })

    file = request.files["image"]

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(file_path)

    # SEND IMAGE TO ROBOFLOW

    with open(file_path, "rb") as image_file:

        response = requests.post(

            f"{MODEL_URL}?api_key={API_KEY}",

            files={
                "file": image_file
            }
        )

    result = response.json()

    predictions = result.get(
        "predictions",
        []
    )

    # LOAD IMAGE

    image = Image.open(file_path).convert("RGB")

    draw = ImageDraw.Draw(image)

    total_cost = 0

    damage_report = []

    # DRAW DETECTIONS

    for p in predictions:

        confidence = p["confidence"]

        # FILTER LOW CONFIDENCE

        if confidence < 0.40:
            continue

        x = p["x"]
        y = p["y"]

        width = p["width"]
        height = p["height"]

        x1 = x - width / 2
        y1 = y - height / 2

        x2 = x + width / 2
        y2 = y + height / 2

        damage_class = p["class"]

        # GET DAMAGE COST

        cost = damage_costs.get(
            damage_class,
            4000
        )

        total_cost += cost

        # DRAW RECTANGLE

        draw.rectangle(

            [x1, y1, x2, y2],

            outline="red",

            width=4
        )

        # DRAW LABEL

        label = f"{damage_class} ({confidence:.2f})"

        draw.text(

            (x1, y1 - 20),

            label,

            fill="red"
        )

        # SAVE DAMAGE REPORT

        damage_report.append({

            "damage": damage_class,

            "confidence": round(
                confidence,
                2
            ),

            "cost": cost
        })

    # SAVE RESULT IMAGE

    result_filename = "result_" + file.filename

    result_path = os.path.join(
        UPLOAD_FOLDER,
        result_filename
    )

    image.save(result_path)

    # RETURN RESPONSE

    return jsonify({

        "damages": damage_report,

        "total_cost": total_cost,

        "result_image": f"uploads/{result_filename}"
    })

# RUN APP

if __name__ == "__main__":

    app.run(debug=True)
