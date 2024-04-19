import asyncio
import nextcord
from valorant_api import get_live_scores, get_news
from embeds import live_scores_embed, news_embed, score_update_embed
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)

notification_channels = {}
live_scores_cache = {}
news_cache = {}

async def notify_live_matches(client):
    """Envia notificações de partidas ao vivo conforme elas acontecem."""
    while True:
        if notification_channels:
            for guild_id, channel_id in notification_channels.items():
                channel = client.get_channel(channel_id)
                if channel:
                    try:
                        live_matches = await asyncio.to_thread(get_live_scores)
                        if live_matches:
                            for live_match in live_matches:
                                match_id = live_match.get('id')
                                team1 = live_match.get('team1')
                                team2 = live_match.get('team2')
                                score1 = live_match.get('score1')
                                score2 = live_match.get('score2')

                                # A partida é considerada nova se o ID da partida não estiver no cache
                                if match_id not in live_scores_cache.get(channel_id, {}):
                                    # Notifica a partida ao vivo apenas se ela for nova
                                    if score1 == 0 and score2 == 0:
                                        embed = live_scores_embed([live_match])
                                        await channel.send(embed=embed)
                                        live_scores_cache.setdefault(channel_id, {})[match_id] = (score1, score2)
                                else:
                                    # Envia atualização de placar apenas se o placar tiver mudado
                                    if (score1, score2) != live_scores_cache[channel_id][match_id] and (score1 > 0 or score2 > 0):
                                        embed = score_update_embed(team1, team2, score1, score2)
                                        await channel.send(embed=embed)
                                        # Atualiza o placar no cache
                                        live_scores_cache[channel_id][match_id] = (score1, score2)
                    except Exception as e:
                        logging.error(f"Erro ao obter partidas ao vivo: {e}")
        await asyncio.sleep(30)  # Atualiza a cada 5 minutos

async def notify_news(client):
  """Envia notificações das últimas notícias de Valorant."""
  while True:
      if notification_channels:
          for guild_id, channel_id in notification_channels.items():
              channel = client.get_channel(channel_id)
              if channel:
                  try:
                      news_items = get_news()  # Supomos que get_news() retorna uma lista de notícias ordenadas pela data, a mais recente primeiro
                      if news_items:
                          # Obtenha a data da última notícia enviada para este canal, se houver
                          last_news_date = news_cache.get(channel_id, {}).get('date', None)

                          # A primeira notícia da lista é a mais recente
                          latest_news = news_items[0]
                          latest_news_date = latest_news.get('date')

                          # Verifica se a última notícia é mais recente do que a última notícia notificada
                          if latest_news_date is not None and (last_news_date is None or latest_news_date > last_news_date):
                              embed = news_embed([latest_news])  # Supomos que news_embed() pode aceitar uma lista de notícias
                              await channel.send(embed=embed)

                              # Atualizar o cache com a data da última notícia enviada
                              news_cache[channel_id] = {'date': latest_news_date}
                  except Exception as e:
                      logging.error(f"Erro ao obter notícias: {e}")
      await asyncio.sleep(60)

def set_notification_channel(guild_id, channel_id):
    """Define o canal de notificações para uma guilda específica."""
    notification_channels[guild_id] = channel_id
    return True
