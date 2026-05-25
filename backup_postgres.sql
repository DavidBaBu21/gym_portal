-- Adaptado desde SQLite a PostgreSQL
-- Eliminados PRAGMA y BEGIN/COMMIT

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

-- Todos tus ejercicios (ejemplo, mantén todos los INSERT originales)
INSERT INTO ejercicio (id,nombre,archivo,repeticiones,grupo_id) VALUES
(1,'Press banca','press_banca.png','',1),
(2,'Press inclinado','press_inclinado.png','',1),
(3,'Aperturas mancuernas','aperturas_mancuernas.png','',1),
(4,'Cruce polea','cruce_polea.png','',1),
(5,'Flexiones','flexiones.png','',1),
(6,'Dominadas','dominadas.png','',4),
(7,'Jalón pecho polea','jalon_pecho_polea.png','',4),
(8,'Remo barra','remo_barra.png','',4),
(9,'Remo mancuernas','remo_mancuernas.png','',4),
(10,'Peso muerto','peso_muerto.png','',4),
(11,'Press militar','press_militar.png','',5),
(12,'Elevaciones laterales','elevaciones_laterales.png','',5),
(13,'Elevaciones frontales','elevaciones_frontales.png','',5),
(14,'Face pulls','face_pulls.png','',5),
(15,'Press Arnold','press_arnold.png','',5),
(16,'Curl barra recta','curl_barra_recta.png','',2),
(17,'Curl mancuernas','curl_mancuernas.png','',2),
(18,'Curl martillo','curl_martillo.png','',2),
(19,'Curl concentrado','curl_concentrado.png','',2),
(20,'Curl polea baja','curl_polea_baja.png','',2),
(21,'Fondos paralelas','fondos_paralelas.png','',3),
(22,'Extensión polea cuerda','extension_polea_cuerda.png','',3),
(23,'Press francés barra','press_frances_barra.png','',3),
(24,'Patada tríceps','patada_triceps.png','',3),
(25,'Flexiones diamante','flexiones_diamante.png','',3),
(26,'Curl muñeca','curl_muneca.png','',6),
(27,'Curl invertido','curl_invertido.png','',6),
(28,'Farmer’s walk','farmers_walk.png','',6),
(29,'Extensiones muñeca','extensiones_muneca_mancuerna.png','',6),
(30,'Dominadas invertidas','dominadas_invertidas.png','',6),
(31,'Crunch abdominal','crunch_abdominal.png','',7),
(32,'Plancha','plancha.png','',7),
(33,'Elevación piernas','elevacion_piernas.png','',7),
(34,'Russian twists','russian_twists.png','',7),
(35,'AB wheel','ab_wheel.png','',7),
(36,'Hip thrust','hip_thrust.png','',8),
(37,'Sentadilla sumo','sentadilla_sumo.png','',8),
(38,'Peso muerto rumano','peso_muerto_rumano.png','',8),
(39,'Puente glúteos','puente_gluteos.png','',8),
(40,'Step ups','step_ups.png','',8),
(41,'Sentadilla barra','sentadilla_barra.png','',9),
(42,'Prensa pierna','prensa_pierna.png','',9),
(43,'Zancadas','zancadas.png','',9),
(44,'Extensión pierna máquina','extension_pierna_maquina.png','',9),
(45,'Sentadilla frontal','sentadilla_frontal.png','',9),
(46,'Curl pierna máquina','curl_pierna_maquina.png','',10),
(47,'Buenos días barra','buenos_dias_barra.png','',10),
(48,'Glute ham raise','glute_ham_raise.png','',10),
(49,'Sentadilla búlgara','sentadilla_bulgara.png','',10),
(50,'Peso muerto rumano','peso_muerto_rumano.png','',10),
(51,'Elevación talones pie','elevacion_talones_pie.png','',11),
(52,'Elevación talones sentado','elevacion_talones_sentado.png','',11),
(53,'Saltos pliométricos','saltos.png','',11),
(54,'Farmer’s walk puntillas','farmers_walk.png','',11),
(55,'Correr pendiente','correr_pendiente.png','',11),
(56,'Pull over','pull_over.png',NULL,4),
(57,'Remo T en máquina','remo_t.png',NULL,4),
(58,'Remo en polea baja','remo_polea_baja.png',NULL,4),
(59,'Vuelos posteriores','vuelos_posteriores.png',NULL,4),
(60,'Pantorrilla en máquina','pantorrilla_maquina.png',NULL,11),
(61,'Abductores en máquina','abductores_maquina.png',NULL,12),
(62,'Femorales en máquina','femorales_maquina.png',NULL,12);

CREATE TABLE rutina (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    dia_semana VARCHAR(20) NOT NULL,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id)
);

INSERT INTO rutina (id,nombre,dia_semana,usuario_id) VALUES
(2,'Rutina de Brazo, Tricep y Espalda','martes',1),
(3,'Rutina de Pecho, Hombro y Antebrazo','lunes',1),
(4,'Rutina de Pierna Completa','miércoles',1),
(5,'Rutina prueba','domingo',1);

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
(8,3,2,4,10,60,FALSE),
(9,3,3,4,12,60,FALSE),
(10,3,11,4,10,60,FALSE),
(11,3,12,4,12,60,FALSE),
(12,2,7,4,10,60,FALSE),
(13,2,8,4,12,60,FALSE),
(14,2,16,3,10,60,FALSE),
(15,2,17,3,12,60,FALSE),
(16,2,18,3,15,60,FALSE),
(17,2,22,4,12,60,FALSE),
(18,2,23,4,12,60,FALSE),
(19,2,56,3,12,60,FALSE),
(20,2,57,3,10,60,FALSE),
(21,2,58,3,10,60,FALSE),
(22,2,59,3,12,60,FALSE),
(23,4,41,3,10,60,FALSE),
(24,4,42,3,12,60,FALSE),
(25,4,44,3,10,60,FALSE),
(26,4,49,3,10,60,FALSE),
(27,4,60,3,12,60,FALSE),
(28,4,61,3,12,60,FALSE),
(29,4,62,3,12,60,FALSE),
(30,5,1,3,10,60,FALSE),
(31,5,2,3,10,60,FALSE),
(32,5,3,3,10,60,FALSE),
(33,5,4,3,10,60,FALSE),
(34,5,24,3,10,60,FALSE),
(35,5,25,3,10,60,FALSE);


CREATE TABLE alembic_version (
    version_num VARCHAR(32) PRIMARY KEY
);

INSERT INTO alembic_version (version_num) VALUES ('c5173c5d38f2');
