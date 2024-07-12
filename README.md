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


#### Colocando dados inicias no postgres

Da raíz do arquivo, e com o shell do poetry ativado:

```bash
cd src
python3 main.py
>>> Fake data inserted successfully!
```