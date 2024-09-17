-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS SistemaPae;

-- Usar la base de datos recién creada
USE SistemaPae;

-- Crear la tabla Estudiantes
CREATE TABLE Estudiantes (
    Documento INT PRIMARY KEY,
    Nombres VARCHAR(100) NOT NULL,
    Apellidos VARCHAR(100) NOT NULL,
    Grado VARCHAR(50) NOT NULL
);

-- Crear la tabla EventosAlimenticios
CREATE TABLE EventosAlimenticios (
    ID_evento INT PRIMARY KEY,
    Documento INT,
    Fecha DATE NOT NULL,
    Hora TIME NOT NULL,
    Tipo_evento VARCHAR(50) NOT NULL,
    FOREIGN KEY (Documento) REFERENCES Estudiantes(Documento)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Crear la tabla Asistencia
CREATE TABLE Asistencia (
    ID_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    ID_evento INT,
    Documento INT,
    Asistencia TINYINT(1),
    FOREIGN KEY (ID_evento) REFERENCES EventosAlimenticios(ID_evento)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Documento) REFERENCES Estudiantes(Documento)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Crear la tabla EstudiantesActions
CREATE TABLE EstudiantesActions (
    ActionID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Documento INTEGER,
    Nombres VARCHAR(100),
    Apellidos VARCHAR(100),
    Grado VARCHAR(50),
    ActionTime DATETIME,
    Action VARCHAR(20),
    ConsultDate DATE,
    FOREIGN KEY (Documento) REFERENCES Estudiantes(Documento)
);

-- Insertar datos de ejemplo en la tabla Estudiantes
INSERT INTO Estudiantes (Documento, Nombres, Apellidos, Grado)
VALUES (1, 'Juan', 'Pérez', '10'),
       (2, 'Ana', 'Gómez', '11');

-- Insertar datos de ejemplo en la tabla EventosAlimenticios
INSERT INTO EventosAlimenticios (ID_evento, Documento, Fecha, Hora, Tipo_evento)
VALUES (1, 1, '2024-08-10', '08:00:00', 'Desayuno'),
       (2, 2, '2024-08-10', '12:00:00', 'Almuerzo');