document.getElementById("confirmemail").addEventListener("submit", function (event) {
    event.preventDefault(); // Formun yeniden yüklenmesini engelle

    const codeInput = document.querySelector(".code").value; // Kullanıcının girdiği kodu al
    const newPasswordForm = document.getElementById("newpassword");
    const confirmForm = document.getElementById("confirmemail");

    // Kod doğrulama işlemi (örnek: doğru kod "1234")
    if (codeInput === "1234") {
        // İlk formu gizle
        confirmForm.classList.add("hidden");

        // İkinci formu göster
        newPasswordForm.classList.remove("hidden");
        console.log("Hidden class removed successfully.");
    } else {
        alert("Invalid code. Please try again.");
    }
});
