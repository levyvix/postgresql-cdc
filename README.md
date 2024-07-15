# PosgreSQL CDC - Big Data Challenge


## Como rodar

- Clone o repositorio

`http`
```bash
git clone https://github.com/levyvix/postgresql-cdc.git
```

`ssh`
```bash
git clone git@github.com:levyvix/postgresql-cdc.git
```

- Entre na pasta clonada
```bash
cd postgresql-cdc
```

- Instale as dependências com `Poetry`
```bash
pip3 install poetry
poetry install
poetry shell
```

### Subindo o postgres local

```bash
cd docker
docker compose -f postgres-docker.yaml up -d
```

Isso sobe um container postgres localmente com as seguintes configurações:
- HOST: localhost
- USER: levi
- PASSWORD: levi
- PORT: 5432
- DATABASE: levicdc

##### Ativando o CDC no Postgres

- Se conecte ao servidor do postgres (DBeaver)
- Abra um script SQL e digite o seguinte comando

```sql
ALTER SYSTEM SET wal_level = logical;
```

- Reinicie o container

entre na pasta /docker do repositório
```bash
docker compose -f postgres-docker.yaml restart
```


#### Colocando dados inicias no postgres

Da raíz do arquivo, e com o shell do poetry ativado:

```bash
cd src
python3 main.py
>>> Fake data inserted successfully!
```

## Subindo o cluster do Kafka

Da pasta raíz

```bash
cd docker
docker compose -f docker-compose-kafka.yaml up -d
```

Este comando irá iniciar os containers em segundo plano para criar um ambiente de desenvolvimento que inclui o Kafka, Zookeeper, MinIO e um serviço de criação de buckets.

### Serviços

1. Zookeeper
	- **Imagem**: `docker.io/bitnami/zookeeper:3.8`
	- **Portas**: `2181:2181`
	- **Volumes**: `zookeeper_data:/bitnami`
	- **Importância**: O Zookeeper é usado para coordenar e gerenciar o Kafka.

2. Kafka
	- **Imagem**: `docker.io/bitnami/kafka:3.4`
	- **Portas**: `9093:9093`
	- **Dependências**: `zookeeper`
	- **Importância**: Kafka é uma plataforma de streaming de eventos utilizada para construir pipelines de dados em tempo real e aplicativos de streaming.

3. Connect
	- **Imagem**: `debezium/connect`
	- **Portas**: `8083:8083`
	- **Links**:
	- `zookeeper:zookeeper`
	- `kafka:kafka`
	- **Dependências**:
	- `zookeeper`
	- `kafka`
	- **Importância**: Kafka Connect é uma ferramenta para importar e exportar dados de forma confiável entre Kafka e outros sistemas.

4. Minio
	- **Imagem**: `quay.io/minio/minio:RELEASE.2022-05-26T05-48-41Z`
	- **Hostname**: `minio`
	- **Portas**: `9000:9000`, `9001:9001`
	- **Comando**: `server --console-address ":9001" /data`
	- **Importância**: Minio é um armazenamento de objetos compatível com S3.

5. CreateBuckets
	- **Imagem**: `minio/mc`
	- **Dependências**: `minio`
	- **Importância**: Cria buckets no Minio e aplica políticas, garantindo a preparação do ambiente de armazenamento.

## Configurando o Kafka Connect para ler o arquivo WAL e enviar para o cluster do Kafka

Com os containers rodando, é hora de enviar a configuração para o Debezium se conectar no servidor de banco de dados PostgreSQL para enviar os dados ao Kafka.

Para enviar conectores para o Debezium, utilize uma requisição POST para a API REST do Debezium escutando na porta 8083.

### Exemplo de requisição:

Para verificar quais conectores estão configurados:

```bash
curl -i -X GET -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/
```
Response: []

Para enviar uma configuração de conector PostgreSQL:

```bash
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '{
    "name": "exampledb-connector",
    "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "plugin.name": "pgoutput",
        "database.hostname": "postgres_cdc",
        "database.port": "5432",
        "database.user": "levi",
        "database.password": "levi",
        "database.dbname": "levicdc",
        "topic.prefix": "cdc"
    }
}'
```
Response: 201 Created

Para verificar se recebeu a configuração:

```bash
curl -i -X GET -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/
```
Response: ['exampledb-connector']


A partir de agora o kafka está escutando cada alteração no database "levicdc", cada insert, update e delete está sendo enviada para o kafka.


Para verificar os dados entrando, podemos configurar um consumer em Python

- [consumer.py](kafka/consumer.py)
- [consumer.ipynb](kafka/consumer.ipynb)

O script está configurado para ler todas as mensagens do topico, desde a sua criação, caso queira ler somente as mensagens chegando, mude `auto_offset_reset` para `latest`.

## Configurando o Kafka Connect para enviar os dados para o Minio/S3

Para enviar os dados para o Minio, é necessário configurar um novo conector no Kafka Connect.

### Exemplo de requisição:

Para enviar uma configuração de conector S3:

```bash
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '{
  "name": "s3-sink",
  "config": {
    "connector.class": "io.aiven.kafka.connect.s3.AivenKafkaConnectS3SinkConnector",
    "aws.access.key.id": "minio",
    "aws.secret.access.key": "minio123",
    "aws.s3.bucket.name": "commerce",
    "aws.s3.endpoint": "http://minio:9000",
    "aws.s3.region": "us-east-1",
    "format.output.type": "jsonl",
    "topics": "cdc-.sales.orders, cdc-.sales.products, cdc-.sales.users",
    "file.compression.type": "none",
    "flush.size": "20",
    "file.name.template": "/{{topic}}/{{timestamp:unit=yyyy}}-{{timestamp:unit=MM}}-{{timestamp:unit=dd}}/{{timestamp:unit=HH}}/{{partition:padding=true}}-{{start_offset:padding=true}}.json"
  }
}'
```

Isso fará com que o Kafka Connect envie os dados dos tópicos `cdc-.sales.orders`, `cdc-.sales.products` e `cdc-.sales.users` para o bucket `commerce` no Minio.

Para verificar se recebeu a configuração:

```bash
curl -i -X GET -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/
```

Response: ['example-db-connector', 's3-sink']

# Usando o Spark para processar os dados