import { GoogleLogin } from '@react-oauth/google'
import { useState } from 'react'
import { acceder } from '../api/cliente'
import { useSesion } from '../stores/useSesion'

export const Login = () => {
  const login = useSesion((sesion) => sesion.login)
  const [error, setError] = useState(null)

  const entrar = async ({ credential }) => {
    const resp = await acceder(
      '/api/cuentas/google/',
      {
        method: 'POST',
        body: JSON.stringify({ credential }),
      },
      false,
    )
    const datos = await resp.json()

    if (!resp.ok) {
      setError(datos.error ?? 'No ha podido acceder')
      return
    }

    login(datos)
  }

  return (
    <main className="bg-amber-200">
      <h1>Kento</h1>
      <GoogleLogin
        onSuccess={entrar}
        onError={() => setError('No se ha podido iniciar sesion en Google')}
      />
      {error && <p className="border-secundario bg-tinta text-primario">{error}</p>}
    </main>
  )
}
