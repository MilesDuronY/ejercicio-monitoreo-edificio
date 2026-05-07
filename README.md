# Ejercicio: Monitoreo de Edificio

En este ejercicio vas a aplicar `Interface`, `Composite` y `Observer` en un
escenario de edificio inteligente.

## Contexto

Un edificio corporativo tiene sensores distribuidos por torre, piso y area. El
sistema necesita representar esa estructura jerarquica y, cuando ocurre un
incidente, actualizar el conteo total y avisar al equipo de mantenimiento.

La necesidad real es doble:

- modelar la estructura completa del edificio sin duplicar logica,
- notificar automaticamente cuando el sistema registra un nuevo incidente,
- y distinguir cuando un sensor ya se vuelve critico por acumulacion.

## Que patron resuelve cada problema

- `Interface`: unifica sensores y zonas bajo el mismo contrato.
- `Composite`: permite recorrer torre, piso y sensor como una sola estructura.
- `Observer`: desacopla el monitoreo del equipo que reacciona a la alerta.

## Objetivo

Completar `monitoreo_edificio_base.py` para que:

1. las zonas sumen incidentes de forma recursiva,
2. el edificio principal registre observadores,
3. el reporte de incidente dispare una alerta,
4. el sistema tambien cuente cuantos sensores tienen incidentes activos,
5. el sistema detecte cuantos sensores ya son criticos,
6. la alerta cambie de nivel cuando un sensor acumule dos o mas incidentes,
7. la jerarquia se muestre claramente en consola.

## Estructura

```text
ejercicio-monitoreo-edificio/
|-- README.md
`-- ejercicio/
    `-- monitoreo_edificio_base.py
```

## Pasos sugeridos

Sigue estos pasos exactamente en orden. No intentes resolver primero
`Zona.reportar_incidente()` porque depende de varias piezas previas.

La meta es que cada paso deje una idea cerrada:

1. primero resuelves el nodo hoja,
2. despues resuelves el composite,
3. luego conectas el observer,
4. y al final integras todo.

### Paso 1: Entender la estructura antes de programar

Antes de escribir codigo, ubica estas dos ideas:

- `Sensor` es el caso simple del arbol.
- `Zona` es el caso compuesto del arbol.

Traduccion practica:

- un `Sensor` no tiene hijos,
- una `Zona` si tiene hijos,
- tanto `Sensor` como `Zona` responden a la misma interfaz
  `ElementoMonitoreo`.

Que debes observar en el archivo:

- `Sensor.reportar_incidente()` ya esta resuelto.
- Ese metodo te dice como funciona el caso base.
- Tu trabajo sera hacer que `Zona` delegue esa misma operacion a sus hijos.

### Paso 2: Completar primero el caso hoja en `Sensor`

Metodo a completar:

- `Sensor.incidentes_del_sensor(nombre_sensor)`

Que debe hacer:

1. comparar si `self.nombre` es igual a `nombre_sensor`,
2. si coincide, regresar `self.incidentes`,
3. si no coincide, regresar `None`.

Importante:

- No debe recorrer nada porque `Sensor` no tiene hijos.
- Este metodo sera usado despues por `Zona` para preguntar cuantas incidencias
  lleva un sensor concreto.

Comprobacion mental antes de seguir:

- Si el sensor se llama `"Sensor Lobby"` y preguntas por `"Sensor Lobby"`,
  debe regresar un numero.
- Si preguntas por otro nombre, debe regresar `None`.

### Paso 3: Resolver las agregaciones recursivas en `Zona`

Metodos a completar:

- `Zona.total_incidentes()`
- `Zona.sensores_con_incidentes()`
- `Zona.sensores_criticos()`

La idea de los tres metodos es la misma:

1. recorrer `self.elementos`,
2. pedirle a cada hijo su respuesta,
3. sumar todas las respuestas.

Que responde cada metodo:

- `total_incidentes()`: suma todos los incidentes acumulados del arbol.
- `sensores_con_incidentes()`: cuenta cuantos sensores tienen al menos 1
  incidente.
- `sensores_criticos()`: cuenta cuantos sensores tienen 2 o mas incidentes.

Pista importante:

- No necesitas preguntar si el hijo es `Sensor` o `Zona`.
- Ambos ya saben responder a esos metodos.

Comprobacion mental antes de seguir:

- Si una zona tiene dos sensores con `1` y `2` incidentes, entonces:
  `total_incidentes()` debe regresar `3`,
  `sensores_con_incidentes()` debe regresar `2`,
  `sensores_criticos()` debe regresar `1`.

### Paso 4: Conectar el patrón observer

Metodos a completar:

- `Zona.agregar_observador(observador)`
- `Zona.notificar_alerta(mensaje)`

Que debe hacer cada uno:

