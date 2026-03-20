<?php
$conexion = mysqli_connect("localhost", "root", "", "clinident_db");

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre   = $_POST['nombre'];
    $apellido = $_POST['apellido'];
    $email    = $_POST['email'];
    $telefono = $_POST['telefono'];
    $password = password_hash($_POST['password'], PASSWORD_DEFAULT);

    $sql = "INSERT INTO usuarios (nombre, apellido, email, telefono, password) 
            VALUES ('$nombre', '$apellido', '$email', '$telefono', '$password')";

    if (mysqli_query($conexion, $sql)) {
        echo "success";
    } else {
        echo "error";
    }
}
?>