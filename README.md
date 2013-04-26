# django-shortener-example

Essa é uma aplicação bastante simples de encurtamento de urls usando o framework Django. 

***

## Rodando o aplicativo

Em primeiro lugar você deve instalar as dependências com o comando: 
    
    pip install -r requirements.txt


Após instalado, crie as tabelas:
    
    python manage.py syncdb
    

Agora basta rodar usando o servidor de desenvolvimento do próprio Django:
    
    python manage.py runserver

Lembre-se de acessar a interface administrativa e alterar a configuração do aplicativo sites de example.com para 127.0.0.1:8000 (caso você rode o projeto em localhost e porta 8000).