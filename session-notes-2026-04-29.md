# Session Notes 2026-04-29

## Punto de continuidad

Quedó cerrada la fase de:

- seguridad base de n8n
- separación `admin` / `hooks`
- refactor del blog a Markdown dinámico

El siguiente paso del proyecto ya quedó definido:

`n8n -> GitHub -> crear post Markdown de prueba`

## Estado del sistema

### n8n

- `n8n-admin.cristobalht.cl` operativo
- `n8n-hooks.cristobalht.cl` operativo
- certificados `Active`
- `Cloud Armor` aplicado al panel admin
- `WEBHOOK_URL` apuntando a `https://n8n-hooks.cristobalht.cl/`

### Blog

La app Flask ya usa:

- `content/posts/*.md`
- front matter simple
- ruta dinámica `/blog/<slug>`
- preview `/preview/<slug>`

### Verificación ya hecha

El contenedor se construyó y corrió correctamente:

- `docker build -t paginaweb:blog-dynamic .`
- `docker run -p 8080:8080 paginaweb:blog-dynamic`

Y cargaron bien:

- `/blog`
- `/blog/primera-pagina-web`
- `/blog/menu-cocineria`

## Siguiente fase

### Objetivo

Probar que n8n puede crear un archivo Markdown nuevo en este repositorio siguiendo la nueva estructura del blog.

### Aún no usar

- Gemini
- WhatsApp

Primero se validará solo:

- `n8n -> GitHub`

## Recomendación para GitHub

Empezar con un **fine-grained personal access token** con acceso solo a este repositorio.

Permisos recomendados:

- `Contents`: `Read and write`
- `Metadata`: `Read`
- opcional para después:
  - `Pull requests`: `Read and write`

## Archivo de prueba sugerido

Ruta:

`content/posts/2026-04-29-post-prueba-desde-n8n.md`

Contenido:

```md
---
title: "Post de prueba desde n8n"
slug: "post-prueba-desde-n8n"
date: "2026-04-29"
summary: "Este post fue creado automáticamente desde n8n para validar el flujo hacia GitHub."
image: ""
tags: DevOps, n8n, GitHub
status: draft
---

Este es un post de prueba generado automáticamente desde n8n.
```

## Flujo mínimo a construir en n8n

1. `Manual Trigger`
2. nodo para construir:
   - ruta del archivo
   - contenido Markdown
3. nodo `GitHub` para crear el archivo en el repo

## Recomendación de seguridad para la primera prueba

No escribir en producción todavía.

Mejor usar:

- una rama de prueba, por ejemplo `n8n-test`

## Próximo paso exacto al retomar

1. Crear el token fine-grained en GitHub
2. Guardarlo como credencial en n8n
3. Crear el workflow manual mínimo
4. Ejecutarlo y verificar que aparece el archivo en GitHub
