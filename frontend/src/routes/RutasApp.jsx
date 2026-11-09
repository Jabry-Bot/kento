import { Navigate, Route, Routes } from 'react-router'
import { Inicio } from '../pages/Inicio'
import { Login } from '../pages/Login'
import { ProtectedRoute } from './ProtectedRoute'
import { PublicRoute } from './PublicRoute'
import { Gimnasio } from '../pages/Gimnasio'
import { Invitacion } from '../pages/Invitacion'
import { Perfil } from '../pages/Perfil'
import { Recuperar } from '../pages/Recuperar'
import { Registro } from '../pages/Registro'
import { Verificar } from '../pages/Verificar'
import { NuevaContrasena } from '../pages/NuevaContrasena'

export const RutasApp = () => {
  return (
    <Routes>
      <Route element={<PublicRoute />}>
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />
        <Route path="/recuperar" element={<Recuperar />} />
      </Route>

      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<Inicio />} />
        <Route path="/gimnasios/:gimnasioId" element={<Gimnasio />} />
        <Route path="/perfil" element={<Perfil />} />
      </Route>

      <Route path="/invitacion/:codigo" element={<Invitacion />} />
      <Route path="/verificar/:usuarioId/:token" element={<Verificar />} />
      <Route path="/nueva-pass/:usuarioId/:token" element={<NuevaContrasena />} />
      <Route path="/*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
