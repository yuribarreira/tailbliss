"""
SME CRM Cleaner - Sistema de Limpeza e Normalização de Dados
Adaptado para Netlify Functions
"""

import json
import re
from typing import Dict, Any, List
from datetime import datetime


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handler para funcionalidades de limpeza de dados CRM
    
    Args:
        event: Dados da requisição HTTP
        context: Contexto da execução da função
        
    Returns:
        Resposta HTTP formatada para Netlify
    """
    
    # Headers padrão para CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    try:
        # Processar método HTTP
        http_method = event.get('httpMethod', 'GET')
        
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        elif http_method == 'POST':
            # Processar dados para limpeza
            body = event.get('body', '{}')
            if isinstance(body, str):
                data = json.loads(body)
            else:
                data = body
            
            # Executar limpeza conforme o tipo solicitado
            operation = data.get('operation', 'clean_lead')
            
            if operation == 'clean_lead':
                result = clean_lead_data(data.get('lead_data', {}))
            elif operation == 'normalize_contact':
                result = normalize_contact_data(data.get('contact_data', {}))
            elif operation == 'validate_company':
                result = validate_company_data(data.get('company_data', {}))
            elif operation == 'deduplicate':
                result = deduplicate_leads(data.get('leads_list', []))
            else:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({
                        'error': 'Operação não reconhecida',
                        'operation': operation,
                        'available_operations': ['clean_lead', 'normalize_contact', 'validate_company', 'deduplicate']
                    })
                }
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'status': 'success',
                    'operation': operation,
                    'result': result,
                    'processed_at': datetime.now().isoformat()
                })
            }
        
        elif http_method == 'GET':
            # Retornar informações sobre as funcionalidades disponíveis
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'status': 'ativo',
                    'service': 'sme-crm-cleaner',
                    'version': '1.0.0',
                    'operations': {
                        'clean_lead': 'Limpa e normaliza dados de lead',
                        'normalize_contact': 'Normaliza informações de contato',
                        'validate_company': 'Valida dados da empresa',
                        'deduplicate': 'Remove leads duplicados'
                    }
                })
            }
        
        else:
            return {
                'statusCode': 405,
                'headers': headers,
                'body': json.dumps({
                    'error': 'Método não permitido',
                    'allowed_methods': ['GET', 'POST']
                })
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Erro interno do servidor',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            })
        }


def clean_lead_data(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Limpa e normaliza dados de um lead
    
    Args:
        lead_data: Dados do lead para limpeza
        
    Returns:
        Dados limpos e normalizados
    """
    
    cleaned_data = {}
    
    # Limpar nome
    if 'nome' in lead_data:
        cleaned_data['nome'] = clean_name(lead_data['nome'])
    
    # Limpar email
    if 'email' in lead_data:
        cleaned_data['email'] = clean_email(lead_data['email'])
    
    # Limpar telefone
    if 'telefone' in lead_data:
        cleaned_data['telefone'] = clean_phone(lead_data['telefone'])
    
    # Limpar empresa
    if 'empresa' in lead_data:
        cleaned_data['empresa'] = clean_company_name(lead_data['empresa'])
    
    # Limpar cargo
    if 'cargo' in lead_data:
        cleaned_data['cargo'] = clean_job_title(lead_data['cargo'])
    
    # Preservar outros campos
    for key, value in lead_data.items():
        if key not in cleaned_data:
            cleaned_data[key] = value
    
    # Adicionar metadados da limpeza
    cleaned_data['_cleaned_at'] = datetime.now().isoformat()
    cleaned_data['_cleaning_rules_applied'] = get_applied_rules(lead_data)
    
    return cleaned_data


def normalize_contact_data(contact_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza especificamente dados de contato
    """
    
    normalized = {}
    
    # Normalizar email
    if 'email' in contact_data:
        normalized['email'] = normalize_email(contact_data['email'])
        normalized['email_domain'] = extract_email_domain(normalized['email'])
    
    # Normalizar telefone
    if 'telefone' in contact_data:
        normalized['telefone'] = normalize_phone(contact_data['telefone'])
        normalized['telefone_formatado'] = format_phone_brazilian(normalized['telefone'])
    
    # Normalizar endereço se presente
    if 'endereco' in contact_data:
        normalized['endereco'] = normalize_address(contact_data['endereco'])
    
    return normalized


def validate_company_data(company_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valida dados da empresa
    """
    
    validation_result = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'suggestions': []
    }
    
    # Validar nome da empresa
    if 'nome' in company_data:
        if len(company_data['nome'].strip()) < 2:
            validation_result['errors'].append('Nome da empresa muito curto')
            validation_result['is_valid'] = False
    
    # Validar CNPJ se presente
    if 'cnpj' in company_data:
        if not validate_cnpj(company_data['cnpj']):
            validation_result['errors'].append('CNPJ inválido')
            validation_result['is_valid'] = False
    
    # Validar website se presente
    if 'website' in company_data:
        if not validate_website(company_data['website']):
            validation_result['warnings'].append('Website pode estar incorreto')
    
    return validation_result


