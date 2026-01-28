
CREATE DATABASE IF NOT EXISTS consultorio_don_morrondo
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE consultorio_don_morrondo;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    role VARCHAR(20) NOT NULL
);

CREATE TABLE paciente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    eliminado BOOLEAN DEFAULT FALSE
);

CREATE TABLE historia_clinica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    grupo_sanguineo VARCHAR(5),
    eliminado BOOLEAN DEFAULT FALSE
);
