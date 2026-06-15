
async function uploadImage() {

    const input = document.getElementById("imageInput");
    const file = input.files[0];

    if (!file) {
        alert("Please select an image.");
        return;
    }

    // Show preview
    const previewURL = URL.createObjectURL(file);

    document.getElementById("preview").innerHTML = `
        <h2>📷 Uploaded Image</h2>
        <img src="${previewURL}" alt="Uploaded Image">
    `;

    document.getElementById("loading").innerHTML = `
        <div style="text-align:center;padding:20px;">
            <h2>🤖 AI is analyzing your vehicle...</h2>
            <p>Please wait a few seconds.</p>
        </div>
    `;

    document.getElementById("result").innerHTML = "";
    document.getElementById("resultImage").innerHTML = "";

    const formData = new FormData();
    formData.append("image", file);

    try {

        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        document.getElementById("loading").innerHTML = "";

        let severity = "Low";
        let severityClass = "low";

        if (data.total_cost > 25000) {
            severity = "High";
            severityClass = "high";
        }
        else if (data.total_cost > 10000) {
            severity = "Medium";
            severityClass = "medium";
        }

        let html = `

        <div class="summary-cards">

            <div class="card">
                <h3>Total Damages</h3>
                <p>${data.damages.length}</p>
            </div>

            <div class="card">
                <h3>Estimated Cost</h3>
                <p>₹${data.total_cost}</p>
            </div>

            <div class="card">
                <h3>Severity</h3>
                <p class="${severityClass}">
                    ${severity}
                </p>
            </div>

        </div>

        `;

        if (severity === "High") {

            html += `
            <div class="damage-card">

            🚨 High Damage Detected

            <br><br>

            Insurance claim is recommended.

            </div>
            `;
        }

        else if (severity === "Medium") {

            html += `
            <div class="damage-card">

            ⚠ Moderate Damage

            <br><br>

            Repair soon to avoid further issues.

            </div>
            `;
        }

        else {

            html += `
            <div class="damage-card">

            ✅ Minor Damage

            <br><br>

            Basic repair is sufficient.

            </div>
            `;
        }

        data.damages.forEach(d => {

            const confidence =
                Math.round(d.confidence * 100);

            let barClass = "low";

            if (confidence > 80)
                barClass = "high";

            else if (confidence > 60)
                barClass = "medium";

            html += `

            <div class="damage-card">

                <h2>${d.damage}</h2>

                <p>

                Repair Cost:
                ₹${d.cost}

                </p>

                <p>

                Confidence:
                ${confidence}%

                </p>

                <div class="progress-bar">

                    <div
                        class="progress ${barClass}"
                        style="width:${confidence}%"
                    >

                        ${confidence}%

                    </div>

                </div>

            </div>

            `;
        });

        document.getElementById("result").innerHTML = html;

    }

    catch (error) {

        document.getElementById("loading").innerHTML = "";

        document.getElementById("result").innerHTML = `

        <div class="damage-card">

        ❌ Error while processing image.

        <br><br>

        Please try again.

        </div>

        `;
    }

}

