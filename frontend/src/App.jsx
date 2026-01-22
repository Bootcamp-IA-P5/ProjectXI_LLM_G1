import { useState } from 'react';
import ContentForm from './components/ContentForm';
import OutputDisplay from './components/OutputDisplay';
import { generateContent } from './services/api.js';
import './styles/App.css';

export default function App() {

    const [contenidoGenerado, setContenidoGenerado] = useState("");
    const [imagenGenerada, setImagenGenerada] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [darkMode, setDarkMode] = useState(() => {
        const saved = localStorage.getItem('darkMode');
        return saved !== null ? JSON.parse(saved) : false;
    });

    const toggleDarkMode = () => {
        const newMode = !darkMode;
        setDarkMode(newMode);
        localStorage.setItem('darkMode', JSON.stringify(newMode));
        document.documentElement.setAttribute('data-theme', newMode ? 'dark' : 'light');
    };

    async function handleFormSubmit(datos) {

        // TODO: Guardar datos en estado
       // setDatosForm(datos);

        // setLoading(true)
        setLoading(true);
        setError("");
        setContenidoGenerado("");
        setImagenGenerada("");

        // TODO: Llamar api.js
        try {
            const response = await generateContent(datos);
            console.log("🎉 RESPONSE COMPLETO:", response);
            console.log("📝 CONTENIDO:", response.contenido);
            console.log("🖼️ IMAGE_URL RAW:", response.image_url);
            console.log("✅ Tipo de image_url:", typeof response.image_url);

            if (response.contenido) {
                setContenidoGenerado(response.contenido);

                // Procesar imagen URL - ya viene completa del backend
                if (response.image_url && response.image_url.trim() !== "") {
                    console.log("🔗 URL de imagen a setear:", response.image_url);
                    setImagenGenerada(response.image_url);
                    console.log("✅ setImagenGenerada ejecutado con:", response.image_url);
                } else {
                    console.warn("⚠️ No hay image_url válida en la respuesta");
                    setImagenGenerada("");
                }
                setError("");
            } else {
                setError("No se generó contenido");
            }

        } catch (error) {
            console.error("❌ ERROR:", error);
            console.error("📍 Error Message:", error.message);
            setError(error.message || "Error desconocido");
            setContenidoGenerado("");
            setImagenGenerada("");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="app-container">
            <header className="app-header">
                <div className="header-content">
                    <div className="logo-section">
                        <h1 className="app-title">✨ Synthetix</h1>
                        <p className="app-subtitle">Generador de Contenido Inteligente con IA</p>
                    </div>
                    <button className="theme-toggle" onClick={toggleDarkMode} aria-label="Cambiar tema">
                        {darkMode ? '☀️' : '🌙'}
                    </button>
                </div>
            </header>

            <main className="app-main">
                <div className="content-wrapper">
                    <div className="form-container">
                        <ContentForm onSubmit={handleFormSubmit} />
                    </div>
                    <div className="output-container">
                        <OutputDisplay
                            contenido={contenidoGenerado}
                            imagen={imagenGenerada}
                            loading={loading}
                            error={error}
                        />
                    </div>
                </div>
            </main>

            <footer className="app-footer">
                <p>&copy; 2026 Synthetix - Grupo 1 Factoria F5. Potenciado por IA avanzada.</p>
            </footer>
        </div>
    )
}