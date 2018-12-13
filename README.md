Team: Julio Oliveira

# Resumo

Por meio de uma API a aplicação recebe como parâmetros uma palavra e uma lista de urls. Retorna quantas vezes em cada site aquela palavra foi mencionada.

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
* Cache com memcached
* Documentação(para o Swagger) usando quart-openapi
* Validação usando quart-openapi.

### Motivação

**Python 3.7**: melhor performance lidando com asyncio em relação as versões anteriores.\
\
**Quart**: Basicamente um flask que usa asyncio por padrão. Por conta disso tem uma performance melhor que o flask puro.\
\
**memcached:** Menor consumo de memória. A aplicação não necessita de uma politica 
complexa de cache que justifique o uso do redis.\
\
**quart-openapi(documentação):** Cria um arquivo e gera uma rota /openapi.json baseado nas validações e rotas feitas. O Swagger-ui pode ler esse arquivo e mostrar de forma visual a documentação.\
\
**quart-openapi(validação):** Verifica o json recebido está de acordo com o schema esperado. Caso não, o próprio quart-openapi manda a resposta indicando qual o erro.

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
