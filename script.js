// Function to upload image and send it to Flask backend
async function uploadImage() {
    const fileInput = document.getElementById("imageInput");
    const loader = document.getElementById("loader");

    // Check if any file is selected
    if (fileInput.files.length === 0) {
        alert("Please select an image first!");
        return;
    }

    // Create FormData object
    let formData = new FormData();
    formData.append("image", fileInput.files[0]);

    // Show loader
    loader.style.display = "block";

    try {
        // Send request to backend
        const response = await fetch("http://127.0.0.1:5000/process", {
            method: "POST",
            body: formData
        });

        // Convert response to JSON
        const data = await response.json();

        // Hide loader
        loader.style.display = "none";

        // Show OCR text
        document.getElementById("ocrText").value = data.ocr_text;

        // Show Summary text
        document.getElementById("summaryText").value = data.summary;

    } catch (error) {
        loader.style.display = "none";
        alert("Error while processing the image.");
        console.error(error);
    }
}
