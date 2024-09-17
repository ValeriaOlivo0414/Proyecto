DELIMITER //

CREATE PROCEDURE FuncionEstudiantesAction(IN est_id INT)
BEGIN
    DECLARE estudiante_nombres VARCHAR(100);
    DECLARE estudiante_apellidos VARCHAR(100);
    DECLARE estudiante_grado VARCHAR(50);
    DECLARE action_type VARCHAR(20);
    DECLARE current_count INT;

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

    -- Contar el número de acciones ya registradas para hoy
    SELECT COUNT(*) INTO current_count
    FROM EstudiantesActions
    WHERE Documento = est_id AND DATE(ActionTime) = CURDATE();
    
    -- Insertar en la tabla de respaldo solo si no se han registrado dos acciones hoy
    IF current_count < 2 THEN
        INSERT INTO EstudiantesActions (Documento, Nombres, Apellidos, Grado, ActionTime, Action)
        VALUES (est_id, estudiante_nombres, estudiante_apellidos, estudiante_grado, NOW(), action_type);
    END IF;
    
    -- Devolver los datos del estudiante, ordenados por apellido
    SELECT Documento, Nombres, Apellidos, Grado, ActionTime, Action
    FROM EstudiantesActions
    WHERE Documento = est_id AND DATE(ActionTime) = CURDATE()
    ORDER BY Apellidos;
END //

DELIMITER ;

-- siiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii

DELIMITER //

CREATE PROCEDURE MarcarNoReclamado(IN action_date DATE)
BEGIN
    DECLARE est_id INT;
    DECLARE estudiante_nombres VARCHAR(100);
    DECLARE estudiante_apellidos VARCHAR(100);
    DECLARE estudiante_grado VARCHAR(50);
    DECLARE action_time DATETIME;

    -- Cursor para recorrer todos los estudiantes
    DECLARE cur CURSOR FOR 
        SELECT Documento, Nombres, Apellidos, Grado 
        FROM estudiantes;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET @done = 1;

    OPEN cur;

    -- Procesar cada estudiante
    read_loop: LOOP
        FETCH cur INTO est_id, estudiante_nombres, estudiante_apellidos, estudiante_grado;
        IF @done THEN
            LEAVE read_loop;
        END IF;

        -- Verificar cuántas acciones ha realizado el estudiante en la fecha dada
        IF (SELECT COUNT(*) FROM EstudiantesActions WHERE Documento = est_id AND DATE(ActionTime) = action_date) = 0 THEN
            -- Insertar dos acciones "No reclamado" si no ha registrado ninguna acción
            INSERT INTO EstudiantesActions (Documento, Nombres, Apellidos, Grado, ActionTime, Action)
            VALUES (est_id, estudiante_nombres, estudiante_apellidos, estudiante_grado, CONCAT(action_date, ' 09:00:00'), 'No reclamado'),
                   (est_id, estudiante_nombres, estudiante_apellidos, estudiante_grado, CONCAT(action_date, ' 13:00:00'), 'No reclamado');
        ELSE
            -- Insertar la acción faltante como "No reclamado" si falta alguna
            SET action_time = CONCAT(action_date, ' 09:00:00');
            IF (SELECT COUNT(*) FROM EstudiantesActions WHERE Documento = est_id AND ActionTime = action_time) = 0 THEN
                INSERT INTO EstudiantesActions (Documento, Nombres, Apellidos, Grado, ActionTime, Action)
                VALUES (est_id, estudiante_nombres, estudiante_apellidos, estudiante_grado, action_time, 'No reclamado');
            END IF;

            SET action_time = CONCAT(action_date, ' 13:00:00');
            IF (SELECT COUNT(*) FROM EstudiantesActions WHERE Documento = est_id AND ActionTime = action_time) = 0 THEN
                INSERT INTO EstudiantesActions (Documento, Nombres, Apellidos, Grado, ActionTime, Action)
                VALUES (est_id, estudiante_nombres, estudiante_apellidos, estudiante_grado, action_time, 'No reclamado');
            END IF;
        END IF;
    END LOOP;

    CLOSE cur;
END //

DELIMITER ;

-- siiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii

DELIMITER //

CREATE PROCEDURE FuncionEstudiantesActionByDate(IN action_date DATE)
BEGIN
    -- Seleccionar los registros de la tabla EstudiantesActions para una fecha específica
    SELECT Documento, Nombres, Apellidos, Grado, Action, ActionTime
    FROM EstudiantesActions
    WHERE DATE(ActionTime) = action_date
    ORDER BY Apellidos, Nombres;  -- Ordenar por Apellidos, luego por Nombres
END //

DELIMITER ;