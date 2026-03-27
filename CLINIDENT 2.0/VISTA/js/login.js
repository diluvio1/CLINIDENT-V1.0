



function gestionarAcceso() {
    const user = document.getElementById('user-name').value;
    const pass = document.getElementById('user-pass').value;
    const rol = document.getElementById('user-role').value;

            // 1. Verificamos que no esté vacío
    if (user === "" || pass === "") {
        alert("⚠️ Por favor escribe tu usuario y contraseña");
        return;
    }

    // REDIRECCIONES
    if(rol === "paciente"){
        window.location.href = "agenda.html";
    } 
    else if(rol === "odontologo"){
        window.location.href = "odontologo.html";
    }
    else if(rol === "admin"){
        window.location.href = "odontologo.html";
    }
    else{
        window.location.href = "odontologo.html";
    }
}

// PWA
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js')
    .then(() => console.log('Service Worker registrado'))
    .catch(err => console.log('Error:', err));
}

function irARegistro(){
    window.location.href = "registro.html";
}
