import { useEffect, useState } from 'react'
import { Link } from 'react-router'
import { acceder } from '../api/cliente'
import { FormularioFicha } from '../components/FormularioFicha'
import { useSesion } from '../stores/useSesion'

export const Perfil = () => {
  const usuario = useSesion((sesion) => sesion.usuario)
  const [ficha, setFicha] = useState(null)

  useEffect(() => {
    const cargarFicha = async () => {
      const resp = await acceder('/api/cuentas/yo/ficha/')
      setFicha(await resp.json())
    }
    cargarFicha()
  }, [])

  return (
    <main className="flex min-h-screen flex-col items-center gap-6 bg-fondo p-6">
      <header className="flex w-full max-w-sm items-center justify-between">
        <Link to="/" className="text-tenue underline">
          Volver
        </Link>
      </header>
      {usuario?.foto && (
        <img src={usuario.foto} alt="" className="h-24 w-24 rounded-full object-cover" />
      )}
      <div className="text-center">
        <h1 className="text-2xl font-bold text-tinta">
          {usuario?.first_name} {usuario?.last_name}
        </h1>
        <p className="text-tenue">{usuario?.email}</p>
      </div>

      {ficha === null ? (
        <p className="text-tenue">Cargando...</p>
      ) : (
        <FormularioFicha ficha={ficha} />
      )}
    </main>
  )
}
