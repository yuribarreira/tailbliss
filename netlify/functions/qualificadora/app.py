"""
App Principal - Sistema Qualificadora de Leads
Adaptado para Netlify Functions
"""

import json
import os
from typing import Dict, Any, List
from datetime import datetime

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handler para funcionalidades principais da aplicação
    
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
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    try:
        # Processar método HTTP
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        query_params = event.get('queryStringParameters') or {}
        
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Roteamento baseado no path
        if '/leads' in path:
            return handle_leads(event, http_method, headers)
        elif '/qualificacao' in path:
            return handle_qualificacao(event, http_method, headers)
        elif '/dashboard' in path:
            return handle_dashboard(event, http_method, headers)
        elif '/status' in path or path == '/':
            return handle_status(headers)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({
                    'error': 'Endpoint não encontrado',
                    'path': path,
                    'available_endpoints': ['/leads', '/qualificacao', '/dashboard', '/status']
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

def handle_leads(event: Dict[str, Any], method: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Gerencia operações com leads
    """
    
    if method == 'GET':
        # Listar leads
        leads_data = get_leads_data()
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'success',
                'data': leads_data,
                'count': len(leads_data)
            })
        }
    
    elif method == 'POST':
        # Criar novo lead
        body = event.get('body', '{}')
        if isinstance(body, str):
            lead_data = json.loads(body)
        else:
            lead_data = body
            
        new_lead = create_lead(lead_data)
        
        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps({
                'status': 'success',
                'message': 'Lead criado com sucesso',
                'data': new_lead
            })
        }
    
    elif method == 'PUT':
        # Atualizar lead existente
        body = event.get('body', '{}')
        if isinstance(body, str):
            update_data = json.loads(body)
        else:
            update_data = body
            
        updated_lead = update_lead(update_data)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'success',
                'message': 'Lead atualizado com sucesso',
                'data': updated_lead
            })
        }
    
    else:
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({
                'error': 'Método não permitido para /leads',
                'allowed_methods': ['GET', 'POST', 'PUT']
            })
        }

def handle_qualificacao(event: Dict[str, Any], method: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Gerencia processo de qualificação de leads
    """
    
    if method == 'POST':
        body = event.get('body', '{}')
        if isinstance(body, str):
            qualificacao_data = json.loads(body)
        else:
            qualificacao_data = body
            
        resultado = process_qualificacao(qualificacao_data)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'success',
                'message': 'Qualificação processada',
                'resultado': resultado
            })
        }
    
    elif method == 'GET':
        # Buscar critérios de qualificação
        criterios = get_qualificacao_criterios()
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'success',
                'criterios': criterios
            })
        }
    
    else:
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({
                'error': 'Método não permitido para /qualificacao',
                'allowed_methods': ['GET', 'POST']
            })
        }

def handle_dashboard(event: Dict[str, Any], method: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Fornece dados para dashboard
    """
    
    if method == 'GET':
        dashboard_data = get_dashboard_data()
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'success',
                'dashboard': dashboard_data
            })
        }
    
    else:
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({
                'error': 'Método não permitido para /dashboard',
                'allowed_methods': ['GET']
            })
        }

def handle_status(headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Status da aplicação
    """
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'status': 'ativo',
            'service': 'qualificadora-app',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat(),
            'environment': os.getenv('NETLIFY_ENV', 'development')
        })
    }

# Funções auxiliares (exemplo)
def get_leads_data() -> List[Dict[str, Any]]:
    """Retorna dados mockados de leads"""
    return [
        {
            'id': 1,
            'nome': 'João Silva',
            'email': 'joao@empresa.com',
            'telefone': '(11) 99999-9999',
            'empresa': 'Empresa XYZ',
            'status': 'qualificado',
            'pontuacao': 85
        },
        {
            'id': 2,
            'nome': 'Maria Santos',
            'email': 'maria@empresa.com',
            'telefone': '(11) 88888-8888',
            'empresa': 'Empresa ABC',
            'status': 'em_analise',
            'pontuacao': 72
        }
    ]

def create_lead(data: Dict[str, Any]) -> Dict[str, Any]:
    """Cria um novo lead"""
    # Simular criação
    new_lead = {
        'id': len(get_leads_data()) + 1,
        'created_at': datetime.now().isoformat(),
        **data
    }
    return new_lead

def update_lead(data: Dict[str, Any]) -> Dict[str, Any]:
    """Atualiza um lead existente"""
    # Simular atualização
    updated_lead = {
        'updated_at': datetime.now().isoformat(),
        **data
    }
    return updated_lead

def process_qualificacao(data: Dict[str, Any]) -> Dict[str, Any]:
    """Processa qualificação de lead"""
    # Lógica de qualificação simulada
    pontuacao = calcular_pontuacao(data)
    status = 'qualificado' if pontuacao >= 70 else 'nao_qualificado'
    
    return {
        'lead_id': data.get('lead_id'),
        'pontuacao': pontuacao,
        'status': status,
        'criterios_atendidos': get_criterios_atendidos(data, pontuacao),
        'processado_em': datetime.now().isoformat()
    }

def calcular_pontuacao(data: Dict[str, Any]) -> int:
    """Calcula pontuação do lead"""
    pontuacao = 0
    
    # Critérios de pontuação (exemplo)
    if data.get('empresa'):
        pontuacao += 20
    if data.get('cargo') and 'gerente' in data.get('cargo', '').lower():
        pontuacao += 25
    if data.get('orcamento', 0) > 10000:
        pontuacao += 30
    if data.get('necessidade_urgente'):
        pontuacao += 15
    if data.get('autoridade_decisao'):
        pontuacao += 10
    
    return min(pontuacao, 100)

def get_criterios_atendidos(data: Dict[str, Any], pontuacao: int) -> List[str]:
    """Retorna lista de critérios atendidos"""
    criterios = []
    
    if data.get('empresa'):
        criterios.append('Empresa identificada')
    if data.get('cargo') and 'gerente' in data.get('cargo', '').lower():
        criterios.append('Cargo de liderança')
    if data.get('orcamento', 0) > 10000:
        criterios.append('Orçamento adequado')
    if data.get('necessidade_urgente'):
        criterios.append('Necessidade urgente')
    if data.get('autoridade_decisao'):
        criterios.append('Autoridade de decisão')
        
    return criterios

def get_qualificacao_criterios() -> Dict[str, Any]:
    """Retorna critérios de qualificação"""
    return {
        'criterios': [
            {'nome': 'Empresa identificada', 'peso': 20},
            {'nome': 'Cargo de liderança', 'peso': 25},
            {'nome': 'Orçamento adequado', 'peso': 30},
            {'nome': 'Necessidade urgente', 'peso': 15},
            {'nome': 'Autoridade de decisão', 'peso': 10}
        ],
        'pontuacao_minima': 70
    }

def get_dashboard_data() -> Dict[str, Any]:
    """Retorna dados para dashboard"""
    leads = get_leads_data()
    
    return {
        'total_leads': len(leads),
        'leads_qualificados': len([l for l in leads if l['status'] == 'qualificado']),
        'leads_em_analise': len([l for l in leads if l['status'] == 'em_analise']),
        'pontuacao_media': sum(l['pontuacao'] for l in leads) / len(leads) if leads else 0,
        'ultima_atualizacao': datetime.now().isoformat()
    }
