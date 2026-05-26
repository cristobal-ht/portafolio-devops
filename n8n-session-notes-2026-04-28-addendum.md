# n8n Session Notes Addendum

Fecha: 2026-04-28

## Tema

SeparaciÃ³n del acceso de n8n en dos subdominios:

- `n8n-admin.cristobalht.cl`
- `n8n-hooks.cristobalht.cl`

## Por quÃ©

El panel de n8n no deberÃ­a quedar expuesto pÃºblicamente, pero el proyecto sÃ­ necesitarÃ¡ webhooks pÃºblicos para WhatsApp y otros callbacks.

La separaciÃ³n permite:

- panel admin privado
- webhooks pÃºblicos

## Estado del repo

Se dejaron preparados estos cambios, pero aÃºn no se aplican al clÃºster:

- `n8n-values.yaml`
  - `editorBaseUrl` -> `https://n8n-admin.cristobalht.cl`
  - `N8N_HOST` -> `n8n-admin.cristobalht.cl`
  - `WEBHOOK_URL` -> `https://n8n-hooks.cristobalht.cl/`
  - `ingress.enabled: false`

Archivos nuevos:

- `n8n-admin-service.yaml`
- `n8n-hooks-service.yaml`
- `n8n-admin-ingress.yaml`
- `n8n-hooks-ingress.yaml`
- `n8n-admin-certificate.yaml`
- `n8n-hooks-certificate.yaml`
- `n8n-frontendconfig.yaml`
- `n8n-admin-backendconfig-iap.yaml`

## DecisiÃ³n tÃ©cnica importante

GKE documenta que un mismo par `(Service, port)` solo puede consumir un `BackendConfig`.

Por eso no conviene usar un solo `Service` si queremos:

- `IAP` para admin
- y webhooks pÃºblicos sin IAP

SoluciÃ³n preparada:

- `Service` `n8n-admin`
- `Service` `n8n-hooks`

Ambos apuntan al mismo deployment de n8n.

## Estado del clÃºster

El acceso vigente que sigue activo hoy es:

- `https://n8n.cristobalht.cl`

La separaciÃ³n nueva todavÃ­a no se aplica.

## Dato importante sobre IAP

Se verificÃ³ que el clÃºster corre:

`v1.34.4-gke.1193000`

Eso soporta `IAP` con `BackendConfig` y Google-managed OAuth client.

Pero Google indica que el cliente OAuth administrado por Google solo permite acceso a usuarios dentro de la organizaciÃ³n del proyecto.

Por eso, antes de aplicar IAP, hay que confirmar si el acceso del administrador se hace con:

- cuenta personal
- o cuenta de Google Workspace / organizaciÃ³n

## Siguiente paso

Confirmar una sola cosa:

- si entras a GCP con cuenta personal
  o
- con cuenta de Google Workspace

Con eso se decide si el panel admin se protege con:

- `IAP`
  o
- allowlist de IP / Cloud Armor
