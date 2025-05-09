CREATE DATABASE IF NOT EXISTS propiedades_de_alquiler;
USE propiedades_de_alquiler;

CREATE TABLE IF NOT EXISTS anuncios (
    anuncio_id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(500),
    precio FLOAT,
    ubicacion VARCHAR(300),
    habitaciones INT,
    baños INT,
    metros INT,
    superficie_construida INT,
    tipo_vivienda VARCHAR(100),
    link TEXT
);