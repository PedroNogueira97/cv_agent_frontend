# CV Agent Frontend

Este é o repositório do frontend para o projeto **CV Agent**. A aplicação é construída com **Streamlit** e consome uma API desenvolvida utilizando **FastAPI** e **Agno** (anteriormente Phidata).

## 🚀 Tecnologias

- **Streamlit**: Interface do usuário moderna e interativa.
- **Python**: Linguagem base para o desenvolvimento.
- **FastAPI (Backend)**: API robusta para processamento dos agentes.
- **Agno (Backend)**: Framework para criação e gerenciamento de agentes de IA.

## 🛠️ Como Executar

1. **Clone o repositório:**

   ```bash
   git clone git@github.com:PedroNogueira97/cv_agent_frontend.git
   cd cv_agent_frontend
   ```

2. **Crie um ambiente virtual e instale as dependências:**

   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   ```

3. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto com as chaves necessárias (baseie-se no `.env.example` se disponível).

4. **Execute a aplicação:**

   ```bash
   streamlit run app.py
   ```

## 📄 Arquitetura

O projeto segue uma arquitetura desacoplada:

- **Frontend**: Streamlit cuidando da renderização e interação com o usuário.
- **Backend (API)**: FastAPI integrando Agno para fornecer inteligência via agentes.
