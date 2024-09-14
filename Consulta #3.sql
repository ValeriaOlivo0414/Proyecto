-- crear una vista para estudiantes
DELIMITER $$
CREATE PROCEDURE verEstudiantes()
BEGIN
     SELECT * FROM estudiantes;
END$$
DELIMITER ;

-- inserción estudiante
DELIMITER $$

CREATE PROCEDURE CrearEstudiante(
    IN p_Documento INT,
    IN p_Nombres VARCHAR(100),
    IN p_Apellidos VARCHAR(100),
    IN p_Grado VARCHAR(50)
)
BEGIN
    INSERT INTO Estudiantes (Documento, Nombres, Apellidos, Grado)
    VALUES (p_Documento, p_Nombres, p_Apellidos, p_Grado);
END$$

DELIMITER ;

CALL CrearEstudiante('1037674375', 'Kelvin Javier', 'Restrepo Villalonga','11');
SELECT * FROM estudiantes

-- actualizar estudiante 
DELIMITER $$

CREATE PROCEDURE ActualizarEstudiante(
    IN p_Documento INT,
    IN p_Nombres VARCHAR(100),
    IN p_Apellidos VARCHAR(100),
    IN p_Grado VARCHAR(50)
)
BEGIN
    UPDATE Estudiantes
    SET Nombres = p_Nombres,
        Apellidos = p_Apellidos,
        Grado = p_Grado
    WHERE Documento = p_Documento;
END$$

DELIMITER ;

-- eliminar estudiante 
DELIMITER $$

CREATE PROCEDURE EliminarEstudiante(
    IN p_Documento INT
)
BEGIN
    DELETE FROM Estudiantes
    WHERE Documento = p_Documento;
END$$

DELIMITER ;

-- buscar estudiante por Id
DELIMITER $$
CREATE PROCEDURE BuscarEstudiante(
    IN p_Documento INTEGER
)
BEGIN
    SELECT 
        Documento, 
        Nombres, 
        Apellidos, 
        Grado
    FROM estudiantes
    WHERE Documento = p_Documento;
END$$
DELIMITER ;

CALL BuscarPorID(1);