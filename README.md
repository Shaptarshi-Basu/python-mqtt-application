# MQTT Charging System

The MQTT Charging System simulates charging sessions, publishes data to an MQTT broker, and stores the data in a MongoDB database. An API is provided to fetch charging session data.

## MQTT Publisher

The MQTT Publisher simulates charging session data and publishes it to the MQTT broker.

## MQTT Subscriber

The MQTT subscribes is a consumer for the mqtt publisher. It reads the data published to the broker, logs it and then pushed it to a mongodb


## MQTT API

This is REST API which reads the Charging System data from the mongodb which has been pushed by the mqtt subscriber component.

#### Endpoints

* GET /mqtt-payloads - fetches all the charging system data

### Prerequisites

- Docker installed
- Docker Compose installed

### Deployment

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   docker compose up -d
