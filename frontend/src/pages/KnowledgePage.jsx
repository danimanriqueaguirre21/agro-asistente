import { useEffect, useState } from "react";
import { ingestKnowledge, listKnowledgeDocuments } from "../api/client";
import AuthFooter from "../components/AuthFooter.jsx";
import AuthenticatedShell from "../components/AuthenticatedShell.jsx";

const emptyForm = {
  title: "",
  topic: "",
  content: "",
};

export default function KnowledgePage() {
  const [documents, setDocuments] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  function loadDocuments() {
    setLoading(true);
    listKnowledgeDocuments()
      .then((response) => {
        setDocuments(response.data);
      })
      .catch((err) => {
        if (err.response?.status !== 401) {
          setError("No se pudieron cargar los documentos.");
        }
      })
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    loadDocuments();
  }, []);

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  function handleIngest(event) {
    event.preventDefault();
    setSaving(true);
    setSuccess("");
    setError("");
    ingestKnowledge(form)
      .then((response) => {
        setSuccess(`Documento registrado: ${response.data.title}`);
        setForm(emptyForm);
        loadDocuments();
      })
      .catch((err) => {
        const status = err.response?.status;
        const detail = err.response?.data?.detail;
        if (status === 401) {
          return;
        }
        if (status === 409) {
          setError(typeof detail === "string" ? detail : "Ese documento ya está registrado.");
        } else if (status === 400 || status === 422) {
          setError("Revisa título, tema y contenido. No pueden estar vacíos.");
        } else {
          setError("No se pudo incorporar el documento.");
        }
      })
      .finally(() => setSaving(false));
  }

  return (
    <AuthenticatedShell>
      <section className="card card-wide">
        <p className="eyebrow">HU-05</p>
        <h1>Base de conocimiento</h1>
        <p className="lead">
          Incorpora documentos agrícolas de prueba. Se guarda el contenido y un hash para evitar duplicados.
          Todavía no hay búsqueda semántica ni RAG.
        </p>

        <form className="form" onSubmit={handleIngest}>
          <label>
            Título
            <input name="title" value={form.title} onChange={handleChange} required maxLength={200} />
          </label>
          <label>
            Tema
            <input name="topic" value={form.topic} onChange={handleChange} required maxLength={50} />
          </label>
          <label>
            Contenido (Markdown)
            <textarea
              name="content"
              value={form.content}
              onChange={handleChange}
              required
              maxLength={20000}
              placeholder="# Material de prueba HU-05"
            />
          </label>
          <button type="submit" disabled={saving}>
            {saving ? "Incorporando…" : "Incorporar documento"}
          </button>
        </form>

        {loading && <p>Cargando documentos…</p>}
        {success && <div className="status status-ok"><p>{success}</p></div>}
        {error && <div className="status status-error"><p>{error}</p></div>}

        <ul className="document-list">
          {documents.map((item) => (
            <li key={item.id}>
              <div>
                <strong>{item.title}</strong> · {item.topic}
              </div>
              <p className="document-meta">{item.source_path}</p>
              <p className="document-meta">Hash: {item.content_hash.slice(0, 12)}… · {item.ingested_at}</p>
            </li>
          ))}
        </ul>
        {!loading && documents.length === 0 && <p>Aún no hay documentos registrados.</p>}

        <AuthFooter />
      </section>
    </AuthenticatedShell>
  );
}
