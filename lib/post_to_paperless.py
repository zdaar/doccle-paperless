import os
import requests
import logging

# Initialize the logger
logger = logging.getLogger(__name__)


class PaperlessUploadError(Exception):
    """Custom exception for Paperless upload errors."""

    pass


def post_to_paperless(file_path):
    paperless_url = os.getenv("PAPERLESS_URL")
    paperless_token = os.getenv("PAPERLESS_TOKEN")

    # Check if Paperless URL and Token are provided
    if not paperless_url or not paperless_token:
        error_msg = "Paperless URL or Token is not set in environment variables."
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Ensure the URL ends with a trailing slash
    post_url = f"{paperless_url.rstrip('/')}/api/documents/post_document/"
    headers = {"Authorization": f"Token {paperless_token}"}

    # Log the environment variables for debugging (Remove in production)
    logger.debug(f"PAPERLESS_URL: {paperless_url}, PAPERLESS_TOKEN: {paperless_token}")

    try:
        with open(file_path, "rb") as file:
            response = requests.post(
                post_url, headers=headers, files={"document": file}
            )

            # Success response from Paperless
            if 200 <= response.status_code < 300:
                logger.info(f"Document posted successfully: {file_path}")
            else:
                # Log detailed error message from Paperless
                error_msg = (
                    f"Failed to post document: {response.status_code} - {response.text}"
                )
                logger.error(error_msg)
                raise PaperlessUploadError(error_msg)

    except FileNotFoundError:
        error_msg = f"File not found: {file_path}"
        logger.error(error_msg)
        raise PaperlessUploadError(error_msg)

    except requests.exceptions.RequestException as e:
        error_msg = f"Error posting document to Paperless: {file_path}. Error: {str(e)}"
        logger.error(error_msg)
        raise PaperlessUploadError(error_msg)

    except Exception as e:
        # Generic error handling for any unexpected exceptions
        error_msg = f"An unexpected error occurred: {str(e)}"
        logger.error(error_msg)
        raise PaperlessUploadError(error_msg)
