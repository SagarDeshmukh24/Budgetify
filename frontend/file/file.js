document.getElementById("csvForm").addEventListener("submit", function (e) {
    e.preventDefault();

    var fileInput = document.getElementById("csvFile");
    var file = fileInput.files[0];

    if (!file) {
        alert("Please select a CSV file");
        return;
    }

    var formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:8000/customer/upload_csv/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("message").innerText = data.message;
        console.log("Success:", data);
        
        $timeout(function () {
      }, 5000);
        
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("message").innerText = "Upload failed";
    });
});
