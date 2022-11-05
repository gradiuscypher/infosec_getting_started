#!/usr/bin/env python3
import os

md_file_header = f"""

| URL | Title | Description |
| --- | --- | --- |
"""


def create_md_file(dir_list):
    # get the title
    title = dir_list[0].split("_")[1]

    # check to see if the md file exists, if not, create it
    if os.path.isfile(f"books/link_collection/{title}.md"):
        print(f"title exists: {title}")
    else:
        print(f"title doesn't exist: {title}\nfiles:{dir_list[2]}")

        content_list = []
        for file_name in dir_list[2]:
            file_name = f"{dir_list[0]}/{file_name}"
            content_list.append(parse_md_file(file_name))

        with open(f"books/link_collection/{title}.md", "w") as out_md:
            out_md.write(f"# {title}")
            out_md.write(md_file_header)

            for entry in content_list:
                out_md.write(f'| [{entry["target"]}]({entry["target"]}) | {entry["name"]} | {entry["short_description"]} |\n')


def parse_md_file(file_name):
    import_fields = ["name", "target", "short_description"]
    md_dict = {}
    with open(file_name) as md_file:
        for line in md_file:
            split_line = line.split(":")
            if not line.startswith("---") and split_line[0] in import_fields:
                md_dict[split_line[0]] = "".join(split_line[1:]).strip()
    return md_dict


def iterate_over_files():
    # iterate through the books folder, uploading each directory as a book, overwrite any existing books
    # for each .md file, upload a page with the title from the first line of the .md file, overwrite any already existing pages
    book_dirs = os.walk("collections")

    for dir in book_dirs:
        # this means that there isn't any sub directories, so it's a book dir
        if not len(dir[1]):
            create_md_file(dir)


if __name__ == "__main__":
    iterate_over_files()
