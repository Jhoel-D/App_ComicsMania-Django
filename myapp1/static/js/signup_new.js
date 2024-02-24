document.addEventListener("DOMContentLoaded", function() {
    // Agrega un evento de clic al botón "Iniciar Sesión"
    const btnSignIn = document.getElementById("sign-in");
    btnSignIn.addEventListener("click", function() {
        // Redirecciona al usuario a la página de inicio de sesión
        window.location.href = "{% url 'signin_new' %}";
    });

    // Agrega un evento de clic al botón "Registrarse"
    const btnSignUp = document.getElementById("sign-up");
    btnSignUp.addEventListener("click", function() {
        // Redirecciona al usuario a la página de registro
        window.location.href = "{% url 'signup_new' %}";
    });
});
