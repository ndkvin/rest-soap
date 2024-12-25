const soap = require("soap");
const url = "http://localhost:8000/wsdl?wsdl";

function main(client) {
    const maba = {
        nim: "M0521007",
        nama: "John",
        prodi: "Informatika",
    };

    client.create_mahasiswa(maba, function (err, result) {
        if (err) {
            console.error("Error calling MyFunction:", err);
            return;
        }
        console.log("Response from MyFunction:", result);
    });

    client.read_mahasiswa(maba, function (err, result) {
        if (err) {
            console.error("Error calling MyFunction:", err);
            return;
        }
        console.log("Response from MyFunction:", result);
    });

    // client.read_all_mahasiswa({}, function (err, result) {
    //     if (err) {
    //         console.error("Error calling MyFunction:", err);
    //         return;
    //     }
    //     console.log("Response from MyFunction:", result.data);
    // });
}

soap.createClient(url, {}, function (err, client) {
    if (err) {
        console.error("Error creating client:", err);
        return;
    }

    main(client);
});
