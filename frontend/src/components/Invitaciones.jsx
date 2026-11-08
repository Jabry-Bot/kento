import { QRCodeSVG } from 'qrcode.react'
import { useEffect, useState } from 'react'
import { acceder } from '../api/cliente'

export const Invitaciones = ({ gimnasioId, rol }) => {
  const [invitaciones, setInvitaciones] = useState([])
  const [rolInvitado, setRolInvitado] = useState('alumno')
  const [error, setError] = useState(null)
  const ruta = `/api/gimnasios/${gimnasioId}/invitaciones/`

  useEffect(() => {
    const cargarInvitaciones = async () => {
      const resp = await acceder(ruta)
      setInvitaciones(await resp.json())
    }
    cargarInvitaciones()
  }, [ruta])

  const crearInvitacion = async () => {
    const resp = await acceder(ruta, {
      method: 'POST',
      body: JSON.stringify({ rol: rolInvitado }),
    })
    const datos = await resp.json()
    if (!resp.ok) {
      setError(datos.error ?? 'No se ha podido crear la invitacion')
      return
    }
    setInvitaciones([datos, ...invitaciones])
  }

  const anularInvitaciones = async (id) => {
    const resp = await acceder(`${ruta}${id}/`, { method: 'DELETE' })
    if (resp.ok) setInvitaciones(invitaciones.filter((invitacion) => invitacion.id !== id))
  }

  const enlace = (codigo) => `${window.location.origin}/invitacion/${codigo}`

  return (
    <section className="flex w-full max-w-sm flex-col gap-3">
      <h2 className="text-xl font-bold text-tinta">Invitaciones</h2>
      <div className="flex gap-2">
        <select
          value={rolInvitado}
          onChange={(e) => setRolInvitado(e.target.value)}
          className="flex-1 rounded border border-borde bg-superficie px-3 py-2"
        >
          <option value="alumno">Alumno</option>
          {rol === 'propietario' && <option value="entrenador">Entrenador</option>}
          {rol === 'propietario' && <option value="propietario">Propietario</option>}
        </select>
        <button onClick={crearInvitacion} className="rounded bg-primario px-4 py-2 text-white">
          Crear
        </button>
      </div>

      {error && <p className="text-primario">{error}</p>}

      <ul className="flex flex-col gap-3">
        {invitaciones.map((invitacion) => (
          <li
            key={invitacion.id}
            className="flex flex-col items-center gap-2 rounded border border-borde bg-superficie p-3"
          >
            <p className="text-tinta">
              {invitacion.rol} {'->'} {invitacion.usos}/{invitacion.usos_max} (caduca:{' '}
              {new Date(invitacion.caduca).toLocaleDateString()})
            </p>
            <QRCodeSVG value={enlace(invitacion.codigo)} size={160} />
            <button
              onClick={() => navigator.clipboard.writeText(enlace(invitacion.codigo))}
              className="text-tenue underline"
            >
              Copiar enlace
            </button>
            <button
              onClick={() => anularInvitaciones(invitacion.id)}
              className="text-primario underline"
            >
              Anular
            </button>
          </li>
        ))}
      </ul>
    </section>
  )
}
