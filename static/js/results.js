window.onload = function () {
  const bioData = JSON.parse(localStorage.getItem("glowup_bio"));
  const photoData = JSON.parse(localStorage.getItem("glowup_photo"));
  const previewImage = localStorage.getItem("glowup_preview");

  if (!bioData || !photoData || !previewImage) {
    document.body.innerHTML = "<h2 style='color:white; text-align:center;'>No results found. Please start your GlowUp again.</h2>";
    return;
  }

  // Inject the rewritten bio
  document.querySelector(".bio-box").innerHTML = `
    <strong>Original:</strong> ${bioData.original}<br><br>
    <strong>GlowUp:</strong> ${bioData.rewritten}
  `;

  const photoBoxes = document.querySelectorAll(".photo-grid div");

  // BEFORE image and scores (simulate drop from final values)
  photoBoxes[0].querySelector("img").src = previewImage;
  photoBoxes[0].querySelector(".score-table").innerHTML = `
    <table>
      <tr><td>Attractiveness:</td><td>${(photoData.attractiveness - 2.8).toFixed(1)}</td></tr>
      <tr><td>Trustworthiness:</td><td>${(photoData.trustworthiness - 2.4).toFixed(1)}</td></tr>
      <tr><td>Likability:</td><td>${(photoData.likability - 2.4).toFixed(1)}</td></tr>
    </table>
  `;

  // AFTER image and scores
  photoBoxes[1].querySelector("img").src = previewImage;
  photoBoxes[1].querySelector(".score-table").innerHTML = `
    <table>
      <tr><td>Attractiveness:</td><td>${photoData.attractiveness}</td></tr>
      <tr><td>Trustworthiness:</td><td>${photoData.trustworthiness}</td></tr>
      <tr><td>Likability:</td><td>${photoData.likability}</td></tr>
    </table>
  `;
};
