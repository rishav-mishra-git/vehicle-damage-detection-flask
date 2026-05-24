async function uploadImage() {

    const input = document.getElementById("imageInput");

    const file = input.files[0];

    if (!file) {

        alert("Please select an image");

        return;
    }

    // IMAGE PREVIEW

    const previewURL = URL.createObjectURL(file);

    document.getElementById("preview").innerHTML = `

        <h2>Uploaded Image</h2>

        <img src="${previewURL}" width="600">
    `;

    document.getElementById("loading").innerHTML =
        "🔍 Analyzing vehicle damage...";

    const formData = new FormData();

    formData.append("image", file);

    const response = await fetch("/predict", {

        method: "POST",

        body: formData
    });

    const data = await response.json();

    let totalDamages = data.damages.length;

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

    let html = "";

    // RESULT IMAGE

    html += `

        <h2>Detected Damage</h2>

        <img
            src="/${data.result_image}"
            width="600"
        >

        <div class="summary-cards">

            <div class="card">

                <h3>Total Damages</h3>

                <p>${totalDamages}</p>

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

    // INSURANCE MESSAGE

    if (data.total_cost > 25000) {

        html += `
            <div class="damage-card">

                ⚠ Insurance Claim Recommended

            </div>
        `;
    }

    else if (data.total_cost > 10000) {

        html += `
            <div class="damage-card">

                ⚠ Moderate Damage Detected

            </div>
        `;
    }

    else {

        html += `
            <div class="damage-card">

                ✅ Minor Damage Detected

            </div>
        `;
    }

    // DAMAGE DETAILS

    data.damages.forEach(d => {

        let confidencePercent =
            Math.round(d.confidence * 100);

        let barClass = "low";

        if (confidencePercent > 80) {

            barClass = "high";
        }

        else if (confidencePercent > 60) {

            barClass = "medium";
        }

        html += `

            <div class="damage-card">

                <h3>${d.damage}</h3>

                <p>
                    Estimated Cost:
                    ₹${d.cost}
                </p>

                <p>
                    Confidence:
                    ${confidencePercent}%
                </p>

                <div class="progress-bar">

                    <div
                        class="progress ${barClass}"
                        style="width:${confidencePercent}%"
                    >

                        ${confidencePercent}%

                    </div>

                </div>

            </div>
        `;
    });

    document.getElementById("loading").innerHTML = "";

    document.getElementById("result").innerHTML = html;
}
