import { useEffect, useState } from 'react'
import { Link } from 'react-router'
import { acceder, primerError } from '../api/cliente'
import { FormularioFicha } from '../components/FormularioFicha'
import { useSesion } from '../stores/useSesion'

export const Perfil = () => {
  const usuario = useSesion((sesion) => sesion.usuario)
  const [ficha, setFicha] = useState(null)
  const actualizarUsuario = useSesion((sesion) => sesion.actualizarUsuario)
  const [error, setError] = useState(null)

  useEffect(() => {
    const cargarFicha = async () => {
      const resp = await acceder('/api/cuentas/yo/ficha/')
      setFicha(await resp.json())
    }
    cargarFicha()
  }, [])

  const cambiarFoto = async (e) => {
    const datosForm = new FormData()
    datosForm.append('foto_perfil', e.target.files[0])

    const resp = await acceder('/api/cuentas/yo/foto/', { method: 'PATCH', body: datosForm })
    const datos = await resp.json()
    if (!resp.ok) {
      setError(primerError(datos))
      return
    }
    setError(null)
    actualizarUsuario(datos)
  }

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
      <label className="cursor-pointer text-primario underline">
        Cambiar foto
        <input type="file" accept="image/*" onChange={cambiarFoto} className="hidden" />
      </label>
      {error && <p className="text-primario">{error}</p>}

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
