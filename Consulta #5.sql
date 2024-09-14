-- Crear la tabla EstudiantesActions
CREATE TABLE EstudiantesActions (
    ActionID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Documento INTEGER,
    Nombres VARCHAR(100),
    Apellidos VARCHAR(100),
    Grado VARCHAR(50),
    ActionTime DATETIME,
    Action VARCHAR(20),
    FOREIGN KEY (Documento) REFERENCES estudiantes(Documento)
);

-- Crear el procedimiento almacenado
DELIMITER //

CREATE PROCEDURE FuncionEstudiantesAction(IN est_id INT)
BEGIN
    DECLARE estudiante_nombres VARCHAR(100);
    DECLARE estudiante_apellidos VARCHAR(100);
    DECLARE estudiante_grado VARCHAR(50);
    DECLARE action_type VARCHAR(20);
    
    -- Obtener los datos del estudiante
    SELECT Nombres, Apellidos, Grado 
    INTO estudiante_nombres, estudiante_apellidos, estudiante_grado
    FROM estudiantes 
    WHERE Documento = est_id;
    
    -- Determinar la acción basada en la hora actual
    SET action_type = 'Fuera de horario';
    
    IF CURRENT_TIME() BETWEEN '08:00:00' AND '10:00:00' THEN
        SET action_type = 'Refrigerio';
    ELSEIF CURRENT_TIME() BETWEEN '12:00:00' AND '13:40:00' THEN
        SET action_type = 'Almuerzo';
    END IF;
    
    -- Insertar en la tabla de respaldo
    INSERT INTO EstudiantesActions (Documento, Nombres, Apellidos, Grado, ActionTime, Action)
    VALUES (est_id, estudiante_nombres, estudiante_apellidos, estudiante_grado, NOW(), action_type);
    
    -- Devolver los datos del empleado
    SELECT Documento, Nombres, Apellidos, Grado, action_type AS Action
    FROM estudiantes
    WHERE Documento = est_id;
END //

DELIMITER ;

INSERT INTO estudiantesactions VALUES(1037674375,'Kelvin Javier','Restrepo Villalonga','11-T');

CALL FuncionEstudiantesAction(5962225)
SELECT * FROM EstudiantesActions
SELECT * FROM estudiantes

CALL EstudiantesActions



-- Modificar la tabla EstudiantesActions para incluir la fecha de consulta
ALTER TABLE EstudiantesActions
ADD COLUMN ConsultDate DATE AFTER ActionTime;















-- Modificar el procedimiento almacenado
DELIMITER //

DROP PROCEDURE IF EXISTS FuncionEstudiantesAction 

CREATE PROCEDURE FuncionEstudiantesAction(IN est_id INT)
BEGIN
    DECLARE estudiante_nombres VARCHAR(100);
    DECLARE estudiante_apellidos VARCHAR(100);
    DECLARE estudiante_grado VARCHAR(50);
    DECLARE action_type VARCHAR(20);
    
    -- Obtener los datos del empleado
    SELECT Nombres, Apellidos, Grado
    INTO estudiante_nombres, estudiante_apellidos, estudiante_grado
    FROM estudiantes
    WHERE Documento = est_id;
    
    -- Determinar la acción basada en la hora actual
    SET action_type = 'FUERA DE HORARIO';
    
    IF CURRENT_TIME() BETWEEN '08:00:00' AND '10:00:00' THEN
        SET action_type = 'REFRIGERIO';
    ELSEIF CURRENT_TIME() BETWEEN '12:00:00' AND '13:40:00' THEN
        SET action_type = 'ALMUERZO';
    END IF;
    
    -- Insertar en la tabla de respaldo
    INSERT INTO EstudiantesActions (Documento, Nombres, Apellidos, Grado, ActionTime, ConsultDate, Action)
    VALUES (est_id, estudiante_nombres, estudiante_apellidos, estudiante_grado, NOW(), CURDATE(), action_type);
    
    -- Devolver los datos del empleado
    SELECT Documento, Nombres, Apellidos, Grado, action_type AS Action, CURDATE() AS ConsultDate
    FROM estudiantes
    WHERE Documento = est_id;
END //

DELIMITER ;

-- Ejemplo de uso del procedimiento
-- CALL FuncionEstudiantesAction(1);