---
title: "Cómo Creé mi Primera Página Web"
slug: "primera-pagina-web"
date: "2026-03-17"
summary: "Cómo construí este portafolio con Flask, Docker y Kubernetes como parte de mi camino hacia DevOps."
image: "/static/img/blog-img-1.jpg"
tags: Flask, Docker, Kubernetes
status: published
---

Este proyecto nació con un objetivo claro: tener un portafolio propio donde mostrar mi transición hacia el mundo DevOps.

## El punto de partida: Python y Flask

Elegí **Python con Flask** porque es un framework minimalista, perfecto para aprender. Flask no te da nada "mágico": tú defines cada ruta, cada template y cada respuesta. Eso lo hace ideal para entender cómo funciona la web por dentro.

El archivo principal es `paginaweb.py`. Cada función con `@app.route()` define una URL de la página. Por ejemplo:

```python
@app.route("/")
def home():
    return render_template("home.html")
```

## Templates con Jinja2

Flask usa **Jinja2** para los templates HTML. Lo más útil fue la herencia de templates: creé un `layout.html` con la navbar y el footer, y cada página solo define su contenido propio usando bloques. Así evité repetir código en cada archivo.

## Dockerización

Una vez funcionando localmente, el siguiente paso fue crear el **Dockerfile**. La idea es simple: empaquetar la app y todas sus dependencias en una imagen que corra igual en cualquier entorno.

```bash
docker build -t paginaweb:1.0 .
docker run -p 8080:8080 paginaweb:1.0
```

## Despliegue en Kubernetes

El paso final fue desplegar la imagen en un clúster local con **Kind**. Creé un `deployment.yaml` que define el contenedor y el servicio, y un script `despliege.sh` que automatiza todo el proceso: build, carga al clúster y port-forward.

## Conclusión

No es solo teoría. Es un proyecto real, corriendo en Kubernetes, que puedo mostrar como parte de mi camino hacia DevOps.
