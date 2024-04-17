function togglePasswordVisibilitySignup(field1Id, field2Id) {
    var passwordField1 = document.getElementById(field1Id);
    var passwordField2 = document.getElementById(field2Id);
    var keyIcon = document.getElementById("key-icon");

    if (passwordField1.type === "password") {
        passwordField1.type = "text";
        passwordField2.type = "text";
        keyIcon.textContent = "visibility_off";
    } else {
        passwordField1.type = "password";
        passwordField2.type = "password";
        keyIcon.textContent = "visibility";
    }
}

function togglePasswordVisibilityLogin(fieldId) {
    var passwordField = document.getElementById(fieldId);
    var keyIcon = document.getElementById("key-icon");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        keyIcon.textContent = "visibility_off";
    } else {
        passwordField.type = "password";
        keyIcon.textContent = "visibility";
    }
}




