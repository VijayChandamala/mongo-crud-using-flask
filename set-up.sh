#!/bin/bash

docker run -itd -p 27017:27017 --name mongo -e MONGO_INITDB_ROOT_USERNAME=mongo -e MONGO_INITDB_ROOT_PASSWORD=mongo mongo

docker cp dbcreate.js mongo:/.

docker build -t app .

mongohost=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mongo)

echo $mongohost

docker exec -it --user mongodb mongo bash -c 'mongo -u mongo -p mongo < dbcreate.js'

docker run -id --name app -p 5000:5000 -e MONGOHOST=$mongohost app

if $(python --version)
then
	python -m webbrowser http://localhost:5000
else
	echo "goto http://localhost:5000"
fi
