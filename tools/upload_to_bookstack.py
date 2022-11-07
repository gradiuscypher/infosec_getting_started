#!/usr/bin/env python3

# TODO: set the header image when creating a book
# TODO: deduplicate or update book rather than deleting and recreating every time
# TODO: generate the readme.md with each page link for easier reading on Github
# ref: https://demo.bookstackapp.com/api/docs

import config
import json
import os
import requests
import traceback
from sys import argv

api_url = "https://docs.grds.io/api"
headers = {
    "Authorization": f"Token {config.token_id}:{config.token_secret}"
}


def create_book(name, description):
    endpoint = "/books"

    try:
        book_body = {
            "name": name,
            "description": description
        }
        result = requests.post(api_url + endpoint, json=book_body, headers=headers)
        if result.status_code == 200:
            book_id = result.json()["id"]
            print(f"Book created successfully: {book_id}")
            return book_id
        else:
            print("Unable to create book.")
            return None

    except:
        print(f"Unable to create book: {name}")
        print(traceback.format_exc())
        return None


def create_page(book_id, name, markdown):
    endpoint = "/pages"

    try:
        page_body = {
            "book_id": book_id,
            "name": name,
            "markdown": markdown
        }
        result = requests.post(api_url + endpoint, json=page_body, headers=headers)
        if result.status_code == 200:
            page_id = result.json()["id"]
            print(f"Page created successfully: {page_id}")
            return page_id
        else:
            print("Unable to create page.")
            return None

    except:
        print(f"Unable to create page: {name}")
        print(traceback.format_exc())
        return None


def process_book_dir(book_tuple):
    book_dir = book_tuple[0]
    file_names = book_tuple[2]

    with open(book_dir + "/metadata.json") as json_file:
        metadata = json.loads(json_file.read())

        # # create the book
        book_id = create_book(metadata["title"], metadata["description"])

        # start adding pages
        if book_id:

            for page_filename in file_names:
                if page_filename.endswith(".md") and page_filename != "readme.md":
                    with open(f"{book_dir}/{page_filename}") as md_page:
                        page_title = md_page.readline().strip().replace("# ", "")
                        page_content = md_page.read()
                        create_page(book_id, page_title, page_content)
        else:
            print("The book wasn't created.")


def iterate_over_files():
    # iterate through the books folder, uploading each directory as a book, overwrite any existing books
    # for each .md file, upload a page with the title from the first line of the .md file, overwrite any already existing pages
    book_dirs = os.walk("books")

    for dir in book_dirs:
        # this means that there isn't any sub directories, so it's a book dir
        if not len(dir[1]):
            process_book_dir(dir)


def run_cicd(added_files, modified_files, deleted_files):
    print("Running CICD...")
    # when new files are added, determine if they're a new or already existing book, then add the pages
    added_files = json.loads(added_files)
    print(f"Added: {added_files}")

    # when files are modified, determine which book and page was modified, then upload the new contents
    modified_files = json.loads(modified_files)
    print(f"Modified: {modified_files}")

    # when files are deleted, determine which book and page was deleted, then delete those. If an entire directory was deleted, remove the book as well
    deleted_files = json.loads(deleted_files)
    print(f"Deleted: {deleted_files}")


if __name__ == "__main__":
    # iterate_over_files()
    added_files = argv[1]
    modified_files = argv[2]
    deleted_files = argv[3]

    run_cicd(added_files, modified_files, deleted_files)
