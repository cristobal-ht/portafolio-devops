# n8n Session Notes

Fecha: 2026-04-24

## Objetivo

Instalar n8n en GKE para luego integrarlo con GitHub, IA y eventualmente WhatsApp, con la idea de automatizar publicaciones del blog del portafolio.

## Estado actual

- n8n fue instalado en Kubernetes con Helm usando el chart `community-charts/n8n`.
- El namespace usado es `n8n`.
- El servicio de n8n quedó expuesto con `LoadBalancer`.
- El PVC `n8n-main-persistence` quedó en estado `Bound`.
- Se pudo acceder a la interfaz web de n8n e iniciar sesión.

## Problemas resueltos

### 1. Chart y values

- El archivo `n8n-values.yaml` tenía una estructura incompatible con el chart.
- Se corrigió para usar:
  - `existingEncryptionKeySecret`
  - `main.persistence`
  - `main.resources`
  - `service.type: LoadBalancer`

### 2. Secret de Kubernetes

- Se creó el secret `n8n-secret`.
- El chart espera la clave `N8N_ENCRYPTION_KEY`.
- La clave configurada actualmente es:

`dev.roll.sur.alegre.2.8`

Nota: esta clave no es la contraseña del panel de n8n; es la clave de cifrado interna para credenciales almacenadas por n8n.

### 3. CrashLoopBackOff

- n8n arrancaba, pero Kubernetes lo reiniciaba por probes demasiado agresivas.
- Se corrigieron `readinessProbe` y `livenessProbe` para dar más tiempo de arranque.

### 4. Problema de secure cookie

- Al abrir n8n por IP pública con `http://`, aparecía el mensaje de secure cookie.
- Se agregó temporalmente:

`N8N_SECURE_COOKIE: "false"`

Esto permite usar n8n por HTTP mientras se aprende y se prueba la instalación.

### 5. Problema de rollout con PVC

- El pod nuevo quedó `Pending` porque el volumen es `ReadWriteOnce`.
- Se cambió la estrategia del deployment a:

`strategy.type: Recreate`

Así futuras actualizaciones no intentarán levantar dos pods a la vez con el mismo disco.

## Archivos relevantes

- `n8n-values.yaml`
- `n8n-session-notes.md`

## Estado de seguridad

### Bien

- La encryption key no está escrita en Git.
- La clave vive en un `Secret` de Kubernetes.
- Helm usa `existingEncryptionKeySecret: n8n-secret`.

### Temporal / no ideal para producción

- n8n está público por `LoadBalancer`.
- El acceso es por HTTP.
- `N8N_SECURE_COOKIE` está desactivado.

## Idea del proyecto

Flujo objetivo:

WhatsApp -> n8n -> IA -> GitHub -> GitHub Actions -> página web

## Observación sobre la página actual

La página actual sí sirve para este proyecto, pero el blog todavía es manual:

- Las rutas de posts están hardcodeadas en `paginaweb.py`.
- El listado de posts está hardcodeado en `templates/blog.html`.

Eso no bloquea el proyecto, pero más adelante conviene volver el blog más dinámico para automatizar publicaciones de forma limpia.

## Siguiente paso recomendado

Conectar n8n con GitHub y hacer una automatización mínima:

1. Crear o actualizar un archivo de prueba en el repo desde n8n.
2. Verificar que GitHub Actions despliega el cambio.
3. Luego integrar IA.
4. Finalmente integrar WhatsApp.

## Comandos útiles

Ver pods:

```powershell
kubectl get pods -n n8n
```

Ver servicio:

```powershell
kubectl get svc -n n8n
```

Ver PVC:

```powershell
kubectl get pvc -n n8n
```

Reaplicar Helm:

```powershell
helm upgrade --install n8n community-charts/n8n --namespace n8n --values n8n-values.yaml
```

## Nota para retomar mañana

Lo más recomendable es empezar directamente con:

