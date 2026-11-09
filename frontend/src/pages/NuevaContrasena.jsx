import { useState } from 'react'
import { useNavigate, useParams } from 'react-router'
import { acceder, primerError } from '../api/cliente'
import { PantallaAcceso } from '../components/PantallaAcceso'
import { useForm } from '../hooks/useForm'
import { useSesion } from '../stores/useSesion'

export const NuevaContrasena = () => {
  const { usuarioId, token } = useParams()
  const login = useSesion((sesion) => sesion.login)
  const navigate = useNavigate()
  const { password, formState, onInputChange } = useForm({ password: '' })
  const [error, setError] = useState(null)

  const guardar = async (e) => {
    e.preventDefault()

    const resp = await acceder(
      `/api/cuentas/nueva-contrasena/${usuarioId}/${token}/`,
      { method: 'POST', body: JSON.stringify(formState) },
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
    <PantallaAcceso titulo="Nueva contraseña">
      <form onSubmit={guardar} className="flex flex-col gap-3">
        <input
          type="password"
          name="password"
          value={password}
          onChange={onInputChange}
          placeholder="Contraseña nueva (mínimo 8 caracteres)"
          minLength={8}
          required
          className="rounded border border-borde bg-superficie px-3 py-2"
        />
        <button type="submit" className="rounded bg-primario px-4 py-2 text-white">
          Guardar y entrar
        </button>
      </form>

      {error && <p className="text-primario">{error}</p>}
    </PantallaAcceso>
  )
}
