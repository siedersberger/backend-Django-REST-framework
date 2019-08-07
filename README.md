# API de roteiros de viagem

## Como rodar a aplicação:

Para rodar a aplicação deve-se ter o python 3 instalado.
Também é necessário instalar alguns requerimentos, mas antes disso 
eu aconselho criar um ambiente virtual com o virtualenv.
Após clonar este repositório e entrar no diretório, 
os seguintes comandos/passos são necessários:

1. `pip3 install virtualenv`
2. `virtualenv env`
3. `source env/bin/activate`
4. `pip install -r requirements.txt`
5. `python manage.py makemigrations`
6. `python manage.py migrate`
7. `python manage.py runserver`

Agora você já pode acessar a API Django REST framework pelo endereço http://127.0.0.1:8000

## Criando roteiro:

Endpoint para criação (POST) e listagem (GET) dos roteiros: http://127.0.0.1:8000/roteiro/

Formato application/json para criação (POST) do roteiro:

```json
{
    "data_de_chegada": "YYYY-MM-DD",
    "data_de_saida": "YYYY-MM-DD",
    "numero_de_pessoas": 2,
    "passeios": [
        614365,
        1106,
        380721,
        1596
    ]
}
```
A API irá retornar um JSON com os horários marcados para cada passeio.
Caso não haja disponibilidade de horário, uma mensagem é retornada.

## Rodando os testes:

Para rodar os testes deve-se executar, na mesma pasta do manager.py, o seguinte comando:

`python manager.py test roteiro -v 2`
