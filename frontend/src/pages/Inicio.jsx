import { useEffect, useState } from 'react'
import { useSesion } from '../stores/useSesion'

const url = `${import.meta.env.VITE_API_URL}/api/health/`

export const Inicio = () => {
  const [estado, setEstado] = useState('Cargando...')
  const usuario = useSesion((sesion) => sesion.usuario)
  const logout = useSesion((sesion) => sesion.logout)

  useEffect(() => {
    const probarApi = async () => {
      try {
        const resp = await fetch(url)
        const data = await resp.json()
        setEstado(`API: ${data.status}`)
      } catch (error) {
        console.log(error)
        setEstado('API sin conexion')
      }
    }
    probarApi()
  }, [])

  return (
    <main className="flex min-h-screen items-center justify-center bg-fondo flex-col gap-2">
      <h1 className="text-4xl font-bold text-primario">Kento</h1>
      <hr className="w-40 border-tinta" />
      <p className="text-tenue">{estado}</p>
      <p className="text-tinta">Hola, {usuario?.first_name}</p>
      <button onClick={logout} className="rounded bg-primario px-4 py-2 text-white">
        Salir
      </button>
    </main>
  )
}
