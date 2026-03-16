# ============================================================
# paginaweb.py — Aplicación Flask del portafolio DevOps
# 
# Flask es un framework web minimalista para Python.
# Este archivo es el "cerebro" del sitio: define las rutas URL
# y qué template HTML renderizar para cada una.
# ============================================================

from flask import Flask, render_template, request

# --- Inicialización ---
# Flask(__name__) crea la aplicación usando el directorio actual
# como punto de referencia para buscar templates y archivos estáticos
app = Flask(__name__)


# --- RUTA HOME: "/" ---
# El decorador @app.route() indica qué URL activa esta función.
# render_template() busca el archivo en la carpeta "templates/"
@app.route("/")
def home():
    return render_template("home.html")


# --- RUTA PROYECTOS: "/proyectos" ---
# Página con el listado detallado de proyectos DevOps
@app.route("/proyectos")
def proyectos():
    return render_template("proyectos.html")


# --- RUTA STACK: "/stack" ---
# Página con el stack tecnológico y herramientas usadas
@app.route("/stack")
def stack():
    return render_template("stack.html")


# --- RUTA BLOG: "/blog" ---
# Listado de artículos técnicos del blog
@app.route("/blog")
def blog():
    return render_template("blog.html")


# --- RUTA ABOUT: "/about" ---
# Página "Sobre Mí" con información personal y redes sociales
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/blog/primera-pagina-web")
def blog_primera_pagina():
    return render_template("blog/primera-pagina-web.html")

@app.route("/blog/menu-cocineria")
def blog_menu_cocineria():
    return render_template("blog/menu-cocineria.html")

# --- INICIO DE LA APLICACIÓN ---
# Este bloque solo se ejecuta cuando corres el script directamente
# (no cuando lo importa otro módulo, como en producción con Gunicorn)
if __name__ == "__main__":
    # debug=True: muestra errores detallados y recarga automáticamente al guardar
    # host='0.0.0.0': escucha en todas las interfaces de red (necesario para Docker/K8s)
    # port=8080: puerto donde corre la app (alineado con el containerPort del deployment.yaml)
    app.run(debug=True, host='0.0.0.0', port=8080)
