import asyncio
import nextcord
from valorant_api import get_live_scores, get_news
from embeds import live_scores_embed, news_embed

notification_channels = {}

async def notify_live_matches(client):
    """Envia notificações de partidas ao vivo conforme elas acontecem."""
    while True:
        if notification_channels:
            live_matches = get_live_scores()
            for guild_id, channel_id in notification_channels.items():
                channel = client.get_channel(channel_id)
                if live_matches and channel:
                    embed = live_scores_embed(live_matches)
                    await channel.send(embed=embed)
                elif channel:
                    await channel.send("Nenhum jogo ao vivo no momento.")
        await asyncio.sleep(300)  # Atualiza a cada 5 minutos

async def notify_news(client):
    """Envia notificações das últimas notícias de Valorant."""
    last_news_date = None  # Guarda a data da última notícia notificada
    while True:
        if notification_channels:
            news_items = get_news()
            for guild_id, channel_id in notification_channels.items():
                channel = client.get_channel(channel_id)
                if news_items and channel:
                    new_news_items = [
                        news for news in news_items if last_news_date is None or news['date'] > last_news_date
                    ]
                    if new_news_items:  # Garante que o embed será criado apenas se houver novas notícias
                        embed = news_embed(new_news_items)
                        await channel.send(embed=embed)
                        last_news_date = new_news_items[0]['date']  # Atualiza a data da última notícia notificada
                elif channel:
                    await channel.send("Nenhuma nova notícia no momento.")
        await asyncio.sleep(1800)  # Atualiza a cada 30 minutos

notification_channels = {}

def set_notification_channel(guild_id, channel_id):
    """Define o canal de notificações para uma guilda específica."""
    notification_channels[guild_id] = channel_id
    return True