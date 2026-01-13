import { useState } from 'react';
import ContentForm from './components/ContentForm';
import OutputDisplay from './components/OutputDisplay';
import { generateContent } from './services/api.js'; // {} porque no es export default; ruta con comillas

export default function App() {

    const [datosForm, setDatosForm] = useState(null);
    const [contenidoGenerado, setContenidoGenerado] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleFormSubmit(datos) {

        // TODO: Guardar datos en estado
        setDatosForm(datos);

        // setLoading(true)
        setLoading(true);

        // TODO: Llamar api.js
        try {
            const response = await generateContent(datos);  // generateContent Tambien es async
            console.log("RESPONSE COMPLETO:", response);
            console.log("CONTENIDO:", response.contenido);
            setContenidoGenerado(response.contenido);
            setError("");

        } catch (error) {
            console.error("ERROR:", error);  // ← Y AQUÍ
            setError(error.message);
            setContenidoGenerado("")

        } finally {
            setLoading(false);
        }
    }

    return (
        <div>
            {/*TODO: Pasar handleFormSubmit a ContentForm */}
            <ContentForm onSubmit={handleFormSubmit} />
            {/*          ↑ "onSubmit" es una prop
                                    ↑ handleFormSubmit es el valor*/}

            {/* Pasar contenidoGenerado a OutputDisplay */}
            <OutputDisplay 
                contenido={contenidoGenerado}
                loading={loading}
                error={error}
            />
        </div>
    )
}