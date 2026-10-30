export const RUTA_RIESGO = "/api/v1/riesgo";

export const ADVERTENCIA_EXPERIMENTAL =
  "Este resultado es experimental y se genera con un modelo entrenado con datos sintéticos. No representa un diagnóstico de campo, una alerta oficial ni una evaluación agronómica validada. No debe utilizarse como única base para tomar decisiones agrícolas reales.";

const ETIQUETAS_CATEGORIA = {
  bajo: "Bajo",
  medio: "Medio",
  alto: "Alto",
};

export const FORMULARIO_INICIAL = {
  familia_escenario: "meteorologico",
  cultivo: "",
  region: "",
  etapa_fenologica: "",
  temperatura_c: "",
  precipitacion_mm: "",
  dias_sin_lluvia: "",
  sintoma_observado: "false",
  proporcion_afectada: "",
  condicion_suelo: "adecuado",
};

export function etiquetaCategoria(valor) {
  return ETIQUETAS_CATEGORIA[valor] ?? null;
}

export function construirCuerpoRiesgo(formulario) {
  return {
    familia_escenario: formulario.familia_escenario,
    cultivo: formulario.cultivo.trim(),
    region: formulario.region.trim(),
    etapa_fenologica: formulario.etapa_fenologica.trim(),
    temperatura_c: numeroOpcional(formulario.temperatura_c),
    precipitacion_mm: numeroOpcional(formulario.precipitacion_mm),
    dias_sin_lluvia: Number(formulario.dias_sin_lluvia),
    sintoma_observado: formulario.sintoma_observado === true || formulario.sintoma_observado === "true",
    proporcion_afectada: Number(formulario.proporcion_afectada),
    condicion_suelo: formulario.condicion_suelo,
  };
}

export function validarFormularioRiesgo(formulario) {
  const errores = [];
  if (!formulario.cultivo.trim()) {
    errores.push("Indica el cultivo.");
  }
  if (!formulario.region.trim()) {
    errores.push("Indica la región.");
  }
  if (!formulario.etapa_fenologica.trim()) {
    errores.push("Indica la etapa de desarrollo.");
  }
  if (!enteroEscrito(formulario.dias_sin_lluvia)) {
    errores.push("Indica los días sin lluvia con un número entero. Un campo vacío no se envía como cero.");
  }
  if (!proporcionEscrita(formulario.proporcion_afectada)) {
    errores.push("Indica la proporción afectada entre 0 y 1. Si no hay síntoma, escribe 0.");
  }
  if (!numeroOpcionalValido(formulario.temperatura_c)) {
    errores.push("La temperatura debe ser un número o quedar vacía. Un texto no se envía como cero ni como dato ausente.");
  }
  if (!numeroOpcionalValido(formulario.precipitacion_mm)) {
    errores.push("La precipitación debe ser un número o quedar vacía. Un texto no se envía como cero ni como dato ausente.");
  }
  const sintoma = formulario.sintoma_observado === true || formulario.sintoma_observado === "true";
  if (!sintoma && formulario.proporcion_afectada !== "" && Number(formulario.proporcion_afectada) !== 0) {
    errores.push("Si no hay síntoma observado, la proporción afectada debe ser 0.");
  }
  return errores;
}

export function esRespuestaRiesgoValida(datos) {
  if (!datos || typeof datos !== "object") {
    return false;
  }
  return (
    etiquetaCategoria(datos.categoria_predicha) !== null &&
    typeof datos.identificador_modelo === "string" &&
    datos.identificador_modelo.trim() !== "" &&
    typeof datos.version_reglas === "string" &&
    datos.version_reglas.trim() !== "" &&
    datos.naturaleza === "prototipo_academico_sintetico" &&
    datos.es_riesgo_agricola_validado === false
  );
}

export function mensajeErrorRiesgo(error) {
  if (!error?.response) {
    return "No se pudo comunicar con el servidor. Comprueba que el backend esté en ejecución. No se muestra una categoría.";
  }
  const status = error.response.status;
  const detail = error.response.data?.detail;
  if (status === 401) {
    return "La sesión no es válida o venció. Vuelve a iniciar sesión. No se muestra una categoría.";
  }
  if (status === 422 || status === 400) {
    const base =
      typeof detail === "string"
        ? detail
        : "Revisa el escenario. Hay un dato con formato no admitido. La temperatura y la precipitación vacías no se reemplazan por cero.";
    return `${base} No se muestra una categoría.`;
  }
  if (status === 503) {
    return typeof detail === "string"
      ? `${detail} No se muestra una categoría.`
      : "El modelo de riesgo no está disponible. No se muestra una categoría.";
  }
  return "No se pudo obtener la predicción. No se muestra una categoría.";
}

export function textoValorEnviado(valor) {
  if (valor === null || valor === undefined || valor === "") {
    return "No indicada";
  }
  if (valor === true) {
    return "Sí";
  }
  if (valor === false) {
    return "No";
  }
  return String(valor);
}

function numeroOpcional(valor) {
  if (valor === "" || valor === null || valor === undefined) {
    return null;
  }
  return Number(valor);
}

function numeroOpcionalValido(valor) {
  if (valor === "" || valor === null || valor === undefined) {
    return true;
  }
  return Number.isFinite(Number(valor));
}

function enteroEscrito(valor) {
  if (typeof valor === "number") {
    return Number.isInteger(valor);
  }
  if (typeof valor !== "string" || !valor.trim()) {
    return false;
  }
  return /^-?\d+$/.test(valor.trim());
}

function proporcionEscrita(valor) {
  if (valor === "" || valor === null || valor === undefined) {
    return false;
  }
  const numero = Number(valor);
  return Number.isFinite(numero) && numero >= 0 && numero <= 1;
}
