<?php
// Desactivar cualquier error visible que ensucie la respuesta
error_reporting(0);

// 1. Conexión
$conexion = mysqli_connect("localhost", "root", "", "clinident_db");

if (!$conexion) {
    echo "error_conexion";
    exit;
}

// 2. Proceso
if (isset($_POST['email'])) {
    $email = mysqli_real_escape_string($conexion, $_POST['email']);

    // IMPORTANTE: Verifica si tu columna se llama 'email' o 'correo'
    $sql = "SELECT id FROM usuarios WHERE email = '$email'";
    $resultado = mysqli_query($conexion, $sql);

    if (mysqli_num_rows($resultado) > 0) {
        echo "registrado";
    } else {
        echo "no_registrado";
    }
} else {
    echo "no_llego_dato";
}

mysqli_close($conexion);
?>