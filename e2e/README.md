# Tests de navegador

Pruebas end-to-end contra un despliegue real. Están fuera de `frontend/` a propósito: así
Playwright no entra en el `npm ci` de la imagen de producción.

## Ejecutar

```bash
docker compose up -d          # desde la raíz del repo
cd e2e && npm install
npm test
```

Contra otro entorno o con otras credenciales:

```bash
BASE=https://escaque.linuxarena.net USER_NAME=manuel USER_PASS=... npm test
```

Si el sistema ya trae un Chromium y no quieres el de Playwright:

```bash
CHROME_PATH=/usr/bin/chromium npm test
```

## Qué cubre `trainer.spec.mjs`

Que el tablero **sigue aceptando movimientos al pasar de un ejercicio al siguiente**.

Es una regresión concreta y difícil de ver leyendo el código: chessground registra sus
listeners dentro de `redrawAll()` y se los salta si el tablero es `viewOnly`. Su `set()`
llama a `redrawAll()` cuando cambia la orientación, y lo hace **antes** de aplicar el resto
de la configuración — así que un tablero que venía de terminar un ejercicio (`viewOnly`) y
recibe el siguiente (interactivo y del otro bando) se redibujaba estando aún marcado como
`viewOnly` y se quedaba sin ningún listener. Recargar la página lo ocultaba.

El test no necesita saber las soluciones: recorre varios ejercicios usando *Ver solución* y
comprueba en cada uno que el tablero está vivo, tocando piezas hasta que alguna ofrece
destinos legales. Un tablero vivo siempre tiene al menos una.

Como recorre varios ejercicios seguidos, garantiza que en algún momento hay un cambio de
orientación, que es la condición que dispara el fallo.
