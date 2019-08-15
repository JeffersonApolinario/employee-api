# Employeer Manager API

API criada utilizando o django rest framework, para simular um gerenciamento de empregado relacionado a um departamento.

## Criado com
- Python 3.7.4
- Django 2.2.4
- Django Rest Framework 3.10.2
- Django Rest Framework Simple JWT 4.3.0

## Observações
Este projeto esta usando o SQLite caso você queira configurar outro banco vá na pasta employee_manager e altere o arquivo settings.py

Para utilizar corretamente você precisará realizar três etapas:
- Rodar o comando para gerar o arquivo de migração das suas models para o banco de dados
- Rodar o comando para realizar a migração
- Criar um usuário

Neste projeto utilizei o venv para criar o ambiente virtual, caso esteja utilizando outro configure do seu modo.

## Instalação
Aqui está as etapas que deverão ser seguidas

```
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Uso
Para subir a app execute este comando
```
    python manage.py runserver
```

## Rotas
Neste projeto é possível utilizar o django admin para gerenciar, ele está no endpoint raiz

```
http://localhost:8000/
```

Existem outras rotas para o acesso aos endpoints de employee(Empregado), department(Departamento) e o endpoint para gerar o token de autenticação, eles são:

```
GET http://localhost:8000/api/employees
POST http://localhost:8000/api/employees/
GET http://localhost:8000/api/employees/{id}/
PUT http://localhost:8000/api/employees/{id}/
DELETE http://localhost:8000/api/employees/{id}/
GET http://localhost:8000/api/departments
POST http://localhost:8000/api/departments
POST http://localhost:8000/api/token/
```

Para mais detalhes, existe um arquivo chamado swagger.yml com a documentação da API. Adicione o conteúdo do arquivo no [site](https://editor.swagger.io)

## Testes
Para executar os testes utilize este comando

```
python manage.py test
```