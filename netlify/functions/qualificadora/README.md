# Sistema Qualificadora de Leads - Netlify Functions

Este diretório contém as funções adaptadas para o padrão Netlify Functions do sistema Qualificadora de Leads.

## Estrutura dos Arquivos

```
netlify/functions/qualificadora/
├── main.py                    # Handler principal do sistema
├── app.py                     # Aplicação principal com roteamento
├── dashboard_interativo.py    # Funções do dashboard
├── sme_crm_cleaner.py        # Limpeza e normalização de dados
├── requirements.txt          # Dependências Python
└── README.md                 # Esta documentação
```

## Funcionalidades Disponíveis

### 1. Main Handler (`main.py`)
- **Endpoint**: `/api/main/`
- **Métodos**: GET, POST, OPTIONS
- **Descrição**: Handler principal com health check e processamento básico

#### Exemplos de uso:
```bash
# Health check
GET /api/main/

# Processamento de dados
POST /api/main/
{
  "action": "process",
  "data": {...}
}
```

### 2. App Principal (`app.py`)
- **Endpoints**: 
  - `/api/app/leads` - Gerenciamento de leads
  - `/api/app/qualificacao` - Processo de qualificação
  - `/api/app/dashboard` - Dados do dashboard
  - `/api/app/status` - Status da aplicação
- **Métodos**: GET, POST, PUT, DELETE, OPTIONS

#### Exemplos de uso:

**Listar leads:**
```bash
GET /api/app/leads
```

**Criar novo lead:**
```bash
POST /api/app/leads
{
  "nome": "João Silva",
  "email": "joao@empresa.com",
  "telefone": "(11) 99999-9999",
  "empresa": "Empresa XYZ",
  "cargo": "Gerente"
}
```

**Qualificar lead:**
```bash
POST /api/app/qualificacao
{
  "lead_id": 1,
  "empresa": "Empresa XYZ",
  "cargo": "Gerente de TI",
  "orcamento": 50000,
  "necessidade_urgente": true,
  "autoridade_decisao": true
}
```

### 3. Dashboard Interativo (`dashboard_interativo.py`)
- **Endpoint**: `/api/dashboard/`
- **Métodos**: GET, OPTIONS
- **Descrição**: Fornece dados para visualização no dashboard

#### Exemplo de uso:
```bash
GET /api/dashboard/
```

### 4. SME CRM Cleaner (`sme_crm_cleaner.py`)
- **Endpoint**: `/api/cleaner/`
- **Métodos**: GET, POST, OPTIONS
- **Descrição**: Limpeza e normalização de dados CRM

#### Operações disponíveis:

**Limpar dados de lead:**
```bash
POST /api/cleaner/
{
  "operation": "clean_lead",
  "lead_data": {
    "nome": "  joão silva  ",
    "email": "JOAO@EMPRESA.COM",
    "telefone": "(11) 9.9999-9999",
    "empresa": "Empresa XYZ LTDA"
  }
}
```

**Normalizar contato:**
```bash
POST /api/cleaner/
{
  "operation": "normalize_contact",
  "contact_data": {
    "email": "CONTATO@EMPRESA.COM",
    "telefone": "11999999999"
  }
}
```

**Validar empresa:**
```bash
POST /api/cleaner/
{
  "operation": "validate_company",
  "company_data": {
    "nome": "Empresa ABC",
    "cnpj": "12.345.678/0001-90",
    "website": "www.empresa.com"
  }
}
```

**Remover duplicatas:**
```bash
POST /api/cleaner/
{
  "operation": "deduplicate",
  "leads_list": [
    {"email": "joao@empresa.com", "telefone": "11999999999"},
    {"email": "joao@empresa.com", "telefone": "11888888888"},
    {"email": "maria@empresa.com", "telefone": "11999999999"}
  ]
}
```

## Configuração e Deploy

### 1. Dependências
As dependências estão definidas em `requirements.txt` e serão instaladas automaticamente pelo Netlify.

### 2. Configuração no netlify.toml
O arquivo raiz `netlify.toml` já foi configurado com:
- Diretório das functions
- Runtime Python 3.9
- Redirecionamentos de API
- Headers CORS

### 3. Deploy
O deploy é automático através do Netlify quando os arquivos são commitados no repositório.

## Características da Implementação

### Headers CORS
Todas as functions incluem headers CORS apropriados para permitir chamadas de diferentes origens.

### Tratamento de Erros
Implementação robusta de tratamento de erros com retorno de códigos HTTP apropriados.

### Compatibilidade
- Handlers compatíveis com Netlify Functions
- Suporte a métodos HTTP múltiplos
- Estrutura de resposta padronizada

### Logging
Timestamps e informações de processamento são incluídos nas respostas para facilitar debugging.

## Monitoramento

### Health Checks
Todos os handlers possuem endpoints de health check que retornam:
- Status do serviço
- Versão
- Timestamp
- Informações do ambiente

### Estrutura de Resposta Padrão
```json
{
  "status": "success|error",
  "message": "Mensagem descritiva",
  "data": {...},
  "timestamp": "ISO-8601",
  "service": "nome-do-serviço",
  "version": "1.0.0"
}
```

## Desenvolvimento Local

Para testar as functions localmente, você pode executar cada arquivo Python individualmente:

```bash
python netlify/functions/qualificadora/main.py
```

Cada arquivo inclui um bloco `if __name__ == '__main__':` para testes básicos.

## Próximos Passos

1. **Integração com Database**: Conectar com banco de dados real (PostgreSQL, MongoDB, etc.)
2. **Autenticação**: Implementar sistema de autenticação JWT
3. **Logs Estruturados**: Integrar com serviços de logging
4. **Métricas**: Adicionar métricas de performance
5. **Testes**: Implementar testes automatizados
