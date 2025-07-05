CREATE DATABASE IF NOT EXISTS spk_saw_db;
USE spk_saw_db;

CREATE TABLE cafes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100),
    lokasi VARCHAR(200)
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100)
);

CREATE TABLE ulasan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    isi TEXT,
    nilai FLOAT,
    cafe_id INT,
    user_id INT,
    FOREIGN KEY (cafe_id) REFERENCES cafes(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE kriteria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100),
    bobot FLOAT,
    tipe VARCHAR(10)
);
