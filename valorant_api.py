import requests

BASE_URL = "https://vlrggapi.vercel.app"

def fetch_data(endpoint):
    """Busca dados do endpoint da API especificado."""
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('data', {}).get('segments', [])
    return []

def get_news():
    """Busca as últimas notícias relacionadas a eSports de Valorant."""
    return fetch_data("/news")


def get_rankings(region):
    """Busca rankings para uma região específica."""
    return fetch_data(f"/rankings/{region}")

def get_stats(region, timespan):
    """Busca estatísticas de jogadores para uma região e período específicos."""
    return fetch_data(f"/stats/{region}/{timespan}")

def get_upcoming_matches():
    """Busca partidas futuras."""
    return fetch_data("/match/upcoming")

def get_live_scores():
    """Busca placares ao vivo para partidas em andamento."""
    return fetch_data("/match/live_score")
