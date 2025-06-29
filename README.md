<h1>Flask API Base </h1>


<h2>Architecture</h2>
![Flask API Base Architecture](compose/local/flask/api-base-arch.png)


<h2>Configurations</h2>

* Application configs are stored at this location 
* * `.envdir\.env`
* updated the `GUNICORN_CMD_ARGS="--bind 0.0.0.0:8080 --workers=2 --threads=4 --worker-class=gthread --worker-tmp-dir /dev/shm"` for CMD line in Docker file.




<h2>Pipeline Setup<h2>


<h2>Docker Setup</h2>

* Install Docker Desktop
* Navigate to the root of the directory in terminal. You should be at the same level as the `docker-compose.yml` file.
* Run `docker-compose build`
* The step above will take around 5-10 minutes for the first time as the images get downloaded. Subsequent executions will be faster. 
* If the above step runs to its end successfully, run `docker image ls`. You should see below 5 images
* * `flask_api_base_celery_worker`
* * `flask_api_base_webapp`
* * `flask_api_base_celery_flower`
* * `flask_api_base_celery_beat`
* * `redis`
* Run `docker-compose up`
* If the above runs successfully, the applcation can be browsed at `http://127.0.0.1:5010/auth/login`
* If you wish to stop the container, press `ctrl+c` in the terminal 