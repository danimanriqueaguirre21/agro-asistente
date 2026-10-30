import { Link, useNavigate } from "react-router-dom";
import { clearSession } from "../api/client";

export default function AuthFooter({ showDashboardLink = true }) {
  const navigate = useNavigate();

  function handleLogout() {
    clearSession();
    navigate("/login", { replace: true });
  }

  return (
    <div className="auth-footer">
      {showDashboardLink && (
        <p className="nav-link">
          <Link to="/dashboard">Volver al panel</Link>
        </p>
      )}
      <button type="button" className="logout-button" onClick={handleLogout}>
        Cerrar sesión
      </button>
    </div>
  );
}
