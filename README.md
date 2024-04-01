# netflix-stream-pulse


#### Add architecture diagram

### <To do points>


#### Steps (to be updated):
##### install docker - https://docs.docker.com/engine/install/
##### setup a GCP acconut if you dont have one
#### create a database in GBQ called 'real_time_analytics'
#### Create service account with full permissions to GBQ 
#### Create a key and download JSON credentials file from above step 
#### Add JSON file from above step to 'data-upload' folder of this project
#### Clone this project and navigate to project folder in terminal 
#### run docker-compose up -d from insinde the project folder (note: this step will take approx 50-90sec. The entire program will execute for approx 5 min, look out for the message '*** Data simulation completed! ***' on your terminal. Once you see this msg, you can check GBQ)