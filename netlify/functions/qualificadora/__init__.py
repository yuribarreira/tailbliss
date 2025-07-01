"""
Sistema Qualificadora de Leads - Netlify Functions
Pacote Python com handlers adaptados para Netlify Functions

Versão: 1.0.0
Autor: Sistema Qualificadora
Descrição: Handlers para processamento de leads, dashboard e limpeza de dados CRM
"""

__version__ = "1.0.0"
__author__ = "Sistema Qualificadora"
__description__ = "Netlify Functions para Sistema de Qualificação de Leads"

# Importações principais
from .main import handler as main_handler
from .app import handler as app_handler
from .dashboard_interativo import handler as dashboard_handler
from .sme_crm_cleaner import handler as cleaner_handler

# Metadata do pacote
__all__ = [
    'main_handler',
    'app_handler', 
    'dashboard_handler',
    'cleaner_handler'
]

# Configurações globais
DEFAULT_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Content-Type': 'application/json'
}

SERVICE_INFO = {
    'name': 'qualificadora-functions',
    'version': __version__,
    'description': __description__,
    'endpoints': {
        'main': '/api/main/',
        'app': '/api/app/',
        'dashboard': '/api/dashboard/',
        'cleaner': '/api/cleaner/'
    }
}
