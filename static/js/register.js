const form = document.getElementById("registerForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // collect values using IDs
  const data = {
    username: document.getElementById("UserName").value.trim(),
    phone: document.getElementById("PhoneNO").value.trim(),
    email: document.getElementById("SignupEmail").value.trim(),
    password: document.getElementById("SignupPassword").value.trim(),
  };

  try {
    const response = await fetch("/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (result.status === "success") {
      alert("✅ Registered successfully: " + result.message);
      form.reset();
      // optionally redirect to login page
      window.location.href = "/feeds";
    } else {
      alert("❌ Registration failed: " + result.message);
    }
  } catch (err) {
    alert("⚠️ Something went wrong: " + err.message);
  }
});
