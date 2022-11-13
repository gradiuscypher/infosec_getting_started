#!/usr/bin/env python3

# TODO: set the header image when creating a book
# TODO: deduplicate or update book rather than deleting and recreating every time
# TODO: generate the readme.md with each page link for easier reading on Github
# ref: https://demo.bookstackapp.com/api/docs

import json
import os
import requests
import traceback
from sys import argv

api_url = "https://docs.grds.io/api"
headers = {
    "Authorization": f"Token {os.environ.get('TOKEN_ID')}:{os.environ.get('TOKEN_SECRET')}"
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
            print(result.json())
            return None

    except:
        print(f"Unable to create book: {name}")
        print(traceback.format_exc())
        return None


def update_page(book_id, page_id, page_title, markdown):
    endpoint = f"/pages/{page_id}"

    try:
        page_body = {
            "book_id": book_id,
            "name": page_title,
            "markdown": markdown
        }

        result = requests.put(api_url + endpoint, json=page_body, headers=headers)
        return result.json()["id"]

    except:
        print(f"Unable to update page: {page_title}")
        print(traceback.format_exc())
        return None


def delete_page(page_id):
    endpoint = f"/pages/{page_id}"

    try:
        result = requests.delete(api_url + endpoint, headers=headers)
        return (result.status_code, result.text)
    except:
        print(f"Unable to delete page: {page_id}")
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
            print(result.json())
            return None

    except:
        print(f"Unable to create page: {name}")
        print(traceback.format_exc())
        return None


def get_current_books():
    endpoint = "/books"
    books = {}

    try:
        result = requests.get(api_url + endpoint, headers=headers)

        if result.status_code == 200:
            data = result.json()["data"]
            for book in data:
                books[book["name"]] = book["id"]
        return books

    except:
        print(f"Unable to get books")
        print(traceback.format_exc())
        return None


def get_current_pages():
    endpoint = "/pages"
    pages = {}

    try:
        result = requests.get(api_url + endpoint, headers=headers)
        if result.status_code == 200:
            data = result.json()["data"]
            for page in data:
                pages[page["name"]] = page["id"]

        return pages

    except:
        print(f"Unable to get Pages")
        print(traceback.format_exc())
        return None


def process_book_dir(book_tuple):
    book_dir = book_tuple[0]
    file_names = book_tuple[2]

    with open(book_dir + "/metadata.json") as json_file:
        metadata = json.loads(json_file.read())

        # create the book
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


def upload_page(full_page_filename, delete=False):
    # get a list of all the current pages and books so that we can update them when appropriate
    current_pages = get_current_pages()
    current_books = get_current_books()

    page_title = full_page_filename.split("/")[-1].split(".")[0].replace("_", " ").title()

    # delete the page if the update action was delete
    if delete:
        if page_title in current_pages:
            page_id = current_pages[page_title]
            delete_page(page_id)
        else:
            print("Page ID doesn't exist")

    else:
        # open the metadata file for the book
        book_dir = ("/").join(full_page_filename.split("/")[:-1])

        with open(book_dir + "/metadata.json") as json_file:
            metadata = json.loads(json_file.read())
            book_title = metadata["title"]
            book_description = metadata["description"]

            # create the book if it doesn't already exist
            if book_title not in current_books.keys():
                book_id = create_book(book_title, book_description)
            else:
                book_id = current_books[book_title]

            # create the page if it doesn't exist, otherwise update it
            with open(f"{full_page_filename}") as md_page:
                # skip the first line since that's the title in markdown
                md_page.readline()

                # get the title and the rest of the content
                page_content = md_page.read()

                if page_title not in current_pages.keys():
                    create_page(book_id, page_title, page_content)
                else:
                    page_id = current_pages[page_title]
                    update_page(book_id, page_id, page_title, page_content)


def run_cicd(added_files, modified_files, deleted_files):
    print("Running CICD...")
    # when new files are added, determine if they're a new or already existing book, then add the pages
    added_files = json.loads(added_files)
    print(f"Added: {added_files}")
    for filename in added_files:
        if filename.endswith(".md"):
            upload_page(filename)

    # when files are modified, determine which book and page was modified, then upload the new contents
    modified_files = json.loads(modified_files)
    print(f"Modified: {modified_files}")
    for filename in modified_files:
        if filename.endswith(".md"):
            upload_page(filename)

    # when files are deleted, determine which book and page was deleted, then delete those. If an entire directory was deleted, remove the book as well
    deleted_files = json.loads(deleted_files)
    print(f"Deleted: {deleted_files}")
    for filename in deleted_files:
        if filename.endswith(".md"):
            upload_page(filename, delete=True)


if __name__ == "__main__":
    # iterate_over_files()
    added_files = argv[1]
    modified_files = argv[2]
    deleted_files = argv[3]

    run_cicd(added_files, modified_files, deleted_files)
