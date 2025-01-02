document.getElementById('createbtn').addEventListener('click', function(){
    const username = document.getElementById('firstname').value;
    const lastname = document.getElementById('lastname').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const passwordd = document.getElementById('passwordd').value;

    if(firstname && lastname && email && password && passwordd)
    {
        if(isValidEmail(email))
        {
            if(checkPasswords(password, passwordd)){
                createAccount(username, email);
            }
            else{
                alert('Passwords do not match.')
                event.preventDefault(); // Formun gönderilmesini engelle
                return;
            }
        }
        else if(!isValidEmail(email))
        {
            alert('Plese enter a valid email!')
            event.preventDefault(); // Formun gönderilmesini engelle
                return;
        }
    }
    else{
        alert('Please fill out all fields.')
        event.preventDefault(); // Formun gönderilmesini engelle
        return;
    }
    function isValidEmail(email){
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    function checkPasswords(password, passwordd){
        if(password === passwordd)
            return 1;
        else
            return 0;
    }
    function createAccount(username,email){
        alert('Welcome! ' + username);
    }
});

/* document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Sayfanın yenilenmesini önler
  
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://localhost:8000/auth_service/signin/",{
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
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
}); */