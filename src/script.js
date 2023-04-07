const { PythonShell } = require("python-shell");
const path = require("path")

const btnIniciar = document.getElementById("iniciar")
const btnDetener = document.getElementById("detener")

const options = {
    scriptPath: path.join(__dirname, "../python/"),
    pythonPath: 'C:/Users/Ricardo/AppData/Local/Programs/Python/Python311/python.exe'
}

let activado = false

btnIniciar.addEventListener("click", () => {
    if (activado) return null
    activado = true
    btnIniciar.classList.remove("botonHabilitado")
    btnIniciar.classList.add("botonDeshabilitado")
    btnDetener.classList.add("botonHabilitado")
    btnDetener.classList.remove("botonDeshabilitado")

    const asistente = new PythonShell("asistente_virtual.py", options);
    
    asistente.on("message", message => {
        console.log(message)
    });

    asistente.end((err, code, message) => {
        if (err) console.log(err);
        alert("Terminado :(")
    })

    btnDetener.addEventListener("click", (e_d) => {
        asistente.kill('SIGINT')
        btnIniciar.classList.add("botonHabilitado")
        btnIniciar.classList.remove("botonDeshabilitado")
        btnDetener.classList.remove("botonHabilitado")
        btnDetener.classList.add("botonDeshabilitado")
        activado = false
    })
})
