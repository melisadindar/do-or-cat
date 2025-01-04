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
