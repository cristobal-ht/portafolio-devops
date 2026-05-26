from datetime import date
from functools import lru_cache
from pathlib import Path
import re

from flask import Flask, abort, render_template
from markdown import markdown


app = Flask(__name__)
POSTS_DIR = Path(__file__).parent / "content" / "posts"


def _strip_quotes(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _parse_tags(raw_value):
    cleaned = raw_value.strip()
    if cleaned.startswith("[") and cleaned.endswith("]"):
        cleaned = cleaned[1:-1]
    return [tag.strip().strip('"').strip("'") for tag in cleaned.split(",") if tag.strip()]


def _excerpt_from_markdown(body, length=180):
    plain_text = re.sub(r"[#*_>`-]", " ", body)
    plain_text = re.sub(r"\s+", " ", plain_text).strip()
    return plain_text[:length].rstrip() + ("..." if len(plain_text) > length else "")


def _load_post_file(path):
    raw_text = path.read_text(encoding="utf-8")
    metadata = {}
    body = raw_text

    if raw_text.startswith("---"):
        parts = raw_text.split("---", 2)
        if len(parts) == 3:
            _, front_matter, body = parts
            for line in front_matter.strip().splitlines():
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                metadata[key.strip()] = _strip_quotes(value.strip())

    slug = metadata.get("slug", path.stem)
    date_value = metadata.get("date", date.today().isoformat())

    try:
        parsed_date = date.fromisoformat(date_value)
    except ValueError:
        parsed_date = date.today()
        date_value = parsed_date.isoformat()

    tags = _parse_tags(metadata.get("tags", ""))
    summary = metadata.get("summary") or _excerpt_from_markdown(body)
    title = metadata.get("title", slug.replace("-", " ").title())
    status = metadata.get("status", "draft").lower()
    image = metadata.get("image", "").strip()

    return {
        "title": title,
        "slug": slug,
        "date": parsed_date,
        "date_display": date_value,
        "summary": summary,
        "image": image,
        "tags": tags,
        "status": status,
        "content_html": markdown(body.strip(), extensions=["fenced_code", "tables"]),
    }


@lru_cache(maxsize=1)
def load_posts():
    posts = []

    if POSTS_DIR.exists():
        for path in POSTS_DIR.glob("*.md"):
            posts.append(_load_post_file(path))

    posts.sort(key=lambda post: post["date"], reverse=True)
    return posts


def get_post_by_slug(slug, include_drafts=False):
    for post in load_posts():
        if post["slug"] != slug:
            continue
        if post["status"] != "published" and not include_drafts:
            return None
        return post
    return None


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/proyectos")
def proyectos():
    return render_template("proyectos.html")


@app.route("/stack")
def stack():
    return render_template("stack.html")


@app.route("/blog")
def blog():
    posts = [post for post in load_posts() if post["status"] == "published"]
    return render_template("blog.html", posts=posts)


@app.route("/blog/<slug>")
def blog_post(slug):
    post = get_post_by_slug(slug)
    if not post:
        abort(404)
    return render_template("blog_post.html", post=post)


@app.route("/preview/<slug>")
def preview_post(slug):
    post = get_post_by_slug(slug, include_drafts=True)
    if not post:
        abort(404)
    return render_template("blog_post.html", post=post, preview_mode=True)


@app.route("/about")
def about():
    return render_template("about.html")
# Ruta: Política de Privacidad — Bot WhatsApp
@app.route("/politica-de-privacidad-bot-whatsapp")
def politica_privacidad():
    return render_template("politica-privacidad.html")

# Ruta: Términos del Servicio — Bot WhatsApp
@app.route("/terminos-bot-whatsapp")
def terminos_servicio():
    return render_template("terminos-servicio.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
