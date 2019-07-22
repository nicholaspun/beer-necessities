docker build -t my-docker-image .

docker run -it --rm -v $(pwd)/code:/code my-docker-image