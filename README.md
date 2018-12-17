Team: Julio Oliveira

# Resumo

Por meio de uma API a aplicação recebe como parâmetros uma palavra e uma lista de urls. Retorna quantas vezes em cada site aquela palavra foi mencionada.\
Endpoint: http://ponto-tel-test.herokuapp.com/ \
Openapi: http://ponto-tel-test.herokuapp.com/openapi.json

Exemplo:
```bash
curl --header "Content-Type: application/json" \
     --request POST \
     -d '{"word": "the", "urls":["http://github.com", "http://google.com", "http://wiki.c2.com/"]}' \
     https://ponto-tel-test.herokuapp.com/
```

## Contexto

A aplicação não tem fim específico. É  uma ferramenta para outras aplicações utilizarem.\
Exemplo: \
\- Saber quantas vezes sua marca foi mencionada em determinados sites.

## Objetivo

A aplicação preza por eficiência de recursos.\
Tempo de resposta, consumo de memória e processamento, como lida com concorrência e alta carga são as métricas levadas em consideração durante o desenvolvimento.

# Proposta

## API

* Python 3.7
* Framework Quart
* Cache com redis
* Documentação(para o Swagger) usando quart-openapi
* Validação usando quart-openapi, validators, marshmallow.

### Motivação

**Python 3.7**: melhor performance lidando com asyncio em relação as versões anteriores.\
\
**Quart**: Basicamente um flask que usa asyncio por padrão. Por conta disso tem uma performance melhor que o flask puro.\
\
**redis:** Servidor de cache de fácil uso e com boa performance. Escolhido por conta das suas estruturas de dados.\
\
**quart-openapi(documentação):** Cria um arquivo e gera uma rota /openapi.json baseado nas validações e rotas feitas. O Swagger-ui pode ler esse arquivo e mostrar de forma visual a documentação.\
\
**quart-openapi(validação):** O quart-openapi com o marshmallow verificam se o json recebido está de acordo com o schema esperado. Caso não, retorna-se uma resposta indicando qual o erro. O validator verifica se a urls recebidas são válidas.

## Crawler

* Requisições com aiohttp 
* Tratamento dos dados com html2text

### Motivação

**aiohttp:** Usa asyncio para fazer as requisições.\
\
**html2text:** A parte útil dos dados é apenas o texto e não o html em si.

## Arquitetura

* Servidor da aplicação rodando a API.
* Servidor de cache rodando memcached.

### Motivação

Separar o servidor de cache da API permiti que a aplicação como um todo seja escalável.\
Exemplo:\
\- Horizontal: A API tá recebendo muitas requisições. Fica fácil configurar um load balancer para distribuir a carga entre servidores rodando a mesma API, mas todos compartilham a mesma cache.\
\- Vertical: O servidor de cache precisa de mais memória, pois começou a não ser o suficiente. Basta mudar o tipo da instância do servidor de cache, sem afetar a aplicação.

# Problemas durante o desenvolvimento

## Api com quart

Quart é muito novo, com pouca documentação e exemplos. Por muitas vezes foi demorado encontrar informações.

## Documentação com quart-openapi

1 - Se já foi dificil encontrar informações do quart, do quart-openapi foi ainda mais. A documentação da sintaxe de como descrever os schemas é horrível.\
\
2 - A função que cria a documentação é a mesma que faz a validação. A validação não é boa. Logo para conseguir manter a documentação foi necessário manter duas validações de schema.

## Validação

Apenas o quart-openapi não foi o bastante para fazer a validação. Foi necessário usar o marshmallow para checar o schema e o validators para checar as urls recebidas.

## Cache

Foi necessário trocar o memcached pelo redis. Trabalhar com várias chaves no memcached não é prático.
