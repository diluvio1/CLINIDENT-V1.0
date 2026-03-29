<?php
// Conexión
$conexion = mysqli_connect("localhost", "root", "", "clinident_db");

// Verificar si la conexión falló
if (!$conexion) {
    die("Error de conexión: " . mysqli_connect_error());
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Recibir datos del HTML
    $nombre   = $_POST['nombre'];
    $apellido = $_POST['apellido'];
    $email    = $_POST['email'];
    $telefono = $_POST['telefono'];
    $password = password_hash($_POST['password'], PASSWORD_DEFAULT);

    // SQL ajustado (Solo 5 columnas: nombre, apellido, email, telefono, password)
    // El 'id' se salta porque es AUTO_INCREMENT
    $sql = "INSERT INTO usuarios (nombre, apellido, email, telefono, password) 
            VALUES ('$nombre', '$apellido', '$email', '$telefono', '$password')";

    if (mysqli_query($conexion, $sql)) {
        echo "success";
    } else {
        // Esto nos dirá exactamente qué columna falta o sobra
        echo "Error en la base de datos: " . mysqli_error($conexion);
    }
}
?>