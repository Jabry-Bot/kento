import { useState } from 'react'
import { Link } from 'react-router'
import { acceder, primerError } from '../api/cliente'
import { PantallaAcceso } from '../components/PantallaAcceso'
import { useForm } from '../hooks/useForm'

export const Recuperar = () => {
  const { email, formState, onInputChange } = useForm({ email: '' })
  const [mensaje, setMensaje] = useState(null)

  const pedirEnlace = async (e) => {
    e.preventDefault()

    const resp = await acceder(
      '/api/cuentas/recuperar/',
      { method: 'POST', body: JSON.stringify(formState) },
      false,
    )
    const datos = await resp.json()
    setMensaje(resp.ok ? datos.mensaje : primerError(datos))
  }

  return (
    <PantallaAcceso titulo="Recuperar contraseña">
      <form onSubmit={pedirEnlace} className="flex flex-col gap-3">
        <input
          type="email"
          name="email"
          value={email}
          onChange={onInputChange}
          placeholder="Tu email"
          required
          className="rounded border border-borde bg-superficie px-3 py-2"
        />
        <button type="submit" className="rounded bg-primario px-4 py-2 text-white">
          Enviarme un enlace
        </button>
      </form>

      {mensaje && <p className="text-tinta">{mensaje}</p>}

      <Link to="/login" className="text-tenue underline">
        Volver a iniciar sesion
      </Link>
    </PantallaAcceso>
  )
}
