export default function OutputDisplay({contenido, loading, error}) {
    return (
        //JSX aqui
        <div>
            {loading && <p>Cargando...</p>}
            {error && <p>Error: {error}</p>}
            {contenido && <p>{contenido}</p>}
            {!loading && !error && !contenido && <p>Nada que mostrar</p>}
        </div>
    )
}