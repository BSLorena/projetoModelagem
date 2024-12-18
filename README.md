# projetoModelagem
BSI SPORTS
Projeto desenvolvido para a disciplina de Modelagem de Sistemas. O objetivo é criar uma aplicação desktop que permita o registro e a configuração de perfis de usuários com foco em esportes, utilizando conceitos de banco de dados e interface gráfica.

Descrição do Projeto
O BSI SPORTS é uma aplicação simples que permite:

Registro de usuários com validação de dados e segurança de senha.
Configuração de perfis esportivos, incluindo informações pessoais, esportes praticados e objetivos.
Persistência de dados utilizando um banco de dados relacional SQLite.
A aplicação é construída com a biblioteca Tkinter, que oferece uma interface gráfica intuitiva para o usuário.

Funcionalidades
Registro de Usuários:

Validação de e-mail e senha.
Verificação de duplicidade de e-mail.
Configuração de Perfil:

Registro de dados pessoais: nome, peso, altura e idade.
Definição de esportes praticados, nível de experiência, conquistas e objetivos.
Banco de Dados Relacional:

Utilização do SQLite para armazenar dados dos usuários e seus perfis.
Tecnologias Utilizadas
Python 3.10+: Linguagem principal do projeto.
Tkinter: Para construção da interface gráfica.
SQLite: Banco de dados relacional embutido.
Expressões Regulares (re): Para validação de senhas.
Como Executar o Projeto
Pré-requisitos:

Python 3.10 ou superior instalado.
Editor de texto ou IDE (ex.: VSCode, PyCharm).
Clone o Repositório:

bash
Copiar código
git clone <URL_DO_REPOSITÓRIO>
cd <PASTA_DO_PROJETO>
Execute o Projeto:
No terminal, execute o seguinte comando:

bash
Copiar código
python main.py
Interaja com a Aplicação:

Registre-se com um e-mail e senha.
Configure seu perfil esportivo.
Estrutura do Projeto
bash
Copiar código
.
├── main.py       # Código principal do projeto
├── users.db      # Banco de dados SQLite (gerado automaticamente)
└── README.md     # Arquivo de documentação
Casos de Uso
Caso de Uso 001: Registro de Usuários
O sistema permite o registro de novos usuários, garantindo que:
A senha tenha no mínimo 8 caracteres e inclua números e letras.
O e-mail seja único.
Caso de Uso 002: Configuração de Perfis
Após o registro, o usuário pode configurar informações como:
Dados pessoais (nome, peso, altura, idade).
Detalhes esportivos (esporte praticado, nível de experiência, conquistas, objetivos).
Autor
Este projeto foi desenvolvido por:
Emilie Nelise Rodrigues da Silva
Ketlen Victória Martins de Souza
Lorena Bitencourt Salvador
como parte dos requisitos da disciplina Modelagem de Sistemas do curso de Sistemas de Informação, Usp São Carlos.

