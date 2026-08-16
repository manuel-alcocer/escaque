# Escaque

Plataforma para estudiar aperturas de ajedrez: teoría, variantes y muchos ejercicios sobre
el tablero. Diseñada para el móvil, que es donde más se usa.

Contenido actual: **Apertura Española** (C60–C99), **Defensa India de Rey** (E60–E99) y
**Defensa Caro-Kann** (B10–B19). 35 variantes y 282 ejercicios.

- **Backend**: Django 6 + Django REST Framework, PostgreSQL, JWT.
- **Frontend**: Vue 3 + Vite, chessground para el tablero, chess.js para la legalidad.
- **Motor**: Stockfish en un contenedor propio, hablando UCI por TCP.

---

## Arranque rápido con Docker

```bash
docker compose up --build -d
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_curriculum
docker compose exec backend python manage.py createuser manuel --superuser
```

Abre <http://localhost:8080>.

## Desarrollo sin Docker

```bash
# Motor (lo único que necesita contenedor)
docker compose up -d stockfish

# Backend
cd backend
uv venv .venv && uv pip install --python .venv/bin/python -r pyproject.toml
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_curriculum
.venv/bin/python manage.py createuser manuel --superuser
STOCKFISH_HOST=127.0.0.1 DEBUG=True .venv/bin/python manage.py runserver

# Frontend (otra terminal)
cd frontend && npm install && npm run dev
```

El servidor de Vite queda en <http://localhost:5173> y hace proxy de `/api` al backend.
Sin `DATABASE_URL` el backend usa SQLite, así que no hace falta Postgres para desarrollar.

## Altas de usuario

No hay registro público. Las cuentas se crean a mano:

```bash
python manage.py createuser ana --email ana@example.com --display-name "Ana Ruiz"
python manage.py createuser ana --generate-password       # imprime una contraseña aleatoria
python manage.py createuser admin --superuser
```

Sin `--password` la pide por consola sin mostrarla. El modelo `User` ya tiene el campo
`google_sub`, así que activar el acceso con Google más adelante será añadir el flujo OIDC
y rellenar ese campo: no hará falta migrar datos.

---

## Cómo está organizado

```
backend/
  config/                 settings, urls, wsgi/asgi
  apps/accounts/          usuario propio + management command createuser
  apps/curriculum/        secciones, aperturas, variantes, teoría
    seed/                 el contenido, escrito en SAN y compilado contra un tablero real
  apps/exercises/         ejercicios, intentos y progreso
    services.py           corrección de respuestas y registro de fallos
  apps/engine/            cliente UCI para el contenedor de Stockfish
  tests/                  pytest
frontend/src/
  components/             ChessBoard, AutoBoard, MoveSheet, EnginePanel…
  views/                  Login, Home, Opening, Variation, Trainer, Progress
  lib/notation.js         traducción de SAN inglés a notación española
docker/stockfish/         imagen del motor (stockfish + socat)
argocd/application.yaml   Application de ArgoCD (la despliega k8s-home-apps)
deploy/k8s/               manifiestos de producción (kustomize)
.github/workflows/        build multiarch y bump de tags
```

### Dónde se decide si una respuesta es correcta

En el servidor, siempre: `apps/exercises/services.py`. El navegador comprueba la
**legalidad** de la jugada con chess.js para que el tablero se comporte bien, pero nunca
sabe cuál es la respuesta. La solución sólo viaja al cliente cuando el intento ya ha
terminado.

Consecuencias buscadas:

- La línea del ejercicio no se puede leer desde la pestaña de red.
- Una jugada **ilegal** devuelve 400: es una petición inválida, no una respuesta incorrecta.
- Una jugada **legal pero equivocada** marca el ejercicio como fallido.

### El registro de fallos

La regla del producto es que un ejercicio no resuelto correctamente queda marcado como
fallido, y `services.register_attempt` es el único sitio que escribe ese resultado:

