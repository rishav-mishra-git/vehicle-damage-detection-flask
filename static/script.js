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

        <h3>Uploaded Image</h3>

        <img
            src="${previewURL}"
            width="500"
            style="border-radius:10px;"
        >
    `;

    document.getElementById("loading").innerHTML =
        "<p>Detecting damages...</p>";

    const formData = new FormData();

    formData.append("image", file);

    const response = await fetch("/predict", {

        method: "POST",

        body: formData
    });

    const data = await response.json();

    let html = "";

    // RESULT IMAGE

    html += `

        <h2>Detected Damage</h2>

        <img
            src="/${data.result_image}"
            width="500"
            style="border-radius:10px;"
        >

        <h2>
            Total Estimated Cost:
            ₹${data.total_cost}
        </h2>
    `;

    // DAMAGE DETAILS

    data.damages.forEach(d => {

        html += `

            <div
                style="
                    background:#f4f4f4;
                    padding:10px;
                    margin:10px;
                    border-radius:8px;
                "
            >

                <strong>${d.damage}</strong>

                <br>

                Confidence: ${d.confidence}

                <br>

                Estimated Cost: ₹${d.cost}

            </div>
        `;
    });

    document.getElementById("loading").innerHTML = "";

    document.getElementById("result").innerHTML = html;
}
