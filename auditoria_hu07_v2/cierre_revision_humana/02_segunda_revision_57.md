# Segunda revisión de las 57 consultas

Fecha: 18 de octubre de 2026.

## Limitación

No se realizó una segunda revisión humana independiente.

El informe `auditoria_hu07_v2/INFORME_AUDITORIA_PILOTO_HU07.md` lo escribió este mismo agente, en esta misma herramienta. Volver a leer las 57 aquí y poner una categoría sería una segunda pasada del mismo revisor, no otra persona. El encargo prohíbe presentar esa pasada como segundo revisor y prohíbe copiar la etiqueta inicial como si el segundo revisor la hubiera propuesto.

Por eso, en las 57 fichas:

- la categoría propuesta por el segundo revisor no se emite;
- el resultado es pendiente;
- la justificación del primer revisor se copia solo como antecedente;
- no hay acuerdo ni desacuerdo, porque el segundo dictamen no existe;
- todas requieren revisor humano.

Son 48 consultas con `review_note` en el piloto y las nueve que el informe de auditoría añadió sin nota. Los tres casos dudosos no están en estas 57; van en `01_tres_casos_dudosos.md`.

No se entrenó ningún modelo. No se crearon particiones.

## Fichas

### 1. `piloto-v2-0ae231115b`

- **Texto original:** Las hojas de abajo de la papa se ponen amarillas y la planta no crece. ¿Le falta comida o espero a ver si reacciona sola?
- **Categoría inicial:** `fertilizacion_nutricion`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `fertilizacion_nutricion`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Pregunta si a la papa le falta comida. La nota separa bien esa decisión de una identificación de enfermedad o de un insecto. El amarilleo, por sí solo, no cambia la etiqueta.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión pedida es si falta alimento. No pide el nombre de una enfermedad ni habla de un insecto.
- **Cultivo original:** papa

### 2. `piloto-v2-464c8602df`

- **Texto original:** ¿Qué es el polvo blanco del envés de la papa?
- **Categoría inicial:** `enfermedades_cultivos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `enfermedades_cultivos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Pide identificar el polvo blanco del envés de la papa y no describe un animal. La nota se sostiene. No es la misma pregunta que piloto-v2-99b5624803, que queda dudosa.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es identificar el polvo de la hoja. No describe un insecto.
- **Cultivo original:** papa

### 3. `piloto-v2-ff4bc93ac0`

- **Texto original:** ¿Las piedras grandes se sacan de la melga o se pueden dejar a un lado si el hoyo de siembra cae entre ellas?
- **Categoría inicial:** `suelos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `suelos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Pregunta qué hacer con las piedras grandes. El hoyo de siembra es el uso previsto, como dice la nota, no la decisión.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es qué hacer con las piedras. El hoyo se menciona solo como el uso previsto del terreno.

### 4. `piloto-v2-0e420f3289`

- **Texto original:** El tallo del kion se está doblando y la hoja amarillea. ¿Eso avisa que el rizoma ya está para sacarlo?
- **Categoría inicial:** `cosecha_poscosecha`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `cosecha_poscosecha`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Pregunta si el tallo doblado y la hoja amarilla avisan que el rizoma de kion ya está para sacarlo. La nota se sostiene. Esta auditoría no confirma que ese síntoma sea señal de madurez.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** Pregunta si el rizoma ya está para sacarlo. No pide identificar una enfermedad de la hoja.
- **Cultivo original:** kion

### 5. `piloto-v2-6cb18529e8`

- **Texto original:** El café después del recojo queda flaco. ¿Le alcanza con la pulpa descompuesta o hace falta otra fuente de comida?
- **Categoría inicial:** `fertilizacion_nutricion`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `fertilizacion_nutricion`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Después del recojo del café pregunta si alcanza la pulpa descompuesta u otra fuente de comida. La nota separa bien esa decisión del secado y de la guarda.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es la fuente de alimento después del recojo. No pide cómo secar ni cómo guardar el grano.
- **Cultivo original:** café

### 6. `piloto-v2-4d8651680b`

- **Texto original:** En Yauli anuncian frío de varios grados bajo cero y la papa está en brote. ¿Muevo el turno de agua de mañana para esta noche, solo por ese frío, o el agua no sirve en este caso?
- **Categoría inicial:** `clima_heladas`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `clima_heladas`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: En Yauli el agua se menciona solo para el frío anunciado sobre la papa en brote. La nota aplica el criterio de la taxonomía: riego cuyo único fin es atenuar el frío es clima_heladas.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** El agua se menciona solo como posible protección ante el frío anunciado. No pide el calendario normal de riego.
- **Cultivo original:** papa
- **Región original:** Yauli

### 7. `piloto-v2-3f8c9f09bd`

