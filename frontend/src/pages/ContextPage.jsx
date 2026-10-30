import { useEffect, useState } from "react";
import { createAgriculturalContext, listContexts, selectContext } from "../api/client";
import AuthFooter from "../components/AuthFooter.jsx";
import AuthenticatedShell from "../components/AuthenticatedShell.jsx";

const emptyForm = {
  plot_name: "",
  crop: "",
  region: "",
  notes: "",
};

export default function ContextPage() {
  const [contexts, setContexts] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  function loadContexts() {
    setLoading(true);
    setError("");
    listContexts()
      .then((response) => {
        setContexts(response.data);
      })
      .catch((err) => {
        if (err.response?.status !== 401) {
          setError("No se pudieron cargar los contextos.");
        }
      })
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    loadContexts();
  }, []);

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  function handleCreate(event) {
    event.preventDefault();
    setSaving(true);
    setSuccess("");
    setError("");
    createAgriculturalContext({
      plot_name: form.plot_name || null,
      crop: form.crop,
      region: form.region,
      notes: form.notes || null,
    })
      .then(() => {
        setSuccess("Contexto agrícola creado.");
        setForm(emptyForm);
        loadContexts();
      })
      .catch((err) => {
        if (err.response?.status === 401) {
          return;
        }
        if (err.response?.status === 400 || err.response?.status === 422) {
          setError("Revisa cultivo y región. El predio y las notas son opcionales.");
        } else {
          setError("No se pudo crear el contexto.");
        }
      })
      .finally(() => setSaving(false));
  }

  function handleSelect(contextId) {
    setSaving(true);
    setSuccess("");
    setError("");
    selectContext(contextId)
      .then(() => {
        setSuccess("Contexto seleccionado.");
        loadContexts();
      })
      .catch((err) => {
        if (err.response?.status === 401) {
          return;
        }
        if (err.response?.status === 404) {
          setError("Ese contexto no está disponible.");
        } else {
          setError("No se pudo seleccionar el contexto.");
        }
      })
      .finally(() => setSaving(false));
  }

  return (
    <AuthenticatedShell>
      <section className="card card-wide">
        <p className="eyebrow">HU-03</p>
        <h1>Contexto agrícola</h1>
        <p className="lead">
          Registra el cultivo y la región de tu predio. El contexto seleccionado se usará después en las consultas.
        </p>

        <form className="form" onSubmit={handleCreate}>
          <label>
            Nombre del predio
            <input name="plot_name" value={form.plot_name} onChange={handleChange} />
          </label>
          <label>
            Cultivo
            <input name="crop" value={form.crop} onChange={handleChange} required />
          </label>
          <label>
            Región
            <input name="region" value={form.region} onChange={handleChange} required />
          </label>
          <label>
            Notas
            <input name="notes" value={form.notes} onChange={handleChange} />
          </label>
          <button type="submit" disabled={saving}>
            {saving ? "Guardando…" : "Crear contexto"}
          </button>
        </form>

        {loading && <p>Cargando contextos…</p>}
        {success && <div className="status status-ok"><p>{success}</p></div>}
        {error && <div className="status status-error"><p>{error}</p></div>}

        <ul className="context-list">
          {contexts.map((item) => (
            <li key={item.id} className={item.is_selected ? "selected" : ""}>
              {item.is_selected && <span className="selected-badge">Seleccionado</span>}
              <div>
                <strong>{item.crop}</strong> · {item.region}
                {item.plot_name ? ` · ${item.plot_name}` : ""}
              </div>
              {item.notes && <p>{item.notes}</p>}
              <button type="button" disabled={saving || item.is_selected} onClick={() => handleSelect(item.id)}>
                {item.is_selected ? "En uso" : "Seleccionar"}
              </button>
            </li>
          ))}
        </ul>
        {!loading && contexts.length === 0 && <p>Aún no hay contextos registrados.</p>}

        <AuthFooter />
      </section>
    </AuthenticatedShell>
  );
}
