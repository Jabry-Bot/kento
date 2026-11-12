import { useEffect } from 'react'
import { Link, Outlet } from 'react-router'
import { acceder } from '../api/cliente'
import { useSesion } from '../stores/useSesion'

export const MarcoApp = () => {
  const usuario = useSesion((sesion) => sesion.usuario)
  const actualizarUsuario = useSesion((sesion) => sesion.actualizarUsuario)
  const logout = useSesion((sesion) => sesion.logout)

  useEffect(() => {
    const cargarUsuario = async () => {
      const resp = await acceder('/api/cuentas/yo/')
      if (resp.ok) actualizarUsuario(await resp.json())
    }
    cargarUsuario()
  }, [actualizarUsuario])

  return (
    <div className="min-h-screen bg-fondo">
      <header className="flex items-center justify-between border-b border-borde bg-superficie px-4 py-3">
        <Link to="/" className="text-xl font-bold text-primario">
          Kento
        </Link>

        <div className="flex items-center gap-4">
          <Link to="/perfil" className="flex items-center gap-2 text-tinta">
            {usuario?.foto && (
              <img src={usuario.foto} alt="" className="h-8 w-8 rounded-full object-cover" />
            )}
            {usuario?.first_name}
          </Link>
          <button onClick={logout} className="text-tenue underline">
            Cerrar sesión
          </button>
        </div>
      </header>

      <main className="flex flex-col items-center gap-6 p-6">
        <Outlet />
      </main>
    </div>
  )
}