- **Texto original:** La yuca de Satipo amarillea solo en el bajo, donde el barro no seca ni en tres días de sol. ¿El arreglo es sacar esa agua con una zanja hacia la quebrada?
- **Categoría inicial:** `suelos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `suelos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: La yuca amarillea solo en el bajo que no seca y pregunta si el arreglo es una zanja hacia la quebrada. La nota se sostiene: la decisión es sacar el agua estancada.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es sacar el agua estancada del bajo. No pide un turno de riego ni el nombre de una enfermedad.
- **Cultivo original:** yuca
- **Región original:** Satipo

### 8. `piloto-v2-1d4ef1a7bd`

- **Texto original:** En la parte alta de Junín el viento de agosto tumba las plantas y seca la hoja en un solo día. ¿Ese viento se amortigua con cortinas vivas o espero a que pase la semana y miro qué quedó en pie?
- **Categoría inicial:** `clima_heladas`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** señalada por la auditoría, sin nota en el piloto
- **Etiqueta original:** `clima_heladas`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: En la parte alta de Junín el viento tumba plantas y seca la hoja, y pregunta si amortiguarlo con cortinas vivas o esperar. La decisión es la protección ante ese viento, así que clima_heladas se sostiene. La cortina viva roza siembra y manejo, y esa frontera no tiene nota. Region Junín es válida porque no hay provincia.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación:** el piloto no trae `review_note`. El primer revisor pidió segunda lectura por una frontera o por poca claridad. Esa petición no se convierte en acuerdo.
- **Región original:** Junín

### 9. `piloto-v2-18d29e2be0`

- **Texto original:** La quinua de la parte alta de Junín tiene el surco de arriba empapado y el de abajo polvoriento. El agua entra de más por la cabecera. Quiero que las plantas de abajo también reciban, sin ahogar las de arriba, mientras siga esta semana sin lluvia. ¿Cómo reparto esa agua en el surco?
- **Categoría inicial:** `riego`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `riego`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Pide cómo repartir el agua del surco de quinua para que abajo reciba sin ahogar arriba, en una semana sin lluvia. La nota se sostiene: no pide proteger el cultivo ante una sequía como evento. Region Junín coincide con «parte alta de Junín».
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es repartir el agua en el surco. No pide proteger el cultivo ante una sequía como evento climático.
- **Cultivo original:** quinua
- **Región original:** Junín

### 10. `piloto-v2-a3e3d16ab5`

- **Texto original:** En Concepción las habas del año pasado quedaron muy tupidas, se tumbaron con el viento y casi no se pudo entrar al surco a cosecharlas. Este año no quiero repetir ese trazo. Puedo abrir más la distancia entre surcos o dejar el mismo ancho y poner menos semillas en cada golpe. ¿Cuál de las dos formas evita que se vuelvan a tumbar?
- **Categoría inicial:** `siembra_manejo_cultivo`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `siembra_manejo_cultivo`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: En Concepción pregunta si abrir los surcos de haba o poner menos semilla por golpe. La nota se sostiene: el viento del año pasado es antecedente, no un evento a proteger ahora.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es la distancia y la cantidad de semilla. El viento del año pasado se menciona como antecedente, no como un evento que haya que proteger ahora.
- **Cultivo original:** haba
- **Región original:** Concepción

### 11. `piloto-v2-59a61015e2`

- **Texto original:** La sequía ya va tres semanas y el maíz amiláceo enrolla la hoja desde el mediodía. El aviso dice que la seca sigue. ¿Hay algo que hacer por este evento, aparte de mirar el cielo?
- **Categoría inicial:** `clima_heladas`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `clima_heladas`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: La sequía de tres semanas y el aviso de que sigue se consultan como evento. La nota se sostiene. No pide un calendario de riego. Comparte escenario con piloto-v2-e57aab2fbf, pero la decisión es otra: si hay algo que hacer por el evento.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La sequía se consulta como evento climático anunciado. No pide un calendario de riego ni una obra en el terreno.
- **Cultivo original:** maíz amiláceo

### 12. `piloto-v2-60e345941d`

- **Texto original:** En Huancayo la ladera se está llevando la capa de arriba cuando llueve fuerte: se ven canalitos y la raíz queda al aire. ¿Eso se frena con terrazas o con barreras de pasto en el bordo?
- **Categoría inicial:** `suelos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `suelos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: En Huancayo pregunta si frenar la erosión con terrazas o con barreras de pasto. La nota se sostiene: la lluvia es la causa del arrastre, no un evento del que haya que proteger la planta esta noche.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es frenar la erosión. La lluvia se menciona como la causa del arrastre, no como un evento del que haya que proteger la planta esta noche.
- **Región original:** Huancayo

### 13. `piloto-v2-9c434b0971`

- **Texto original:** ¿La plaga que perfora el fruto del cacao se baja recogiendo las mazorcas picadas?
- **Categoría inicial:** `plagas`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** señalada por la auditoría, sin nota en el piloto
- **Etiqueta original:** `plagas`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Pregunta si la plaga que perfora el cacao baja al recoger las mazorcas picadas. El fin declarado es la plaga, así que la etiqueta se sostiene. Recoger mazorcas roza cosecha y esa frontera no tiene nota.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación:** el piloto no trae `review_note`. El primer revisor pidió segunda lectura por una frontera o por poca claridad. Esa petición no se convierte en acuerdo.
- **Cultivo original:** cacao

