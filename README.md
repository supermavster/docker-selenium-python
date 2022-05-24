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

3. Edit the file .env to the workspace.

    As example, can be `source/.env`

    ```dotenv
    ENVIRONMENT=local
    #ENVIRONMENT=docker
    #ENVIRONMENT=remote

    PATH_ASSETS=assets

    #BROWSER=chrome
    #EXTENSIONS_CHROME=["metamask"]

    BROWSER=firefox
    EXTENSIONS_FIREFOX=["metamask", "captcha"]

    REMOTE_URL=http://selenium-hub:4444/wd/hub
    #REMOTE_URL=http://0.0.0.0:4444/wd/hub
    #REMOTE_URL=http://localhost:4444/wd/hub

    METAMASK_AUTH=["SECRET", "A B C D E F G H I J K L"]
    ```

4. Inside to the folder `source`

    ```shell
   cd source 
    ```

5. Install the dependencies.

    ```shell
    python -m pip install --upgrade pip
    pip install -r requirements.txt
   ```

6. Execute the script.

    ```shell
    python main.py
    ```

7. Stop the workspace.

    ```shell
    deactivate
    ```

## Dockerfile

1. Edit the file .env to the workspace.

    As example, can be `source/.env`

    ```dotenv
    #ENVIRONMENT=local
    ENVIRONMENT=docker
    #ENVIRONMENT=remote

    PATH_ASSETS=assets

    BROWSER=chrome
    EXTENSIONS_CHROME=["metamask", "captcha"]

    #BROWSER=firefox
    #EXTENSIONS_FIREFOX=["metamask"]

    REMOTE_URL=http://selenium-hub:4444/wd/hub
    #REMOTE_URL=http://0.0.0.0:4444/wd/hub
    #REMOTE_URL=http://localhost:4444/wd/hub

    METAMASK_AUTH=["SECRET", "A B C D E F G H I J K L"]

    ```

2. Build the Docker image.

    ```shell
    docker build -f docker/single/Dockerfile -t selenium-python-docker .
    ```

3. Run the Docker image.

    ```shell
    docker run -it --rm -v $(pwd)/source:/usr/src/app -w /usr/src/app --env-file=.env selenium-python-docker
    ```

## Docker-compose

1. Edit the file .env to the workspace.

    As example, can be `source/.env`

    ```dotenv
    #ENVIRONMENT=local
    #ENVIRONMENT=docker
    ENVIRONMENT=remote

    PATH_ASSETS=assets

    BROWSER=chrome
    EXTENSIONS_CHROME=["metamask"]

    #BROWSER=firefox
    #EXTENSIONS_FIREFOX=["metamask"]

    REMOTE_URL=http://selenium-hub:4444/wd/hub
    #REMOTE_URL=http://0.0.0.0:4444/wd/hub
    #REMOTE_URL=http://localhost:4444/wd/hub

    METAMASK_AUTH=["SECRET", "A B C D E F G H I J K L"]

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
    # python main.py
    ```
  
5. In the localhost:4000, you can see the result in session, note: the password of session vnc is `secret`

6. Stop the Docker image.

    ```shell
    docker-compose down
    ```
