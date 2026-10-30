import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { clearSession } from "../api/client";
import BrandMark from "./BrandMark.jsx";

export default function AppHeader() {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  function handleLogout() {
    clearSession();
    navigate("/login", { replace: true });
  }

  function closeMenu() {
    setOpen(false);
  }

  return (
    <header className="site-header">
      <div className="site-header-inner">
        <NavLink to="/dashboard" className="brand-link" onClick={closeMenu}>
          <BrandMark />
        </NavLink>
        <button
          type="button"
          className="nav-toggle"
          aria-expanded={open}
          aria-controls="app-navigation"
          onClick={() => setOpen((current) => !current)}
        >
          Menú
        </button>
        <nav id="app-navigation" className={`site-nav ${open ? "is-open" : ""}`}>
          <NavLink to="/dashboard" onClick={closeMenu}>
            Dashboard
          </NavLink>
          <NavLink to="/context" onClick={closeMenu}>
            Contexto
          </NavLink>
          <NavLink to="/query" onClick={closeMenu}>
            Consulta
          </NavLink>
          <NavLink to="/knowledge" onClick={closeMenu}>
            Base de conocimiento
          </NavLink>
          <NavLink to="/riesgo" onClick={closeMenu}>
            Riesgo experimental
          </NavLink>
          <button type="button" className="logout-button logout-button-header" onClick={handleLogout}>
            Cerrar sesión
          </button>
        </nav>
      </div>
    </header>
  );
}