### 14. `piloto-v2-2e641787b4`

- **Texto original:** ¿La poda del café se hace apenas termina el recojo o cuando la planta vuelve a brotar?
- **Categoría inicial:** `siembra_manejo_cultivo`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `siembra_manejo_cultivo`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Pregunta si podar el café al terminar el recojo o cuando vuelve a brotar. La nota se sostiene. Comparte el molde «la poda de X se hace A o B» con la palta, pero los momentos y el cultivo son otros; no es paráfrasis.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es el momento de la poda. No pide cómo secar el grano ni qué alimento echar.
- **Cultivo original:** café

### 15. `piloto-v2-09602c7344`

- **Texto original:** ¿El análisis de suelo me dice si esta tierra es ácida?
- **Categoría inicial:** `suelos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `suelos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Pregunta si el análisis de suelo dice si la tierra es ácida. La nota se sostiene: no pide dosis de abono.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La pregunta es si la tierra es ácida. No pide una dosis de abono.

### 16. `piloto-v2-09973b49b9`

- **Texto original:** La piña muestra la base del fruto blanda y con olor agrio, sin mordedura. ¿La corto para que no pase a las otras?
- **Categoría inicial:** `enfermedades_cultivos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `enfermedades_cultivos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: La base de la piña está blanda y con olor agrio, sin mordedura, y pregunta si cortarla para que no pase a las otras. La nota se sostiene. No es el punto de corte de piloto-v2-3a3ecfb9c3.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** No hay mordedura. La decisión es la pudrición del fruto en la planta, no el punto de corte para la venta.
- **Cultivo original:** piña

### 17. `piloto-v2-7f4b6435a7`

- **Texto original:** Ayer abrí la acequia un buen rato y hoy el piso sigue brilloso. Las plantas amanecieron decaídas, como si hubieran tenido el pie en agua toda la noche. No estoy pidiendo una zanja nueva. ¿La próxima vez cierro antes, o el daño vino de dejar correr el agua demasiado tiempo?
- **Categoría inicial:** `riego`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `riego`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: El exceso vino de dejar correr la acequia y pregunta si la próxima vez cerrar antes. La nota se sostiene: no pide una zanja nueva. Encaja en la inclusión de riego sobre encharcamiento causado por el riego.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** El exceso de agua lo causó la acequia que abrí. La decisión es cuánto tiempo dejar el agua, no una obra de drenaje.

### 18. `piloto-v2-597103e2ad`

- **Texto original:** La zanahoria sale chica y la hoja se ve lavada, sin manchas ni mordeduras. ¿Qué le puedo dar para que engrose?
- **Categoría inicial:** `fertilizacion_nutricion`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `fertilizacion_nutricion`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Zanahoria chica y hoja lavada, sin manchas ni mordeduras: qué darle para que engrose. La nota se sostiene.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** Se descartan manchas y mordeduras. La decisión es qué alimento dar para que la raíz engrose.
- **Cultivo original:** zanahoria

### 19. `piloto-v2-44037fd77a`

- **Texto original:** En Jauja la quinua está en panoja y anuncian lluvia fuerte con viento para esta noche. ¿Amarro las panojas antes de que llegue o las dejo y solo miro que el agua no se represé en el surco?
- **Categoría inicial:** `clima_heladas`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `clima_heladas`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: En Jauja anuncian lluvia fuerte con viento y pregunta si amarrar las panojas de quinua. La nota se sostiene. Mirar que el agua no se represé es vigilancia de ese evento, no una obra de drenaje.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** El evento es la lluvia con viento anunciada. No pide construir un drenaje del terreno.
- **Cultivo original:** quinua
- **Región original:** Jauja

### 20. `piloto-v2-f4aca3376f`

- **Texto original:** El maíz amiláceo tiene la mazorca con granos rayados y la planta queda achaparrada. No veo gusano. ¿Puede ser un mal de la planta?
- **Categoría inicial:** `enfermedades_cultivos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `enfermedades_cultivos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Mazorca con granos rayados y planta achaparrada, sin gusano: si puede ser un mal de la planta. La nota se sostiene.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** No hay gusano. La decisión es si se trata de un mal de la planta.
- **Cultivo original:** maíz amiláceo

### 21. `piloto-v2-5eb777e476`

- **Texto original:** ¿La tierra colorada y pegajosa se encostra apenas pierde humedad, y así no le sirve al olluco?
- **Categoría inicial:** `suelos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `suelos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Pregunta si la tierra colorada y pegajosa se encostra al perder humedad y si así no le sirve al olluco. La nota se sostiene: el objeto es el suelo, no la fecha de siembra.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La pregunta es si esa tierra se encostra. No pide la fecha de siembra del olluco.
- **Cultivo original:** olluco

