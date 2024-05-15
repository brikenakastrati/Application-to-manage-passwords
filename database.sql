create database siguria;
use siguria;

CREATE TABLE tblusers (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE tblpasswords(
    pwd_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    encrypted_pwd VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES tblusers(user_id)
)
