from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import db

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

class Mahasiswa(BaseModel):
    nama: str
    nim: str

@app.get('/mahasiswa')
def get_mahasiswa():
    query = "SELECT * FROM mahasiswa"
    mahasiswa = db.execute_query(query)
    
    mahasiswa_list = []
    for row in mahasiswa:
        mahasiswa_list.append({
            "id": row[0],
            "nama": row[1],
            "nim": row[2]
        })
    return {
        "detail": {
            "status": "success",
            "message": "Data mahasiswa berhasil didapatkan",
            "data": mahasiswa_list
        }
    }

@app.get('/mahasiswa/{id}')
def get_mahasiswa(id: int): 
    query = "SELECT * FROM mahasiswa where id = %s"
    mahasiswa = db.execute_query(query, (id,))
    
    return {
        "detail": {
            "status": "success",
            "message": "Data mahasiswa berhasil didapatkan",
            "data": {
                "id": mahasiswa[0][0],
                "nama": mahasiswa[0][1],
                "nim": mahasiswa[0][2]
            }
        }
    }

@app.post('/mahasiswa')
def create_mahasiswa(mahasiswa : Mahasiswa):
    if len(mahasiswa.nim) != 8:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "NIM harus terdiri dari 8 digit angka"
        })

    query_check = "SELECT * FROM mahasiswa WHERE nim = %s"
    
    results = db.execute_query(query_check, (mahasiswa.nim,))

    if results:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "NIM sudah digunakan"
        })
    
    query = "INSERT INTO mahasiswa (nama, nim) VALUES (%s, %s)"
    cursor = db.execute_query(query, (mahasiswa.nama, mahasiswa.nim), commit=True)
    
    return {
        "detail": {
            "status": "success",
            "message": "Mahasiswa berhasil ditambahkan",
            "data": {
                "nama": mahasiswa.nama,
                "nim": mahasiswa.nim
            },
        },
    }
    
@app.put('/mahasiswa/{id}')
def update_mahasiswa(mahasiswa : Mahasiswa, id: int):
    
    query_check = "SELECT * FROM mahasiswa WHERE id = %s"
    
    results = db.execute_query(query_check, (id,))

    if not results:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Mahasiswa tidak ditemukan"
        })
    
    if len(mahasiswa.nim) != 8:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "NIM harus terdiri dari 8 digit angka"
        })
    
    query_check = "SELECT * FROM mahasiswa WHERE nim = %s"
    
    results = db.execute_query(query_check, (mahasiswa.nim,))

    if results :
        if results[0][0] != id:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "message": "NIM sudah digunakan"
            })
    
    query = "UPDATE mahasiswa SET nama = %s, nim = %s WHERE id = %s"
    
    cursor = db.execute_query(query, (mahasiswa.nama, mahasiswa.nim, id), commit=True)
    
    return {
        "detail": {
            "status": "success",
            "message": "Mahasiswa berhasil diperbarui",
            "data": {
                "nama": mahasiswa.nama,
                "nim": mahasiswa.nim
            },
        },
    }
    
    
@app.delete('/mahasiswa/{id}')
def delete_mahasiswa(id: int):
    query_check = "SELECT * FROM mahasiswa WHERE id = %s"
    
    results = db.execute_query(query_check, (id,))

    if not results:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "NIM tidak ditemukan"
        })
    
    query_check = "SELECT * FROM mahasiswa WHERE id = %s"
    
    results = db.execute_query(query_check, (id,))

    if not results:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "NIM tidak ditemukan"
        })
    
    query = "DELETE FROM mahasiswa WHERE id = %s"
    
    cursor = db.execute_query(query, (id, ), commit=True)
    
    return {
        "detail": {
            "status": "success",
            "message": "Mahasiswa berhasil dihapus"
        },
    }
    
class MataKuliah(BaseModel):
    nama: str
    semester: int
    sks: int

@app.get('/matakuliah')
def get_mahasiswa():
    query = "SELECT * FROM mata_kuliah"
    mata_kuliah = db.execute_query(query)
    
    mata_kuliah_list = []
    for row in mata_kuliah:
        mata_kuliah_list.append({
            "id": row[0],
            "nama": row[1],
            "sks": row[2],
            "semester": row[3]
        })
    return {
        "detail": {
            "status": "success",
            "message": "Data mata kuliah berhasil didapatkan",
            "data": mata_kuliah_list
        }
    }

@app.get('/matakuliah/{id}')
def get_mata_kuliah(id: int): 
    query = "SELECT * FROM mata_kuliah where id = %s"
    mata_kuliah = db.execute_query(query, (id,))
    
    if not mata_kuliah:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Mata kuliah tidak ditemukan"
        })
    
    return {
        "detail": {
            "status": "success",
            "message": "Data mata kuliah berhasil didapatkan",
            "data": {
                "id": mata_kuliah[0][0],
                "nama": mata_kuliah[0][1],
                "sks": mata_kuliah[0][2],
                "semester": mata_kuliah[0][3]
            }
        }
    }

