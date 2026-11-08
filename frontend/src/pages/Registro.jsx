import { useState } from 'react'
import { Link } from 'react-router'
import { acceder, primerError } from '../api/cliente'
import { PantallaAcceso } from '../components/PantallaAcceso'
import { useForm } from '../hooks/useForm'

export const Registro = () => {
  const { first_name, last_name, email, password, formState, onInputChange } = useForm({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
  })
  const [error, setError] = useState(null)
  const [enviado, setEnviado] = useState(false)

  const registrarse = async (e) => {
    e.preventDefault()

    const resp = await acceder(
      '/api/cuentas/registro/',
      { method: 'POST', body: JSON.stringify(formState) },
      false,
    )
    const datos = await resp.json()

    if (!resp.ok) {
      setError(primerError(datos))
      return
    }
    setEnviado(true)
  }

  if (enviado) {
    return (
      <PantallaAcceso titulo="Revise su correo">
        <p className="text-tinta">
          Le hemos enviado un enlace a <b>{email}</b> para activar su cuenta
        </p>
      </PantallaAcceso>
    )
  }

  return (
    <PantallaAcceso titulo="Crear Cuenta">
      {' '}
      <form onSubmit={registrarse} className="flex flex-col gap-3">
        <input
          name="first_name"
          value={first_name}
          onChange={onInputChange}
          placeholder="Nombre"
          required
          className="rounded border border-borde bg-superficie px-3 py-2"
        />
        <input
          name="last_name"
          value={last_name}
          onChange={onInputChange}
          placeholder="Apellidos"
          className="rounded border border-borde bg-superficie px-3 py-2"
        />
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
          placeholder="Contraseña (mínimo 8 caracteres)"
          minLength={8}
          required
          className="rounded border border-borde bg-superficie px-3 py-2"
        />
        <button type="submit" className="rounded bg-primario px-4 py-2 text-white">
          Crear cuenta
        </button>
      </form>
      {error && <p className="text-primario">{error}</p>}
      <Link to="/login" className="text-tenue underline">
        Ya tengo cuenta
      </Link>
    </PantallaAcceso>
  )
}
