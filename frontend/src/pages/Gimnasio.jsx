import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router'
import { acceder } from '../api/cliente'
import { Invitaciones } from '../components/Invitaciones'
import { Miembros } from '../components/Miembros'

export const Gimnasio = () => {
  const { gimnasioId } = useParams()
  const navigate = useNavigate()
  const [membresia, setMembresia] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    const cargarMembresia = async () => {
      const resp = await acceder('/api/gimnasios/')
      const membresias = await resp.json()
      const membresia_buscada = membresias.find((m) => m.gimnasio.id === parseInt(gimnasioId))
      setMembresia(membresia_buscada ?? false)
    }
    cargarMembresia()
  }, [gimnasioId])

  if (membresia === null) return <p className="p-6 text-tenue">Cargando...</p>
  if (membresia === false) return <p className="p-6 text-tenue">No perteneces a este gimnasio</p>

  const puedeInvitar = membresia.rol !== 'alumno'

  const salir = async () => {
    if (!window.confirm(`¿Salir de ${membresia.gimnasio.nombre}?`)) return

    const resp = await acceder(`/api/gimnasios/${gimnasioId}/salir/`, { method: 'POST' })

    if (!resp.ok) {
      const datos = await resp.json()
      setError(datos.error)
      return
    }
    navigate('/')
  }

  return (
    <main className="flex min-h-screen flex-col items-center gap-6 bg-fondo p-6">
      <header className="flex w-full max-w-sm items-center justify-between">
        <Link to="/" className="text-tenue underline">
          Volver
        </Link>
        <p className="text-tenue">{membresia.rol}</p>
      </header>

      <h1 className="text-2xl font-bold text-tinta">{membresia.gimnasio.nombre}</h1>
      {puedeInvitar && <Miembros gimnasioId={gimnasioId} rol={membresia.rol} />}
      {puedeInvitar && <Invitaciones gimnasioId={gimnasioId} rol={membresia.rol} />}
      <button onClick={salir} className="text-primario underline">
        Salir del gimnasio
      </button>
      {error && <p className="text-primario">{error}</p>}
    </main>
  )
}
