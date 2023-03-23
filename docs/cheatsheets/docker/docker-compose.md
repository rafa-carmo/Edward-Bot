# Docker Compose
O Docker compose é uma ferramenta para orquestrar os container docker.

## Como utilizar.
Criar um arquivo yml para gerenciar os containers
exemplo: 
```
# neste exemplo sera criado um container docker para um banco de dados mysql e outro container para o phpmyamin

# Versão do yml
version: '3'

services:
    # criação do container para mysql
    mysql:
        #expecificar a imagem
        image: mysql:5.7
        #o que deve ser feito caso o container desligue
        restart: always
        #o nome para o container
        container_name: mysql_database
        #as variaveis de ambiente
        environment:
            MYSQL_DATABASE: 'db'
            MYSQL_PASSWORD: 'root'
            MYSQL_ROOT_PASSWORD: root
        #a porta que sera exposta no container
        expose:
        - '3306'
        #volume para salvar os dados do container para que quando seja reiniciado nao seja perdido
        volumes:
        - ./docker/.mysql/my-db:/var/lib/mysql
        #o mapeamento de portas <Porta Local>:<Porta no Container>
        ports:
        - 3306:3306
    
    phpmyadmin:
        image: phpmyadmin/phpmyadmin:latest
        ports:
        - 8880:80
        environment:
        - PMA_ARBITRARY=1
        #Esta opção é para ele aguardar e somente iniciar quando o container do mysql estiver rodando.
        depends_on:
        - mysql

```

Após a criação do arquivo yml na pasta do projeto.
inicie com o comando
<br>

```
#argumentos
# up para subir o projeto
# -d para rodar oculto sem ocupar o terminal.
docker compose up -d
```

Caso queira apenas construir as imagens utilize o seguinte comando
<br>
```
# podendo utilizar o argumento --no-cache caso não queira que o docker utilize cache na construção
docker compose build
```