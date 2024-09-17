-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS SistemaPae;

-- Usar la base de datos recién creada
USE SistemaPae;

-- Crear la tabla Estudiantes
CREATE TABLE Estudiantes (
    Documento INT PRIMARY KEY,       -- Suponiendo que Documento es un número entero
    Nombres VARCHAR(100) NOT NULL,   -- Longitud máxima para los nombres
    Apellidos VARCHAR(100) NOT NULL, -- Longitud máxima para los apellidos
    Grado VARCHAR(50) NOT NULL       -- Longitud máxima para el grado
);

-- Crear la tabla EventosAlimenticios
CREATE TABLE EventosAlimenticios (
    ID_evento INT PRIMARY KEY,          -- Suponiendo que ID_evento es un número entero
    Documento INT,                      -- Referencia al Documento en la tabla Estudiantes
    Fecha DATE NOT NULL,               -- Tipo de dato para la fecha del evento
    Hora TIME NOT NULL,                -- Tipo de dato para la hora del evento
    Tipo_evento VARCHAR(50) NOT NULL, -- Longitud máxima para el tipo de evento
    FOREIGN KEY (Documento) REFERENCES Estudiantes(Documento) -- Definir la clave foránea
);

--Crear la tabla Asistencia
CREATE TABLE Asistencia (
    ID_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    ID_evento INT,
    Documento INT,
    Asistencia BOOLEAN,
    FOREIGN KEY (ID_evento) REFERENCES EventosAlimenticios(ID_evento),
    FOREIGN KEY (Documento) REFERENCES Estudiantes(Documento)
);





-- Opcional: insertar datos de ejemplo en la tabla Estudiantes
INSERT INTO Estudiantes (Documento, Nombres, Apellidos, Grado)
VALUES (1, 'Juan', 'Pérez', '10º'),
       (2, 'Ana', 'Gómez', '11º');

-- Opcional: insertar datos de ejemplo en la tabla EventosAlimenticios


INSERT INTO EventosAlimenticios (ID_evento, Documento, Fecha, Hora, Tipo_evento)
VALUES (1, 1, '2024-08-10', '08:00:00', 'Desayuno'),
       (2, 2, '2024-08-10', '12:00:00', 'Almuerzo');