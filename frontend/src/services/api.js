// Esta función TARDA (espera respuesta del backend)
// Por eso es "async", necesitamos decirle a JS "espera a que termine"
export async function generateContent (datos) {

    const baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
    const url = `${baseUrl}/generate`;
    
    try { // maneja errores
        const response = await fetch(url, { // hace la peticion y response lo que vuelve del servidor
            // await espera (porque es async)
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos),
        });

        const result = await response.json(); // los datos parseados
        // Espera a que response.json() termine antes de continuar

        console.log("✅ RESPUESTA DEL BACKEND:", result);
        console.log("CONTENIDO:", result.contenido);
        
        // Chequear si response fue OK
        if (!response.ok) {
            throw new Error(result.detail || `Error ${response.status}: ${result.message || 'Unknown error'}`);
        }

        console.log(result);
        return result;
    
    } catch (error) {
        console.error("❌ ERROR EN API.JS:", error);
        console.error("Mensaje:", error.message);
        throw error;
    }
}