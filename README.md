

Create the requirements.txt file:
`pip freeze > requirements.txt`


Run server: `uvicorn app.main:app --port 9000` <br>
Run server in dev mode: `uvicorn app.main:app --port 9000 --reload`

 
 ### https://github.com/provectus/kafka-ui 
 docker run -p 8080:8080 \
	-e KAFKA_CLUSTERS_0_NAME=local \
	-e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka:9092 \
	-d provectuslabs/kafka-ui:latest 