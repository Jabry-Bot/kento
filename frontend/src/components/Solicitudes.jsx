import { useEffect, useState } from 'react'
import { acceder } from '../api/cliente'

export const Solicitudes = ({ gimnasioId }) => {
  const [solicitudes, setSolicitudes] = useState([])
  const ruta = `/api/gimnasios/${gimnasioId}/solicitudes/`

  useEffect(() => {
    const cargarSolicitudes = async () => {
      const resp = await acceder(ruta)
      setSolicitudes(await resp.json())
    }
    cargarSolicitudes()
  }, [ruta])

  const responder = async (solicitud, estado) => {
    const resp = await acceder(`${ruta}${solicitud.id}/`, {
      method: 'PATCH',
      body: JSON.stringify({ estado }),
    })
    if (resp.ok) setSolicitudes(solicitudes.filter((s) => s.id !== solicitud.id))
  }
  if (solicitudes.length === 0) return null

  return (
    <section className="flex w-full max-w-sm flex-col gap-3">
      <h2 className="text-xl font-bold text-tinta">Solicitudes ({solicitudes.length})</h2>

      <ul className="flex flex-col gap-2">
        {solicitudes.map((solicitud) => (
          <li
            key={solicitud.id}
            className="flex items-center gap-3 rounded border border-borde bg-superficie p-3"
          >
            <div className="flex-1">
              <p className="font-bold text-tinta">
                {solicitud.usuario.first_name} {solicitud.usuario.last_name}
              </p>
              <p className="text-tenue">{solicitud.usuario.email}</p>
            </div>
            <button
              onClick={() => responder(solicitud, 'aceptada')}
              className="text-primario underline"
            >
              Aceptar
            </button>
            <button
              onClick={() => responder(solicitud, 'rechazada')}
              className="text-tenue underline"
            >
              Rechazar
            </button>
          </li>
        ))}
      </ul>
    </section>
  )
}
