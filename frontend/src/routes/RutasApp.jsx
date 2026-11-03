import { Navigate, Route, Routes } from 'react-router'
import { Inicio } from '../pages/Inicio'
import { Login } from '../pages/Login'
import { ProtectedRoute } from './ProtectedRoute'
import { PublicRoute } from './PublicRoute'

export const RutasApp = () => {
  return (
    <Routes>
      <Route element={<PublicRoute />}>
        <Route path="/login" element={<Login />} />
      </Route>

      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<Inicio />} />
      </Route>

      <Route path="/*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
