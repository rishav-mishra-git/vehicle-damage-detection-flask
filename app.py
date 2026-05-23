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

    # SEND IMAGE TO ROBOFLOW

    with open(file_path, "rb") as image_file:

        response = requests.post(
            f"{MODEL_URL}?api_key={API_KEY}",
            files={"file": image_file}
        )

    result = response.json()

    predictions = result.get("predictions", [])

    
    # LOAD IMAGE USING PIL

    image = Image.open(file_path).convert("RGB")

    draw = ImageDraw.Draw(image)

    total_cost = 0

    damage_report = []

    # DRAW BOXES

    for p in predictions:

        confidence = p["confidence"]

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

        damage_report.append({

            "damage": damage_class,
            "confidence": round(confidence, 2),
            "cost": cost
        })

    
    # SAVE RESULT IMAGE
   

    result_path = os.path.join(
        UPLOAD_FOLDER,
        "result_" + file.filename
    )

    image.save(result_path)

    return jsonify({

        "damages": damage_report,
        "total_cost": total_cost,
        "result_image": result_path
    })
