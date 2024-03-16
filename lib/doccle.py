# This code uses part of the py-doccle library created by Steve Gilissen
# https://github.com/sgilissen/py-doccle


import warnings
import requests
from requests.auth import HTTPBasicAuth


class Connector:
    def __init__(self, username="", password=""):
        self.base_url = "https://secure.doccle.be/doccle-euui/rest/v2/"
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()

    def get_documents(self, only_new=False, max_docs=0):
        """
        Fetches the list of documents and returns a dictionary with all relevant info.
        :param only_new: Boolean: Only fetch the new documents.
        :param max_docs: Maximum number of documents to download. 0 = no limitation.
        :return: Dictionary of documents or None.
        """
        page_size_str = ""
        if max_docs > 0:
            page_size_str = f"&pageSize={max_docs}"

        if only_new:
            url = (
                self.base_url
                + "documents/new?lang=en&order=DESC&page=1&sort=date"
                + page_size_str
            )
        else:
            url = (
                self.base_url
                + "documents?lang=en&order=DESC&page=1&sort=date"
                + page_size_str
            )

        try:
            response = self.session.get(url, auth=self.auth)
            response.raise_for_status()  # This will raise an exception for HTTP error responses
            data = response.json()

            # Directly return the list of documents without simplifying them into doc_dict
            return {"documents": data["documents"]}
        except requests.exceptions.RequestException as err:
            warnings.warn(str(err))
            return None

    def download_document(self, file_url):
        """
        Downloads the document and returns it as bytes.
        :param file_url: String: The full URL to the document content.
        :return: Document content as bytes or None.
        """
        try:
            # Use the provided file_url directly, assuming it's complete and correct
            response = self.session.get(file_url, auth=self.auth)

            # Check if the request was successful
            if response.status_code == 200:
                return response.content
            else:
                warnings.warn(
                    f"Failed to download document: HTTP {response.status_code} - {response.reason}"
                )
                return None
        except (requests.exceptions.RequestException, ConnectionResetError) as err:
            warnings.warn(f"An error occurred while downloading the document: {err}")
            return None

    def archive_document(self, doc):
        # Debug: Print the entire document data
        print("Document being processed for archiving:", doc)

        if "actions" in doc:
            # Debug: Confirm 'actions' key exists and print its value
            print("Actions found in document:", doc["actions"])
        else:
            # Debug: Indicate missing 'actions' key
            print("No 'actions' key found in document.")

        for action in doc.get("actions", []):
            # Debug: Print each action being processed
            print(f"Processing action: {action}")

            # Normalize action label
            action_label = action.get("label", "").strip().upper()
            # Normalize action method
            action_method = action.get("method", "").strip().upper()

            if action_label == "ARCHIVE" and action_method == "PUT":
                archive_url = action.get("url")
                # Debug: Confirm archive URL extraction
                print(f"Archive URL found: {archive_url}")

                response = self.session.put(archive_url, auth=self.auth)
                # Debug: Print archive request response status
                print(f"Archive request response status: {response.status_code}")

                if response.status_code in [200, 204]:
                    print(f"Document {doc['name']} archived successfully.")
                    return
                else:
                    # Debug: Print detailed archive failure message
                    print(f"Failed to archive document {doc['name']}: {response.text}")
                    return

        # Debug: Indicate no matching action found after loop
        print("No 'ARCHIVE' action found in document actions.")
