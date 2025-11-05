# Agregador de Links (SaaS)

Um agregador de links multi-usuário (estilo "Linktree") completo, construído com Python, Flask e PostgreSQL. A aplicação permite que utilizadores se registem, façam login e personalizem uma página de perfil pública com os seus links, bio e foto de perfil.

> **Site ao Vivo:** [https://agregador-links.onrender.com/](https://agregador-links.onrender.com/)

*(Nota: O plano gratuito do Render pode demorar até 50 segundos a "acordar" no primeiro acesso.)*

---

## 🚀 Funcionalidades Principais

* **Autenticação de Utilizador:** Sistema completo de Registo, Login e Logout usando `Flask-Login` e passwords encriptadas (hash).
* **Painel de Controlo (`/admin`):** Um painel de gestão privado para cada utilizador, protegido por login (`@login_required`).
* **Gestão de Links (CRUD):** Os utilizadores podem Adicionar, Editar e Apagar os seus próprios links.
* **Gestão de Perfil:** Os utilizadores podem editar o seu Nome de Exibição, Bio e fazer o upload de uma Foto de Perfil personalizada.
* **Página Pública Dinâmica:** Cada utilizador tem uma página de perfil pública e única (ex: `/diego`), que exibe a sua foto, bio e links guardados no banco de dados.

---

## 🛠️ Stack de Tecnologias

* **Backend:** Python 3.12+
* **Framework:** Flask
* **Base de Dados:** PostgreSQL
* **ORM:** Flask-SQLAlchemy
* **Migrações:** Flask-Migrate (Alembic)
* **Autenticação:** Flask-Login
* **Frontend:** HTML5, CSS3, Bootstrap 5 (Dark Theme)
* **Deploy (Servidor):** Gunicorn
* **Configuração:** `python-dotenv`

---

## 🏗️ Estrutura do Projeto

O projeto foi refatorado para usar uma estrutura de "pacote" (`agregador/`) para uma melhor organização e manutenção:

/Agregador_Links ├── agregador/ <-- Pacote principal da aplicação │ ├── init.py (Marca a pasta como um pacote) │ ├── config.py (Guarda as configurações da app) │ ├── main.py (Onde estão as rotas e a lógica Flask) │ ├── models.py (Definições das tabelas do banco de dados) │ ├── static/ (CSS e imagens de upload) │ └── templates/ (Todos os ficheiros HTML) │ ├── migrations/ (Ficheiros de migração do Flask-Migrate) ├── .gitignore (Ignora ficheiros sensíveis e lixo) ├── Procfile (Instruções de deploy para o Render/Gunicorn) ├── requirements.txt (Lista de dependências Python) └── README.MD (Você está aqui!)


---

## ⚙️ Como Executar Localmente

### Pré-requisitos

* Python 3.10+
* PostgreSQL (ter um servidor local ou na nuvem a correr)
* Git

### 1. Clonar o Repositório

```bash
git clone [https://github.com/JoaoSandovall/Agregador_Links.git](https://github.com/JoaoSandovall/Agregador_Links.git)
cd Agregador_Links
2. Configurar o Ambiente Virtual
Bash

# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente (Windows)
.\venv\Scripts\activate
# (macOS/Linux)
# source venv/bin/activate
3. Instalar as Dependências
Bash

pip install -r requirements.txt
4. Configurar as Variáveis de Ambiente
Crie um ficheiro chamado .env na raiz do projeto (onde está o .gitignore). Este ficheiro não é enviado para o GitHub.

Crie um banco de dados PostgreSQL (ex: agregador_db) e preencha o .env com as suas credenciais:

Fragmento do código

# .env
# Substitua com os seus dados do PostgreSQL local
DATABASE_URL="postgresql://SEU_USER:SUA_SENHA@localhost:5432/agregador_db"

# Gere uma chave secreta forte (ex: python -c "import secrets; print(secrets.token_hex(24))")
SECRET_KEY="SUA_CHAVE_SECRETA_LONGA_E_ALEATORIA"
5. Correr as Migrações do Banco
Para construir as tabelas (usuario e link) no seu banco de dados pela primeira vez:

Bash

# Definir a app Flask (PowerShell)
$env:FLASK_APP = "agregador.main"
# (macOS/Linux: export FLASK_APP="agregador.main")

# Correr o "upgrade"
python -m flask db upgrade
6. Executar a Aplicação
Bash

# Correr o servidor de desenvolvimento do Flask
python -m flask run
Abra http://127.0.0.1:5000 no seu navegador. Você será redirecionado para a página de login.