### 22. `piloto-v2-df7f31f7d9`

- **Texto original:** El frijol está en flor y quiero que cuaje. ¿Le echo algo al pie ahora o ya es tarde?
- **Categoría inicial:** `fertilizacion_nutricion`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** señalada por la auditoría, sin nota en el piloto
- **Etiqueta original:** `fertilizacion_nutricion`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: El frijol está en flor, quiere que cuaje y pregunta si echar algo al pie ahora. No pide agua, no nombra un animal y no habla del terreno, así que fertilización sigue teniendo más peso que riego. El texto no dice abono. No se reescribe. Un revisor puede retirarla si no ve esa decisión.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación:** el piloto no trae `review_note`. El primer revisor pidió segunda lectura por una frontera o por poca claridad. Esa petición no se convierte en acuerdo.
- **Cultivo original:** frijol

### 23. `piloto-v2-3458d186c1`

- **Texto original:** La quinua tiene un gusano que corta la plantita al ras, de noche. ¿Qué busco al amanecer junto al tallo cortado?
- **Categoría inicial:** `plagas`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `plagas`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Un gusano corta la quinua al ras y pregunta qué buscar junto al tallo. La nota se sostiene: no pide preparar ni drenar el terreno.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** El corte lo hace un gusano. No pide preparar ni drenar el terreno.
- **Cultivo original:** quinua

### 24. `piloto-v2-2d59493e39`

- **Texto original:** La arveja se me enreda por el piso. ¿Le pongo ramas de tutor o la dejo rastrera?
- **Categoría inicial:** `siembra_manejo_cultivo`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `siembra_manejo_cultivo`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: La arveja se enreda por el piso y pregunta si ponerle tutor. La nota se sostiene.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es el tutor. No pide corregir el terreno.
- **Cultivo original:** arveja

### 25. `piloto-v2-113babe101`

- **Texto original:** Esta noche el termómetro del pueblo marcó bajo cero y al amanecer la hoja está oscura, como cocida, sin polvo ni bicho encima. ¿Ese daño es del frío de anoche, y qué plantas miro primero para ver si rebrotan?
- **Categoría inicial:** `clima_heladas`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `clima_heladas`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Tras una noche bajo cero la hoja está oscura, como cocida, sin polvo ni bicho, y pregunta si el daño es del frío y qué plantas mirar. La nota se sostiene.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** Pide reconocer el daño del frío ya ocurrido. No pide el nombre de una enfermedad.

### 26. `piloto-v2-c0a9c01736`

- **Texto original:** Quiero apartar semilla para la otra campaña, distinta de lo que voy a vender. ¿La escogo el mismo día del recojo o después de que seque bajo techo?
- **Categoría inicial:** `cosecha_poscosecha`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `cosecha_poscosecha`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Apartar semilla el mismo día del recojo o después de secarla bajo techo. La nota se sostiene: es selección y secado de lo recién recogido. No es la semilla ya guardada de piloto-v2-6eab714edd.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es la selección y el secado de lo recién recogido. No pide cómo ni cuándo volver a sembrarlo.

### 27. `piloto-v2-dacf26a183`

- **Texto original:** La yuca de Satipo está en un lomito. Cuando deja de llover, el agua pasa de largo y no se queda junto a la planta. En la época seca dudo si basta con mojar el pie o si tengo que empapar el camellón entero para que la raíz de verdad reciba. ¿Qué hago en una semana sin lluvias?
- **Categoría inicial:** `riego`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `riego`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Yuca de Satipo en un lomito: en una semana sin lluvias, mojar el pie o empapar el camellón. La nota se sostiene. No es la sequía consultada como evento en piloto-v2-59a61015e2.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** Pregunta por cómo mojar la yuca en la época seca. No pide proteger el cultivo ante una sequía anunciada.
- **Cultivo original:** yuca
- **Región original:** Satipo

### 28. `piloto-v2-cae4b79822`

- **Texto original:** En el grano del café hay un hueco redondo y, al abrirlo, sale un polvillo claro. No es un grano suelto: ya encontré varios en el mismo tendal, unos con el hueco fresco y otros vacíos. No quiero botar el lote entero si el daño está solo en una parte. ¿Cómo bajo esa broca sin perder lo que todavía está sano?
- **Categoría inicial:** `plagas`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** señalada por la auditoría, sin nota en el piloto
- **Etiqueta original:** `plagas`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Hueco redondo y polvillo en el grano de café, ya en el tendal, y pregunta cómo bajar esa broca sin perder lo sano. El organismo es una plaga y la etiqueta se sostiene. El lugar es de poscosecha y esa frontera no tiene nota. «Me dijeron» no aparece; el texto nombra la broca. No se atribuye ningún manejo a las fichas de fuentes.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación:** el piloto no trae `review_note`. El primer revisor pidió segunda lectura por una frontera o por poca claridad. Esa petición no se convierte en acuerdo.
- **Cultivo original:** café

