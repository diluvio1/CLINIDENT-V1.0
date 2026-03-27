<?php
$conexion = mysqli_connect("localhost", "root", "", "clinident_db");

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $correo = mysqli_real_escape_string($conexion, $_POST['usuario']);
    $pass_escrita = $_POST['password'];

    $sql = "SELECT * FROM usuarios WHERE email = '$correo' LIMIT 1";
    $res = mysqli_query($conexion, $sql);

    if (mysqli_num_rows($res) > 0) {
        $fila = mysqli_fetch_assoc($res);
        // Aquí comparamos el hash
        if (password_verify($pass_escrita, $fila['password'])) {
            echo "success";
        } else {
            echo "incorrecto";
        }
    } else {
        echo "no_existe";
    }
}
mysqli_close($conexion);
?>