def deduplicate_leads(leads_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Remove duplicatas de uma lista de leads
    """
    
    unique_leads = []
    duplicates_found = []
    seen_emails = set()
    seen_phones = set()
    
    for i, lead in enumerate(leads_list):
        is_duplicate = False
        duplicate_reason = []
        
        # Verificar por email
        email = lead.get('email', '').lower().strip()
        if email and email in seen_emails:
            is_duplicate = True
            duplicate_reason.append('email')
        
        # Verificar por telefone
        phone = clean_phone(lead.get('telefone', ''))
        if phone and phone in seen_phones:
            is_duplicate = True
            duplicate_reason.append('telefone')
        
        if is_duplicate:
            duplicates_found.append({
                'index': i,
                'lead': lead,
                'duplicate_reason': duplicate_reason
            })
        else:
            unique_leads.append(lead)
            if email:
                seen_emails.add(email)
            if phone:
                seen_phones.add(phone)
    
    return {
        'original_count': len(leads_list),
        'unique_count': len(unique_leads),
        'duplicates_count': len(duplicates_found),
        'unique_leads': unique_leads,
        'duplicates_found': duplicates_found
    }


# Funções utilitárias de limpeza
def clean_name(name: str) -> str:
    """Limpa e normaliza nome"""
    if not name:
        return ""
    
    # Remover espaços extras e caracteres especiais
    name = re.sub(r'\s+', ' ', name.strip())
    # Capitalizar primeira letra de cada palavra
    return name.title()


def clean_email(email: str) -> str:
    """Limpa e normaliza email"""
    if not email:
        return ""
    
    return email.lower().strip()


def clean_phone(phone: str) -> str:
    """Limpa telefone removendo caracteres não numéricos"""
    if not phone:
        return ""
    
    # Remove tudo que não é número
    numbers_only = re.sub(r'[^\d]', '', phone)
    return numbers_only


def clean_company_name(company: str) -> str:
    """Limpa nome da empresa"""
    if not company:
        return ""
    
    # Remover espaços extras
    company = re.sub(r'\s+', ' ', company.strip())
    # Remover sufixos comuns desnecessários
    suffixes = [' LTDA', ' S/A', ' S.A.', ' ME', ' EPP']
    for suffix in suffixes:
        if company.upper().endswith(suffix):
            company = company[:-len(suffix)]
    
    return company.strip()


def clean_job_title(title: str) -> str:
    """Limpa cargo/função"""
    if not title:
        return ""
    
    return title.strip().title()


def normalize_email(email: str) -> str:
    """Normaliza email"""
    return clean_email(email)


def extract_email_domain(email: str) -> str:
    """Extrai domínio do email"""
    if '@' in email:
        return email.split('@')[1]
    return ""


def normalize_phone(phone: str) -> str:
    """Normaliza telefone"""
    return clean_phone(phone)


def format_phone_brazilian(phone: str) -> str:
    """Formata telefone no padrão brasileiro"""
    if len(phone) == 11:  # Celular
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    elif len(phone) == 10:  # Fixo
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    else:
        return phone


def normalize_address(address: str) -> str:
    """Normaliza endereço"""
    if not address:
        return ""
    
    # Remover espaços extras
    address = re.sub(r'\s+', ' ', address.strip())
    return address.title()


def validate_cnpj(cnpj: str) -> bool:
    """Valida CNPJ (validação básica)"""
    cnpj = re.sub(r'[^\d]', '', cnpj)
    return len(cnpj) == 14


def validate_website(website: str) -> bool:
    """Valida website"""
    if not website:
        return False
    
    # Padrão básico para URL
    pattern = r'^https?://[^\s/$.?#].[^\s]*$|^[^\s/$.?#].[^\s]*\.[a-z]{2,}$'
    return re.match(pattern, website, re.IGNORECASE) is not None


def get_applied_rules(original_data: Dict[str, Any]) -> List[str]:
    """Retorna lista de regras de limpeza aplicadas"""
    rules = []
    
    if 'nome' in original_data:
        rules.append('normalize_name')
    if 'email' in original_data:
        rules.append('clean_email')
    if 'telefone' in original_data:
        rules.append('clean_phone')
    if 'empresa' in original_data:
        rules.append('clean_company_name')
    
    return rules
