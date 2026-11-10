import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useSesion = create(
  persist(
    (set) => ({
      estado: 'no-autenticado',
      usuario: null,
      access: null,
      refresh: null,

      login: ({ access, refresh, usuario }) =>
        set({ estado: 'autenticado', access, refresh, usuario }),

      actualizarTokens: ({ access, refresh }) =>
        set((estadoActual) => ({ access, refresh: refresh ?? estadoActual.refresh })),

      actualizarUsuario: (usuario) => set({ usuario }),

      logout: () => set({ estado: 'no-autenticado', usuario: null, access: null, refresh: null }),
    }),
    { name: 'sesion' },
  ),
)
