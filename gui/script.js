const get_asistente = () => {
    const {PythonShell} = require("python-shell");
    const path = require("path")
    
    const options = {
        scriptPath: path.join(__dirname, "/../engine/"),
        pythonPath: 'C:/Users/Ricardo/AppData/Local/Programs/Python/Python311/python.exe'
    }

    const asistente = new PythonShell("asistente_virtual.py", options);
    
    asistente.on("message", message => {
        console.log(message)
    });

    asistente.end((err, code, message) => {
        if (err) console.log(err);
        alert("Terminado :(")
    })
}
