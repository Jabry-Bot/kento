import { useState } from 'react'
import { acceder } from '../api/cliente'
import { useForm } from '../hooks/useForm'

export const SinGimnasio = ({ alCrear }) => {
  const { nombre, ciudad, formState, onInputChange } = useForm({ nombre: '', ciudad: '' })
  const [error, setError] = useState(null)

  const crearGimnasio = async (e) => {
    e.preventDefault()

    const resp = await acceder('/api/gimnasios/', {
      method: 'POST',
      body: JSON.stringify(formState),
    })
    const datos = await resp.json()

    if (!resp.ok) {
      setError(datos.nombre?.[0] ?? 'No se ha podido crear el gimnasio')
      return
    }
    alCrear(datos)
  }

  return (
    <form onSubmit={crearGimnasio} className="flex w-full max-w-sm flex-col gap-3">
      <h2 className="text-xl font-bold text-tinta">Crea tu gimnasio</h2>
      <p>Serás su propietario y podrás invitar a entrenadores y alumnos.</p>

      <input
        name="nombre"
        value={nombre}
        onChange={onInputChange}
        placeholder="Nombre del gimnasio"
        required
        className="rounded border border-borde bg-superficie px-3 py-2"
      />

      <input
        name="ciudad"
        value={ciudad}
        onChange={onInputChange}
        placeholder="Ciudad"
        className="rounded border border-borde bg-superficie px-3 py-2"
        required
      />

      <button type="submit" className="rounded bg-primario px-4 py-2 text-white">
        Crear gimnasio
      </button>
      {error && <p className="text-primario">{error}</p>}
    </form>
  )
}
