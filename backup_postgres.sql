-- Eliminados PRAGMA y BEGIN/COMMIT de SQLite
-- Adaptado para PostgreSQL

CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

INSERT INTO usuario (id, usuario, password) VALUES (1,'david','1234');

CREATE TABLE grupo_muscular (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO grupo_muscular (id, nombre) VALUES
(1,'pecho'),
(2,'biceps'),
(3,'triceps'),
(4,'espalda'),
(5,'hombros'),
(6,'antebrazos'),
(7,'abdomen'),
(8,'gluteos'),
(9,'cuadriceps'),
(10,'isquiotibiales'),
(11,'pantorrillas'),
(12,'pierna');

CREATE TABLE ejercicio (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    archivo VARCHAR(100),
    repeticiones VARCHAR(50),
    grupo_id INTEGER NOT NULL REFERENCES grupo_muscular(id)
);

-- Ejemplo de inserts (puedes mantener todos los que ya tienes)
INSERT INTO ejercicio (id,nombre,archivo,repeticiones,grupo_id) VALUES
(1,'Press banca','press_banca.png','',1),
(2,'Press inclinado','press_inclinado.png','',1),
(3,'Aperturas mancuernas','aperturas_mancuernas.png','',1);

CREATE TABLE rutina (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    dia_semana VARCHAR(20) NOT NULL,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id)
);

INSERT INTO rutina (id,nombre,dia_semana,usuario_id) VALUES
(2,'Rutina de Brazo, Tricep y Espalda','martes',1),
(3,'Rutina de Pecho, Hombro y Antebrazo','lunes',1);

CREATE TABLE progreso (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    peso_levantado INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id)
);

INSERT INTO progreso (id,fecha,peso_levantado,usuario_id) VALUES
(1,'2026-05-24',80,1);

CREATE TABLE ejercicio_rutina (
    id SERIAL PRIMARY KEY,
    rutina_id INTEGER NOT NULL REFERENCES rutina(id),
    ejercicio_id INTEGER NOT NULL REFERENCES ejercicio(id),
    series INTEGER DEFAULT 3 NOT NULL,
    repeticiones INTEGER DEFAULT 10 NOT NULL,
    descanso INTEGER DEFAULT 60 NOT NULL,
    calentamiento BOOLEAN DEFAULT FALSE NOT NULL
);

INSERT INTO ejercicio_rutina (id,rutina_id,ejercicio_id,series,repeticiones,descanso,calentamiento) VALUES
(7,3,1,4,10,60,FALSE),
(8,3,2,4,10,60,FALSE);

CREATE TABLE alembic_version (
    version_num VARCHAR(32) PRIMARY KEY
);

INSERT INTO alembic_version (version_num) VALUES ('c5173c5d38f2');
