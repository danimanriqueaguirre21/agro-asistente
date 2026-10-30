import { Link } from "react-router-dom";
import { getSessionFarmer } from "../api/client";
import AuthFooter from "../components/AuthFooter.jsx";
import AuthenticatedShell from "../components/AuthenticatedShell.jsx";

export default function DashboardPage() {
  const farmerLabel = getSessionFarmer();

  return (
    <AuthenticatedShell>
      <section className="card card-wide">
        <h1>Panel de Agro-Asistente</h1>
        <p className="lead">{farmerLabel ? `Bienvenido, ${farmerLabel}` : "Bienvenido"}</p>

        <ul className="panel-links">
          <li>
            <Link to="/context">
              <strong>Contexto agrícola</strong>
              <p>Gestiona y selecciona el contexto de tu cultivo.</p>
            </Link>
          </li>
          <li>
            <Link to="/query">
              <strong>Consulta agrícola</strong>
              <p>Realiza consultas de asistencia técnica agrícola.</p>
            </Link>
          </li>
          <li>
            <Link to="/knowledge">
              <strong>Base de conocimiento</strong>
              <p>Accede a la base de conocimiento disponible.</p>
            </Link>
          </li>
          <li>
            <Link to="/riesgo">
              <strong>Riesgo experimental</strong>
              <p>Prototipo académico con datos sintéticos. No es una evaluación agronómica validada.</p>
            </Link>
          </li>
        </ul>

        <AuthFooter showDashboardLink={false} />
      </section>
    </AuthenticatedShell>
  );
}
