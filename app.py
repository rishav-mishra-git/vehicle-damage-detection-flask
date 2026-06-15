from flask import Flask, render_template, request, jsonify
import requests
import os

from PIL import Image
from PIL import ImageDraw

app = Flask(__name__)

# ==========================
# ROBOFLOW CONFIG
# ==========================

API_KEY = "9PU75Z9tiNgXhZlgx5cW"

MODEL_URL = "https://detect.roboflow.com/car_dent_scratch_detection-1-mczqd/1"

# ==========================
# FOLDERS
# ==========================

UPLOAD_FOLDER = "uploads"

RESULT_FOLDER = "static/results"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    RESULT_FOLDER,
    exist_ok=True
)

# ==========================
# DAMAGE COST DATABASE
# ==========================

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

    "Sidemirror-Damage": 3500

}

# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )

# ==========================
# PREDICT API
# ==========================

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:

        return jsonify({
            "error": "No image uploaded"
        }), 400

    file = request.files["image"]

    if file.filename == "":

        return jsonify({
            "error": "No file selected"
        }), 400

    filename = file.filename

    upload_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(upload_path)
        # ==========================
    # SEND IMAGE TO ROBOFLOW
    # ==========================

    with open(upload_path, "rb") as img:

        response = requests.post(

            f"{MODEL_URL}?api_key={API_KEY}",

            files={

                "file": img

            }

        )

    if response.status_code != 200:

        return jsonify({

            "error": "Roboflow API Error",

            "status": response.status_code

        }), 500

    result = response.json()

    predictions = result.get(

        "predictions",

        []

    )

    total_cost = 0

    damage_report = []

    image = Image.open(

        upload_path

    ).convert("RGB")

    draw = ImageDraw.Draw(

        image

    )
        # ==========================
    # PROCESS PREDICTIONS
    # ==========================

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

            "confidence": round(

                confidence,

                2

            ),

            "cost": cost

        })

        x = p["x"]

        y = p["y"]

        width = p["width"]

        height = p["height"]

        x1 = x - width / 2

        y1 = y - height / 2

        x2 = x + width / 2

        y2 = y + height / 2

        draw.rectangle(

            [

                x1,

                y1,

                x2,

                y2

            ],

            outline="red",

            width=5

        )

        draw.text(

            (

                x1,

                y1 - 20

            ),

            damage_class,

            fill="red"

        )
            # ==========================
    # SAVE DETECTED IMAGE
    # ==========================

    result_filename = "detected_" + filename

    result_path = os.path.join(

        RESULT_FOLDER,

        result_filename

    )

    image.save(result_path)

    severity = "Low"

    insurance = "No"

    if total_cost > 25000:

        severity = "High"

        insurance = "Recommended"

    elif total_cost > 10000:

        severity = "Medium"

        insurance = "Recommended"

    else:

        severity = "Low"

        insurance = "Not Required"

    response_data = {

        "damages": damage_report,

        "total_cost": total_cost,

        "severity": severity,

        "insurance": insurance,

        "result_image": result_path.replace("\\\\", "/")

    }
        # ==========================
    # RETURN RESPONSE
    # ==========================

    return jsonify(

        response_data

    )


# ==========================
# HEALTH CHECK
# ==========================

@app.route("/health")
def health():

    return jsonify({

        "status": "running",

        "application": "AI Vehicle Damage Detection",

        "version": "2.0"

    })


# ==========================
# RUN APPLICATION
# ==========================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
