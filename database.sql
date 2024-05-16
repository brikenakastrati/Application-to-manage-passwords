create database siguria;
use siguria;

CREATE TABLE tblusers (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
ALTER TABLE tblusers
ADD COLUMN aes_key VARCHAR(255) NOT NULL AFTER password;


CREATE TABLE tblpasswords(
    pwd_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    account VARCHAR(255) NOT NULL,
    encrypted_pwd VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES tblusers(user_id)
);

select * from tblpasswords;
