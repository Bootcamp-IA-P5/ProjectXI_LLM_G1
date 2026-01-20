import { useState } from 'react';

export default function ContentForm({ onSubmit }) {
    // Estados originales
    const [tema, setTema] = useState("");
    const [plataforma, setPlataforma] = useState("");
    const [audiencia, setAudiencia] = useState("");
    const [infoAdicional, setInfoAdicional] = useState("");

    // --- NUEVOS ESTADOS (Nivel Avanzado) ---
    const [idioma, setIdioma] = useState("es"); // Por defecto Castellano
    const [useNews, setUseNews] = useState(false); // Por defecto noticias desactivadas

    function handleSubmit(e) {
        e.preventDefault();

        // Validaciones básicas
        if (!tema || !plataforma || !audiencia) {
            alert("Por favor, rellena todos los campos obligatorios.");
            return;
        }

        console.log("Enviando datos con idioma y noticias:", { idioma, useNews });

        // Empaquetamos todo para el ContentFlow que va al Backend
        const datos = { 
            tema, 
            plataforma, 
            audiencia, 
            infoAdicional,
            idioma,      // Inyectamos el idioma seleccionado
            use_news: useNews // Inyectamos el booleano para el RAG de noticias
        };

        onSubmit(datos); 
    }

    return (
        <form onSubmit={handleSubmit} className="form-container"> 
            {/* Campo: Tema */}
            <label>Tema</label>
            <input 
                type="text"
                value={tema}                                
                onChange={(e) => setTema(e.target.value)}
                placeholder="Ej: Futuro de Bitcoin"   
            />

            {/* Campo: Plataforma */}
            <label>Plataforma</label>
            <select value={plataforma} onChange={(e) => setPlataforma(e.target.value)}>
                <option value="">Selecciona plataforma</option>
                <option value="twitter">Twitter/X</option>
                <option value="blog">Blog Post</option>
                <option value="instagram">Instagram</option>
                <option value="linkedin">LinkedIn</option>
            </select>

            {/* --- SELECCIÓN DE IDIOMA (Nivel Avanzado) --- */}
            <label>Idioma del contenido</label>
            <select value={idioma} onChange={(e) => setIdioma(e.target.value)}>
                <option value="es">Castellano</option>
                <option value="en">English</option>
                <option value="fr">Français</option>
                <option value="it">Italiano</option>
            </select>

            {/* Campo: Audiencia */}
            <label>Audiencia</label>
            <input 
                type="text"
                value={audiencia}
                onChange={(e) => setAudiencia(e.target.value)} 
                placeholder="Ej: Inversores jóvenes"
            />

            {/* --- SWITCH DE NOTICIAS FINANCIERAS (Nivel Avanzado) --- */}
            <div className="checkbox-group" style={{ margin: '15px 0', display: 'flex', alignItems: 'center', gap: '10px' }}>
                <input 
                    type="checkbox"
                    id="news-toggle"
                    checked={useNews}
                    onChange={(e) => setUseNews(e.target.checked)} 
                />
                <label htmlFor="news-toggle" style={{ fontWeight: 'bold', color: '#2c3e50' }}>
                    🚀 Incluir noticias financieras actuales (RAG)
                </label>
            </div>

            <label>Información Adicional (Opcional)</label>
            <textarea
                value={infoAdicional}
                onChange={(e) => setInfoAdicional(e.target.value)}
                placeholder="Datos específicos de la marca o empresa..."
            />

            <button type="submit" style={{ marginTop: '10px' }}>
                {useNews ? "Generar con Noticias" : "Generar Contenido"}
            </button>
        </form>
    );
}