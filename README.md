# Netflix-Stream-Pulse

> Status: **TBD**

## Project Overview
*(Brief description of what this project does)*

### Architecture
*(Description of the architecture)*

#### Architecture Diagram
*(To be added)*

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

1. Docker - Follow the installation guide [here](https://docs.docker.com/engine/install/).
2. A Google Cloud Platform (GCP) account. If you don't have one, set it up [here](https://cloud.google.com/).

### Installation

A step by step series of examples that tell you how to get a development env running:

1. **Create a database in Google BigQuery (GBQ):**
   - Database Name: `real_time_analytics`

2. **Service Account Setup:**
   - Create a service account in GBQ with full permissions.
   - Create a key and download the JSON credentials file.

3. **Configure the Project:**
   - Clone this repository.
   - Navigate to the project folder in the terminal.
   - Add the downloaded JSON file to the `data-upload` folder of this project.

4. **Run the Project:**
   - Execute `docker-compose up -d` from inside the project folder.
   - Note: This step will take approximately 50-90 seconds. The entire program will execute for approximately 5 minutes. Look out for the message '*** Data simulation completed! ***' in your terminal. Once you see this message, you can check your GBQ instance.

## Contributing

Please read [CONTRIBUTING.md](LINK_TO_CONTRIBUTING_GUIDELINES) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Your Name** - *Initial work* - [YourGithubProfile](LINK_TO_YOUR_GITHUB_PROFILE)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LINK_TO_LICENSE) file for details

## Acknowledgments

