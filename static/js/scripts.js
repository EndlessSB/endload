document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("downloadModal");
    const openModalBtn = document.getElementById("openModalBtn");
    const closeModal = document.querySelector(".close");
    const startDownloadBtn = document.getElementById("startDownload");
    
    openModalBtn.onclick = function () {
        modal.style.display = "block";
    };

    closeModal.onclick = function () {
        modal.style.display = "none";
    };

    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };

    startDownloadBtn.onclick = function () {
        const url = document.getElementById("downloadUrl").value;
        if (!url) {
            alert("Please enter a valid URL.");
            return;
        }

        fetch("/api/downloads/start-download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.succsess || data.error);
            modal.style.display = "none";
        })
        .catch(error => console.error("Error:", error));
    };
});
