import os
import requests
import logging


# Custom exception for clarity in error handling
class PaperlessUploadError(Exception):
    pass


logger = logging.getLogger(__name__)


def post_to_paperless(file_path):
    paperless_url = os.getenv("PAPERLESS_URL")
    paperless_token = os.getenv("PAPERLESS_TOKEN")

    # Early exit if critical configuration is missing
    if not paperless_url or not paperless_token:
        logger.error("Paperless URL or Token is not set in environment variables.")
        raise ValueError("Paperless URL or Token is not set in environment variables.")

    post_url = f"{paperless_url.rstrip('/')}/api/documents/post_document/"
    headers = {"Authorization": f"Token {paperless_token}"}

    success = False
    error_message = ""

    try:
        with open(file_path, "rb") as file:
            response = requests.post(
                post_url, headers=headers, files={"document": file}
            )
            # Check for success using the entire 2xx range
            if 200 <= response.status_code < 300:
                success = True
                logger.info(f"Document posted successfully: {file_path}")
            else:
                error_message = (
                    f"Failed to post document: {response.status_code} - {response.text}"
                )
                logger.error(error_message)
                raise PaperlessUploadError(error_message)
    except FileNotFoundError as e:
        error_message = f"File not found: {file_path}. Error: {str(e)}"
    except IOError as e:
        error_message = f"Error reading file: {file_path}. Error: {str(e)}"
    except requests.exceptions.RequestException as e:
        error_message = (
            f"Error posting document to Paperless: {file_path}. Error: {str(e)}"
        )
    except Exception as e:  # Catch-all for unexpected exceptions
        error_message = f"An unexpected error occurred: {str(e)}"

    if not success:
        logger.error(error_message)
        raise PaperlessUploadError(error_message)
