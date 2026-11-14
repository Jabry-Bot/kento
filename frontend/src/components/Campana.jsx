import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router'
import { acceder } from '../api/cliente'

export const Campana = () => {
  const navigate = useNavigate()
  const [abierta, setAbierta] = useState(false)
  const [noLeidas, setNoLeidas] = useState(0)
  const [lista, setLista] = useState([])
  useEffect(() => {
    const cargar = async () => {
      const resp = await acceder('/api/notificaciones/')
      if (!resp.ok) return
      const datos = await resp.json()
      setNoLeidas(datos.no_leidas)
      setLista(datos.lista)
    }
    cargar()
    const intervalo = setInterval(cargar, 30000)
    return () => clearInterval(intervalo)
  }, [])

  const abrir = (notificacion) => {
    setAbierta(false)
    if (notificacion.enlace) navigate(notificacion.enlace)
  }

  const leerTodas = async () => {
    const resp = await acceder('/api/notificaciones/leidas/', { method: 'POST' })
    if (!resp.ok) return
    setNoLeidas(0)
    setLista(lista.map((n) => ({ ...n, leida: true })))
  }

  return (
    <div className="relative">
      <button
        onClick={() => setAbierta(!abierta)}
        aria-label="Notificaciones"
        className="relative text-tinta"
      >
        {/* Icono de campana en SVG: sin librerías de iconos. */}
        <svg
          viewBox="0 0 24 24"
          className="h-6 w-6"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path d="M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9" />
          <path d="M13.7 21a2 2 0 0 1-3.4 0" />
        </svg>
        {noLeidas > 0 && (
          <span className="absolute -top-1 -right-2 rounded-full bg-primario px-1.5 text-xs text-white">
            {noLeidas}
          </span>
        )}
      </button>

      {abierta && (
        // absolute: se abre encima de la página, debajo de la campana, sin mover nada.
        <div className="absolute right-0 z-10 mt-2 flex w-80 max-w-[90vw] flex-col gap-2 rounded border border-borde bg-superficie p-3 shadow">
          <div className="flex items-center justify-between">
            <p className="font-bold text-tinta">Notificaciones</p>
            {noLeidas > 0 && (
              <button onClick={leerTodas} className="text-sm text-primario underline">
                Marcar todas como leídas
              </button>
            )}
          </div>

          {lista.length === 0 && <p className="text-tenue">No tienes notificaciones</p>}

          <ul className="flex max-h-96 flex-col gap-1 overflow-y-auto">
            {lista.map((notificacion) => (
              <li key={notificacion.id}>
                <button
                  onClick={() => abrir(notificacion)}
                  className={`w-full rounded p-2 text-left hover:bg-fondo ${notificacion.leida ? '' : 'font-bold'}`}
                >
                  <p className="text-tinta">{notificacion.titulo}</p>
                  {notificacion.texto && <p className="text-sm text-tenue">{notificacion.texto}</p>}
                  <p className="text-xs text-tenue">
                    {new Date(notificacion.fecha).toLocaleString('es-ES')}
                  </p>
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
