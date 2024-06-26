# Netflix-Stream-Pulse

## Project Overview
The Netflix-Stream-Pulse project is designed to simulate Netflix user activity, providing a platform for real-time data processing and analytics.

<br>

## Problem Statement
In today’s fast-paced online streaming arena, swiftly and accurately understanding user behavior is not just beneficial; it's essential. The challenge lies in the sheer volume and rapidity of data generated, which can be overwhelming. Traditional data processing methods often stumble under the weight of such real-time, heavy data flows, leading to critical delays in deriving insights and impacting decision-making. The Netflix-Stream-Pulse project ambitiously confronts this challenge. It meticulously simulates an environment where continuous streams of user data—encompassing viewing patterns, user profiles, and more—are efficiently captured and processed. Leveraging a robust combination of cutting-edge technologies like Apache Kafka, Apache Flink, PostgreSQL, PySpark, and Google BigQuery, the project crafts an innovative end-to-end pipeline. This sophisticated setup not only adeptly handles the demands of large-scale, real-time data but also excels in extracting valuable insights from it. By processing and analyzing this streaming data in a scalable, efficient manner, the project illuminates how strategic data utilization can significantly enhance user experiences in the streaming service sector, transforming raw data into a goldmine of actionable intelligence.

The project is centered around three key patterns of real-time analytics:

1. Demographic and Maturity Rating Trends: By tracking the preferences and viewership patterns across different demographics and maturity ratings, we can tailor content recommendations and marketing strategies more effectively. Understanding these trends is vital for curating a diverse and appealing content library that resonates with a broad audience spectrum.

2. Age Group and Gender Trends: By dissecting viewership trends across different age groups and genders, we gain valuable insights into the varying content preferences and viewing habits. This enables us to craft more targeted content strategies and promotional campaigns, ensuring that each segment of our audience finds content that appeals to their unique tastes and preferences.

3. Device and Genre Trends: Analyzing the correlation between the types of devices used and the genres preferred allows us to optimize streaming quality and user interface design for various devices. This insight helps in enhancing the overall user experience, ensuring that content is not only accessible but also enjoyable on the preferred devices of our audience.

<br>

## Technology used:
 - Apache Kafka (Simulating data)
 - Apache Flink (Real time analytics)
 - Postgres (Database)
 - PySpark (Transformations)
 - Docker (Containerizing)
 - GCP Big Query (Datawarehouse)
 - GCP Looker Studio (Dashboarding)
 - Python, Java

 <br>

## Architecture
The architecture is built upon a series of interconnected services and technologies, ensuring efficient data flow and processing.

1. Data Production: The process begins with a Python-based Kafka producer, simulating real-time user data related to Netflix, including user profiles and viewing habits. This data is produced and continuously streamed to a Kafka topic.

2. Real-time Data Processing: An Apache Flink application is employed as a consumer, which subscribes to the Kafka topic. It processes these events in real-time, performing analytics to derive insights from the streaming data. Every 5 minutes, the aggregated data is stored in PostgreSQL tables for persistent storage and further analysis.

3. Data Transformation and Loading: Upon completion of data production, a special 'complete' message is published to a separate Kafka topic. A PySpark application, listening to this second topic, triggers once it receives the 'complete' event. It then extracts data from the PostgreSQL tables, performs necessary transformations, and loads the processed data into Google BigQuery. This step is crucial for preparing the data for advanced analytics and visualization.
   - PySpark transformations include converting the window_end_utctime column into a date format and extracting the hour and minute components. Additionally, the original time column is dropped, and specific columns are selected and rearranged based on the target table name.


4. Data Storage Optimization: BigQuery tables are partitioned by date and clustered by hour and minute. Partitioning by date organizes data into separate segments for each date, significantly improving query performance and reducing costs by limiting the amount of data scanned for date-specific queries. Clustering by hour and minute further optimizes performance for queries involving these time elements, as data within each date partition is ordered based on hour and minute. This approach not only accelerates query execution but also aids in efficient data management, particularly for large datasets commonly used in time-based analytics.

5. Visualization: Finally, Looker Studio is used to create interactive dashboards and visualizations. These visualizations provide insights into various user metrics such as device usage, genre preferences, location-based trends, maturity ratings, gender, and age group distributions.

#### Architecture Diagram
![Architecture Diagram](/images/architecture_diagram.png "Architecture Diagram")

<br>

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites

1. Docker - Follow the installation guide [here](https://docs.docker.com/engine/install/).
2. A Google Cloud Platform (GCP) account. If you don't have one, you can set one up [here](https://cloud.google.com/).

<br>

### Installation

A step by step series of examples that tell you how to get a development env running:

1. **Create a new project on Google Cloud with any name**
   - `Note`: Keep a track of the Project ID as you will have to use it later.

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
   - Download a ZIP of this repository with the default name.
   - Add the downloaded JSON file from step 4 to the `data-upload` folder of this project.
   - Open `docker-compose.yaml` file, this is in the 'netflix-stream-pulse' folder.
   - Replace `<ADD JSON FILE NAME HERE>` with filename of JSON filename from above step.
   - Replace `<ADD PROJECT ID HERE>` with ID of GCP project created in step 1.
   

4. **Run the Project:**
   - Open the Docker application downloaded as a part of prerequisites and keep the application open before moving to next step.
   - Open the terminal inside 'netflix-stream-pulse-main' downloaded project folder. (This repo has 5 subfolders, docker-compose.yaml, LICENSE.md and README file)
   - Execute `docker-compose up`.
   - <u>Note</u>: This step will take approximately 2 minutes. The entire program will execute for approximately 5 minutes. Look out for the message `***  DATA SIMULATION COMPLETED ***` on your terminal. Once you see this message, you can check your Google BigQuery instance.


<br>



## Dashboarded results:

<i>Since my GCP account is part of my university organization, I am unable to publically share dashboarding links.</i>

Please find a video and screenshots of my interactive dashboards below -
[Video](/images/dashboard-vid.mov)

   - Device & Genre trends: <br>
   ![Device & Genre dashboard](/images/DeviceGenre.png "Device & Genere dashboard")
   - Location & Maturity Rating trends: <br>
   ![Location & Maturity Rating dashboard](/images/LocationMR.png "Location & Maturity Raing dashboard")
   - Gender & Age Group trends: <br>
   ![Gender & Age Group dashboard](/images/GenderAgeGroup.png "Gender & Age Group dashboard")


<br>


## Future work
   - Create a bespoke connector enabling Google BigQuery to function as a sink for Apache Flink. An alternative approach might involve implementing 'change data capture' to gradually retrieve data from PostgreSQL tables and transfer it to BigQuery.
   - Perform more advanced real-time analytics such as tracking user jouneys and drop-off points.


<br>

## Authors

* **Mihr Chhatre** - [Github](https://github.com/mihir-chhatre)

<br>

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

<br>

## Acknowledgments

This project was created as a part of DEZoompcamp2024, and I'd like to extend a big thank you to the entire organizing team for their efforts in hosting and teaching concepts throughout this zoomcamp.


