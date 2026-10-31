const fileInput = document.getElementById("video");
const fileLabel = document.getElementById("file-label");
const form = document.getElementById("upload-form");
const submitButton = document.getElementById("submit-button");
const statusText = document.getElementById("status");

if (fileInput) {
  fileInput.addEventListener("change", () => {
    fileLabel.textContent = fileInput.files.length
      ? fileInput.files[0].name
      : "Choose a traffic video";
  });
}

if (form) {
  form.addEventListener("submit", () => {
    submitButton.disabled = true;
    submitButton.textContent = "Processing...";
    statusText.textContent = "AI is analyzing your video. Please keep this tab open.";
  });
}