### 29. `piloto-v2-9f43588f66`

- **Texto original:** ¿Un suelo arenoso se queda sin reserva de humedad más rápido que uno negro, y eso cambia cómo lo preparo antes de usar la chacra?
- **Categoría inicial:** `suelos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `suelos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Pregunta si un suelo arenoso pierde la reserva de humedad más rápido y si eso cambia la preparación. La nota se sostiene: no pide el calendario de riego.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es la preparación según la textura. No pide un calendario de riego.

### 30. `piloto-v2-d733f0b0d1`

- **Texto original:** El frijol seco se está manchando en la era porque todavía llueve sobre las plantas ya arrancadas. ¿Lo termino de secar bajo techo?
- **Categoría inicial:** `cosecha_poscosecha`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `cosecha_poscosecha`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Frijol ya arrancado se mancha en la era porque llueve, y pregunta si terminar de secarlo bajo techo. La nota se sostiene.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** Las plantas ya están arrancadas. El problema es el secado en la era, no un mal en planta en pie.
- **Cultivo original:** frijol

### 31. `piloto-v2-967f4ea269`

- **Texto original:** La cebada está amarillenta desde la punta. No veo bichos. ¿Será que le falta comida?
- **Categoría inicial:** `fertilizacion_nutricion`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `fertilizacion_nutricion`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: La cebada amarillea desde la punta, no hay bichos, y pregunta si le falta comida. La nota se sostiene.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** No hay un animal a la vista. La consulta atribuye el amarillamiento a falta de comida.
- **Cultivo original:** cebada

### 32. `piloto-v2-a00996c1e8`

- **Texto original:** La yuca tiene las hojas con mosaico, unas partes verdes y otras amarillas, y no encuentro bicho. ¿Ese mal se queda en la rama que corto para la próxima campaña?
- **Categoría inicial:** `enfermedades_cultivos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `enfermedades_cultivos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Mosaico en la yuca, sin bicho, y si ese mal se queda en la rama que se corta para la próxima campaña. La nota se sostiene: no pide fecha ni distancia de siembra.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es si el mal pasa con la rama que se guarda para sembrar. No pide fecha ni distancia de siembra.
- **Cultivo original:** yuca

### 33. `piloto-v2-94bdd9fa4c`

- **Texto original:** Al sacudir la granadilla caen unos trips diminutos de la flor. ¿Puedo quitar los brotes cargados de esos trips o me quedo sin cuaje?
- **Categoría inicial:** `plagas`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `plagas`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Trips en la flor de la granadilla y si quitar los brotes cargados. La nota se sostiene: quitar brotes es un medio de ese control, no una poda de manejo.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es qué hacer con los trips de la flor. Quitar brotes se menciona solo como medio posible de ese control.
- **Cultivo original:** granadilla

### 34. `piloto-v2-5585a9b353`

- **Texto original:** Unos frutos de naranja caen con una mancha hundida y dura. No hay larva adentro. ¿Qué puede estar pudriendo la cáscara todavía en el árbol?
- **Categoría inicial:** `enfermedades_cultivos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `enfermedades_cultivos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Naranjas que caen con mancha hundida y dura, sin larva, todavía referidas al árbol. La nota se sostiene: no es guarda ni insecto.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** El fruto sigue en el árbol y no hay larva. No es una consulta de guarda ni de insecto.
- **Cultivo original:** naranja

### 35. `piloto-v2-80f3cb2f44`

- **Texto original:** ¿Limpio la zanja que embebe la papa?
- **Categoría inicial:** `suelos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `suelos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Pregunta si limpiar la zanja que embebe la papa. La nota se sostiene: no pide cómo regar. La taxonomía manda el drenaje, cuando no se pregunta cómo regar, a suelos. El texto es muy breve.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es limpiar la zanja que embebe la chacra. No pide cómo regar la papa.
- **Cultivo original:** papa

### 36. `piloto-v2-0216a38b4f`

- **Texto original:** Después de una semana de llovizna salieron manchas aceitosas en las hojas de abajo, con un borde amarillo. No encuentro bicho ni mordedura. Quiero saber qué mal es antes de tocar las plantas de al lado.
- **Categoría inicial:** `enfermedades_cultivos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `enfermedades_cultivos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Tras una semana de llovizna hay manchas aceitosas y quiere saber qué mal es, sin bicho ni mordedura. La nota se sostiene: no pide riego ni protección ante la lluvia.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** Pide identificar el mal aparecido después de la lluvia. No pide una labor de riego ni protección ante el evento de lluvia.

### 37. `piloto-v2-83896490d1`

- **Texto original:** En Chanchamayo el kion de la sombra salió con hoja clara y el rizoma delgado. ¿Le incorporo hoja de monte descompuesta al juntar tierra al tallo, o busco otra fuente de comida?
- **Categoría inicial:** `fertilizacion_nutricion`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `fertilizacion_nutricion`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Kion de Chanchamayo con hoja clara y rizoma delgado: incorporar hoja de monte u otra fuente de comida. La nota se sostiene. Juntar tierra es el momento, no la decisión.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es la fuente de comida. Juntar tierra al tallo se menciona solo como el momento de incorporarla.
- **Cultivo original:** kion
- **Región original:** Chanchamayo

