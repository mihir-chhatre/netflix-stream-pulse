import json
import random
import time
from faker import Faker
from kafka import KafkaProducer
from datetime import datetime

# Initialize Faker
fake = Faker()

# Predefined list of movies and TV shows
movies = [{
    "ContentType": "Movie",
    "ContentID": fake.uuid4(),
    "ContentName": "Movie " + str(i),
    "Genre": random.choice(["Action", "Comedy", "Drama", "Fantasy", "Horror"]),
    "ReleaseYear": random.randint(1980, 2023),
    "ContentLength": random.randint(80, 180),
    "Language": random.choice(["English", "Spanish", "Hindi"]),
    #"Director": fake.name(),
    "MaturityRating": random.choice(["TV-Y", "TV-G", "PG-13", "R", "NC-17"]),
} for i in range(20)]


tv_shows = [{
    "ContentType": "TV Show",
    "ContentID": fake.uuid4(),
    "ContentName": "TV Show " + str(i),
    "Genre": random.choice(["Action", "Comedy", "Drama", "Fantasy", "Horror"]),
    "ReleaseYear": random.randint(1980, 2023),
    "ContentLength": random.randint(20, 60),
    "Language": random.choice(["English", "Spanish", "Hindi"]),
    #"Director": fake.name(),
    "MaturityRating": random.choice(["TV-Y", "TV-G", "PG-13", "R", "NC-17"]),
} for i in range(20)]

# Kafka Producer setup
kafka_nodes = "kafka:9092"
myTopic = "netflix-event"
completionTopic = "completion-event"  # New topic for completion message
producer = KafkaProducer(bootstrap_servers=kafka_nodes, 
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

def generate_event():
    content = random.choice(movies + tv_shows)

    event = {
        "EventId": fake.uuid4(),
        "UserId": fake.uuid4(),
        "UserName": fake.name(),
        "UserAge": random.randint(18, 70),
        "UserGender": random.choice(["Male", "Female"]),
        "UserLocation": random.choice(["United States", "India", "Australia", "Germany", "Indonesia", "China", "Italy", "Spain", "Canada", "Mexico", "Kenya", "United Kingdom", "Egypt", "South Korea", "Brazil", "Russia", "Japan", "France", "South Africa", "Nigeria"]),
        "DeviceType": random.choice(["Smart TV", "Mobile", "Tablet", "PC"]),
        **content,
        "EventTimestamp": datetime.now().isoformat(),
    }
    print(event)
    
    # Send data to Kafka
    producer.send(myTopic, value=event)
    producer.flush()

def main():
    
    # total_events = 9000       # takes around 30 minutes to complete
    
    total_events = 1500       # takes around 5 minutes to complete


    for _ in range(total_events):
        generate_event()
        time.sleep(0.2)  # delay between each event

    # Send completion message to the completion topic
    completion_message = {"status": "complete", "timestamp": datetime.now().isoformat()}
    producer.send(completionTopic, value=completion_message)
    producer.flush()

if __name__ == "__main__":
    main()

