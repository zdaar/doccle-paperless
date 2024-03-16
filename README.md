# Doccle to Paperless Integration

This project provides an integration between Doccle and Paperless, allowing you to automatically download new documents from Doccle and upload them to Paperless for easy organization and management.

## Features

- Automatically checks for new documents in Doccle
- Downloads new documents as PDF files
- Generates friendly filenames for downloaded documents
- Saves document metadata as JSON files
- Uploads downloaded documents to Paperless
- Archives documents in Doccle after successful upload to Paperless
- Comprehensive logging for easy monitoring and troubleshooting

## Prerequisites

- Python 3.9 or later
- Docker and Docker Compose (optional, for running the application in a container)
- Doccle account with valid credentials
- Paperless instance with API access

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/doccle-to-paperless.git
   cd doccle-to-paperless
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Configuration:
   - For local usage:
     - Create a `.env` file in the project root by copying the `.env.sample` file.
     - Provide the necessary configuration in the `.env` file:

       ```
       DOCCLE_USERNAME=your_doccle_username
       DOCCLE_PASSWORD=your_doccle_password
       PAPERLESS_URL=http://your_paperless_url
       PAPERLESS_TOKEN=your_paperless_token
       ```

     - Replace the placeholders with your actual Doccle and Paperless credentials.

   - For Docker usage:
     - Open the `docker-compose.yaml` file.
     - Provide the necessary configuration in the `environment` section of the `doccle-to-paperless-service`:

       ```yaml
       environment:
         - DOCCLE_USERNAME=your_doccle_username
         - DOCCLE_PASSWORD=your_doccle_password
         - PAPERLESS_URL=http://your_paperless_url
         - PAPERLESS_TOKEN=your_paperless_token
       ```

     - Replace the placeholders with your actual Doccle and Paperless credentials.

## Usage

### Running Locally

To run the application locally, make sure you have populated the `.env` file with the necessary credentials. Then, execute the following command:

```
python main.py
```

The application will check for new documents in Doccle, download them, and upload them to Paperless.

### Running with Docker

To run the application using Docker, make sure you have provided the necessary credentials in the `docker-compose.yaml` file. Then, execute the following command:

```
docker-compose up
```

This will build the Docker image and start a container running the application.

## Logging

The application generates detailed logs for monitoring and troubleshooting purposes. Logs are stored in the `logs` directory with timestamped filenames. Each log entry includes the timestamp, log level, and message.

The following events are logged:

- Successful download of a PDF document from Doccle
- Saving of document metadata as a JSON file
- Successful upload of a document to Paperless
- Archiving of a document in Doccle
- Errors related to missing credentials, failed downloads, invalid PDFs, and upload failures

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Doccle](https://www.doccle.be/) for providing the document management platform
- [Paperless](https://github.com/jonaswinkler/paperless-ng) for the open-source document management system
- [Python](https://www.python.org/) for the programming language and ecosystem