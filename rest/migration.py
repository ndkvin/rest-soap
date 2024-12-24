from database import db

# SQL query to create the table
sql_create = [
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

for query in sql_create:
    db.execute_query(query, commit=True)

db.close()