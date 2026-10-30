import { useRef, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { loginFarmer, saveAccessToken, saveSessionFarmer } from "../api/client";
import PublicShell from "../components/PublicShell.jsx";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const submittingRef = useRef(false);
  const navigate = useNavigate();
  const location = useLocation();
  const registeredNotice = location.state?.registered
    ? "Registro exitoso. Inicia sesión con tus credenciales."
    : "";

  function handleSubmit(event) {
    event.preventDefault();
    if (submittingRef.current || loading) {
      return;
    }

    const trimmedEmail = email.trim();
    if (!trimmedEmail || !password) {
      setError("Revisa el correo y la contraseña.");
      return;
    }

    submittingRef.current = true;
    setLoading(true);
    setError("");

    loginFarmer({ email: trimmedEmail, password })
      .then((response) => {
        const token = response.data?.access_token;
        const farmerEmail = response.data?.farmer?.email;
        if (typeof token !== "string" || !token.trim() || !farmerEmail) {
          setError("No se pudo iniciar sesión. Inténtalo de nuevo.");
          return;
        }
        saveAccessToken(token);
        saveSessionFarmer(response.data.farmer);
        setPassword("");
        navigate("/dashboard", { replace: true });
      })
      .catch((err) => {
        const status = err.response?.status;
        const detail = err.response?.data?.detail;
        if (status === 401) {
          setError(typeof detail === "string" ? detail : "Credenciales inválidas");
        } else if (status === 400 || status === 422) {
          setError("Revisa el correo y la contraseña.");
        } else {
          setError("No se pudo iniciar sesión. Inténtalo de nuevo.");
        }
      })
      .finally(() => {
        submittingRef.current = false;
        setLoading(false);
      });
  }

  return (
    <PublicShell>
      <section className="card">
        <h1>Agro-Asistente</h1>
        <p className="lead">Ingresa con el correo y la contraseña de tu cuenta de agricultor.</p>

        <form className="form" onSubmit={handleSubmit}>
          <label>
            Correo
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
              autoComplete="email"
              disabled={loading}
            />
          </label>
          <label>
            Contraseña
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
              autoComplete="current-password"
              disabled={loading}
            />
          </label>
          <button type="submit" disabled={loading}>
            {loading ? "Ingresando…" : "Iniciar sesión"}
          </button>
        </form>

        {registeredNotice && !error && (
          <div className="status status-ok"><p>{registeredNotice}</p></div>
        )}
        {error && <div className="status status-error"><p>{error}</p></div>}

        <p className="nav-link">
          <Link to="/register">Crear cuenta</Link>
          {" · "}
          <Link to="/">Volver al inicio</Link>
        </p>
      </section>
    </PublicShell>
  );
}
