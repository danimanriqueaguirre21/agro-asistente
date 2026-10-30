import { Fragment, useState } from "react";
import { predictAgriculturalRisk } from "../api/client";
import AuthFooter from "../components/AuthFooter.jsx";
import AuthenticatedShell from "../components/AuthenticatedShell.jsx";
import {
  ADVERTENCIA_EXPERIMENTAL,
  FORMULARIO_INICIAL,
  construirCuerpoRiesgo,
  esRespuestaRiesgoValida,
  etiquetaCategoria,
  mensajeErrorRiesgo,
  textoValorEnviado,
  validarFormularioRiesgo,
} from "../riesgo/presentacion.js";

const FAMILIAS = [
  ["meteorologico", "Meteorológico"],
  ["plaga_enfermedad", "Plagas y enfermedades"],
  ["suelo_agua_manejo", "Suelo, agua y manejo"],
];

const SUELOS = [
  ["adecuado", "Adecuado"],
  ["seco", "Seco"],
  ["encharcado", "Encharcado"],
];

const CAMPOS_ESCENARIO = [
  ["familia_escenario", "Familia del escenario"],
  ["cultivo", "Cultivo"],
  ["region", "Región"],
  ["etapa_fenologica", "Etapa"],
  ["temperatura_c", "Temperatura"],
  ["precipitacion_mm", "Precipitación"],
  ["dias_sin_lluvia", "Días sin lluvia"],
  ["sintoma_observado", "Síntoma observado"],
  ["proporcion_afectada", "Proporción afectada"],
  ["condicion_suelo", "Condición del suelo"],
];

