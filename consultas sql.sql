-- Mostrar todos los anuncios registrados
SELECT * 
FROM anuncios;

-- Mostrar la fecha (timestamp), título y el precio de cada anuncio
SELECT timestamp, titulo, precio 
FROM anuncios;

-- Mostrar propiedades con más de x habitaciones
SELECT titulo, habitaciones 
FROM anuncios 
WHERE habitaciones > ?;

-- Mostrar propiedades con superficie mayor a 100 m²
SELECT titulo, metros 
FROM anuncios 
WHERE metros > 100;

-- Mostrar precio promedio por tipo de propiedad
SELECT tipo_vivienda, AVG(precio) AS precio_promedio 
FROM anuncios 
GROUP BY tipo_vivienda;

-- Mostrar la cantidad total de anuncios publicados
SELECT COUNT(*) AS total_anuncios 
FROM anuncios;

-- Mostrar anuncios ordenados por precio (de mayor a menor)
SELECT titulo, precio 
FROM anuncios 
ORDER BY precio ASC;

-- Mostrar anuncios ordenados por precio (de mayor a menor)
SELECT titulo, precio 
FROM anuncios 
ORDER BY precio DESC;

-- Mostrar propiedades dentro de un rango de precio determinado por el usuario
SELECT titulo, tipo_vivienda, precio, ubicacion 
FROM anuncios 
WHERE precio BETWEEN ? AND ?;