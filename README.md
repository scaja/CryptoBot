# CryptoBot

<details>
<summary>setup vm</summary>

## add new repository in git browser

git clone https://github.com/scaja/CryptoBot.git  
cd CryptoBot  
git add .gitignore  
git commit -m "add gitignore"  
git push  
source myenv/bin/activatesource  


## virtual environment

sudo apt-get update  
sudo apt-get install python3.8-venv --fix-missing  
python3 -m venv myenv  
source myenv/bin/activate  


upgrade pip  
python3 -m pip install --upgrade pip  


## Create Kernel

pip3 install ipykernel  
python3 -m ipykernel install --user --name='vscode'  


## Start Jupiter

pip install notebook ipython  
jupyter notebook  
Install extensions also as host ssh  
restart VSCODE manuelly  

</details>

<details>
<summary>install packages</summary>

pip install pandas  
pip install python-dotenv  
pip install python-binance  
pip install websocket-client
pip install elasticsearch

</details>

<details>
<summary>unittest</summary>

python -m unittest discover

</details>

<details>
<summary>pyspark</summary>

## install Java

sudo apt update
sudo apt install openjdk-8-jre-headless -y
sudo apt install openjdk-8-jdk-headless -y

## install env

sudo apt install python3.8-venv -y

python3 -m venv .venv
. .venv/bin/activate
pip install notebook

## install spark

wget https://dst-de.s3.eu-west-3.amazonaws.com/pyspark_fr/spark.tgz

tar xzvf spark.tgz
sudo mv spark-3.5.0-bin-hadoop3/ /opt/spark

## set environment variable

export SPARK_HOME=/opt/spark
export PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH
export PYTHONPATH=$(ZIPS=("$SPARK_HOME"/python/lib/*.zip); IFS=:; echo "${ZIPS[*]}"):$PYTHONPATH

## 

rm spark.tgz
sed -i 's/rootLogger.level = info/rootLogger.level = error/' /opt/spark/conf/log4j2.properties.template
mv /opt/spark/conf/log4j2.properties.template /opt/spark/conf/log4j2.properties

</details>

<details>
<summary>elasticsearch in docker</summary>

version: "3.0"

services:
  elasticsearch:
    container_name: es-container
    image: docker.elastic.co/elasticsearch/elasticsearch:8.1.2
    environment:
      - xpack.security.enabled=false
      - "discovery.type=single-node"
    networks:
      - es-net
    ports:
      - 9200:9200

  kibana:
    container_name: kb-container
    image: docker.elastic.co/kibana/kibana:8.1.2
    environment:
      - ELASTICSEARCH_HOSTS=http://es-container:9200
    networks:
      - es-net
    depends_on:
      - elasticsearch
    ports:
      - 5601:5601

networks:
  es-net:
    driver: bridge

</details>

<details>
<summary>commands</summary>

docker compose -f docker-compose-bot.yml up --build --force-recreate --renew-anon-volumes

</details>