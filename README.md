# Netflix-Stream-Pulse

> Status: **TBD**

## Project Overview
*(Brief description of what this project does)*

<br>


### Architecture
*(Description of the architecture)*

#### Architecture Diagram
![Architecture Diagram](/images/architecture_diagram.png "Architecture Diagram")

<br>

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

<br>

### Prerequisites

1. Docker - Follow the installation guide [here](https://docs.docker.com/engine/install/).
2. A Google Cloud Platform (GCP) account. If you don't have one, you can set one up [here](https://cloud.google.com/).

<br>

### Installation

A step by step series of examples that tell you how to get a development env running:

1. **Create a new project on Google Cloud with any name**
   - `Note`: Keep a track of the project name as you will have to use it later.

2. **Inside the project created in the above step, create a BigQuery dataset (refer on how to create dataset [here](https://cloud.google.com/bigquery/docs/datasets#create-dataset)):**
   - Dataset Name: `real_time_analytics`

3. **Service Account Setup:**
   - Serach for 'Service account' on the Google Cloud platform and click on 'Create Service Account Button'
   - Add any name to the service account.
   - Grant the service account 'BigQuery Admin' permission.
   - Click 'Done' to complete.

4. **Download the serive account key:**
   - Click on the newly created service account and go into the 'Keys' tab.
   - Click on 'Add Key' and create a new JSON key.
   - Important step: Download this JSON key.

5. **Configure the Project:**
   - Clone this repository.
   - Add the downloaded JSON file from step 4 to the `data-upload` folder of this project.
   - Open docker-compose.yaml file.
   - Replace `<ADD JSON FILE NAME HERE>` with filename of JSON filename from above step.
   - Replace `<ADD PROJECT NAME HERE>` with name of GCP project created in step 1.
   

4. **Run the Project:**
   - Open the terminal inside 'netflix-stream-pulse' downloaded project folder. (This repo has 3 subfolders, docker-compose.yaml and README file)
   - Execute `docker-compose up`.
   - Note: This step will take approximately 2 minutes. The entire program will execute for approximately 5 minutes. Look out for the message '***  DATA SIMULATION COMPLETED ***' on your terminal. Once you see this message, you can check your GBQ instance.


<br>


## Contributing

Please read [CONTRIBUTING.md](LINK_TO_CONTRIBUTING_GUIDELINES) for details on our code of conduct, and the process for submitting pull requests to us.

<br>

## Authors

* **Your Name** - *Initial work* - [YourGithubProfile](LINK_TO_YOUR_GITHUB_PROFILE)

<br>

## License

This project is licensed under the MIT License - see the [LICENSE.md](LINK_TO_LICENSE) file for details

<br>

## Acknowledgments

