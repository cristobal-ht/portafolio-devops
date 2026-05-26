# Session Notes 2026-04-28 End

## Estado general

Se cerraron dos bloques grandes del proyecto:

1. Seguridad y separación de accesos de n8n
2. Refactor del blog a contenido dinámico con Markdown

## n8n: estado actual

### Subdominios activos

- `n8n-admin.cristobalht.cl`
- `n8n-hooks.cristobalht.cl`

### Certificados

Ambos certificados quedaron en estado `Active`.

### Seguridad aplicada

- `n8n-admin` separado de `n8n-hooks`
- `n8n-admin` protegido con Cloud Armor allowlist
- `n8n-hooks` público para webhooks
- n8n ya quedó configurado con:
  - `N8N_EDITOR_BASE_URL=https://n8n-admin.cristobalht.cl`
  - `N8N_HOST=n8n-admin.cristobalht.cl`
  - `WEBHOOK_URL=https://n8n-hooks.cristobalht.cl/`

### Estado del pod

- pod nuevo de n8n en `Running 1/1`
- sin reinicios

## Blog dinámico: estado actual

### Cambios implementados

- `paginaweb.py`
  - carga posts desde `content/posts/*.md`
  - genera `/blog` dinámicamente
  - usa `/blog/<slug>`
  - agrega `/preview/<slug>`

- `templates/blog.html`
  - lista automáticamente los posts publicados

- `templates/blog_post.html`
  - nueva plantilla única de post

- `content/posts/`
  - ya contiene dos posts migrados desde los templates antiguos

- `Dockerfile`
  - ahora instala `markdown`

- `static/css/main.css`
  - tiene estilos para el artículo dinámico

### Verificación realizada

Se construyó y ejecutó el contenedor:

- `docker build -t paginaweb:blog-dynamic .`
- `docker run -p 8080:8080 paginaweb:blog-dynamic`

Se comprobó que cargan bien:

- `/blog`
- `/blog/primera-pagina-web`
- `/blog/menu-cocineria`

## Idea del proyecto confirmada

El blog ya quedó con una estructura apta para automatización.

Eso significa que n8n ya no tendrá que editar:

- rutas Flask
- templates HTML del índice
- templates HTML individuales

Ahora bastará con crear o modificar un solo archivo Markdown.

## Siguiente paso recomendado para mañana

Empezar el flujo mínimo:

`n8n -> GitHub -> crear post Markdown de prueba`

## Objetivo de esa siguiente fase

No usar IA todavía.

Solo comprobar que n8n puede:

1. conectarse a GitHub
2. crear un archivo en este repo
3. seguir la estructura nueva del blog
4. dejar listo el terreno para Gemini

## Archivo de prueba sugerido

Ruta:

`content/posts/2026-04-28-post-prueba-desde-n8n.md`

Contenido sugerido:

```md
---
title: "Post de prueba desde n8n"
slug: "post-prueba-desde-n8n"
date: "2026-04-28"
summary: "Este post fue creado automáticamente desde n8n para validar el flujo hacia GitHub."
image: ""
tags: DevOps, n8n, GitHub
status: draft
---

Este es un post de prueba generado automáticamente desde n8n.
```

## Recomendación de seguridad para GitHub

Empezar con:

- token fine-grained de GitHub

con permisos mínimos para este repo, solo para avanzar rápido y aprender.

Más adelante se puede migrar a GitHub App.
