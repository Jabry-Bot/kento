import { Navigate, Route, Routes } from 'react-router'
import { Inicio } from '../pages/Inicio'

export const RutasApp = () => {
  return (
    <Routes>
      <Route path="/" element={<Inicio />} />

      <Route path="/*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
