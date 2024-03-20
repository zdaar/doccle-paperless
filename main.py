import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from lib.doccle import Connector
import json
from pathvalidate import sanitize_filename
from lib.post_to_paperless import post_to_paperless
from flask import Flask, jsonify
import threading
import time
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Record the start time of the application
start_time = time.time()


@app.route("/health", methods=["GET"])
def health_check():
    uptime_seconds = time.time() - start_time
    return jsonify(
        {
            "status": "UP",
            "uptime": str(timedelta(seconds=int(uptime_seconds))),
        }
    )


print("Starting Flask application...")


def run_app():
    app.run(host="0.0.0.0", port=5000)


# Configure logging
logs_directory = "logs"
os.makedirs(logs_directory, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(logs_directory, f"doccle_paperless_{timestamp}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

print("Application initialized, setting up environment...")


def is_valid_pdf(content):
    return content.startswith(b"%PDF-")


def generate_friendly_filename(document):
    sanitized_name = sanitize_filename(document["name"])
    publish_date = datetime.strptime(
        document["publishDate"], "%Y-%m-%dT%H:%M:%SZ"
    ).strftime("%Y-%m-%d")
    base_filename = f"{sanitized_name}_{publish_date}"
    extension = "PDF"  # Assuming the file type is always PDF
    return f"{base_filename}.{extension}"


# Load environment variables and initialize Connector
load_dotenv()
doccle_username = os.getenv("DOCCLE_USERNAME")
doccle_password = os.getenv("DOCCLE_PASSWORD")
if not doccle_username or not doccle_password:
    logger.error("Doccle credentials not found in environment variables")
    raise ValueError("Doccle credentials not found in environment variables")

docs = Connector(doccle_username, doccle_password)

# Main logic

print("Starting main application loop...")


def main():
    # Fetch all new documents and prepare the download directory
    new_documents = docs.get_documents(
        only_new=True,
    )  # You can add a max_docs parameter to limit the number of documents to download
    download_directory = "downloaded_documents"
    os.makedirs(download_directory, exist_ok=True)

    if new_documents:
        for doc in new_documents["documents"]:
            document_content = docs.download_document(doc["contentUrl"])

            if document_content and is_valid_pdf(document_content):
                friendly_filename = generate_friendly_filename(doc)
                pdf_file_path = os.path.join(download_directory, friendly_filename)

                with open(pdf_file_path, "wb") as pdf_file:
                    pdf_file.write(document_content)
                logger.info(f"Downloaded PDF: {friendly_filename}")

                json_file_name = friendly_filename.rsplit(".", 1)[0] + ".json"
                json_file_path = os.path.join(download_directory, json_file_name)

                with open(json_file_path, "w", encoding="utf-8") as json_file:
                    json.dump(doc, json_file, ensure_ascii=False, indent=4)
                logger.info(f"Saved document data as JSON: {json_file_name}")

                try:
                    post_to_paperless(pdf_file_path)
                    logger.info(f"Document posted to Paperless: {friendly_filename}")
                except Exception as e:
                    logger.error(
                        f"Failed to post document to Paperless: {friendly_filename}. Error: {str(e)}"
                    )

                # Optionally archive the document if necessary
                docs.archive_document(doc)
                logger.info(f"Document Archived: {friendly_filename}")

            else:
                logger.error(
                    f"Failed to download or invalid PDF: {doc.get('name', 'Unknown document')}"
                )

    else:
        logger.info("No new documents to download.")


if __name__ == "__main__":

    load_dotenv()
    print("DOCCLE_USERNAME:", os.getenv("DOCCLE_USERNAME"))
    print("DOCCLE_PASSWORD:", os.getenv("DOCCLE_PASSWORD"))

    threading.Thread(target=run_app, daemon=True).start()

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        main, "interval", seconds=int(os.getenv("FETCH_INTERVAL", "3600"))
    )
    scheduler.start()

    # Start the main function in a background thread
    threading.Thread(target=main, daemon=True).start()

    try:
        # Keep the main thread alive with a sleep loop
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Application shutdown requested via KeyboardInterrupt.")
