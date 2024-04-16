function togglePasswordVisibilitySignup(field1Id, field2Id) {
    var passwordField1 = document.getElementById(field1Id);
    var passwordField2 = document.getElementById(field2Id);
    var button = event.target;
    if (passwordField1.type === "password") {
        passwordField1.type = "text";
        passwordField2.type = "text";
        button.textContent = "Hide password";
    } else {
        passwordField1.type = "password";
        passwordField2.type = "password";
        button.textContent = "Show password";
    }
}

function togglePasswordVisibilityLogin(fieldId) {
    var passwordField = document.getElementById(fieldId);
    var button = event.target;
    if (passwordField.type === "password") {
        passwordField.type = "text";
        button.textContent = "Hide password";
    } else {
        passwordField.type = "password";
        button.textContent = "Show password";
    }
}




