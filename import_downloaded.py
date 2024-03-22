import os

from lib.post_to_paperless import (
    post_to_paperless,
)

download_directory = "downloaded_documents"

from dotenv import load_dotenv

load_dotenv()


def retry_import_documents(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".PDF") or filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            try:
                post_to_paperless(file_path)
                print(f"Document posted successfully: {filename}")
            except Exception as e:
                print(f"Failed to post document: {filename}. Error: {e}")


if __name__ == "__main__":
    retry_import_documents(download_directory)