`n8n -> GitHub -> commit de prueba`

## Actualización 2026-04-27

### Fase 1 de seguridad en preparación

Se preparó la migración de n8n desde IP pública por `LoadBalancer` a acceso por dominio con `Ingress` y `ManagedCertificate`.

Cambios hechos:

- `service.type` de n8n cambió a `ClusterIP`
- se habilitó `ingress` en Helm para `n8n.cristobalht.cl`
- se agregaron variables para reverse proxy:
  - `N8N_HOST`
  - `N8N_PROTOCOL=https`
  - `N8N_PROXY_HOPS=1`
  - `WEBHOOK_URL=https://n8n.cristobalht.cl/`
- se definió `main.editorBaseUrl`
- se quitó el override temporal `N8N_SECURE_COOKIE=false`
- se creó `n8n-certificate.yaml` con `ManagedCertificate`

Archivos nuevos o modificados:

- `n8n-values.yaml`
- `n8n-certificate.yaml`

Pendiente para completar esta fase:

1. Aplicar `n8n-certificate.yaml`
2. Ejecutar `helm upgrade --install` con el nuevo `n8n-values.yaml`
3. Obtener la IP del nuevo `Ingress`
4. Crear el registro DNS `A` para `n8n.cristobalht.cl` en Google Cloud DNS
5. Esperar provisión del certificado
6. Entrar por `https://n8n.cristobalht.cl`

## Actualización 2026-04-28

### Estado actual de n8n por dominio

- Se aplicó `n8n-certificate.yaml`
- Se ejecutó `helm upgrade --install` con la nueva configuración
- El `Ingress` de n8n obtuvo IP pública:

`34.49.36.147`

- Se confirmó que `n8n.cristobalht.cl` ya responde y que se puede entrar a n8n por dominio

### DNS y certificado

- El dominio `cristobalht.cl` usa nameservers de Google:
  - `ns-cloud-d1.googledomains.com`
  - `ns-cloud-d2.googledomains.com`
  - `ns-cloud-d3.googledomains.com`
  - `ns-cloud-d4.googledomains.com`
- Por lo tanto, los subdominios deben administrarse en Google Cloud DNS
- El registro esperado para n8n fue:
  - nombre: `n8n`
  - tipo: `A`
  - valor: `34.49.36.147`
- El certificado administrado quedó en proceso de provisión mientras se resolvía DNS y luego el acceso por dominio quedó operativo

### Hallazgo importante de seguridad

Se detectó una preocupación válida:

- cualquier persona puede llegar a `https://n8n.cristobalht.cl`

Aunque eso no implica que puedan iniciar sesión, el panel de administración sigue expuesto públicamente y eso no es deseable para producción.

### Decisión de arquitectura recomendada

No conviene proteger “todo n8n” de la misma forma, porque el proyecto necesitará webhooks públicos para WhatsApp.

Arquitectura recomendada:

- `n8n-admin.cristobalht.cl`
  - acceso solo para el administrador
  - proteger con IAP o allowlist de IP
- `n8n-hooks.cristobalht.cl`
  - público
  - usado solo para webhooks (WhatsApp, callbacks, etc.)

Idea clave:

- panel admin privado
- endpoints de automatización públicos pero controlados

### Recomendación de seguridad

La mejor opción general para el panel admin parece ser `IAP` con Google, porque:

- no depende de una IP fija
- permite acceso solo a cuentas autorizadas
- es más cómodo que una allowlist si cambias de red

Pero antes de implementarlo, conviene definir si realmente separaremos `admin` y `hooks` en dos entradas distintas, que es lo recomendado.

### Siguiente paso recomendado

Retomar desde aquí:

1. Diseñar la separación entre `admin` y `hooks`
2. Elegir el mecanismo de protección del panel admin (`IAP` recomendado)
3. Aplicar esa separación antes de avanzar con WhatsApp
4. Después continuar con el rediseño dinámico del blog
