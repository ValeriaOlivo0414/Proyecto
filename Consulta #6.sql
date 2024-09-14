DELIMITER //
CREATE PROCEDURE FuncionEstudiantesAction(IN est_id INT, IN action_date DATE)
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
    
    -- Devolver los datos del empleado con la fecha proporcionada
    SELECT Documento, Nombres, Apellidos, Grado, ActionTime, Action
    FROM EstudiantesActions
    WHERE Documento = est_id AND DATE(ActionTime) = action_date;
END //
DELIMITER ;


------------


DELIMITER //
CREATE PROCEDURE FuncionEstudiantesActionByDate(IN action_date DATE)
BEGIN
    -- Devolver los registros que coincidan con la fecha ingresada
    SELECT Documento, Nombres, Apellidos, Grado, ActionTime, Action
    FROM EstudiantesActions
    WHERE DATE(ActionTime) = action_date;
END //
DELIMITER ;
