import { useState } from 'react'
import { acceder } from '../api/cliente'
import { useForm } from '../hooks/useForm'

export const FormularioFicha = ({ ficha }) => {
  const { fecha_nacimiento, sexo, peso, formState, onInputChange } = useForm({
    fecha_nacimiento: ficha.fecha_nacimiento ?? '',
    sexo: ficha.sexo,
    peso: ficha.peso ?? '',
  })

  const [error, setError] = useState(null)

  const guardarFicha = async (e) => {
    e.preventDefault()

    const resp = await acceder('/api/cuentas/yo/ficha/', {
      method: 'PATCH',
      body: JSON.stringify({
        ...formState,
        fecha_nacimiento: fecha_nacimiento || null,
        peso: peso || null,
      }),
    })

    const datos = await resp.json()

    if (!resp.ok) {
      // DRF devuelve -> {peso: ["Error Peso"],}
      setError(Object.values(datos)[0]?.[0] ?? 'No se ha podido guardar')
      return
    }
    setError('Guardado')
  }
  return (
    <form onSubmit={guardarFicha} className="flex w-full max-w-sm flex-col gap-3">
      <h2 className="text-xl font-bold text-tinta">Mi ficha</h2>
      <p className="text-tenue">La ven los entrenadores de todos tus gimnasios.</p>

      <label className="flex flex-col gap-1 text-tinta">
        Fecha de nacimiento
        <input
          type="date"
          name="fecha_nacimiento"
          value={fecha_nacimiento}
          onChange={onInputChange}
          className="rounded border border-borde bg-superficie px-3 py-2"
        />
      </label>

      <label className="flex flex-col gap-1 text-tinta">
        Sexo
        <select
          name="sexo"
          value={sexo}
          onChange={onInputChange}
          className="rounded border border-borde bg-superficie px-3 py-2"
        >
          <option value="">Sin indicar</option>
          <option value="H">Hombre</option>
          <option value="M">Mujer</option>
        </select>
      </label>

      <label className="flex flex-col gap-1 text-tinta">
        Peso en kg (opcional)
        <input
          type="number"
          name="peso"
          value={peso}
          onChange={onInputChange}
          step="0.1"
          min="10"
          max="250"
          className="rounded border border-borde bg-superficie px-3 py-2"
        />
      </label>

      <button type="submit" className="rounded bg-primario px-4 py-2 text-white">
        Guardar
      </button>
      {error && <p className="text-tenue">{error}</p>}
    </form>
  )
}
