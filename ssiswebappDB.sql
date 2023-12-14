CREATE DATABASE ssiswebapp;
USE ssiswebapp;

CREATE TABLE college (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE course (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    college_code VARCHAR(10),
    FOREIGN KEY (college_code) REFERENCES college(code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE student (
    id CHAR(9) PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    course_code VARCHAR(10),
    year INT,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
	cloudinary_image_url VARCHAR(255),
    FOREIGN KEY (course_code) REFERENCES course(code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
