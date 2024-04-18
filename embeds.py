import nextcord  # Modificado de 'import discord' para 'import nextcord'

def live_scores_embed(live_scores):
    embed = nextcord.Embed(title="Partidas Ao Vivo", description="Acompanhe as partidas que estão acontecendo agora!", color=0xe74c3c)
    for live in live_scores:
        embed.add_field(name=f"{live['team1']} vs {live['team2']}", value=f"Placar: {live['score1']}-{live['score2']} - [Detalhes]({live['match_page']})", inline=False)
    return embed

def upcoming_matches_embed(upcoming_matches):
    embed = nextcord.Embed(title="Próximas Partidas", description="Veja as partidas que estão por vir:", color=0x3498db)
    for match in upcoming_matches:
        embed.add_field(name=f"{match['team1']} vs {match['team2']}", value=f"Começa em: {match['time_until_match']} - [Detalhes]({match['match_page']})", inline=False)
    return embed

def tournament_embed(tournament_name, tournament_icon_url):
    embed = nextcord.Embed(title="Informações do Torneio", description=f"Detalhes sobre o torneio: {tournament_name}", color=0xffd700)
    embed.set_thumbnail(url=tournament_icon_url)
    return embed

def news_embed(news_items):
    embed = nextcord.Embed(title="Últimas Notícias de Valorant", description="Confira as novidades mais recentes!", color=0x1abc9c)
    # Limitando a quantidade de itens em news_items para não exceder 25 campos por Embed
    news_items = news_items[:25]
    for news in news_items:
        embed.add_field(name=news['title'], value=f"{news['description']} [Leia mais]({news['url_path']})", inline=False)
    return embed

def ranking_embed(rankings, region):
    embed = nextcord.Embed(title=f"Ranking de Times - {region.capitalize()}", color=0x1abc9c)
    for ranking in rankings:
        embed.add_field(
            name=f"#{ranking['rank']} {ranking['team']}",
            value=f"Record: {ranking['record']} | Ganhos: {ranking['earnings']}",
            inline=False
        )
    return embed