@app.post('/matakuliah')
def create_mata_kuliah(mata_kuliah : MataKuliah):
    query = "INSERT INTO mata_kuliah (nama, sks, semester) VALUES (%s, %s, %s)"
    cursor = db.execute_query(query, (mata_kuliah.nama, mata_kuliah.sks, mata_kuliah.semester), commit=True)
    
    return {
        "detail": {
            "status": "success",
            "message": "Mata kuliah berhasil ditambahkan",
            "data": {
                "nama": mata_kuliah.nama,
                "sks": mata_kuliah.sks,
                "semester": mata_kuliah.semester
            },
        },
    }
    
@app.put('/matakuliah/{id}')
def update_mata_kuliah(mata_kuliah : MataKuliah, id: int):
    query_check = "SELECT * FROM mata_kuliah WHERE id = %s"
    
    results = db.execute_query(query_check, (id,))

    if not results:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Mata kuliah tidak ditemukan"
        })
    query = "UPDATE mata_kuliah SET nama = %s, sks = %s, semester = %s WHERE id = %s"
    
    cursor = db.execute_query(query, (mata_kuliah.nama, mata_kuliah.sks, mata_kuliah.semester, id), commit=True)
    
    return {
        "detail": {
            "status": "success",
            "message": "Mata kuliah berhasil diperbarui",
            "data": {
                "nama": mata_kuliah.nama,
                "sks": mata_kuliah.sks,
                "semester": mata_kuliah.semester
            },
        },
    }
    
    
@app.delete('/matakuliah/{id}')
def delete_mata_kuliah(id: int):
    query_check = "SELECT * FROM mata_kuliah WHERE id = %s"
    
    results = db.execute_query(query_check, (id,))

    if not results:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Mata kuliah tidak ditemukan"
        })
    
    query = "DELETE FROM mata_kuliah WHERE id = %s"
    
    cursor = db.execute_query(query, (id, ), commit=True)
    
    return {
        "detail": {
            "status": "success",
            "message": "Mata kuliah berhasil dihapus"
        },
    }
    
    
class MahasiswaMataKuliah(BaseModel):
    mahasiswa_id: int
    mata_kuliah_id: int

@app.get('/mahasiswamatakuliah')
def get_mahasiswa_mata_kuliah():
    query = '''SELECT 
        mahasiswa_mata_kuliah.id,
        mahasiswa.nama nama_mahasiswa,
        mahasiswa.nim nim_mahasiswa,
        mata_kuliah.nama nama_mata_kuliah,
        mata_kuliah.sks sks_mata_kuliah,
        mata_kuliah.semester semester_mata_kuliah
    FROM mahasiswa_mata_kuliah 
    join mahasiswa on mahasiswa_mata_kuliah.mahasiswa_id = mahasiswa.id 
    join mata_kuliah on mahasiswa_mata_kuliah.mata_kuliah_id = mata_kuliah.id'''
    mata_kuliah = db.execute_query(query)
    
    mata_kuliah_list = []
    for row in mata_kuliah:
        mata_kuliah_list.append({
            "id": row[0],
            "nama_mahasiswa": row[1],
            "nim": row[2],
            "nama_mata_kuliah": row[3],
            "sks": row[4],
            "semester": row[5]
        })

    return {
        "detail": {
            "status": "success",
            "message": "Data berhasil didapatkan",
            "data": mata_kuliah_list
        }
    }

@app.get('/mahasiswamatakuliah/{id}')
def get_mahasiswa_mata_kuliah(id: int): 
    query = '''SELECT 
        mahasiswa_mata_kuliah.id,
        mahasiswa.nama nama_mahasiswa,
        mahasiswa.nim nim_mahasiswa,
        mata_kuliah.nama nama_mata_kuliah,
        mata_kuliah.sks sks_mata_kuliah,
        mata_kuliah.semester semester_mata_kuliah
    FROM mahasiswa_mata_kuliah 
    join mahasiswa on mahasiswa_mata_kuliah.mahasiswa_id = mahasiswa.id 
    join mata_kuliah on mahasiswa_mata_kuliah.mata_kuliah_id = mata_kuliah.id
    where mahasiswa_mata_kuliah.id = %s'''

    mata_kuliah = db.execute_query(query, (id,))
    
    if not mata_kuliah:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Data tidak ditemukan"
        })
    
    return {
        "detail": {
            "status": "success",
            "message": "Data berhasil didapatkan",
            "data": {
                "id": mata_kuliah[0][0],
                "nama_mahasiswa": mata_kuliah[0][1],
                "nim": mata_kuliah[0][2],
                "nama_mata_kuliah": mata_kuliah[0][3],
                "sks": mata_kuliah[0][4],
                "semester": mata_kuliah[0][5]
            }
        }
    }

