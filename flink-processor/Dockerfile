# Use a base image that includes Maven
FROM maven:3.5-jdk-8-alpine as builder

# Copy your source files and POM into the image
COPY ./ /usr/src/myapp/

# Set the working directory
WORKDIR /usr/src/myapp/

# Build your application
RUN mvn clean package

# Now, use the openjdk base image for the final image
FROM openjdk:8u151-jdk-alpine3.7

# Install Bash
RUN apk add --no-cache bash libc6-compat

# Copy resources from the builder image
WORKDIR /
COPY --from=builder /usr/src/myapp/wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh

COPY --from=builder /usr/src/myapp/target/flink-kafka2postgres-1.0-SNAPSHOT-jar-with-dependencies.jar flink-processor.jar

# Wait for Zookeeper and Kafka to be available and run application
CMD ./wait-for-it.sh -s -t 30 $ZOOKEEPER_SERVER -- ./wait-for-it.sh -s -t 30 $KAFKA_SERVER -- java -Xmx512m -jar flink-processor.jar