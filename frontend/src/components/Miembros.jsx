import { useEffect, useState } from 'react'
import { acceder } from '../api/cliente'

export const Miembros = ({ gimnasioId, rol }) => {
  const [miembros, setMiembros] = useState([])
  const ruta = `/api/gimnasios/${gimnasioId}/miembros/`

  useEffect(() => {
    const cargarMiembros = async () => {
      const resp = await acceder(ruta)
      setMiembros(await resp.json())
    }
    cargarMiembros()
  }, [ruta])

  const puedeDarBaja = (miembro) => miembro.rol === 'alumno' || rol === 'propietario'

  const darBaja = async (miembro) => {
    if (!window.confirm(`Esta a punto de dar de baja a ${miembro.usuario.first_name}`)) return

    const resp = await acceder(`${ruta}${miembro.id}/`, { method: 'DELETE' })

    if (resp.ok) setMiembros(miembros.filter((m) => m.id !== miembro.id))
  }

  const resumenFicha = (ficha) => {
    const partes = []
    if (ficha.edad) partes.push(`${ficha.edad} años`)
    if (ficha.sexo) partes.push(ficha.sexo)
    if (ficha.peso) partes.push(`${ficha.peso} kg`)
    return partes.length === 0 ? 'Ficha sin rellenar' : partes.join(' - ')
  }
  return (
    <section className="flex w-full max-w-sm flex-col gap-3">
      <h2 className="text-xl font-bold text-tinta">Miembros ({miembros.length})</h2>

      <ul className="flex flex-col gap-2">
        {miembros.map((miembro) => (
          <li
            key={miembro.id}
            className="flex items-center gap-3 rounded border border-borde bg-superficie p-3"
          >
            {miembro.usuario.foto && (
              <img
                src={miembro.usuario.foto}
                alt=""
                className="h-10 w-10 rounded-full object-cover"
              />
            )}
            <div className="flex-1">
              <p className="font-bold text-tinta">
                {miembro.usuario.first_name} {miembro.usuario.last_name}
              </p>
              <p className="text-tenue">
                {miembro.rol} - {resumenFicha(miembro.ficha)}
              </p>
            </div>
            {puedeDarBaja(miembro) && (
              <button onClick={() => darBaja(miembro)} className="text-primario underline">
                Baja
              </button>
            )}
          </li>
        ))}
      </ul>
    </section>
  )
}
