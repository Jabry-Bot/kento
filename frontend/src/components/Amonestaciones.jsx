import { useEffect, useState } from 'react'
import { acceder, primerError } from '../api/cliente'
import { useForm } from '../hooks/useForm'

export const Amonestaciones = ({ gimnasioId, rol }) => {
  const [amonestaciones, setAmonestaciones] = useState([])
  const [alumnos, setAlumnos] = useState([])
  const [error, setError] = useState(null)
  const { alumno, motivo, gravedad, formState, onInputChange, onResetForm } = useForm({
    alumno: '',
    motivo: '',
    gravedad: 'leve',
  })
  const ruta = `/api/gimnasios/${gimnasioId}/`
  const esEntrenador = rol !== 'alumno'

  useEffect(() => {
    const cargar = async () => {
      const resp = await acceder(ruta + 'amonestaciones/')
      setAmonestaciones(await resp.json())

      if (esEntrenador) {
        const resp = await acceder(ruta + 'miembros/')
        const miembros = await resp.json()
        setAlumnos(miembros.filter((m) => m.rol === 'alumno'))
      }
    }
    cargar()
  }, [ruta, esEntrenador])

  const poner = async (e) => {
    e.preventDefault()
    setError(null)

    const resp = await acceder(ruta + 'amonestaciones/', {
      method: 'POST',
      body: JSON.stringify(formState),
    })
    const data = await resp.json()

    if (!resp.ok) {
      setError(primerError(data))
      return
    }

    setAmonestaciones([data, ...amonestaciones])
    onResetForm()
  }

  const borrar = async (amonestacion) => {
    if (!window.confirm('Esta a punto de quitar la amonestacion a ' + amonestacion.alumno_nombre))
      return
    const resp = await acceder(ruta + `amonestaciones/${amonestacion.id}/`, { method: 'DELETE' })
    if (resp.ok) setAmonestaciones(amonestaciones.filter((a) => a.id !== amonestacion.id))
  }
  return (
    <section className="flex w-full max-w-sm flex-col gap-3">
      <h2 className="text-xl font-bold text-tinta">
        {esEntrenador ? 'Amonestaciones' : 'Mis amonestaciones'}
      </h2>

      {esEntrenador && (
        <form onSubmit={poner} className="flex flex-col gap-2">
          <select
            name="alumno"
            value={alumno}
            onChange={onInputChange}
            required
            className="rounded border border-borde bg-superficie px-3 py-2"
          >
            <option value="">Elige un alumno</option>
            {alumnos.map((m) => (
              <option key={m.id} value={m.usuario.id}>
                {m.usuario.first_name} {m.usuario.last_name}
              </option>
            ))}
          </select>
          <input
            name="motivo"
            value={motivo}
            onChange={onInputChange}
            placeholder="Motivo"
            maxLength={255}
            required
            className="rounded border border-borde bg-superficie px-3 py-2"
          />
          <div className="flex gap-2">
            <select
              name="gravedad"
              value={gravedad}
              onChange={onInputChange}
              className="flex-1 rounded border border-borde bg-superficie px-3 py-2"
            >
              <option value="leve">Leve</option>
              <option value="grave">Grave</option>
            </select>
            <button className="rounded bg-primario px-4 py-2 text-white">Poner</button>
          </div>
        </form>
      )}

      {error && <p className="text-primario">{error}</p>}

      {amonestaciones.length === 0 && <p className="text-tenue">No hay amonestaciones</p>}

      <ul className="flex flex-col gap-2">
        {amonestaciones.map((amonestacion) => (
          <li
            key={amonestacion.id}
            className="flex items-start gap-3 rounded border border-borde bg-superficie p-3"
          >
            <div className="flex-1">
              {esEntrenador && <p className="font-bold text-tinta">{amonestacion.alumno_nombre}</p>}
              <p className="text-tinta">{amonestacion.motivo}</p>
              <p className="text-tenue">
                <span
                  className={amonestacion.gravedad === 'grave' ? 'font-bold text-primario' : ''}
                >
                  {amonestacion.gravedad}
                </span>
                {' - '}
                {new Date(amonestacion.fecha).toLocaleDateString('es-ES')}
                {amonestacion.autor_nombre && ` - ${amonestacion.autor_nombre}`}
              </p>
            </div>
            {esEntrenador && (
              <button onClick={() => borrar(amonestacion)} className="text-primario underline">
                Borrar
              </button>
            )}
          </li>
        ))}
      </ul>
    </section>
  )
}
