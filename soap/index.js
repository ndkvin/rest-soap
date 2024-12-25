const all_mahasiswa = [];

class Mahasiswa {
    constructor(nim, nama, prodi) {
        this.nim = nim;
        this.nama = nama;
        this.prodi = prodi;
    }
}

const create_mahasiswa = (nim, nama, prodi) => {
    const new_mahasiswa = new Mahasiswa(nim, nama, prodi);
    all_mahasiswa.push(new_mahasiswa);
    return new_mahasiswa;
};

const read_mahasiswa = (nim) => {
    return all_mahasiswa.find((mahasiswa) => mahasiswa.nim === nim);
};

const update_mahasiswa = (nim, nama, prodi) => {
    const mahasiswa = all_mahasiswa.find((mahasiswa) => mahasiswa.nim === nim);
    mahasiswa.nama = nama;
    mahasiswa.prodi = prodi;
    return mahasiswa;
};

const delete_mahasiswa = (nim) => {
    const mahasiswa = all_mahasiswa.find((mahasiswa) => mahasiswa.nim === nim);
    all_mahasiswa.splice(all_mahasiswa.indexOf(mahasiswa), 1);
    return mahasiswa;
};

const read_all_mahasiswa = () => {
    return all_mahasiswa;
};

// e
const SoapService = {
    MahasiswaService: {
        MahasiswaPort: {
            sayHello: function (args) {
                console.log("hello");
                return { greeting: `Hello, ${args.name}!` };
            },
            sayHelloTwo: function (args) {
                console.log("hello2");
                return { greeting: `Hello2, ${args.name}!` };
            },
            create_mahasiswa: function (args) {
                const isExist = all_mahasiswa.find(
                    (mahasiswa) => mahasiswa.nim === args.nim
                );

                if (isExist) {
                    return { message: "Mahasiswa sudah ada" };
                }

                const obj = create_mahasiswa(args.nim, args.nama, args.prodi);
                const message = `Mahasiswa dengan nim ${obj.nim} berhasil dibuat`;
                return { message: message, data: obj };
            },
            read_mahasiswa: function (args) {
                const obj = read_mahasiswa(args.nim);
                if (obj === undefined) {
                    return { message: "Mahasiswa tidak ditemukan" };
                }
                return { message: "Mahasiswa ditemukan", data: obj };
            },
            update_mahasiswa: function (args) {
                const obj = update_mahasiswa(args.nim, args.nama, args.prodi);
                const message = `Mahasiswa dengan nim ${obj.nim} berhasil diupdate`;

                if (obj === undefined) {
                    return { message: "Mahasiswa tidak ditemukan" };
                }

                return { message: message, data: obj };
            },
            delete_mahasiswa: function (args) {
                const obj = delete_mahasiswa(args.nim);
                const message = `Mahasiswa dengan nim ${obj.nim} berhasil dihapus`;

                if (obj === undefined) {
                    return { message: "Mahasiswa tidak ditemukan" };
                }

                return { message: message, data: obj };
            },
            read_all_mahasiswa: function () {
                const obj = read_all_mahasiswa();
                return {
                    message: "Berhasil membaca semua mahasiswa",
                    data: obj,
                };
            },
        },
    },
};

// HTTP server example
const http = require("http");
const soap = require("soap");
const fs = require("fs");

const xml = require("fs").readFileSync("SoapService.wsdl", "utf8");

//http server example
const server = http.createServer(function (request, response) {
    response.end("404: Not Found: " + request.url);
});

server.listen(8000);
soap.listen(server, "/wsdl", SoapService, xml, function () {
    console.log("server initialized");
});