@app.post('/mahasiswamatakuliah')
def create_mata_kuliah(mata_kuliah : MahasiswaMataKuliah):
    query_check = "SELECT * FROM mahasiswa WHERE id = %s"
    
    results = db.execute_query(query_check, (mata_kuliah.mahasiswa_id,))

    if not results:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Mahasiswa tidak ditemukan"
        })
    
    query_check = "SELECT * FROM mata_kuliah WHERE id = %s"
    
    results = db.execute_query(query_check, (mata_kuliah.mata_kuliah_id,))

    if not results:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Mata kuliah tidak ditemukan"
        })
        
    query = "UPDATE mata_kuliah SET nama = %s, sks = %s, semester = %s WHERE id = %s"
    
    query = "INSERT INTO mahasiswa_mata_kuliah (mahasiswa_id, mata_kuliah_id) VALUES (%s, %s)"
    cursor = db.execute_query(query, (mata_kuliah.mahasiswa_id, mata_kuliah.mata_kuliah_id), commit=True)
    
    return {
        "detail": {
            "status": "success",
            "message": "Data berhasil ditambahkan",
            "data": {
                "mahasiswa_id": mata_kuliah.mahasiswa_id,
                "mata_kuliah_id": mata_kuliah.mata_kuliah_id,
            },
        },
    }
    
@app.put('/mahasiswamatakuliah/{id}')
def update_mata_kuliah(mata_kuliah : MahasiswaMataKuliah, id: int):
    query = '''SELECT 
        mahasiswa_mata_kuliah.id,
        mahasiswa.nama nama_mahasiswa,
        mahasiswa.nim nim_mahasiswa,
        mata_kuliah.nama nama_mata_kuliah,
        mata_kuliah.sks sks_mata_kuliah,
        mata_kuliah.semester semester_mata_kuliah
    FROM mahasiswa_mata_kuliah 
    join mahasiswa on mahasiswa_mata_kuliah.mahasiswa_id = mahasiswa.id 
    join mata_kuliah on mahasiswa_mata_kuliah.mata_kuliah_id = mata_kuliah.id
    where mahasiswa_mata_kuliah.id = %s'''

    data = db.execute_query(query, (id,))
    
    if not data:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Data tidak ditemukan"
        })
    
    query_check = "SELECT * FROM mahasiswa WHERE id = %s"
    
    results = db.execute_query(query_check, (mata_kuliah.mahasiswa_id,))

    if not results:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Mahasiswa tidak ditemukan"
        })
    
    query_check = "SELECT * FROM mata_kuliah WHERE id = %s"
    
    results = db.execute_query(query_check, (mata_kuliah.mata_kuliah_id,))

    if not results:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Mata kuliah tidak ditemukan"
        })
    
    query = "UPDATE mahasiswa_mata_kuliah SET mahasiswa_id = %s, mata_kuliah_id = %s WHERE id = %s"
    
    cursor = db.execute_query(query, (mata_kuliah.mahasiswa_id, mata_kuliah.mata_kuliah_id, id), commit=True)
    
    return {
        "detail": {
            "status": "success",
            "message": "Data berhasil diperbarui",
            "data": {
                "mahasiswa_id": mata_kuliah.mahasiswa_id,
                "mata_kuliah_id": mata_kuliah.mata_kuliah_id,
            },
        },
    }
    
    
@app.delete('/mahasiswamatakuliah/{id}')
def delete_mata_kuliah(id: int):
    query = '''SELECT 
        mahasiswa_mata_kuliah.id,
        mahasiswa.nama nama_mahasiswa,
        mahasiswa.nim nim_mahasiswa,
        mata_kuliah.nama nama_mata_kuliah,
        mata_kuliah.sks sks_mata_kuliah,
        mata_kuliah.semester semester_mata_kuliah
    FROM mahasiswa_mata_kuliah 
    join mahasiswa on mahasiswa_mata_kuliah.mahasiswa_id = mahasiswa.id 
    join mata_kuliah on mahasiswa_mata_kuliah.mata_kuliah_id = mata_kuliah.id
    where mahasiswa_mata_kuliah.id = %s'''

    mata_kuliah = db.execute_query(query, (id,))
    
    if not mata_kuliah:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Data tidak ditemukan"
        })
    
    query = "DELETE FROM mahasiswa_mata_kuliah WHERE id = %s"
    
    cursor = db.execute_query(query, (id, ), commit=True)
    
    return {
        "detail": {
            "status": "success",
            "message": "Data berhasil dihapus"
        },
    }