1. `agregar_observador()` solo guarda al observador en la lista.
2. `notificar_alerta()` recorre `self.observadores`.
3. por cada observador, llama `actualizar(mensaje)`.

No hagas de mas aqui:

- Este paso no construye mensajes.
- Este paso no busca sensores.
- Solo conecta la lista de observadores con la operacion de aviso.

Comprobacion mental antes de seguir:

- Si agregas dos observadores, ambos deben recibir el mismo mensaje.

### Paso 5: Resolver la busqueda recursiva del sensor en `Zona`

Metodo a completar:

- `Zona.incidentes_del_sensor(nombre_sensor)`

Que debe hacer:

1. recorrer `self.elementos`,
2. pedir a cada hijo `incidentes_del_sensor(nombre_sensor)`,
3. si algun hijo regresa un numero, regresarlo inmediatamente,
4. si ningun hijo lo encuentra, regresar `None`.

Idea clave:

- Este metodo no incrementa incidentes.
- Solo busca y devuelve cuantas incidencias lleva el sensor despues de haber
  sido reportado.

Comprobacion mental antes de seguir:

- Si el sensor esta dentro de una subzona, la busqueda debe encontrarlo igual.
- Si el sensor no existe en ningun nivel, el metodo debe regresar `None`.

### Paso 6: Integrar el flujo completo de `reportar_incidente()`

Metodo a completar:

- `Zona.reportar_incidente(nombre_sensor)`

Este es el paso mas importante. Hazlo en este orden exacto:

1. recorre `self.elementos`,
2. llama `elemento.reportar_incidente(nombre_sensor)` en cada hijo,
3. si un hijo regresa `True`, significa que el sensor si fue encontrado,
4. en ese momento llama `self.incidentes_del_sensor(nombre_sensor)` para saber
   cuantas incidencias lleva ahora,
5. con ese numero calcula el nivel de alerta:
   `MEDIA` si lleva `1`,
   `ALTA` si lleva `2` o mas,
6. arma el mensaje final,
7. llama `self.notificar_alerta(mensaje)`,
8. regresa `True`,
9. si ningun hijo encuentra el sensor, regresa `False`.

El mensaje debe incluir exactamente estas piezas:

1. nombre del sensor,
2. nombre de la zona principal,
3. total acumulado,
4. sensores con incidentes activos,
5. sensores criticos,
6. nivel de alerta.

Comprobacion mental antes de seguir:

- Primer reporte al mismo sensor:
  `Nivel de alerta: MEDIA`
- Segundo reporte al mismo sensor:
  `Nivel de alerta: ALTA`

### Paso 7: Completar la visualizacion del arbol

Metodo a completar:

- `Zona.mostrar(nivel=0)`

Que debe hacer:

1. imprimir la zona actual usando `nivel` para la indentacion,
2. recorrer `self.elementos`,
3. llamar `mostrar(nivel + 1)` en cada hijo.

Comprobacion mental antes de seguir:

- La torre debe aparecer al nivel 0.
- Sus subzonas deben aparecer un nivel mas adentro.
- Los sensores deben quedar debajo de la zona que los contiene.

### Paso 8: Ejecutar y revisar el comportamiento final

Cuando termines todo, ejecuta:

```bash
python .\ejercicio\monitoreo_edificio_base.py
```

Debes observar este flujo:

1. primero se imprime la estructura del edificio,
2. luego se reporta una vez `Sensor Lobby`,
3. despues se reporta una segunda vez el mismo sensor,
4. la primera alerta debe ser `MEDIA`,
5. la segunda alerta debe ser `ALTA`.

## Resultado esperado

La salida final debe parecerse a esto:

```text
Estructura de monitoreo:
- Zona: Torre Norte
  - Zona: Lobby
    - Sensor: Sensor Lobby (incidentes: 0)

[MANTENIMIENTO] Incidente reportado en 'Sensor Lobby' dentro de 'Torre Norte'. Total acumulado: 1. Sensores con incidentes activos: 1. Sensores criticos: 0. Nivel de alerta: MEDIA
[MANTENIMIENTO] Incidente reportado en 'Sensor Lobby' dentro de 'Torre Norte'. Total acumulado: 2. Sensores con incidentes activos: 1. Sensores criticos: 1. Nivel de alerta: ALTA
```

## Ejecucion

Desde la raiz del repositorio:

```bash
python .\ejercicio\monitoreo_edificio_base.py
```

Al inicio el archivo lanza `NotImplementedError`. Esa es la pista de que aun
faltan partes por completar.

## Preguntas de reflexion

1. Por que un piso y una torre pueden modelarse con la misma clase?
2. Que clase deberia cambiar si se agrega un nuevo equipo que recibe alertas?
3. Donde se aprovecha mejor la recursividad en este ejercicio?
4. Que diferencia hay entre contar incidentes y contar sensores afectados?
5. Por que un sensor critico no es lo mismo que un sensor con incidentes?
