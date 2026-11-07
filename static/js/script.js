// =====================================
// 1. GET HTML ELEMENTS
// =====================================

const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");

const canvas = document.getElementById("drawingCanvas");
const ctx = canvas.getContext("2d");

const clearBtn = document.getElementById("clearBtn");
const uploadPredictBtn = document.getElementById("uploadPredictBtn");
const drawPredictBtn = document.getElementById("drawPredictBtn");

const result = document.getElementById("result");


// =====================================
// 2. INITIALIZE DRAWING CANVAS
// =====================================

ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);

ctx.strokeStyle = "black";
ctx.lineWidth = 18;
ctx.lineCap = "round";
ctx.lineJoin = "round";

let drawing = false;


// =====================================
// 3. IMAGE PREVIEW
// =====================================

imageInput.addEventListener("change", function () {

    const file = imageInput.files[0];

    if (!file) return;

    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";

});


// =====================================
// 4. GET CANVAS POSITION
// =====================================

function getPosition(event) {

    const rect = canvas.getBoundingClientRect();

    return {
        x: (event.clientX - rect.left) * canvas.width / rect.width,
        y: (event.clientY - rect.top) * canvas.height / rect.height
    };

}


// =====================================
// 5. START DRAWING
// =====================================

canvas.addEventListener("pointerdown", function (event) {

    drawing = true;

    canvas.setPointerCapture(event.pointerId);

    const position = getPosition(event);

    ctx.beginPath();
    ctx.moveTo(position.x, position.y);
    ctx.lineTo(position.x + 0.1, position.y + 0.1);
    ctx.stroke();

});


// =====================================
// 6. DRAW DIGIT
// =====================================

canvas.addEventListener("pointermove", function (event) {

    if (!drawing) return;

    const position = getPosition(event);

    ctx.lineTo(position.x, position.y);
    ctx.stroke();

});


// =====================================
// 7. STOP DRAWING
// =====================================

function stopDrawing() {

    drawing = false;
    ctx.beginPath();

}

canvas.addEventListener("pointerup", stopDrawing);
canvas.addEventListener("pointercancel", stopDrawing);


// =====================================
// 8. CLEAR CANVAS
// =====================================

clearBtn.addEventListener("click", function () {

    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "black";

    result.innerHTML = "<p>Your prediction will appear here.</p>";

});


// =====================================
// 9. DISPLAY PREDICTION
// =====================================

function showResult(data) {

    result.innerHTML = `
        <h3>Predicted Digit</h3>

        <div class="predicted-digit">
            ${data.predicted_digit}
        </div>

        <p class="confidence">
            Confidence: ${data.confidence}%
        </p>
    `;

}


// =====================================
// 10. SEND IMAGE TO FLASK
// =====================================

async function sendImage(file) {

    const formData = new FormData();

    formData.append("file", file);

    result.innerHTML = "<p>Predicting...</p>";

    uploadPredictBtn.disabled = true;
    drawPredictBtn.disabled = true;

    try {

        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Prediction failed");
        }

        showResult(data);

    }

    catch (error) {

        result.innerHTML = `
            <p class="error">${error.message}</p>
        `;

        console.error(error);

    }

    finally {

        uploadPredictBtn.disabled = false;
        drawPredictBtn.disabled = false;

    }

}


// =====================================
// 11. PREDICT UPLOADED IMAGE
// =====================================

uploadPredictBtn.addEventListener("click", function () {

    const file = imageInput.files[0];

    if (!file) {

        alert("Please select an image first.");
        return;

    }

    sendImage(file);

});


// =====================================
// 12. PREDICT DRAWN DIGIT
// =====================================

drawPredictBtn.addEventListener("click", function () {

    canvas.toBlob(function (blob) {

        if (!blob) {
            alert("Unable to capture drawing.");
            return;
        }

        const file = new File(
            [blob],
            "drawn_digit.png",
            { type: "image/png" }
        );

        sendImage(file);

    }, "image/png");

});

console.log("Digit Recognition JavaScript loaded successfully!");