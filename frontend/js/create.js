document.getElementById("registerform").addEventListener("submit", async function (event) {
    event.preventDefault();

    const firstname = document.getElementById("firstname").value;
    const lastname = document.getElementById("lastname").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("passwordd").value;

    if (!firstname || !lastname || !email || !password || !confirmPassword) {
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
        const response = await fetch("http://localhost:8000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                firstname,
                lastname,
                email,
                password,
            }),
        });

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
        alert(`Bir hata oluştu. Lütfen daha sonra tekrar deneyin. Hata detayları: ${error.message}`);
    }
});

// E-posta doğrulama fonksiyonu
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}
