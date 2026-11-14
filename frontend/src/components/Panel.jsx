import { useEffect, useState } from 'react'
import { acceder } from '../api/cliente'

export const Panel = ({ gimnasioId }) => {
  const [datos, setDatos] = useState(null)
  useEffect(() => {
    const cargar = async () => {
      const resp = await acceder(`/api/gimnasios/${gimnasioId}/datos/`)
      if (resp.ok) setDatos(await resp.json())
    }
    cargar()
  }, [gimnasioId])
  if (!datos) return null

  const cifras = [
    ['Alumnos activos', datos.alumnos],
    ['Altas en 30 días', datos.altas_30_dias],
    ['Solicitudes pendientes', datos.solicitudes],
    ['Amonestaciones en 90 días', datos.amonestaciones_90_dias],
  ]
  return (
    <section className="grid w-full max-w-sm grid-cols-2 gap-3">
      {cifras.map(([texto, valor]) => (
        <div key={texto} className="rounded border border-borde bg-superficie p-3">
          <p className="text-2xl font-bold text-tinta">{valor}</p>
          <p className="text-sm text-tenue">{texto}</p>
        </div>
      ))}
    </section>
  )
}
