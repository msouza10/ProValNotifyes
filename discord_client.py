import nextcord
from nextcord.ext import commands
from valorant_api import get_news, get_rankings, get_stats, get_upcoming_matches, get_live_scores
from notifications import notify_live_matches, notify_news, set_notification_channel
from embeds import news_embed, upcoming_matches_embed, live_scores_embed, ranking_embed
import logging

logging.basicConfig(level=logging.INFO)


permissions_admin = nextcord.Permissions(administrator=True)
intents = nextcord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Habilita o intent de conteúdo de mensagem

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    try:
        await bot.tree.sync()  # Sincroniza os slash commands com o Discord
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Adicionando tarefas assíncronas ao loop do bot
bot.loop.create_task(notify_live_matches(bot))
bot.loop.create_task(notify_news(bot))

@bot.slash_command(name="set_channel", description="Define o canal para notificações")
async def set_channel(interaction: nextcord.Interaction):
    if interaction.user.guild_permissions.manage_channels:
        set_notification_channel(interaction.guild_id, interaction.channel_id)
        await interaction.response.send_message("Canal de notificações definido com sucesso.")
    else:
        await interaction.response.send_message("Você não tem permissão para definir o canal de notificações.", ephemeral=True)

@bot.slash_command(name="news", description="Mostra as últimas notícias")
async def send_news(interaction: nextcord.Interaction):
    news_items = get_news()
    if news_items:
        embed = news_embed(news_items)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Nenhuma notícia disponível.")

@bot.slash_command(name="upcoming", description="Mostra partidas futuras")
async def send_upcoming(interaction: nextcord.Interaction):
    upcoming = get_upcoming_matches()
    if upcoming:
        embed = upcoming_matches_embed(upcoming)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Nenhuma partida futura programada.")

@bot.slash_command(name="live", description="Mostra as pontuações ao vivo")
async def send_live(interaction: nextcord.Interaction):
    live_scores = get_live_scores()
    if live_scores:
        embed = live_scores_embed(live_scores)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Nenhuma partida ao vivo no momento.")
