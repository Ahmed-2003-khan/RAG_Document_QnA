function embedDocuments() {
  showLoading("Embedding documents...");

  fetch("http://127.0.0.1:8000/embed", {
    method: "POST",
  })
    .then((res) => res.json())
    .then((data) => {
      updateResponse("✅ " + data.message);
    })
    .catch((err) => {
      updateResponse("❌ Error: " + err.message);
    });
}


function askQuestion() {
  const question = document.getElementById("userQuestion").value;
  if (!question) return;

  showLoading("Thinking...");

  fetch("http://127.0.0.1:8000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  })
    .then((res) => res.json())
    .then((data) => {
      updateResponse("🤖 " + data.answer);
    })
    .catch((err) => {
      updateResponse("❌ Error: " + err.message);
    });
}

function updateResponse(text) {
  document.getElementById("responseContainer").textContent = text;
}

function showLoading(message) {
  document.getElementById("responseContainer").textContent = "⏳ " + message;
}
