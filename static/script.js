async function uploadImage() {

    const input = document.getElementById("imageInput");

    const file = input.files[0];

    if (!file) {

        alert("Please select an image");

        return;
    }

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

    html += `
        <h2>
            Total Estimated Cost:
            ₹${data.total_cost}
        </h2>
    `;

    data.damages.forEach(d => {

        html += `
            <p>
                <strong>${d.damage}</strong>
                |
                Confidence: ${d.confidence}
                |
                Cost: ₹${d.cost}
            </p>
        `;
    });

    document.getElementById("loading").innerHTML = "";

    document.getElementById("result").innerHTML = html;
}
