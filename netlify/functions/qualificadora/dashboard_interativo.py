"""
Dashboard Interativo - Sistema Qualificadora de Leads
Adaptado para Netlify Functions
"""

import json
from typing import Dict, Any
from datetime import datetime


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handler para dashboard interativo
    
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
        
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        if http_method == 'GET':
            # Fornecer dados do dashboard
            dashboard_data = fetch_dashboard_data()
            
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
                    'error': 'Método não permitido',
                    'allowed_methods': ['GET']
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

def fetch_dashboard_data() -> Dict[str, Any]:
    """
    Busca dados para o dashboard interativo
    """
    
    # Suposto processamento dinâmico de dados
    leads_count = 10  # Exemplo de contagem de leads
    avg_score = 75.5  # Exemplo de pontuação média
    qualificados = 7  # Exemplo de leads qualificados
    em_analise = 3  # Exemplo de leads em análise
    
    return {
        'total_leads': leads_count,
        'leads_qualificados': qualificados,
        'leads_em_analise': em_analise,
        'pontuacao_media': avg_score,
        'ultima_atualizacao': datetime.now().isoformat()
    }
