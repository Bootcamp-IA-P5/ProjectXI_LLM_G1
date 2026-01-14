import { useState } from 'react';
import '../styles/OutputDisplay.css';

export default function OutputDisplay({ contenido, loading, error }) {
    const [copied, setCopied] = useState(false);

    function handleCopy() {
        if (contenido) {
            navigator.clipboard.writeText(contenido);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }
    }

    function handleDownload() {
        if (contenido) {
            const element = document.createElement('a');
            const file = new Blob([contenido], { type: 'text/plain' });
            element.href = URL.createObjectURL(file);
            element.download = `contenido_${new Date().getTime()}.txt`;
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
        }
    }

    return (
        <div className="output-card">
            <div className="output-header">
                <h2 className="output-title">
                    <span className="output-icon">✨</span>
                    Contenido Generado
                </h2>
            </div>

            {loading && (
                <div className="loading-container">
                    <div className="loading-spinner-large"></div>
                    <p className="loading-text">
                        Generando tu contenido<span className="loading-dots"></span>
                    </p>
                </div>
            )}

            {error && !loading && (
                <div className="error-container">
                    <div className="error-header">
                        <span className="error-icon">⚠️</span>
                        <h3 className="error-title">Error en la Generación</h3>
                    </div>
                    <p className="error-message">{error}</p>
                </div>
            )}

            {!loading && !error && contenido && (
                <>
                    <div className="output-content">
                        <p className="output-text">{contenido}</p>
                    </div>
                    <div className="output-actions">
                        <button
                            className={`btn-secondary btn-copy ${copied ? 'copied' : ''}`}
                            onClick={handleCopy}
                            title="Copiar al portapapeles"
                        >
                            {copied ? '✓ Copiado' : '📋 Copiar'}
                        </button>
                        <button
                            className="btn-secondary"
                            onClick={handleDownload}
                            title="Descargar como archivo"
                        >
                            ⬇️ Descargar
                        </button>
                    </div>
                </>
            )}

            {!loading && !error && !contenido && (
                <div className="empty-state">
                    <div className="empty-icon">📄</div>
                    <h3 className="empty-title">Sin contenido aún</h3>
                    <p className="empty-description">
                        Completa el formulario y haz clic en "Generar Contenido" para ver el resultado aquí
                    </p>
                </div>
            )}
        </div>
    )
}