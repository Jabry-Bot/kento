export const PantallaAcceso = ({ titulo, children }) => {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-fondo p-6">
      <h1 className="text-3xl font-bold text-tinta">Kento</h1>
      <section className="flex w-full max-w-sm flex-col gap-3 rounded border border-borde bg-superficie p-6">
        <h2 className="text-xl font-bold text-tinta">{titulo}</h2>
        {children}
      </section>
    </main>
  )
}
