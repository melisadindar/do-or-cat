
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
            body: JSON.stringify({
                email,
                password,
            })
        });
        
        const data = await response.json();
        console.log("API Yanıtı:", data); // API yanıtını logla


        if (data.message === "Sign in is succes"){
            alert("Başarılı Giriş");
            window.location.href = "calendar.html";
            //kullanıcıyı baska bir sayfaya gönder
            //window.location.href = "/login.html";
        }
        else{
            alert(`Giriş başarısız: ${data.message}`);
        }

    }catch (error){
        console.error("Hata:", error);
    }
});