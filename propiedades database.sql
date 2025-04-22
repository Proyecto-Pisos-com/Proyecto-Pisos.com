CREATE DATABASE IF NOT EXISTS propiedadesanuncios;
USE propiedades;

CREATE TABLE IF NOT EXISTS anuncios (
    anuncio_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    titulo VARCHAR(500),
    precio FLOAT,
    ubicacion VARCHAR(300),
    habitaciones INT,
    banos INT,
    metros INT,
    tipo_vivienda VARCHAR(100),
    superficie_construida INT,
    superficie_util INT,
    certificado_energetico VARCHAR(200),
    descripcion_ampliada TEXT,
    link TEXT,
    imagen_destacada TEXT
);
