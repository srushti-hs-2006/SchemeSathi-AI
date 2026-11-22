
document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const fileInput = document.getElementById("pdf_file");
    const fileName = document.getElementById("file-name");
    const submitButton = document.getElementById("submit-btn");
    const languageSelect = document.getElementById("language");

    // Prevent errors if an expected HTML element is missing
    if (!form || !fileInput || !fileName ||
        !submitButton || !languageSelect) {
        console.error("SchemeSathi AI: Required HTML elements not found.");
        return;
    }

    // Add animated loading spinner styles
    const loadingStyles = document.createElement("style");

    loadingStyles.textContent = `
        .scheme-loading-spinner {
            display: inline-block;
            width: 15px;
            height: 15px;
            margin-right: 9px;
            border: 2px solid rgba(255,255,255,0.4);
            border-top-color: white;
            border-radius: 50%;
            vertical-align: middle;
            animation: schemeSpin 0.8s linear infinite;
        }

        @keyframes schemeSpin {
            to {
                transform: rotate(360deg);
            }
        }

        #submit-btn:disabled {
            opacity: 0.75;
            cursor: not-allowed;
        }
    `;

    document.head.appendChild(loadingStyles);


    // --------------------------------
    // DISPLAY SELECTED PDF FILENAME
    // --------------------------------

    fileInput.addEventListener("change", function () {

        const file = fileInput.files[0];

        if (!file) {
            fileName.textContent = "Click here to browse your files";
            return;
        }

        // Check PDF extension
        if (!file.name.toLowerCase().endsWith(".pdf")) {

            alert("Please select a valid PDF file.");

            fileInput.value = "";
            fileName.textContent = "Click here to browse your files";

            return;
        }

        // Check file size
        if (file.size > 10 * 1024 * 1024) {

            alert("File size must be less than 10 MB.");

            fileInput.value = "";
            fileName.textContent = "Click here to browse your files";

            return;
        }

        // Display filename
        fileName.textContent = file.name;

    });


    // --------------------------------
    // FORM VALIDATION
    // --------------------------------

    form.addEventListener("submit", function (event) {

        const file = fileInput.files[0];

        // Check whether a PDF is selected
        if (!file) {

            event.preventDefault();

            alert("Please upload a government scheme PDF.");

            return;
        }

        // Check PDF extension
        if (!file.name.toLowerCase().endsWith(".pdf")) {

            event.preventDefault();

            alert("Only PDF files are allowed.");

            return;
        }

        // Check PDF size
        if (file.size > 10 * 1024 * 1024) {

            event.preventDefault();

            alert("PDF size must not exceed 10 MB.");

            return;
        }

        // Check language selection
        if (!languageSelect.value) {

            event.preventDefault();

            alert("Please select a language.");

            return;
        }

        // Prevent multiple submissions
        if (submitButton.disabled) {

            event.preventDefault();

            return;
        }


        // --------------------------------
        // SHOW LOADING ANIMATION
        // --------------------------------

        submitButton.disabled = true;

        submitButton.innerHTML = `
            <span class="scheme-loading-spinner"></span>
            Analyzing Your Document...
        `;

    });

});
