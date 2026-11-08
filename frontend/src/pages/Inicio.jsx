import { useEffect, useState } from 'react'
import { useSesion } from '../stores/useSesion'
import { acceder } from '../api/cliente'
import { SinGimnasio } from '../components/SinGimnasio'
import { Link } from 'react-router'

export const Inicio = () => {
  const usuario = useSesion((sesion) => sesion.usuario)
  const logout = useSesion((sesion) => sesion.logout)
  const [membresias, setMembresias] = useState(null)

  useEffect(() => {
    const cargarGimnasios = async () => {
      const resp = await acceder('/api/gimnasios/')
      setMembresias(await resp.json())
    }

    cargarGimnasios()
  }, [])

  const alCrear = (gimnasio) => {
    setMembresias([{ id: gimnasio.id, rol: 'propietario', gimnasio }])
  }

  if (membresias === null) {
    return <p className="p-6 text-tenue">Cargando...</p>
  }

  return (
    <main className="flex min-h-screen flex-col items-center gap-6 bg-fondo p-6">
      <header className="flex w-full max-w-sm items-center justify-between">
        <p className="text-tinta">Hola, {usuario?.first_name}</p>
        <button onClick={logout} className="text-tenue underline">
          Cerrar Sesion
        </button>
      </header>

      {membresias.length === 0 ? (
        <SinGimnasio alCrear={alCrear} />
      ) : (
        <ul className="flex w-full max-w-sm flex-col gap-2">
          {membresias.map((membresia) => (
            <li key={membresia.id}>
              <Link
                to={`/gimnasios/${membresia.gimnasio.id}`}
                className="block rounded border border-borde bg-superficie p-3"
              >
                <p className="font-bold text-tinta"> {membresia.gimnasio.nombre}</p>
                <p className=" text-tenue"> {membresia.rol}</p>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </main>
  )
}