- `Attempt` guarda cada intento terminado y no se modifica nunca.
- `ExerciseProgress` lleva los contadores por usuario y ejercicio.
- `needs_review` se pone a `True` al fallar y sólo se limpia al resolverlo bien. El
  historial de fallos se conserva.
- Rendirse (`Ver solución`) cuenta como fallo, igual que una jugada equivocada.

La cola de entrenamiento (`/api/exercises/queue/`) sirve primero lo fallido, luego lo que
no se ha intentado y por último lo resuelto.

### El contenido

`apps/curriculum/seed/` no guarda FENs escritos a mano. Cada línea se escribe una vez en
SAN desde la posición inicial y `schema.py` la reproduce sobre un tablero de verdad para
derivar el FEN, la lista UCI y a quién le toca mover. Una jugada mal escrita rompe el
comando en lugar de convertirse en un ejercicio imposible:

```bash
python manage.py seed_curriculum --check    # compila y valida, sin escribir nada
python manage.py seed_curriculum            # carga o actualiza
python manage.py seed_curriculum --prune    # además borra lo que ya no está declarado
```

Es idempotente: las variantes se identifican por `slug` y los ejercicios por `reference`,
así que reejecutarlo actualiza en su sitio y **no rompe el progreso de los usuarios**.

La mayor parte de los 282 ejercicios se generan desde las propias líneas teóricas
(`drill_plies` marca en qué jugadas hay que preguntar), y encima hay ejercicios escritos a
mano: celadas, tácticas y ejercicios de plan. Los que declaran `expect="mate"` se verifican
como mate al sembrar.

### El motor

Stockfish habla UCI por stdin/stdout, así que el contenedor lo publica en TCP con `socat`
en modo `fork`: cada petición abre su conexión, obtiene un proceso propio y lo cierra al
terminar. Sin estado compartido entre usuarios.

El motor es **opcional**. Los ejercicios se corrigen contra su línea guardada, no contra
Stockfish, así que si el contenedor no responde la aplicación sigue funcionando y sólo se
pierde el panel de análisis. La cabecera muestra si está vivo.

---

## Tests

```bash
cd backend && .venv/bin/python -m pytest -q
```

Cubren la corrección de respuestas, el registro de fallos y los contratos de la API en los
que se apoya la interfaz (que la solución no se filtre, que la cola priorice los fallos).

---

## Producción: `escaque.linuxarena.net`

Desplegada en el homelab (clúster `armlab`) por **ArgoCD**, siguiendo el patrón de
`k8s-home-apps`: la `Application` vive en este repo (`argocd/application.yaml`) y la entrada
app-of-apps (`deployments/escaque.yml` en k8s-home-apps) apunta ArgoCD aquí.

```
push a main
  └─ GitHub Actions construye las 3 imágenes multiarch (amd64 + arm64)
     └─ ghcr.io/manuel-alcocer/escaque-{backend,frontend,stockfish}:main-<sha>
        └─ reescribe deploy/k8s/kustomization.yml y hace commit [skip ci]
           └─ ArgoCD detecta el cambio y redespliega
```

No hay `kubectl apply` manual: todo pasa por git.

### Exposición pública

No hay Ingress ni Traefik: sale por el **túnel de Cloudflare** que ya expone otras apps del
clúster. cloudflared corre en modo token (gestionado remotamente), así que la ruta se define
en el **dashboard de Cloudflare Zero Trust**, no en este repo:

```
escaque.linuxarena.net  ->  http://escaque-frontend.escaque.svc.cluster.local:80
```

El nginx del pod de frontend reenvía `/api`, `/admin` y `/static` al backend, así que el
túnel sólo necesita esa única ruta y el navegador ve un solo origen (sin CORS en producción).

### Base de datos y secretos

- **PostgreSQL compartido** del clúster (`postgresql.databases.svc.cluster.local`). El Job
  `escaque-db-init` crea el rol y la base de datos, y es idempotente.
