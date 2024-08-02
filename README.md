# FIRE-SERVER
A Python Server implementation of FIRE Calculator

## Prerequisites
Ensure you are in the root folder of the project before proceeding.

## Setting Up the Environment

1. **Create a Virtual Environment**
   ```sh
   python3.10 -m venv .venv
2. **Activate the Virtual Environment**
   ```sh
   source .venv/bin/activate
3. **Install Required Packages**
   ```sh
   pip3 install -r requirements.txt
4. **Running the Backend Service**
   ```sh
   uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Use Code Above or Code below

# If You want to try Docker, using the steps below. 

## Build and Run Docker Container

1. **Build docker image**
   ```sh
   sudo docker build -t fire_calculator .
2. **Run Container**
   ```sh
   sudo docker run -d -p 8000:8000 fire_calculator
