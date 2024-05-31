CREATE DATABASE IF NOT EXISTS wifi_analysis;

USE wifi_analysis;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_mac VARCHAR(17) NOT NULL UNIQUE,
    host_name VARCHAR(100),
    device VARCHAR(100),
    os_type VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS access_points (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ap_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_associated_time DATETIME,
    session_duration INT,
    client_id INT,
    ap_id INT,
    upstream_transferred INT,
    downstream_transferred INT,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (ap_id) REFERENCES access_points(id)
);