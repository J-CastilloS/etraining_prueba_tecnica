-- Tabla department
CREATE TABLE department (
    id_department INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Tabla municipality
CREATE TABLE municipality (
    id_municipality INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    id_department INTEGER,
    FOREIGN KEY (id_department) REFERENCES department(id_department)
);

-- Tabla gender
CREATE TABLE gender (
    id_gender INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Tabla status
CREATE TABLE status (
    id_status INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Tabla type_contagion
CREATE TABLE type_contagion (
    id_type_contagion INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Tabla cases
CREATE TABLE cases (
    id_case INTEGER PRIMARY KEY AUTOINCREMENT,
    id_municipality INTEGER,
    age INTEGER,
    id_gender INTEGER,
    id_type INTEGER,
    id_status FLOAT64,
    date_symptom TEXT,
    date_death TEXT,
    date_diagnosis TEXT,
    date_recovery TEXT,
    FOREIGN KEY (id_municipality) REFERENCES municipality(id_municipality),
    FOREIGN KEY (id_gender) REFERENCES gender(id_gender),
    FOREIGN KEY (id_type) REFERENCES type_contagion(id_type_contagion),
    FOREIGN KEY (id_status) REFERENCES status(id_status)
);