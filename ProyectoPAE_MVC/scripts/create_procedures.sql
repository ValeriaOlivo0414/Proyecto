DELIMITER //

-- Procedimiento para ver estudiantes
CREATE PROCEDURE verEstudiantes()
BEGIN
     SELECT * FROM Estudiantes;
END//

-- Procedimiento para crear un estudiante
CREATE PROCEDURE CrearEstudiante(
    IN p_Documento INT,
    IN p_Nombres VARCHAR(100),
    IN p_Apellidos VARCHAR(100),
    IN p_Grado VARCHAR(50)
)
BEGIN
    INSERT INTO Estudiantes (Documento, Nombres, Apellidos, Grado)
    VALUES (p_Documento, p_Nombres, p_Apellidos, p_Grado);
END//

-- Procedimiento para actualizar un estudiante
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
END//

-- Procedimiento para eliminar un estudiante
CREATE PROCEDURE EliminarEstudiante(
    IN p_Documento INT
)
BEGIN
    DELETE FROM Estudiantes
    WHERE Documento = p_Documento;
END//

-- Procedimiento para buscar un estudiante por ID
CREATE PROCEDURE BuscarEstudiante(
    IN p_Documento INTEGER
)
BEGIN
    SELECT
        Documento,
        Nombres,
        Apellidos,
        Grado
    FROM Estudiantes
    WHERE Documento = p_Documento;
END//

-- Procedimiento para ver un evento alimenticio
CREATE PROCEDURE verEventoAlimenticio(
    IN p_ID_evento INT
)
BEGIN
    SELECT * FROM EventosAlimenticios
    WHERE ID_evento = p_ID_evento;
END//

-- Procedimiento para crear un evento alimenticio
CREATE PROCEDURE CrearEventoAlimenticio(
    IN p_ID_evento INT,
    IN p_Documento INT,
    IN p_Fecha DATE,
    IN p_Hora TIME,
    IN p_Tipo_evento VARCHAR(50)
)
BEGIN
    INSERT INTO EventosAlimenticios (ID_evento, Documento, Fecha, Hora, Tipo_evento)
    VALUES (p_ID_evento, p_Documento, p_Fecha, p_Hora, p_Tipo_evento);
END//

-- Procedimiento para actualizar un evento alimenticio
CREATE PROCEDURE ActualizarEventoAlimenticio(
    IN p_ID_evento INT,
    IN p_Documento INT,
    IN p_Fecha DATE,
    IN p_Hora TIME,
    IN p_Tipo_evento VARCHAR(50)
)
BEGIN
    UPDATE EventosAlimenticios
    SET Documento = p_Documento,
        Fecha = p_Fecha,
        Hora = p_Hora,
        Tipo_evento = p_Tipo_evento
    WHERE ID_evento = p_ID_evento;
END//

-- Procedimiento para eliminar un evento alimenticio
CREATE PROCEDURE EliminarEventoAlimenticio(
    IN p_ID_evento INT
)
BEGIN
    DELETE FROM EventosAlimenticios
    WHERE ID_evento = p_ID_evento;
END//

-- Procedimiento para la función de estudiantes action
CREATE PROCEDURE FuncionEstudiantesAction(IN est_id INT)
BEGIN
    DECLARE estudiante_nombres VARCHAR(100);
    DECLARE estudiante_apellidos VARCHAR(100);
    DECLARE estudiante_grado VARCHAR(50);
    DECLARE action_type VARCHAR(20);

    -- Obtener los datos del estudiante
    SELECT Nombres, Apellidos, Grado
    INTO estudiante_nombres, estudiante_apellidos, estudiante_grado
    FROM Estudiantes
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

    -- Devolver los datos del estudiante
    SELECT Documento, Nombres, Apellidos, Grado, action_type AS Action, CURDATE() AS ConsultDate
    FROM Estudiantes
    WHERE Documento = est_id;
END//

DELIMITER ;