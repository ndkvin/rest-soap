from database import db
import os

# SQL query to create the table
sql_table = [
    '''CREATE TABLE `mahasiswa` (
        `id` INT PRIMARY KEY AUTO_INCREMENT,
        `nama` VARCHAR(255),
        `nim` VARCHAR(255) UNIQUE
    );''',
    
    '''CREATE TABLE `mata_kuliah` (
        `id` INT PRIMARY KEY AUTO_INCREMENT,
        `nama` VARCHAR(255),
        `sks` INT,
        `semester` INT
    );''',
    
    '''CREATE TABLE `mahasiswa_mata_kuliah` (
        `id` INT PRIMARY KEY AUTO_INCREMENT,
        `mahasiswa_id` INT,
        `mata_kuliah_id` INT,
        FOREIGN KEY (`mahasiswa_id`) REFERENCES `mahasiswa`(`id`) on DELETE CASCADE,
        FOREIGN KEY (`mata_kuliah_id`) REFERENCES `mata_kuliah`(`id`) on DELETE CASCADE
    );'''
]

# Execute the query
for query in sql_table:
    db.execute_query(query, commit=True)
    print("Table created")

db.close()