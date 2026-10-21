CREATE TABLE IF NOT EXISTS persona (
    rut       TEXT PRIMARY KEY,
    nombre    TEXT NOT NULL,
    direccion TEXT,
    telefono  TEXT,
    email     TEXT
);

CREATE TABLE IF NOT EXISTS departamento (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre           TEXT NOT NULL,
    gerente_asignado TEXT
);

CREATE TABLE IF NOT EXISTS empleado (
    rut             TEXT PRIMARY KEY,
    fecha_ingreso   DATE NOT NULL,
    sueldo_base     INTEGER NOT NULL,
    departamento_id INTEGER,
    FOREIGN KEY (rut) REFERENCES persona(rut),
    FOREIGN KEY (departamento_id) REFERENCES departamento(id)
);

CREATE TABLE IF NOT EXISTS registro_tiempo (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    empleado_rut TEXT NOT NULL,
    proyecto_id  INTEGER NOT NULL,
    horas        REAL NOT NULL,
    fecha        DATE NOT NULL,
    descripcion  TEXT,
    FOREIGN KEY (empleado_rut) REFERENCES empleado(rut) ON DELETE CASCADE
);