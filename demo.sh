docker network create test_network
docker build .

docker run --detach --network test_network --name db -e POSTGRES_PASSWORD=ducanhdz  <prosgres hash>
docker run --detach --network test_network --name api <api hash>