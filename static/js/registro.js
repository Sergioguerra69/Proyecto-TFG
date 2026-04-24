// JavaScript para formulario de registro - VetCT

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-registro');
    const alerta = document.getElementById('js-alerta');

    form.addEventListener('submit', function (event) {
        let error = false;
        let mensajeError = "";

        // Obtener campos
        const firstName = document.getElementById('id_first_name');
        const lastName = document.getElementById('id_last_name');
        const username = document.getElementById('id_username');
        const email = document.getElementById('id_email');
        const pass1 = document.getElementById('id_password1');
        const pass2 = document.getElementById('id_password2');

        // Reset alertas
        alerta.classList.add('d-none');
        alerta.innerText = "";

        // Validar campos vacíos
        if (firstName.value == "" || lastName.value == "" || username.value == "" || email.value == "" || pass1.value == "" || pass2.value == "") {
            error = true;
            mensajeError = "Complete todos los campos obligatorios.";
        }
        // Validar contraseñas
        else if (pass1.value != pass2.value) {
            error = true;
            mensajeError = "Las contraseñas no coinciden.";
        }

        if (error) {
            event.preventDefault();
            alert(mensajeError);
            alerta.innerText = mensajeError;
            alerta.classList.remove('d-none');
            window.scrollTo(0, 0);
        }
    });
});
