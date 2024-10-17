from django.shortcuts import render
from django.views import View
import requests

class IndexView(View):
    def get(self, request):
        # Domínio válido a ser consultado
        domain = 'google.com.br'

        # Fazendo a requisição para a API do Registro.br
        api_url = f'https://registro.br/rdap/domain/{domain}'
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Levanta um erro para códigos de status HTTP como 4xx/5xx

            # Exibindo o status da resposta e seu conteúdo bruto para ajudar no debug
            status_code = response.status_code
            raw_response = response.text

            # Tentando converter a resposta em JSON
            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                data = {
                    'error': 'Não foi possível interpretar a resposta como JSON.',
                    'status_code': status_code,
                    'raw_response': raw_response  # Adicionando a resposta "crua" para ajudar no debug
                }

        except requests.exceptions.RequestException as e:
            # Qualquer erro de conexão ou requisição será tratado aqui
            data = {
                'error': f'Erro ao fazer a requisição: {str(e)}',
                'status_code': 'N/A',
                'raw_response': 'N/A'
            }

        # Renderizando a resposta no template
        return render(request, 'index.html', {'data': data})
