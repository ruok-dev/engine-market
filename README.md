# 🚀 Engine Market - Market Management System

Engine Market é um sistema completo de gestão para mercados, desenvolvido com foco em alta performance, segurança e automação. O projeto abrange desde o controle de vendas e estoque até a reposição automática de produtos via workers em segundo plano.

![Dashboard Preview](https://github.com/ruok-dev/engine-market/raw/main/screenshot_placeholder.png) <!-- Note: Replace with your actual screenshot after push -->

## 🛠️ Tecnologias
- **Backend**: Python 3.11, FastAPI, SQLModel (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL 15
- **Task Queue**: Celery + Redis
- **Frontend**: React (Vite), Tailwind CSS, Lucide Icons, Recharts
- **Infrastructure**: Docker & Docker Compose

## ✨ Funcionalidades
- **Gestão de Vendas**: Processamento de vendas em tempo real com baixa automática no estoque.
- **Controle de Estoque Inteligente**: Monitoramento de níveis mínimos e reposição automática via Celery Workers.
- **Painel Financeiro**: Monitoramento de gastos (compras/reposição) e ganhos (vendas) integrado.
- **Dashboard Premium**: Interface moderna com Glassmorphism e gráficos de performance.
- **Alertas de Sistema**: Notificações de estoque baixo e movimentações financeiras.

## 🚀 Como Rodar o Projeto

### Pré-requisitos
- Docker e Docker Compose instalados.

### Passo a Passo
1. **Clone o repositório**:
   ```bash
   git clone https://github.com/ruok-dev/engine-market.git
   cd engine-market
   ```

2. **Configure as variáveis de ambiente**:
   ```bash
   cp .env.example .env
   # Edite o .env com suas chaves secretas
   ```

3. **Suba os containers**:
   ```bash
   docker-compose up --build
   ```

4. **Inicialize o banco de dados e o superusuário**:
   ```bash
   docker-compose exec api python app/create_superuser.py
   ```

5. **Acesse as interfaces**:
   - **Frontend**: `http://localhost:5173`
   - **API Documentation (Swagger)**: `http://localhost:8000/docs`

## 🔒 Segurança e Melhores Práticas
- **Autenticação**: JWT (JSON Web Tokens) com expiração configurável.
- **Hashing**: Senhas armazenadas com Bcrypt.
- **Proteção de Dados**: Variáveis sensíveis isoladas em `.env` e protegidas pelo `.gitignore`.
- **Arquitetura**: Separação clara entre lógica de negócio (Services) e interfaces (API/Worker).

## 📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

---
Desenvolvido com ❤️ por [ruok-dev](https://github.com/ruok-dev)
