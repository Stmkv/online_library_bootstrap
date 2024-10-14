import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html"])
    )
    template = env.get_template("template.html")

    with open(r"books\books.json", "r", encoding="utf-8") as file:
        books_description = json.load(file)

    books_descriptions = list(chunked(books_description, 20))
    pages_amount = len(books_descriptions)
    for page_number, books_on_page in enumerate(books_descriptions, start=1):
        render_page = template.render(
            books=list(chunked(books_on_page, 2)),
            pages_amount=pages_amount,
            page_number=page_number,
        )
        os.makedirs("pages/", exist_ok=True)
        with open(
            os.path.join("pages/", f"index{page_number}.html"), "w", encoding="utf8"
        ) as file:
            file.write(render_page)


def main():
    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".")


if __name__ == "__main__":
    main()