### 38. `piloto-v2-e57aab2fbf`

- **Texto original:** Lleva un mes sin llover y la zanahoria enrolla la hoja desde el mediodía. El aviso de la radio no aclara si la seca sigue. ¿Me guío por ese aviso o solo miro el día de hoy?
- **Categoría inicial:** `clima_heladas`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `clima_heladas`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Lleva un mes sin llover, la zanahoria enrolla la hoja y el aviso no aclara si la seca sigue: si guiarse por el aviso o por el día. La nota se sostiene. No es la misma decisión que piloto-v2-59a61015e2.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es cómo leer el aviso de seca. No pide abrir una acequia ni cambiar el terreno.
- **Cultivo original:** zanahoria

### 39. `piloto-v2-37eabf9a20`

- **Texto original:** El kion tiene el rizoma con una pudrición acuosa y olor fuerte, y todavía está en la era, sin arrancar. ¿Lo saco entero o corto solo la parte dañada?
- **Categoría inicial:** `enfermedades_cultivos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `enfermedades_cultivos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Pudrición acuosa del rizoma de kion todavía en la era, sin arrancar: sacarlo entero o cortar solo lo dañado. La nota se sostiene. No es el oreo ni la venta.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** El rizoma sigue en la era. La decisión es la pudrición en planta, no el oreo ni la venta.
- **Cultivo original:** kion

### 40. `piloto-v2-45d1e6b6b2`

- **Texto original:** ¿Emparejo ya la era de la zanahoria?
- **Categoría inicial:** `suelos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** señalada por la auditoría, sin nota en el piloto
- **Etiqueta original:** `suelos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Pregunta si emparejar ya la era de la zanahoria. Emparejar el terreno es preparación del suelo y la etiqueta se sostiene. El texto es breve y roza el armado de la era de siembra; esa frontera no tiene nota.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación:** el piloto no trae `review_note`. El primer revisor pidió segunda lectura por una frontera o por poca claridad. Esa petición no se convierte en acuerdo.
- **Cultivo original:** zanahoria

### 41. `piloto-v2-dc3422090c`

- **Texto original:** La granadilla tiene las hojas viejas con el borde seco y el cogollo todavía verde. ¿Le falta alimento en la raíz?
- **Categoría inicial:** `fertilizacion_nutricion`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** señalada por la auditoría, sin nota en el piloto
- **Etiqueta original:** `fertilizacion_nutricion`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: La granadilla tiene el borde de las hojas viejas seco y el cogollo verde, y pregunta si le falta alimento en la raíz. La decisión pedida es la nutrición y la etiqueta se sostiene. El borde seco también se asocia a falta de agua; esa frontera no tiene nota. No se responde si el síntoma es carencia.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación:** el piloto no trae `review_note`. El primer revisor pidió segunda lectura por una frontera o por poca claridad. Esa petición no se convierte en acuerdo.
- **Cultivo original:** granadilla

### 42. `piloto-v2-2642f924ad`

- **Texto original:** En Tarma unos escarabajos nocturnos dejan la hoja de la chacra hecha encaje. ¿Reviso de noche con linterna o busco larvas donde la tierra sigue húmeda?
- **Categoría inicial:** `plagas`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `plagas`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Escarabajos nocturnos en Tarma dejan la hoja como encaje y pregunta cómo encontrarlos. La nota se sostiene. No pide trabajar el terreno. No nombra cultivo y crop queda omitido.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es cómo encontrar al escarabajo que come la hoja. No pide trabajar el terreno.
- **Región original:** Tarma

### 43. `piloto-v2-9870443304`

- **Texto original:** En Huancayo quiero la zanahoria para agosto. Si la pongo en mayo, ¿el surco va más junto porque el tiempo frío la atrasa, o mantengo el mismo trazo de siempre y solo cuido la fecha?
- **Categoría inicial:** `siembra_manejo_cultivo`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `siembra_manejo_cultivo`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: En Huancayo pregunta si juntar el surco de zanahoria por el tiempo frío o solo cuidar la fecha de mayo. La nota se sostiene: el frío es condición de esa fecha, no una helada a la que haya que proteger hoy.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es la fecha y la distancia de siembra. El frío se menciona como condición de esa fecha, no como protección ante una helada.
- **Cultivo original:** zanahoria
- **Región original:** Huancayo

### 44. `piloto-v2-63c243ee65`

- **Texto original:** El granizo golpeó la papaya y partió varias hojas grandes. ¿Esas heridas se atienden como daño del clima de ayer?
- **Categoría inicial:** `clima_heladas`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `clima_heladas`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: El granizo partió hojas de papaya y pregunta si esas heridas se atienden como daño del clima de ayer. La nota se sostiene. El cultivo es papaya, no papa.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es el daño del granizo ya ocurrido. No pide identificar una enfermedad.
- **Cultivo original:** papaya

