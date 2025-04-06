document
  .getElementById("fileInput")
  .addEventListener("change", function (event) {
    let file = event.target.files[0];

    if (file) {
      document.getElementById("fileInfo").style.display = "block";
      document.getElementById("fileName").textContent = file.name;
      document.getElementById("fileSize").textContent = (
        file.size / 1024
      ).toFixed(2);

      // Read file for preview
      let reader = new FileReader();
      reader.onload = function (e) {
        let csvContent = e.target.result.split("\n").slice(0, 5); // Preview first 5 rows
        let tableHTML = "<tr>";

        let headers = csvContent[0].split(",");
        headers.forEach((header) => (tableHTML += <th>${header}</th>));
        tableHTML += "</tr>";

        csvContent.slice(1).forEach((row) => {
          tableHTML += "<tr>";
          let cells = row.split(",");
          cells.forEach((cell) => (tableHTML += <td>${cell}</td>));
          tableHTML += "</tr>";
        });

        document.getElementById("dataPreview").innerHTML = tableHTML;
      };
      reader.readAsText(file);
    }
  });

function uploadFile() {
  let formData = new FormData(document.getElementById("uploadForm"));

  fetch("/", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.blob())
    .then((blob) => {
      let url = window.URL.createObjectURL(blob);
      let a = document.createElement("a");
      a.href = url;
      a.download = "cleaned_dataset.csv";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    })
    .catch((error) => console.error("Error uploading file:", error));
}
