document.getElementById("registerform").addEventListener("submit", async function (event) {
    event.preventDefault();

    const first_name = document.getElementById("firstname").value;
    const last_name = document.getElementById("lastname").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("passwordd").value;

    if (!first_name || !last_name || !email || !password || !confirmPassword) {
        alert("Lütfen tüm alanları doldurun.");
        return;
    }

    if (password !== confirmPassword) {
        alert("Şifreler eşleşmiyor!");
        return;
    }

    if (!isValidEmail(email)) {
        alert("Geçerli bir e-posta adresi giriniz.");
        return;
    }

    try {
        // Backend'e istek gönderiyoruz
            const response = await fetch("http://localhost:8000/auth_service/signup/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                first_name,  // Correct key names
                last_name,
                email,
                password,
            })            
        });
        if (!response.ok) {
            const errorMessage = await response.text(); // Yanıtın ham içeriğini al
            console.error("Hata mesajı:", errorMessage);
            alert("Bir hata oluştu: " + errorMessage);
            return;
        }

        // Backend'den dönen cevabı işliyoruz
        const data = await response.json();

        if (response.ok) {
            alert("Kayıt başarılı!");
            window.location.href = "login.html";
        } else {
            alert(`Kayıt başarısız: ${data.message}`);
        }
    } catch (error) {
        console.error("Hata:", error);
        alert(`Bir hata oluştu. Lütfen daha sonra tekrar deneyin.`);
    }
});

// E-posta doğrulama fonksiyonu
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}
