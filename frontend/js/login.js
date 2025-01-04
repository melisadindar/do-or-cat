
document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Sayfanın yenilenmesini önler
  
    const email = document.getElementById("emailInput").value;
    const password = document.getElementById("passwordInput").value;

    try {
        const response = await fetch("http://localhost:8000/auth_service/signin/",{
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        });
        
        const data = await response.json();
        document.getElementById("responseMessage").textContent = data.message;

        if (data.message === "succes"){
            alert("Başarılı Giriş");
            //kullanıcıyı baska bir sayfaya gönder
            //window.location.href = "/login.html";
        }
    }catch (error){
        console.error("Hata:", error);
        document.getElementById("responseMessage").textContent = "Bir hata oluştu.";
    }
});