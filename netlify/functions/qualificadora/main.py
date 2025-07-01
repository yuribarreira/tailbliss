"""
Função principal adaptada para Netlify Functions
Sistema Qualificadora de Leads - Handler Principal
"""

import json
import os
from typing import Dict, Any

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handler principal para Netlify Functions
    
    Args:
        event: Dados da requisição HTTP
        context: Contexto da execução da função
        
    Returns:
        Resposta HTTP formatada para Netlify
    """
    
    # Headers padrão para CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    try:
        # Processar método HTTP
        http_method = event.get('httpMethod', 'GET')
        
        if http_method == 'OPTIONS':
            # Resposta para preflight CORS
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        elif http_method == 'GET':
            # Endpoint de status/health check
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'status': 'success',
                    'message': 'Sistema Qualificadora ativo',
                    'service': 'main',
                    'version': '1.0.0'
                })
            }
            
        elif http_method == 'POST':
            # Processar dados da requisição
            body = event.get('body', '{}')
            if isinstance(body, str):
                data = json.loads(body)
            else:
                data = body
            
            # Aqui seria a lógica principal da aplicação
            result = process_main_request(data)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(result)
            }
        
        else:
            return {
                'statusCode': 405,
                'headers': headers,
                'body': json.dumps({
                    'error': 'Método não permitido',
                    'allowed_methods': ['GET', 'POST', 'OPTIONS']
                })
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Erro interno do servidor',
                'message': str(e)
            })
        }

def process_main_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processa requisições principais do sistema
    
    Args:
        data: Dados da requisição
        
    Returns:
        Resultado processado
    """
    
    # Lógica principal da aplicação aqui
    # Importar e usar módulos específicos conforme necessário
    
    return {
        'status': 'success',
        'message': 'Requisição processada com sucesso',
        'data': data,
        'timestamp': '2025-01-01T00:00:00Z'
    }

# Para compatibilidade com diferentes ambientes
def lambda_handler(event, context):
    """Alias para AWS Lambda compatibility"""
    return handler(event, context)

# Para testes locais
if __name__ == '__main__':
    # Teste local
    test_event = {
        'httpMethod': 'GET',
        'headers': {},
        'body': '{}'
    }
    
    test_context = {}
    
    result = handler(test_event, test_context)
    print(json.dumps(result, indent=2))
