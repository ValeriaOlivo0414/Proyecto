-- crear una vista para eventos alimenticios 
DELIMITER $$

CREATE PROCEDURE verEventoAlimenticio(
    IN p_ID_evento INT
)
BEGIN
    SELECT * FROM EventosAlimenticios
    WHERE ID_evento = p_ID_evento;
END$$

DELIMITER ;

-- inserción eventos alimenticios 
DELIMITER $$

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
END$$

DELIMITER ;

-- actualizar un evento aliomenticio  
DELIMITER $$

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
END$$

DELIMITER ;

-- eliminar evento alimenticio 
DELIMITER $$

CREATE PROCEDURE EliminarEventoAlimenticio(
    IN p_ID_evento INT
)
BEGIN
    DELETE FROM EventosAlimenticios
    WHERE ID_evento = p_ID_evento;
END$$

DELIMITER ;

-- buscar por ID 
DELIMITER $$
CREATE PROCEDURE BuscarEventoAlimenticio(
    IN p_ID_Evento INTEGER
)
BEGIN
    SELECT 
        ID_Evento, 
        Documento, 
        Fecha, 
        Hora,
        Tipo_Evento
    FROM eventosalimenticios
    WHERE ID_Evento = p_ID_Evento;
END$$
DELIMITER ;

CALL BuscarPorID(1);