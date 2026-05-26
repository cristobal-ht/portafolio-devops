# Session Notes 2026-04-30

## Estado del proyecto

Se validó la primera integración real:

`n8n -> GitHub`

## Lo que se logró

- Se creó correctamente la credencial de GitHub en n8n usando token fine-grained.
- Se construyó un workflow mínimo en n8n.
- El workflow creó un archivo Markdown del blog en GitHub.
- El archivo fue enviado a la rama:

`staging`

- El archivo generado por n8n ya se ve en el repositorio.

## Qué significa esto

Ya quedó comprobado que:

- n8n puede autenticarse con GitHub
- n8n puede escribir contenido en la nueva estructura del blog
- el formato `content/posts/*.md` funciona bien para automatización

Este era el paso crítico antes de integrar Gemini.

## Fase completada

Se puede considerar completada la prueba mínima:

`n8n -> GitHub -> crear post draft`

## Siguiente paso recomendado

Antes de conectar Gemini, conviene mejorar el workflow de n8n para que no cree un archivo “fijo”, sino un draft reutilizable y paramétrico.

## Qué debería hacer el siguiente workflow

Construir dinámicamente:

- `title`
- `slug`
- `date`
- `summary`
- `image`
- `tags`
- `status`
- `body`

Y luego generar el archivo Markdown automáticamente.

## Orden recomendado al retomar

1. convertir el workflow actual en una plantilla reutilizable
2. hacer que el contenido del `.md` se construya desde variables
3. luego conectar Gemini para que rellene esas variables
4. después integrar WhatsApp

## Idea del siguiente avance

Pasar de:

- workflow fijo

a:

- workflow generador de drafts

Eso dejará el sistema listo para que Gemini solo entregue los textos y metadatos.
