import { Navigate, Route, Routes } from 'react-router'
import { Inicio } from '../pages/Inicio'
import { Login } from '../pages/Login'
import { ProtectedRoute } from './ProtectedRoute'
import { PublicRoute } from './PublicRoute'
import { Gimnasio } from '../pages/Gimnasio'
import { Invitacion } from '../pages/Invitacion'

export const RutasApp = () => {
  return (
    <Routes>
      <Route element={<PublicRoute />}>
        <Route path="/login" element={<Login />} />
      </Route>

      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<Inicio />} />
        <Route path="/gimnasios/:gimnasioId" element={<Gimnasio />} />
      </Route>

      <Route path="/invitacion/:codigo" element={<Invitacion />} />
      <Route path="/*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
