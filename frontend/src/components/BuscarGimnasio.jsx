import { useState } from 'react'
import { acceder, primerError } from '../api/cliente'
import { useForm } from '../hooks/useForm'

export const BuscarGimnasio = () => {
  const { texto, onInputChange } = useForm({ texto: '' })
  const [gimnasios, setGimnasios] = useState([])
  const [mensaje, setMensaje] = useState(null)

  const buscar = async (e) => {
    e.preventDefault()
    const resp = await acceder(`/api/gimnasios/buscar/?q=${encodeURIComponent(texto)}`)
    const datos = await resp.json()
    setGimnasios(datos)
    setMensaje(datos.length === 0 ? 'No hemos encontrado coincidencias' : null)
  }

  const solicitar = async (gimnasio) => {
    const resp = await acceder(`/api/gimnasios/${gimnasio.id}/solicitar/`, { method: 'POST' })
    const datos = await resp.json()
    setMensaje(resp.ok ? `Solicitud enviada a ${gimnasio.nombre}` : primerError(datos))
  }
  return (
    <section className="flex w-full max-w-sm flex-col gap-3">
      <h2 className="text-xl font-bold text-tinta">Unirme a un gimnasio</h2>

      <form onSubmit={buscar} className="flex gap-2">
        <input
          name="texto"
          value={texto}
          onChange={onInputChange}
          placeholder="Nombre o ciudad"
          minLength={2}
          required
          className="flex-1 rounded border border-borde bg-superficie px-3 py-2"
        />
        <button type="submit" className="rounded bg-primario px-4 py-2 text-white">
          Buscar
        </button>
      </form>

      {mensaje && <p className="text-tinta">{mensaje}</p>}

      <ul className="flex flex-col gap-2">
        {gimnasios.map((gimnasio) => (
          <li
            key={gimnasio.id}
            className="flex items-center justify-between rounded border border-borde bg-superficie p-3"
          >
            <div>
              <p className="font-bold text-tinta">{gimnasio.nombre}</p>
              <p className="text-tenue">{gimnasio.ciudad}</p>
            </div>
            <button onClick={() => solicitar(gimnasio)} className="text-primario underline">
              Solicitar
            </button>
          </li>
        ))}
      </ul>
    </section>
  )
}
