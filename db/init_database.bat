echo "Copying relevant scripts and data to the docker"
docker cp DDL.sql pg_container:/
docker cp DML.sql pg_container:/
docker cp data pg_container:/
echo "Copied relevant files"


echo "Running Data Definition Language script..."
docker exec pg_container psql tpch -U postgres -f DDL.sql
echo "Added schema"

echo "Running Data Manipulation Language script..."
docker exec pg_container psql tpch -U postgres -f DML.sql
echo "Added tables"


docker exec -it pg_container rm -rf data pg_container:/
docker exec -it pg_container rm DML.sql
docker exec -it pg_container rm DDL.sql