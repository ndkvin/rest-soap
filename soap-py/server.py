import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from spyne import Application, rpc, ServiceBase, Float, Unicode, ComplexModel, AnyDict, Integer, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.error import Fault
from database.database import db
from spyne.protocol.json import JsonDocument

class Mahasiswa(ComplexModel):
    id = Integer
    nama = Unicode
    nim = Unicode

class MataKuliah(ComplexModel):
    nama: Unicode
    semester: Integer
    sks: Integer

class MahasiswaMataKuliah(ComplexModel):
    mahasiswa_id: int
    mata_kuliah_id: int

class MahasiswaService(ServiceBase):
    @rpc(_returns=AnyDict)
    def read_root(ctx):
        return {"Hello": "World"}

    @rpc(_returns=AnyDict)
    def get_all_mahasiswa(ctx):
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
            "status": "success",
            "message": "Data mahasiswa berhasil didapatkan",
            "data": mahasiswa_list
        }

    @rpc(Unicode, Unicode, _returns=AnyDict)
    def create_mahasiswa(ctx, nim, nama):
        if len(nim) != 8:
            raise Fault(faultcode="Client", faultstring="NIM harus terdiri dari 8 digit angka")

        query_check = "SELECT * FROM mahasiswa WHERE nim = %s"
        results = db.execute_query(query_check, (nim,))

        if results:
            raise Fault(faultcode="Client", faultstring="NIM sudah digunakan")

        query = "INSERT INTO mahasiswa (nama, nim) VALUES (%s, %s)"
        db.execute_query(query, (nama, nim), commit=True)

        return {
            "status": "success",
            "message": "Mahasiswa berhasil ditambahkan",
            "data": {
                "nama": nama,
                "nim": nim
            },
        }
    
    @rpc(Integer, _returns=AnyDict)
    def get_mahasiswa_by_id(ctx, id):
        query = "SELECT * FROM mahasiswa where id = %s"
        mahasiswa = db.execute_query(query, (id,))
        
        if not mahasiswa:
            raise Fault (faultcode="Client", faultstring="Data tidak ditemukan")
            
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
    
    @rpc(Unicode, Unicode, Integer, _returns=AnyDict)
    def update_mahasiswa(ctx, nim, nama, id):  
        query_check = "SELECT * FROM mahasiswa WHERE id = %s"
        
        results = db.execute_query(query_check, (id,))

        if not results:
            raise Fault(faultcode="Client", faultstring="Data tidak ditemukan")
        
        if len(nim) != 8:
            raise Fault(faultcode="Client", faultstring="NIM harus terdiri dari 8 digit angka")
        
        query_check = "SELECT * FROM mahasiswa WHERE nim = %s"
        
        results = db.execute_query(query_check, (nim,))

        if results :
            if results[0][0] != id:
                raise Fault(faultcode="Client", faultstring="NIM sudah digunakan")
            
        query = "UPDATE mahasiswa SET nama = %s, nim = %s WHERE id = %s"
        
        cursor = db.execute_query(query, (nama, nim, id), commit=True)
        
        return {
            "detail": {
                "status": "success",
                "message": "Mahasiswa berhasil diperbarui",
                "data": {
                    "nama": nama,
                    "nim": nim
                },
            },
        }
    
    @rpc(Integer, _returns=AnyDict)
    def delete_mahasiswa(ctx, id):
        query_check = "SELECT * FROM mahasiswa WHERE id = %s"
        
        results = db.execute_query(query_check, (id,))

        if not results:
            raise Fault(faultcode="Client", faultstring="Data tidak ditemukan")
        
        query = "DELETE FROM mahasiswa WHERE id = %s"
        
        cursor = db.execute_query(query, (id, ), commit=True)
        
        return {
            "detail": {
                "status": "success",
                "message": "Mahasiswa berhasil dihapus",
                "data": {
                    "id": id,
                    "nama": results[0][1],
                    "nim": results[0][2]
                }
            },
        }

