-- Crear dataset
CREATE SCHEMA IF NOT EXISTS covid_db;

-- Crear tabla department
CREATE TABLE covid_db.department (
    id_department INT64,
    name STRING
);

-- Crear tabla municipality
CREATE TABLE covid_db.municipality (
    id_municipality INT64,
    name STRING,
    id_department INT64
);

-- Crear tabla gender
CREATE TABLE covid_db.gender (
    id_gender INT64,
    name STRING
);

-- Crear tabla status
CREATE TABLE covid_db.status (
    id_status INT64,
    name STRING
);

-- Crear tabla type_contagion
CREATE TABLE covid_db.type_contagion (
    id_type_contagion INT64,
    name STRING
);

-- Crear tabla cases
CREATE TABLE covid_db.cases (
    id_case INT64,
    id_municipality INT64,
    age INT64,
    id_gender INT64,
    id_type INT64,
    id_status FLOAT64,
    date_symptom DATETIME,
    date_death DATETIME,
    date_diagnosis DATETIME,
    date_recovery DATETIME
);