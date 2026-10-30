import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerFarmer } from "../api/client";
import PublicShell from "../components/PublicShell.jsx";

export default function RegisterPage() {
  const [names, setNames] = useState("");
  const [lastNames, setLastNames] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const redirectTimerRef = useRef(null);

  useEffect(() => {
    return () => {
      if (redirectTimerRef.current) {
        window.clearTimeout(redirectTimerRef.current);
      }
    };
  }, []);

  function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setSuccess("");
    setError("");

    registerFarmer({
      names,
      last_names: lastNames,
      email,
      password,
    })
      .then((response) => {
        setSuccess(`Registro exitoso. Cuenta creada para ${response.data.email}. Redirigiendo al inicio de sesión…`);
        setNames("");
        setLastNames("");
        setEmail("");
        setPassword("");
        redirectTimerRef.current = window.setTimeout(() => {
          navigate("/login", { replace: true, state: { registered: true } });
        }, 1200);
      })
      .catch((err) => {
        const status = err.response?.status;
        const detail = err.response?.data?.detail;
        if (status === 409) {
          setError(typeof detail === "string" ? detail : "El correo electrónico ya está registrado");
        } else if (status === 400 || status === 422) {
          setError("Revisa los datos del formulario. Nombres, apellidos, correo válido y contraseña de al menos 8 caracteres.");
        } else {
          setError("No se pudo completar el registro. Inténtalo de nuevo.");
        }
      })
      .finally(() => setLoading(false));
  }

  return (
    <PublicShell>
      <section className="card">
        <h1>Crear cuenta</h1>
        <p className="lead">Crea una cuenta con tus datos básicos.</p>

        <form className="form" onSubmit={handleSubmit}>
          <label>
            Nombres
            <input
              value={names}
              onChange={(event) => setNames(event.target.value)}
              required
              autoComplete="given-name"
            />
          </label>
          <label>
            Apellidos
            <input
              value={lastNames}
              onChange={(event) => setLastNames(event.target.value)}
              required
              autoComplete="family-name"
            />
          </label>
          <label>
            Correo
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
              autoComplete="email"
            />
          </label>
          <label>
            Contraseña
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
              minLength={8}
              autoComplete="new-password"
            />
          </label>
          <button type="submit" disabled={loading || Boolean(success)}>
            {loading ? "Registrando…" : "Registrarme"}
          </button>
        </form>

        {success && <div className="status status-ok"><p>{success}</p></div>}
        {error && <div className="status status-error"><p>{error}</p></div>}

        <p className="nav-link">
          <Link to="/login">Iniciar sesión</Link>
          {" · "}
          <Link to="/">Volver al inicio</Link>
        </p>
      </section>
    </PublicShell>
  );
}