class MatakuliahService(ServiceBase):
    @rpc(_returns=AnyDict)
    def read_root(ctx):
        return {"Hello": "World 2"}

    @rpc(_returns=AnyDict)
    def get_all_matakuliah(ctx):
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
    
    @rpc(Integer, _returns=AnyDict)
    def get_matakuliah_by_id(ctx, id):
        query = "SELECT * FROM mata_kuliah where id = %s"
        mata_kuliah = db.execute_query(query, (id,))
        
        if not mata_kuliah:
            raise Fault (faultcode="Client", faultstring="Data tidak ditemukan")
        
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
        
    @rpc(Unicode, Unicode, Integer, _returns=AnyDict)
    def create_matakuliah(ctx, nama, semester, sks):
        query = "INSERT INTO mata_kuliah (nama, sks, semester) VALUES (%s, %s, %s)"
        cursor = db.execute_query(query, (nama, sks, semester), commit=True)
        
        return {
            "detail": {
                "status": "success",
                "message": "Mata kuliah berhasil ditambahkan",
                "data": {
                    "nama": nama,
                    "sks": sks,
                    "semester": semester
                },
            },
        }
    
    @rpc(Integer, Unicode, Unicode, Integer, _returns=AnyDict)
    def update_matakuliah(ctx, id, nama, semester, sks):  
        query_check = "SELECT * FROM mata_kuliah WHERE id = %s"
    
        results = db.execute_query(query_check, (id,))

        if not results:
            raise Fault(faultcode="Client", faultstring="Data tidak ditemukan")
    
        query = "UPDATE mata_kuliah SET nama = %s, sks = %s, semester = %s WHERE id = %s"
        
        cursor = db.execute_query(query, (nama, sks, semester, id), commit=True)
        
        return {
            "detail": {
                "status": "success",
                "message": "Mata kuliah berhasil diperbarui",
                "data": {
                    "nama": nama,
                    "sks": sks,
                    "semester": semester
                },
            },
        }
    
    @rpc(Integer, _returns=AnyDict)
    def delete_matakuliah(ctx, id):
        query_check = "SELECT * FROM mata_kuliah WHERE id = %s"
        
        results = db.execute_query(query_check, (id,))

        if not results:
            raise Fault(faultcode="Client", faultstring="Matakuliah tidak ditemukan")
        
        query = "DELETE FROM mata_kuliah WHERE id = %s"
        
        cursor = db.execute_query(query, (id, ), commit=True)
        
        return {
            "detail": {
                "status": "success",
                "message": "Mata kuliah berhasil dihapus"
            },
        }

