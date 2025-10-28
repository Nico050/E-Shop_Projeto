# 🛒 E-Shop_Projeto

## Descrição

Este é um projeto de desenvolvimento de um **E-Shop (Loja Virtual)** que utiliza a **Arquitetura de Microserviços**. Foi desenvolvido para a disciplina de Engenharia de Software, com foco na modularização e independência dos serviços.

O projeto demonstra como um sistema de comércio eletrônico pode ser dividido em componentes menores e interconectados, como serviços de usuários, catálogo de produtos e processamento de pedidos.

### 🛠️ Tecnologias Principais

| Categoria | Tecnologia | Detalhes |
| :--- | :--- | :--- |
| **Linguagem** | Python | Linguagem principal de desenvolvimento. |
| **Arquitetura** | Microserviços | Abordagem modular para o sistema. |
| **Containerização** | Docker, Docker Compose | Para garantir um ambiente de desenvolvimento isolado e fácil. |
| **Banco de Dados** | SQLite | Usado como banco de dados padrão para desenvolvimento. |

---

## 🚀 Como Importar e Rodar o Projeto

Siga os passos abaixo para configurar o ambiente e iniciar a aplicação.

### Pré-requisitos

Certifique-se de que você tem instalado em sua máquina:
* **Git**
* **Docker** e **Docker Compose**

### 1. Clonar o Repositório

Abra seu terminal ou prompt de comando, navegue até a pasta desejada e execute os comandos:

```bash
# Comando para clonar o repositório
git clone [https://github.com/Nico050/E-Shop_Projeto.git](https://github.com/Nico050/E-Shop_Projeto.git)

# Acessar a pasta do projeto
cd E-Shop_Projeto
```

### 2. Inicializar os Serviços com Docker Compose

O projeto utiliza Docker Compose para orquestrar todos os microserviços e suas dependências.

Execute o seguinte comando para construir as imagens e iniciar todos os containers:

```bash
# Constrói as imagens (apenas na primeira vez) e inicia os containers em background (-d)
docker-compose up --build -d
```

### 3. Acessar a Aplicação

Após a conclusão do comando, o E-Shop estará rodando e acessível no seu navegador:

http://localhost:8000 (Verifique a porta configurada no seu docker-compose.yml, se for diferente de 8000).