export default function RiskPage() {
  const [formulario, setFormulario] = useState(FORMULARIO_INICIAL);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");
  const [resultado, setResultado] = useState(null);
  const [escenarioEnviado, setEscenarioEnviado] = useState(null);

  function actualizar(evento) {
    const { name, value } = evento.target;
    setFormulario((actual) => ({ ...actual, [name]: value }));
  }

  function enviar(evento) {
    evento.preventDefault();
    if (cargando) {
      return;
    }
    const errores = validarFormularioRiesgo(formulario);
    setResultado(null);
    setEscenarioEnviado(null);
    if (errores.length > 0) {
      setError(errores.join(" "));
      return;
    }
    const cuerpo = construirCuerpoRiesgo(formulario);
    setCargando(true);
    setError("");
    predictAgriculturalRisk(cuerpo)
      .then((respuesta) => {
        if (!esRespuestaRiesgoValida(respuesta.data)) {
          setError("La respuesta no tiene el formato del prototipo. No se muestra una categoría.");
          return;
        }
        setResultado(respuesta.data);
        setEscenarioEnviado(cuerpo);
      })
      .catch((err) => {
        setError(mensajeErrorRiesgo(err));
      })
      .finally(() => setCargando(false));
  }

  const categoriaVisible = resultado ? etiquetaCategoria(resultado.categoria_predicha) : null;

  return (
    <AuthenticatedShell>
      <section className="card card-wide">
        <p className="eyebrow">HU-08 · Prototipo académico</p>
        <h1>Predicción experimental de riesgo</h1>
        <p className="lead">
          Esta sección es independiente de la consulta agrícola. El modelo clasifica un
          escenario de prueba en bajo, medio o alto según reglas de simulación.
        </p>

        <aside className="notice-experimental" role="note">
          <p>{ADVERTENCIA_EXPERIMENTAL}</p>
        </aside>

        <form className="form" onSubmit={enviar}>
          <label>
            Familia del escenario
            <select
              name="familia_escenario"
              value={formulario.familia_escenario}
              onChange={actualizar}
              disabled={cargando}
            >
              {FAMILIAS.map(([valor, texto]) => (
                <option key={valor} value={valor}>
                  {texto}
                </option>
              ))}
            </select>
          </label>
          <label>
            Cultivo
            <input
              name="cultivo"
              value={formulario.cultivo}
              onChange={actualizar}
              disabled={cargando}
              autoComplete="off"
            />
          </label>
          <label>
            Región
            <input
              name="region"
              value={formulario.region}
              onChange={actualizar}
              disabled={cargando}
              autoComplete="off"
            />
          </label>
          <label>
            Etapa de desarrollo
            <input
              name="etapa_fenologica"
              value={formulario.etapa_fenologica}
              onChange={actualizar}
              disabled={cargando}
              placeholder="Por ejemplo: floracion"
              autoComplete="off"
            />
          </label>
          <label>
            Temperatura del aire
            <input
              name="temperatura_c"
              value={formulario.temperatura_c}
              onChange={actualizar}
              disabled={cargando}
              inputMode="decimal"
              placeholder="Vacío si no hay dato"
            />
          </label>
          <label>
            Precipitación
            <input
              name="precipitacion_mm"
              value={formulario.precipitacion_mm}
              onChange={actualizar}
              disabled={cargando}
              inputMode="decimal"
              placeholder="Vacío si no hay dato"
            />
          </label>
          <label>
            Días sin lluvia
            <input
              name="dias_sin_lluvia"
              value={formulario.dias_sin_lluvia}
              onChange={actualizar}
              disabled={cargando}
              inputMode="numeric"
            />
          </label>
          <label>
            Síntoma observado
            <select
              name="sintoma_observado"
              value={formulario.sintoma_observado}
              onChange={actualizar}
              disabled={cargando}
            >
              <option value="false">No</option>
              <option value="true">Sí</option>
            </select>
          </label>
          <label>
            Proporción afectada (0 a 1)
            <input
              name="proporcion_afectada"
              value={formulario.proporcion_afectada}
              onChange={actualizar}
              disabled={cargando}
              inputMode="decimal"
              placeholder="0 si no hay síntoma"
            />
          </label>
          <label>
            Condición del suelo
            <select
              name="condicion_suelo"
              value={formulario.condicion_suelo}
              onChange={actualizar}
              disabled={cargando}
            >
              {SUELOS.map(([valor, texto]) => (
                <option key={valor} value={valor}>
                  {texto}
                </option>
              ))}
            </select>
          </label>
          <button type="submit" disabled={cargando}>
            {cargando ? "Consultando el prototipo…" : "Estimar categoría experimental"}
          </button>
        </form>

        {!cargando && !resultado && !error && (
          <p className="lead">Aún no hay una predicción. Completa el escenario de prueba y envíalo.</p>
        )}
        {cargando && <p className="lead">Consultando el prototipo. Todavía no hay una categoría.</p>}
        {error && (
          <div className="status status-error" role="alert">
            <p>{error}</p>
          </div>
        )}

        {resultado && categoriaVisible && (
          <section className="answer-panel" aria-live="polite">
            <h2>Categoría predicha: {categoriaVisible}</h2>
            <p className="lead">
              El valor devuelto por el prototipo es {resultado.categoria_predicha}. No es un
              diagnóstico ni una alerta oficial.
            </p>
            <aside className="notice-experimental" role="note">
              <p>{ADVERTENCIA_EXPERIMENTAL}</p>
            </aside>
            <dl>
              <dt>Modelo</dt>
              <dd>{resultado.identificador_modelo}</dd>
              <dt>Reglas de simulación</dt>
              <dd>{resultado.version_reglas}</dd>
              <dt>Naturaleza</dt>
              <dd>{resultado.naturaleza}</dd>
              <dt>Riesgo agrícola validado</dt>
              <dd>{resultado.es_riesgo_agricola_validado ? "Sí" : "No"}</dd>
            </dl>
            {escenarioEnviado && (
              <>
                <h2>Escenario enviado</h2>
                <dl>
                  {CAMPOS_ESCENARIO.map(([campo, titulo]) => (
                    <Fragment key={campo}>
                      <dt>{titulo}</dt>
                      <dd>{textoValorEnviado(escenarioEnviado[campo])}</dd>
                    </Fragment>
                  ))}
                </dl>
              </>
            )}
          </section>
        )}

        <AuthFooter />
      </section>
    </AuthenticatedShell>
  );
}
