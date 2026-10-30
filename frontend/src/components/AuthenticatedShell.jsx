import AppHeader from "./AppHeader.jsx";

export default function AuthenticatedShell({ children }) {
  return (
    <div className="app-shell">
      <AppHeader />
      <main className="page page-auth">{children}</main>
    </div>
  );
}
