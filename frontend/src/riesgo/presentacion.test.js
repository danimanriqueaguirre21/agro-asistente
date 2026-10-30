import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import {
  ADVERTENCIA_EXPERIMENTAL,
  RUTA_RIESGO,
  construirCuerpoRiesgo,
  esRespuestaRiesgoValida,
  etiquetaCategoria,
  mensajeErrorRiesgo,
  validarFormularioRiesgo,
} from "./presentacion.js";

const formularioCompleto = {
  familia_escenario: "plaga_enfermedad",
  cultivo: " papa ",
  region: "Huancayo",
  etapa_fenologica: "floracion",
  temperatura_c: "",
  precipitacion_mm: "",
  dias_sin_lluvia: "3",
  sintoma_observado: "true",
  proporcion_afectada: "0.4",
  condicion_suelo: "adecuado",
};

test("el formulario admite el escenario y no convierte vacíos en cero", () => {
  assert.deepEqual(validarFormularioRiesgo(formularioCompleto), []);
  const cuerpo = construirCuerpoRiesgo(formularioCompleto);
  assert.equal(cuerpo.cultivo, "papa");
  assert.equal(cuerpo.temperatura_c, null);
  assert.equal(cuerpo.precipitacion_mm, null);
  assert.equal(cuerpo.dias_sin_lluvia, 3);
  assert.equal(cuerpo.sintoma_observado, true);
  assert.equal(cuerpo.proporcion_afectada, 0.4);
  assert.equal(cuerpo.familia_escenario, "plaga_enfermedad");
});

test("un campo obligatorio vacío no se envía como cero", () => {
  const errores = validarFormularioRiesgo({
    ...formularioCompleto,
    dias_sin_lluvia: "",
    proporcion_afectada: "",
  });
  assert.ok(errores.some((texto) => texto.includes("no se envía como cero")));
  assert.ok(errores.some((texto) => texto.includes("proporción")));
});

test("un texto en temperatura no se convierte en dato ausente", () => {
  const errores = validarFormularioRiesgo({
    ...formularioCompleto,
    temperatura_c: "frío",
    precipitacion_mm: "mucha",
  });
  assert.ok(errores.some((texto) => texto.includes("temperatura")));
  assert.ok(errores.some((texto) => texto.includes("precipitación")));
});

test("sin síntoma, una proporción distinta de cero se rechaza", () => {
  const errores = validarFormularioRiesgo({
    ...formularioCompleto,
    sintoma_observado: "false",
    proporcion_afectada: "0.2",
  });
  assert.equal(errores.length, 1);
});

test("la respuesta válida muestra la categoría y los metadatos del contrato", () => {
  const datos = {
    categoria_predicha: "medio",
    identificador_modelo: "bosque_aleatorio_profundidad12_hoja1",
    version_reglas: "sintetica-hu08-v1",
    naturaleza: "prototipo_academico_sintetico",
    es_riesgo_agricola_validado: false,
  };
  assert.equal(esRespuestaRiesgoValida(datos), true);
  assert.equal(etiquetaCategoria("bajo"), "Bajo");
  assert.equal(etiquetaCategoria("medio"), "Medio");
  assert.equal(etiquetaCategoria("alto"), "Alto");
  assert.equal(etiquetaCategoria("critico"), null);
});

test("una respuesta sin naturaleza experimental no se presenta como predicción", () => {
  assert.equal(
    esRespuestaRiesgoValida({
      categoria_predicha: "alto",
      identificador_modelo: "bosque_aleatorio_profundidad12_hoja1",
      version_reglas: "sintetica-hu08-v1",
      naturaleza: "alerta_oficial",
      es_riesgo_agricola_validado: false,
    }),
    false,
  );
  assert.equal(
    esRespuestaRiesgoValida({
      categoria_predicha: "alto",
      identificador_modelo: "bosque_aleatorio_profundidad12_hoja1",
      version_reglas: "sintetica-hu08-v1",
      naturaleza: "prototipo_academico_sintetico",
      es_riesgo_agricola_validado: true,
    }),
    false,
  );
});

test("los errores del backend no fabrican una categoría", () => {
  assert.match(mensajeErrorRiesgo({ response: { status: 422, data: {} } }), /No se muestra una categoría/);
  assert.match(
    mensajeErrorRiesgo({ response: { status: 422, data: { detail: "dato no admitido" } } }),
    /dato no admitido[\s\S]*No se muestra una categoría/,
  );
  assert.match(mensajeErrorRiesgo({ response: { status: 503, data: { detail: "modelo ausente" } } }), /modelo ausente/);
  assert.match(mensajeErrorRiesgo({ response: { status: 401, data: {} } }), /sesión/i);
  assert.match(mensajeErrorRiesgo({}), /comunicar con el servidor/);
  assert.doesNotMatch(mensajeErrorRiesgo({ response: { status: 503, data: {} } }), /\b(bajo|medio|alto)\b/);
});

test("la advertencia experimental está definida y la sección no entra en la consulta", () => {
  assert.match(ADVERTENCIA_EXPERIMENTAL, /datos sintéticos/);
  assert.match(ADVERTENCIA_EXPERIMENTAL, /No debe utilizarse como única base/);
  const pagina = readFileSync(new URL("../pages/RiskPage.jsx", import.meta.url), "utf8");
  const cliente = readFileSync(new URL("../api/client.js", import.meta.url), "utf8");
  const consulta = readFileSync(new URL("../pages/QueryPage.jsx", import.meta.url), "utf8");
  assert.match(pagina, /ADVERTENCIA_EXPERIMENTAL/);
  assert.match(pagina, /predictAgriculturalRisk/);
  assert.doesNotMatch(pagina, /submitAgriculturalQuery/);
  assert.match(cliente, new RegExp(`api\\.post\\("${RUTA_RIESGO}"`));
  assert.equal(RUTA_RIESGO, "/api/v1/riesgo");
  assert.doesNotMatch(consulta, /predictAgriculturalRisk|\/api\/v1\/riesgo/);
});
