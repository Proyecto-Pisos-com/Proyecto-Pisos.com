CREATE DATABASE IF NOT EXISTS propiedades_de_ventas;
USE propiedades_de_ventas;

CREATE TABLE IF NOT EXISTS anuncios (
    anuncio_id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(500),
    precio FLOAT,
    ubicacion VARCHAR(300),
    habitaciones INT,
    banos INT,
    metros INT,
    superficie_construida INT,
    superficie_util INT,
    tipo_vivienda VARCHAR(100),
    descripcion_ampliada TEXT NULL,
    link TEXT,
    precio_m2 FLOAT NULL
);