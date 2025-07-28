document.getElementById("glowup-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const bio = document.getElementById("bio").value;
  const style = document.getElementById("style").value;
  const file = document.getElementById("photo-upload").files[0];

  if (!bio || !file) {
    alert("Please provide a bio and photo.");
    return;
  }

  // Convert image to base64
  const getBase64 = file => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result.split(",")[1]);
      reader.onerror = error => reject(error);
    });
  };

  const base64Image = await getBase64(file);

  try {
    // Call bio rewriter API
    const bioResponse = await fetch("https://your-backend-url.com/rewrite", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ bio, style })
    });
    const bioData = await bioResponse.json();

    // Call photo scoring API
    const photoResponse = await fetch("https://your-backend-url.com/rate-photo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: base64Image })
    });
    const photoData = await photoResponse.json();

    // Save to localStorage
    localStorage.setItem("glowup_bio", JSON.stringify(bioData));
    localStorage.setItem("glowup_photo", JSON.stringify(photoData));
    localStorage.setItem("glowup_preview", document.getElementById("preview").src);

    // Redirect to results page
    window.location.href = "results.html";
  } catch (error) {
    console.error("Error:", error);
    alert("Something went wrong. Try again.");
  }
});
