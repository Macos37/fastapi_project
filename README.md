# FastApi Project

Building the Docker Image

To build the Docker image, navigate to the directory containing the Dockerfile and run the following command:

```
 docker build -t <image-name> .
```

Run

```
docker run --name mytest -p 8000:8000 <image-name>
```

and go to http://127.0.0.1:8000/docs

![alt text](https://img-host.ru/bmgau.png)