### 45. `piloto-v2-b77cefb95c`

- **Texto original:** En Concepción quiero saber si la tierra está ácida antes de decidir cualquier cultivo. ¿La muestra se saca de un solo hoyo o de varios puntos de la chacra?
- **Categoría inicial:** `suelos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `suelos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: En Concepción pregunta si la muestra para saber si la tierra está ácida sale de un hoyo o de varios. La nota se sostiene: no pide la dosis de abono.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es cómo muestrear el terreno. No se pregunta la dosis de abono.
- **Región original:** Concepción

### 46. `piloto-v2-5d8c063a1b`

- **Texto original:** ¿Empiezo por la cochinilla de la piña?
- **Categoría inicial:** `plagas`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** señalada por la auditoría, sin nota en el piloto
- **Etiqueta original:** `plagas`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Pregunta si empezar por la cochinilla de la piña. La cochinilla es un animal y la categoría se sostiene. La pregunta no dice empezar qué; la claridad es baja y no alcanza para retirarla.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación:** el piloto no trae `review_note`. El primer revisor pidió segunda lectura por una frontera o por poca claridad. Esa petición no se convierte en acuerdo.
- **Cultivo original:** piña

### 47. `piloto-v2-86f762efd9`

- **Texto original:** Veo hilos blancos en la base del plátano y la mata se troncha. No hay picadura de insecto. ¿Cómo evito que pase a los hijuelos?
- **Categoría inicial:** `enfermedades_cultivos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** señalada por la auditoría, sin nota en el piloto
- **Etiqueta original:** `enfermedades_cultivos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Hilos blancos en la base del plátano, la mata se troncha y no hay picadura: cómo evitar que pase a los hijuelos. Niega la picadura y la etiqueta de enfermedad se sostiene. Un hilo blanco también puede leerse como otro organismo; esa frontera no tiene nota. No se le pone nombre.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación:** el piloto no trae `review_note`. El primer revisor pidió segunda lectura por una frontera o por poca claridad. Esa petición no se convierte en acuerdo.
- **Cultivo original:** plátano

### 48. `piloto-v2-31849ca42b`

- **Texto original:** ¿La lluvia torrencial de una noche, la que deja el camino como río, obliga a revisar el cultivo al día siguiente por el golpe del agua?
- **Categoría inicial:** `clima_heladas`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `clima_heladas`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Pregunta si una lluvia torrencial obliga a revisar el cultivo al día siguiente por el golpe del agua. La nota se sostiene: no pide nombrar un mal ni abrir un drenaje.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** Pide revisar el golpe de esa lluvia. No pide identificar un mal de las hojas ni abrir un drenaje definitivo.

### 49. `piloto-v2-3cff8cbcf3`

- **Texto original:** En Concepción el reservorio familiar alcanza para pocas horas. Hay plantas recién salidas y otras ya cargadas, todas con sed el mismo día, y el agua no va a alcanzar para el huerto entero. ¿A cuáles les doy el agua de hoy y cuáles pueden esperar al siguiente turno?
- **Categoría inicial:** `riego`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `riego`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: En Concepción el reservorio no alcanza y pregunta a cuáles plantas dar el agua de hoy. La nota se sostiene: no pide qué sembrar ni qué fecha elegir.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es el reparto del agua del reservorio. No pide qué cultivo sembrar ni qué fecha elegir.
- **Región original:** Concepción

### 50. `piloto-v2-c77fa8da96`

- **Texto original:** La papaya se ve vigorosa arriba y la fruta sale sin dulce. ¿Cambio la comida cuando aparece la flor?
- **Categoría inicial:** `fertilizacion_nutricion`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** señalada por la auditoría, sin nota en el piloto
- **Etiqueta original:** `fertilizacion_nutricion`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: La papaya sale sin dulce y pregunta si cambiar la comida cuando aparece la flor. La decisión pedida es la comida y la etiqueta se sostiene. «Sin dulce» también se asocia al punto de corte; esa frontera no tiene nota y no pesa lo mismo que la pregunta por la comida.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación:** el piloto no trae `review_note`. El primer revisor pidió segunda lectura por una frontera o por poca claridad. Esa petición no se convierte en acuerdo.
- **Cultivo original:** papaya

### 51. `piloto-v2-c7e8e93ece`

- **Texto original:** En Chupaca la campaña de lluvias se atrasa algunos años y otras veces cae antes de que yo tenga la semilla lista. No quiero ponerla en seco, tampoco quiero pasarme de la fecha y perder el ciclo. ¿La dejo preparada y espero la primera lluvia de verdad, o hay un día del calendario del que ya no debo pasar aunque el cielo siga despejado?
- **Categoría inicial:** `siembra_manejo_cultivo`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `siembra_manejo_cultivo`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: En Chupaca pregunta si esperar la primera lluvia de verdad para poner la semilla o si hay un día del que ya no pasar. La nota se sostiene: es la ventana de siembra, no un evento de lluvia ya anunciado.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** Pregunta por la ventana para poner la semilla. No pide qué hacer ante un evento de lluvia ya anunciado.
- **Región original:** Chupaca

