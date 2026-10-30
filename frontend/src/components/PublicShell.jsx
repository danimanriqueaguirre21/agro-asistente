import PublicHeader from "./PublicHeader.jsx";

export default function PublicShell({ children }) {
  return (
    <div className="app-shell">
      <PublicHeader />
      <main className="page">{children}</main>
      <footer className="site-footer">
        <p>Agro-Asistente</p>
      </footer>
    </div>
  );
}
