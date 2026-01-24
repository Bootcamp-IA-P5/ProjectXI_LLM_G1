import { useState } from 'react';
import '../styles/ContentForm.css';

export default function ContentForm({ onSubmit }) {
    const [tema, setTema] = useState("");
    const [plataforma, setPlataforma] = useState("");
    const [audiencia, setAudiencia] = useState("");
    const [idioma, setIdioma] = useState("es");
    const [infoAdicional, setInfoAdicional] = useState("");
    const [errors, setErrors] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    // ✅ NUEVO: Estado para tabs
    const [activeTab, setActiveTab] = useState("normal");

    function validateForm() {
        const newErrors = {};

        if (tema.trim() === "") {
            newErrors.tema = "El tema es requerido";
        }

        if (plataforma === "") {
            newErrors.plataforma = "Selecciona una plataforma";
        }

        if (audiencia.trim() === "") {
            newErrors.audiencia = "La audiencia es requerida";
        }

        return newErrors;
    }

    function handleSubmit(e) {
        e.preventDefault();

        const newErrors = validateForm();
        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            return;
        }

        setErrors({});
        setIsSubmitting(true);

        const datos = { tema, plataforma, audiencia, idioma, informacion_adicional: infoAdicional };

        // ✅ NUEVO: Endpoint diferente según tab
        const endpoint = activeTab === "scientific" ? "/api/generate-scientific" : "/api/generate";
        onSubmit(datos, endpoint);

        setTimeout(() => {
            setIsSubmitting(false);
        }, 500);
    }

    function handleReset() {
        setTema("");
        setPlataforma("");
        setAudiencia("");
        setIdioma("es"); // ES por defecto
        setInfoAdicional("");
        setErrors({});
    }

    return (
        <form onSubmit={handleSubmit} className="form-card">
            <div className="form-header">
                <h2 className="form-title">📝 Crea tu Contenido</h2>

                {/* ✅ NUEVO: TABS */}
                <div className="form-tabs">
                    <button
                        type="button"
                        className={`tab-button ${activeTab === "normal" ? "tab-active" : ""}`}
                        onClick={() => setActiveTab("normal")}
                    >
                        📝 Normal
                    </button>
                    <button
                        type="button"
                        className={`tab-button ${activeTab === "scientific" ? "tab-active" : ""}`}
                        onClick={() => setActiveTab("scientific")}
                    >
                        🔬 Científico
                    </button>
                </div>
            </div>

            {/* ✅ NUEVO: Aviso científico */}
            {activeTab === "scientific" && (
                <div className="scientific-notice">
                    🔬 Contenido fundamentado en papers académicos y fuentes científicas
                </div>
            )}

            <div className={`form-group ${errors.tema ? 'error' : ''}`}>
                <label className="form-label" htmlFor="tema">Tema Principal</label>
                <input
                    id="tema"
                    type="text"
                    placeholder="Ej: Machine Learning, Web Design, Marketing..."
                    value={tema}
                    onChange={(e) => {
                        setTema(e.target.value);
                        if (errors.tema) {
                            setErrors({ ...errors, tema: '' });
                        }
                    }}
                />
                {errors.tema && <span className="form-error">{errors.tema}</span>}
            </div>

            <div className={`form-group ${errors.plataforma ? 'error' : ''}`}>
                <label className="form-label" htmlFor="plataforma">Plataforma Destino</label>
                <select
                    id="plataforma"
                    value={plataforma}
                    onChange={(e) => {
                        setPlataforma(e.target.value);
                        if (errors.plataforma) {
                            setErrors({ ...errors, plataforma: '' });
                        }
                    }}
                >
                    <option value="">Selecciona una plataforma</option>
                    <option value="twitter">🐦 Twitter / X</option>
                    <option value="blog">📰 Blog</option>
                    <option value="instagram">📸 Instagram</option>
                    <option value="linkedin">💼 LinkedIn</option>
                    <option value="tiktok">🎵 TikTok</option>
                    <option value="youtube">▶️ YouTube</option>
                </select>
                {errors.plataforma && <span className="form-error">{errors.plataforma}</span>}
            </div>

            <div className={`form-group ${errors.audiencia ? 'error' : ''}`}>
                <label className="form-label" htmlFor="audiencia">Audiencia Target</label>
                <input
                    id="audiencia"
                    type="text"
                    placeholder="Ej: Desarrolladores, Empresarios, Estudiantes..."
                    value={audiencia}
                    onChange={(e) => {
                        setAudiencia(e.target.value);
                        if (errors.audiencia) {
                            setErrors({ ...errors, audiencia: '' });
                        }
                    }}
                />
                {errors.audiencia && <span className="form-error">{errors.audiencia}</span>}
            </div>

            <div className="form-group">
                <label className="form-label" htmlFor="idioma">🌐 Idioma</label>
                <select
                    id="idioma"
                    value={idioma}
                    onChange={(e) => setIdioma(e.target.value)}
                    className="form-control"
                >
                    <option value="es">🇪🇸 Español</option>
                    <option value="en">🇬🇧 English</option>
                    <option value="fr">🇫🇷 Français</option>
                    <option value="it">🇮🇹 Italiano</option>
                </select>
            </div>

            <div className="form-group">
                <label className="form-label optional" htmlFor="infoAdicional">Información Adicional</label>
                <textarea
                    id="infoAdicional"
                    value={infoAdicional}
                    onChange={(e) => setInfoAdicional(e.target.value)}
                    placeholder="Detalles adicionales, instrucciones especiales, tono deseado, etc... (Opcional)"
                />
            </div>

            <div className="form-button-group">
                <button
                    type="submit"
                    disabled={isSubmitting}
                >
                    {isSubmitting ? (
                        <>
                            <span className="loading-spinner"></span>
                            Generando...
                        </>
                    ) : (
                        <>✨ Generar Contenido</>
                    )}
                </button>
                <button
                    type="reset"
                    onClick={handleReset}
                >
                    🔄 Limpiar
                </button>
            </div>

            <div className="form-tip">
                <span>Proporciona más detalles en la información adicional para obtener mejor contenido.</span>
            </div>
        </form>
    )
}