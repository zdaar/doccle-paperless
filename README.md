# Doccle to Paperless Integration

This project provides an integration between Doccle and Paperless, allowing you to automatically download new documents from Doccle and upload them to Paperless for easy organization and management.

## Features

- Automatically checks for new documents in Doccle at regular intervals
- Downloads new documents as PDF files with friendly filenames
- Saves document metadata as JSON files
- Uploads downloaded documents to Paperless
- Archives documents in Doccle after successful upload to Paperless
- Provides a health check endpoint for monitoring the application's status
- Supports running the application locally or using Docker

## TODO

- [ ] Assign owner, tags, correspondents, and document types from Doccle's metadata
- [ ] Better scheduling
- [ ] Better logging
- [ ] Better status API

## Prerequisites

- Python 3.9 or later
- Docker and Docker Compose (optional, for running the application in a container)
- Doccle account with valid credentials
- Paperless instance with API access

## Installation and Configuration

1. Clone the repository and navigate to the project directory.

2. For local usage, create a `.env` file based on the provided `.env.sample` file and fill in the required Doccle and Paperless credentials.

3. For Docker usage, update the `docker-compose.yaml` file with the necessary Doccle and Paperless credentials in the `environment` section.

## Usage

### Running Locally

1. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python main.py
   ```

### Running with Docker

1. Build the Docker image and start the container:
   ```
   docker-compose up
   ```

The application will periodically check for new documents in Doccle, download them, and upload them to Paperless.

## Logging

Detailed logs are generated in the `logs` directory with timestamped filenames. Each log entry includes the timestamp, log level, and message, covering events such as document downloads, uploads, and errors.

## Monitoring

The application provides a health check endpoint at `/health` that returns the current status and uptime of the application.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

## Acknowledgements

- Steve Gilissen, author of [py-doccle](https://github.com/sgilissen/py-doccle)
- [Doccle](https://www.doccle.be/) for providing the document management platform
- [Paperless-NGX](https://github.com/jonaswinkler/paperless-ngx) for the community-supported open-source document management system
