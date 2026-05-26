# Blog Dynamic Notes

Fecha: 2026-04-28

## Objetivo

Convertir el blog del portafolio desde rutas y templates manuales a una estructura basada en archivos Markdown con front matter.

## Cambios realizados

- `paginaweb.py`
  - ahora carga posts desde `content/posts/*.md`
  - genera el índice `/blog` dinámicamente
  - usa una ruta única `/blog/<slug>`
  - agrega `/preview/<slug>` para ver drafts

- `templates/blog.html`
  - ahora itera sobre la lista de posts publicados

- `templates/blog_post.html`
  - nueva plantilla única para cualquier post

- `content/posts/`
  - se migraron los dos posts existentes a Markdown

- `Dockerfile`
  - se agregó la librería `markdown`

- `static/css/main.css`
  - se agregaron estilos para el artículo dinámico

## Estructura nueva

Cada post vive en un archivo `.md` con metadata simple:

```md
---
title: "Título"
slug: "slug-del-post"
date: "2026-04-28"
summary: "Resumen corto"
image: "/static/img/imagen.jpg"
tags: DevOps, n8n, GKE
status: published
---

Contenido en Markdown...
```

## Ventaja principal

n8n ya no necesitará editar rutas y templates manuales. Para crear un post nuevo bastará con crear o modificar un solo archivo Markdown.

## Pendiente

- reconstruir la imagen Docker de la app para incluir `markdown`
- probar visualmente `/blog` y `/blog/<slug>`
- decidir si se conservan o eliminan los templates antiguos en `templates/blog/`
- luego conectar este formato con el flujo `n8n -> GitHub`