class MahasiswaMataKuliahService(ServiceBase):
    @rpc(_returns=AnyDict)
    def read_root(ctx):
        return {"Hello": "World 3"}
    
    @rpc(_returns=AnyDict) 
    def get_all_mahasiswa_matakuliah(ctx):
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

    @rpc(Integer, _returns=AnyDict)
    def get_mahasiswa_matakuliah_by_id(ctx, id):
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
            raise Fault (faultcode="Client", faultstring="Data tidak ditemukan")
        
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
    
    @rpc(Unicode, Unicode, _returns=AnyDict)
    def create_mahasiswa_matakuliah(ctx, mahasiswa_id, mata_kuliah_id):
        query_check = "SELECT * FROM mahasiswa WHERE id = %s"
        
        results = db.execute_query(query_check, (mahasiswa_id,))

        if not results:
            raise Fault(faultcode="Client", faultstring="Mahasiswa tidak ditemukan")
        
        query_check = "SELECT * FROM mata_kuliah WHERE id = %s"
        
        results = db.execute_query(query_check, (mata_kuliah_id,))

        if not results:
            raise Fault(faultcode="Client", faultstring="Mata kuliah tidak ditemukan")
            
        query = "UPDATE mata_kuliah SET nama = %s, sks = %s, semester = %s WHERE id = %s"
        
        query = "INSERT INTO mahasiswa_mata_kuliah (mahasiswa_id, mata_kuliah_id) VALUES (%s, %s)"
        cursor = db.execute_query(query, (mahasiswa_id, mata_kuliah_id), commit=True)
        
        return {
            "detail": {
                "status": "success",
                "message": "Data berhasil ditambahkan",
                "data": {
                    "mahasiswa_id": mahasiswa_id,
                    "mata_kuliah_id": mata_kuliah_id,
                },
            },
        }
    
    @rpc(Integer, Unicode, Unicode, _returns=AnyDict)
    def update_mahasiswa_matakuliah(ctx, id, mahasiswa_id, mata_kuliah_id):
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
            raise Fault(faultcode="Client", faultstring="Data tidak ditemukan")
        
        query_check = "SELECT * FROM mahasiswa WHERE id = %s"
        
        results = db.execute_query(query_check, (mahasiswa_id,))

        if not results:
            raise Fault(faultcode="Client", faultstring="Mahasiswa tidak ditemukan")
        
        query_check = "SELECT * FROM mata_kuliah WHERE id = %s"
        
        results = db.execute_query(query_check, (mata_kuliah_id,))

        if not results:
            raise Fault(faultcode="Client", faultstring="Mata kuliah tidak ditemukan")
        
        query = "UPDATE mahasiswa_mata_kuliah SET mahasiswa_id = %s, mata_kuliah_id = %s WHERE id = %s"
        
        cursor = db.execute_query(query, (mahasiswa_id, mata_kuliah_id, id), commit=True)
        
        return {
            "detail": {
                "status": "success",
                "message": "Data berhasil diperbarui",
                "data": {
                    "mahasiswa_id": mahasiswa_id,
                    "mata_kuliah_id": mata_kuliah_id,
                },
            },
        }
    
    @rpc(Integer, _returns=AnyDict)
    def delete_mahasiswa_matakuliah(ctx, id):
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
            raise Fault(faultcode="Client", faultstring="Matakuliah tidak ditemukan")
        
        query = "DELETE FROM mahasiswa_mata_kuliah WHERE id = %s"
        
        cursor = db.execute_query(query, (id, ), commit=True)
        
        return {
            "detail": {
                "status": "success",
                "message": "Data matakuliah berhasil dihapus dari mahasiswa",
                "data": {
                    "id": id,
                    "nama_mahasiswa": mata_kuliah[0][1],
                    "nim": mata_kuliah[0][2],
                    "nama_mata_kuliah": mata_kuliah[0][3],
                }
            },
        }


# Spyne Application
soap_mahasiswa = Application(
    [MahasiswaService],
    tns='sister.mahasiswa',
    in_protocol=Soap11(),
    out_protocol=JsonDocument()
)

soap_matakuliah = Application(
    [MatakuliahService],
    tns='sister.matakuliah',
    in_protocol=Soap11(),
    out_protocol=JsonDocument()
)

soap_mahasiswamatakuliah = Application(
    [MahasiswaMataKuliahService],
    tns='sister.mahasiswamatakuliah',
    in_protocol=Soap11(),
    out_protocol=JsonDocument()
)

# FastAPI App
fastapi_app = FastAPI()

@fastapi_app.get("/")
async def read_root():
    return {"message": "Welcome to the SOAP service. Access it via /mahasiswa, /matakuliah, /mahasiswamatakuliah."}

# Add Spyne WSGI Application to FastAPI
fastapi_app.mount("/mahasiswa", WSGIMiddleware(WsgiApplication(soap_mahasiswa)))
fastapi_app.mount("/matakuliah", WSGIMiddleware(WsgiApplication(soap_matakuliah)))
fastapi_app.mount("/mahasiswamatakuliah", WSGIMiddleware(WsgiApplication(soap_mahasiswamatakuliah)))

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    print("Server running at ", f"http://{host}:{port}")
    print("SOAP endpoint (mahasiswa): ", f"http://{host}:{port}/mahasiswa")
    print("SOAP endpoint (matakuliah): ", f"http://{host}:{port}/matakuliah")
    print("SOAP endpoint (mahasiswamatakuliah): ", f"http://{host}:{port}/mahasiswamatakuliah")

    uvicorn.run(fastapi_app, host=host, port=8000)
