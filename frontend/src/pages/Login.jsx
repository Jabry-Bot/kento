import { GoogleLogin } from '@react-oauth/google'
import { useState } from 'react'
import { acceder, primerError } from '../api/cliente'
import { useSesion } from '../stores/useSesion'
import { PantallaAcceso } from '../components/PantallaAcceso'
import { useForm } from '../hooks/useForm'
import { Link } from 'react-router'

export const Login = () => {
  const login = useSesion((sesion) => sesion.login)
  const { email, password, formState, onInputChange } = useForm({ email: '', password: '' })
  const [error, setError] = useState(null)

  const entrar = async (ruta, body) => {
    const resp = await acceder(
      ruta,
      {
        method: 'POST',
        body: JSON.stringify(body),
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

  const entrarEmail = (e) => {
    e.preventDefault()
    entrar('api/cuentas/login/', formState)
  }

  return (
    <PantallaAcceso titulo="Iniciar sesión">
      <GoogleLogin
        onSuccess={({ credential }) => entrar('/api/cuentas/google/', { credential })}
        onError={() => setError('No se ha podido iniciar sesión con Google')}
      />

      <p className="text-center text-tenue">o con tu email</p>

      <form onSubmit={entrarEmail} className="flex flex-col gap-3">
        <input
          type="email"
          name="email"
          value={email}
          onChange={onInputChange}
          placeholder="Email"
          required
          className="rounded border border-borde bg-superficie px-3 py-2"
        />
        <input
          type="password"
          name="password"
          value={password}
          onChange={onInputChange}
          placeholder="Contraseña"
          required
          className="rounded border border-borde bg-superficie px-3 py-2"
        />
        <button type="submit" className="rounded bg-primario px-4 py-2 text-white">
          Entrar
        </button>
      </form>

      {error && <p className="text-primario">{error}</p>}

      <Link to="/recuperar" className="text-tenue underline">
        He olvidado mi contraseña
      </Link>
      <Link to="/registro" className="text-tenue underline">
        Crear una cuenta
      </Link>
    </PantallaAcceso>
  )
}
