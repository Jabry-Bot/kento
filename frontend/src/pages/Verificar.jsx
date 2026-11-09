import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router'
import { acceder, primerError } from '../api/cliente'
import { PantallaAcceso } from '../components/PantallaAcceso'
import { useSesion } from '../stores/useSesion'

export const Verificar = () => {
  const { usuarioId, token } = useParams()
  const login = useSesion((sesion) => sesion.login)
  const navigate = useNavigate()
  const [error, setError] = useState(null)

  const activar = async () => {
    const resp = await acceder(
      `/api/cuentas/verificar/${usuarioId}/${token}/`,
      { method: 'POST' },
      false,
    )
    const datos = await resp.json()
    if (!resp.ok) {
      setError(primerError(datos))
      return
    }
    login(datos)
    navigate('/')
  }
  return (
    <PantallaAcceso titulo="Activa tu cuenta">
      <button onClick={activar} className="rounded bg-primario px-4 py-2 text-white">
        Activar mi cuenta
      </button>
      {error && <p className="text-primario">{error}</p>}
      <Link to="/login" className="text-tenue underline">
        Ir a iniciar sesión
      </Link>
    </PantallaAcceso>
  )
}
