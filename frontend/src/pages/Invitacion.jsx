import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router'
import { acceder } from '../api/cliente'
import { useSesion } from '../stores/useSesion'

export const Invitacion = () => {
  const { codigo } = useParams()
  const estado = useSesion((sesion) => sesion.estado)
  const navigate = useNavigate()
  const [invitacion, setInvitacion] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    const cargarInvitacion = async () => {
      const resp = await acceder(`/api/gimnasios/invitaciones/${codigo}`)
      setInvitacion(resp.ok ? await resp.json() : false)
    }
    cargarInvitacion()
  }, [codigo])

  const unirse = async () => {
    if (estado !== 'autenticado') {
      navigate(`/login?siguiente=/invitacion/${codigo}/`)
      return
    }

    const resp = await acceder(`/api/gimnasios/invitaciones/${codigo}/aceptar/`, {
      method: 'POST',
    })
    const datos = await resp.json()

    if (!resp.ok) {
      setError(datos.error ?? 'No te has podido unir')
      return
    }
    navigate(`/gimnasios/${datos.gimnasio.id}`)
  }
  if (invitacion === null) return <p className="p-6 text-tenue">Cargando...</p>
  if (invitacion === false) return <p className="p-6 text-tenue">Esta Invitacion no existe</p>

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-fondo p-6">
      <h1 className="text-2xl font-bold text-tinta">{invitacion.gimnasio.nombre}</h1>

      <p className="text-tenue">
        {invitacion.creador} te invita como {invitacion.rol}
      </p>

      {invitacion.active ? (
        <button onClick={unirse} className="rounded bg-primario px-4 py-2 text-white">
          {estado === 'autenticado' ? 'Unirme' : 'Inicia sesión para unirte'}
        </button>
      ) : (
        <p className="text-primario">Esta invitación ya no es válida</p>
      )}
      {error && <p className="text-primario">{error}</p>}
    </main>
  )
}
