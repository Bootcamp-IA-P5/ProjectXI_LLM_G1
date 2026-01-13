import {useState} from 'react'; // Hook para crear estado


// Primer paso: ContentForm sirve unicamente para recoger los datos, validar que hay algo, y enviar a App.jsx (padre)
export default function ContentForm({onSubmit}) {
    // useState para estado
    const [tema, setTema] = useState("");
    const [plataforma, setPlataforma] = useState("");
    const [audiencia, setAudiencia] = useState("");
    const [infoAdicional, setInfoAdicional] = useState("");
    
    function handleSubmit(e) {
        
        e.preventDefault();

        if (tema === "") {
            console.log("Error");
            return;
        }

        if (plataforma === "") {
            console.log("Error");
            return;
        }

        if (audiencia === "") {
            console.log("Error");
            return;
        }
        console.log("Datos ok, enviar");
        const datos = {tema, plataforma, audiencia, infoAdicional};
        onSubmit(datos); // Llamar a la funcion onSubmit que viene del padre (App.jsx)
    }


    return (
    <form onSubmit={handleSubmit}> 
        <label>Tema</label>
        {/* value para decir muestra el estado */}
        {/* onChange cuando el usuario escribe, actualiza el estado */}
        <input 
        type="text"
        value={tema}                                
        onChange={(e) => setTema(e.target.value)}   
        />


        <label>Plataforma</label>
        <select value={plataforma} onChange={(e) => setPlataforma(e.target.value)}>
            <option value="">Selecciona plataforma</option>
            <option value="twitter">Twitter</option>
            <option value="blog">Blog</option>
            <option value="instagram">Instagram</option>
            <option value="linkedIn">LinkedIn</option>
        </select>
       

        <label>Audiencia</label>
        <input 
        type="text"
        value={audiencia}
        onChange={(e) => setAudiencia(e.target.value)} 
        />

        <label>Información Adicional (Opcional)</label>
        <textarea
            value={infoAdicional}
            onChange={(e) => setInfoAdicional(e.target.value)}
            placeholder="(opcional)"
        >
            </textarea>

        <button type="submit">Generar</button>
    </form>
    )
}