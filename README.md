# Docker + Docker-compose + Selenium + Python

<div align="center">
    <img src="https://i.gyazo.com/18b3a08d39ef8154491bdc66b015fbc1.png" />
</div>

This is a simple example of how to use Docker, Docker-compose and Selenium together to run a simple Python script.

In this case, we can use three different ways to run the script:

1. Native
2. Dockerfile
3. Docker-compose with Simulated Web Driver

## Native

To run the script natively, we can use the next commands.

1. You need to install Chrome or Firefox.

2. Start the workspace.
    ```shell
    virtualenv venv
    source venv/bin/activate
    ```
3. Copy the file .env to the workspace.
    ```shell
   cp .env source/
    ```
   
    As example, can be `source/.env`

    ```dotenv
    ENVIRONMENT=local
    PATH_ASSETS=assets/
    BROWSER=chrome
    EXTENSIONS_CHROME=[""]
    #BROWSER=firefox
    #EXTENSIONS_FIREFOX=[""]
    ```

5. Inside to the folder `source`
    ```shell
   cd source 
    ```

6. Install the dependencies.
    ```shell
    python -m pip install --upgrade pip
    pip install -r requirements.txt
   ```
7. Execute the script.
    ```shell
    python app.py
    ```
8. Stop the workspace.
    ```shell
    deactivate
    ```
   
## Dockerfile

1. Copy the file .env to the workspace.
    ```shell
   cp .env source/
    ```
   
    As example, can be `source/.env`

    ```dotenv
    ENVIRONMENT=docker
    PATH_ASSETS=assets/
    BROWSER=chrome
    EXTENSIONS_CHROME=[""]
    ```
   
2. Build the Docker image.
    ```shell
    docker build -f docker/single/Dockerfile -t selenium-python-docker .
    ```

3. Run the Docker image.
    ```shell
    docker run -it --rm -v $(pwd)/source:/usr/src/app -w /usr/src/app selenium-python-docker
    ```

## Docker-compose

1. Copy the file .env to the workspace.
    ```shell
   cp .env source/
    ```
   
    As example, can be `source/.env`

    ```dotenv
    ENVIRONMENT=remote
    PATH_ASSETS=assets/
    BROWSER=chrome
    EXTENSIONS_CHROME=[""]
    #BROWSER=firefox
    #EXTENSIONS_FIREFOX=[""]
    REMOTE_URL=http://selenium-hub:4444/wd/hub
    ```

2. Build the Docker image.
    ```shell
    docker-compose build
    ```
   
3. Up the Docker image.
    ```shell
    docker-compose up
    ```
   
4. Execute the script in docker service.
    ```shell
    docker-compose exec -it app bash
    ```
     
    Or execute the script in the container.
    ```shell
    docker exec -it $(docker ps | grep app | awk '{print $1}') bash
    # python app.py
    ```
  
5. Stop the Docker image.
    ```shell
    docker-compose down
    ```