### 52. `piloto-v2-226b8b322c`

- **Texto original:** ¿Las terrazas que ya existen en la ladera de Tarma hay que rehacerlas si el muro se venció, o puedo seguir usándolas así?
- **Categoría inicial:** `suelos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `suelos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Pregunta si rehacer las terrazas de Tarma cuando el muro se venció. La nota se sostiene: no pide una fecha de siembra.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es reparar la terraza. No pide una fecha de siembra.
- **Región original:** Tarma

### 53. `piloto-v2-038ffc061a`

- **Texto original:** ¿Un análisis de suelo alcanza con la capa de los primeros veinte centímetros?
- **Categoría inicial:** `suelos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `suelos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Pregunta si el análisis de suelo alcanza con los primeros veinte centímetros. La nota se sostiene: no pide interpretar una dosis.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** Pregunta por la profundidad de la muestra de tierra. No pide interpretar una dosis.

### 54. `piloto-v2-f454b7c529`

- **Texto original:** En Yauli el viento seca la chacra en un día. ¿Acorto los días entre cada riego o alargo la hora que dejo abierta la acequia?
- **Categoría inicial:** `riego`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `riego`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: En Yauli el viento seca la chacra y pregunta si acortar los días entre riegos o alargar la acequia. La nota se sostiene. No es la protección ante el viento de piloto-v2-1d4ef1a7bd ni el agua usada solo contra el frío de piloto-v2-4d8651680b.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** El viento se menciona como causa de que la chacra se seque. La decisión pedida es el intervalo y la duración del agua, no una protección ante un evento de viento.
- **Región original:** Yauli

### 55. `piloto-v2-e7cca92a8f`

- **Texto original:** Las hojas nuevas del olluco salen pequeñas. No hay mordeduras. ¿Refuerzo la comida a mitad del ciclo?
- **Categoría inicial:** `fertilizacion_nutricion`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `fertilizacion_nutricion`
- **Evaluación del primer revisor:** resultado «correcta»; confianza media. Justificación de ese informe: Hojas nuevas del olluco pequeñas, sin mordeduras, y si reforzar la comida a mitad del ciclo. La nota se sostiene.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** No hay daño de un animal. La decisión es si se refuerza la comida a mitad del ciclo.
- **Cultivo original:** olluco

### 56. `piloto-v2-d9aa2b7030`

- **Texto original:** La granadilla tiene manchas aceitosas en el fruto y se arruga en la planta. ¿Retiro los frutos así o espero a ver si maduran?
- **Categoría inicial:** `enfermedades_cultivos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `enfermedades_cultivos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: Manchas aceitosas en el fruto de granadilla, que se arruga en la planta: retirar esos frutos o esperar. La nota se sostiene. No es el punto de recolección de piloto-v2-9018b8aefd.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** El fruto sigue en la planta. La decisión es la mancha, no el punto de recolección.
- **Cultivo original:** granadilla

### 57. `piloto-v2-45b44ad4dc`

- **Texto original:** El hoyo de la palta junta agua contra el tronco cada vez que llueve. ¿Lo abro a un lado para que el agua salga?
- **Categoría inicial:** `suelos`
- **Categoría propuesta por el segundo revisor:** no emitida
- **Resultado:** pendiente
- **Justificación basada en la taxonomía:** no hay segunda aplicación de la taxonomía. Emitir una aquí sería el mismo agente. La ficha queda abierta hasta que otra persona lea el texto sin heredar esta sesión.
- **Necesidad de arbitraje humano:** sí
- **Grupo:** nota de frontera en el piloto
- **Etiqueta original:** `suelos`
- **Evaluación del primer revisor:** resultado «correcta»; confianza alta. Justificación de ese informe: El hoyo de la palta junta agua contra el tronco cuando llueve y pregunta si abrirlo para que el agua salga. La nota se sostiene: es salida del agua del terreno, no un mal del tronco ni un turno de riego.
- **Corrección que el primer revisor propuso y no aplicó:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Evaluación del segundo revisor:** no realizada
- **Resolución final:** no existe
- **Estado:** pendiente
- **Observación, nota ya presente en el piloto:** La decisión es abrir el hoyo para que salga el agua. No pide diagnosticar un mal del tronco ni un turno de riego.
- **Cultivo original:** palta

## Conteo de esta lista

- Fichas: 57
- Con nota de frontera: 48
- Sin nota, tomadas del informe: 9
- Acuerdos: 0
- Desacuerdos: 0
- Pendientes: 57
- Categorías nuevas emitidas por un segundo revisor: 0
