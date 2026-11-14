import { useEffect, useState } from 'react'
import { acceder, primerError } from '../api/cliente'
import { useForm } from '../hooks/useForm'

export const EnviarAviso = ({ gimnasioId }) => {
  const [alumnos, setAlumnos] = useState([])
  const [mensaje, setMensaje] = useState(null)
  const [error, setError] = useState(null)
  const { alumno, titulo, texto, onInputChange, onResetForm } = useForm({
    alumno: '',
    titulo: '',
    texto: '',
  })

  useEffect(() => {
    const cargarAlumnos = async () => {
      const resp = await acceder(`/api/gimnasios/${gimnasioId}/miembros/`)
      const miembros = await resp.json()
      setAlumnos(miembros.filter((m) => m.rol === 'alumno'))
    }
    cargarAlumnos()
  }, [gimnasioId])

  const enviar = async (e) => {
    e.preventDefault()
    setError(null)
    setMensaje(null)

    const cuerpo = alumno ? { alumno, titulo, texto } : { titulo, texto }
    const resp = await acceder(`/api/gimnasios/${gimnasioId}/avisos/`, {
      method: 'POST',
      body: JSON.stringify(cuerpo),
    })
    const datos = await resp.json()

    if (!resp.ok) {
      setError(primerError(datos))
      return
    }
    setMensaje(`Aviso enviado a ${datos.enviados} alumnos`)
    onResetForm()
  }
  return (
    <section className="flex w-full max-w-sm flex-col gap-3">
      <h2 className="text-xl font-bold text-tinta">Enviar aviso</h2>

      <form onSubmit={enviar} className="flex flex-col gap-2">
        <select
          name="alumno"
          value={alumno}
          onChange={onInputChange}
          className="rounded border border-borde bg-superficie px-3 py-2"
        >
          <option value="">Todos los alumnos</option>
          {alumnos.map((m) => (
            <option key={m.id} value={m.usuario.id}>
              {m.usuario.first_name} {m.usuario.last_name}
            </option>
          ))}
        </select>
        <input
          name="titulo"
          value={titulo}
          onChange={onInputChange}
          placeholder="Título"
          maxLength={100}
          required
          className="rounded border border-borde bg-superficie px-3 py-2"
        />
        <textarea
          name="texto"
          value={texto}
          onChange={onInputChange}
          placeholder="Mensaje (opcional)"
          maxLength={255}
          rows={3}
          className="rounded border border-borde bg-superficie px-3 py-2"
        />
        <button className="rounded bg-primario px-4 py-2 text-white">Enviar</button>
      </form>

      {mensaje && <p className="text-tinta">{mensaje}</p>}
      {error && <p className="text-primario">{error}</p>}
    </section>
  )
}
