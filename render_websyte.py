import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def on_reload():
    with open(r"books\books.json", "r") as file:
        books = file.read()

    books_description = json.loads(books)

    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("template.html")

    render_page = template.render(books=books_description)

    with open("index.html", "w", encoding="utf8") as file:
        file.write(render_page)


def main():
    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".")


if __name__ == "__main__":
    main()