- **Ningún secreto vive en este repo.** El `SECRET_KEY` de Django y la contraseña de la base
  de datos los genera el *Password generator* de External Secrets Operator y se materializan
  como `Secret` con `refreshInterval: "0"` y `deletionPolicy: Retain`: se generan una vez y
  **no rotan**. Rotar el `SECRET_KEY` invalidaría todos los JWT emitidos.
- Las imágenes son públicas, así que no hace falta pull-secret.

### Operaciones

```bash
# Ver el estado
argocd app get escaque
kubectl -n escaque get pods

# Forzar una sincronización
argocd app sync escaque

# Crear un usuario
kubectl -n escaque exec -it deploy/escaque-backend -- python manage.py createuser manuel --superuser

# Ver el log del seed tras un despliegue
kubectl -n escaque logs job/escaque-migrate
```

### Detalles del despliegue

- **Migraciones en un Job `PostSync`**, no en un initContainer: con dos réplicas de backend
  un initContainer competiría consigo mismo. `seed_curriculum` se ejecuta en cada sync, lo
  que actualiza la teoría sin tocar el progreso de los usuarios.
- **Stockfish prefiere el nodo amd64** (`nodeAffinity` *preferred*, no *required*): el
  análisis es puro CPU y ultron es bastante más rápido que las Orange Pi. Como la imagen es
  multiarch, ARM sigue siendo un fallback válido.
- **Multiarch no es opcional**: el clúster mezcla dos nodos arm64 con uno amd64.
- **Stockfish escala aparte.** Es lo único que consume CPU de verdad; si el análisis va
  lento, sube sus réplicas sin tocar el resto.

### Variables de entorno

| Variable | Por defecto | Para qué |
| --- | --- | --- |
| `SECRET_KEY` | clave insegura de desarrollo | Obligatoria en producción |
| `DEBUG` | `False` | Activa las protecciones cuando está apagado |
| `DATABASE_URL` | SQLite en `backend/` | Postgres en producción |
| `ALLOWED_HOSTS` | `*` | Lista separada por comas |
| `CORS_ALLOWED_ORIGINS` | `localhost:5173` | Sólo hace falta en desarrollo |
| `STOCKFISH_HOST` / `STOCKFISH_PORT` | `stockfish` / `23249` | Dónde está el motor |
| `STOCKFISH_MAX_MOVETIME` | `5000` | Tope de tiempo de análisis, en ms |
| `ACCESS_TOKEN_LIFETIME_MINUTES` | `60` | Vida del token de acceso |

En producción los valores salen de `deploy/k8s/configmap.yml` (los no sensibles) y de los
`Secret` que genera External Secrets Operator (`SECRET_KEY`, `DATABASE_URL`).

---

## Añadir contenido

Para una variante nueva, edita el fichero de su apertura en `apps/curriculum/seed/` y
añade un `VariationSpec`:

```python
VariationSpec(
    slug="espanola-nueva",
    name="Variante Nueva",
    eco="C80",
    line=RUY + ["a6", "Ba4", "Nf6", "O-O"],   # SAN desde la posición inicial
    tagline="Una frase que diga de qué va.",
    idea="Qué intentan los dos bandos.",
    description="Markdown para el texto largo.",
    drill_plies=[5, 6, 7, 8],                 # jugadas que el usuario tendrá que encontrar
    exercises=[...],                          # ejercicios escritos a mano, opcional
)
```

Después, `python manage.py seed_curriculum --check` para comprobar que todas las jugadas
son legales, y `seed_curriculum` para cargarlo.

Para una sección nueva (táctica, finales…), añade un `SectionSpec` en
`apps/curriculum/seed/__init__.py`. El resto de la aplicación ya la mostrará: la portada,
los filtros y el progreso se construyen a partir de lo que haya en la base de datos.
