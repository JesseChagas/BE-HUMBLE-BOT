import discord
from discord.ext import commands
import pandas as pd
from datetime import datetime, timedelta
from discord import app_commands
from discord.ui import View, Select, Button
import asyncio
import pytz

from config import bot_token

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


df = pd.DataFrame()  # Variável global
data_loaded = False  # Flag para indicar se os dados foram carregados

@bot.event
async def on_ready():
    print('Logged on as {0.user}!'.format(bot))

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands successfully!")
    except Exception as e:
        print(e)

    timezone = pytz.timezone('America/Sao_Paulo')

    # Carrega os dados apenas na primeira vez que o bot é iniciado
    global data_loaded, df
    if not data_loaded:
        df = pd.read_excel('teste.xlsx', engine='openpyxl')
        data_loaded = True

    # Agenda o evento para ocorrer todos os dias no fuso horário configurado
    while True:
        now = datetime.now(timezone)
        target_time = now.replace(hour=17, minute=30, second=0, microsecond=0)
        if now > target_time:
            target_time += timedelta(days=1)  # Se já passou do horário, agenda para o próximo dia
        delta = target_time - now
        await asyncio.sleep(delta.total_seconds())
        await verificar_aniversarios(timezone)

async def verificar_aniversarios(timezone):
    global df
    today = datetime.now(timezone).strftime('%d/%m')

    for index, row in df.iterrows():
        aniversario = row['Aniversario']
        nome_discord = row['Nome_discord']
        member = bot.get_guild(1171876536991891459).get_member_named(nome_discord)

        if aniversario == today and member:
            channel = bot.get_guild(1171876536991891459).get_channel(1171884351269654560)

            if channel:
                # Criar um objeto Embed
                embed = discord.Embed(
                    title=f'Feliz aniversário, {member.display_name}! 🎉',
                    description=f'Agradecemos por fazer parte da nossa comunidade BE | HUMBLE.\n\n'
                                f'Neste dia especial, queremos não apenas reconhecer seu talento como jogador, mas também desejar a você um ano repleto de vitórias dentro e fora do game. Que cada partida seja uma oportunidade para mostrar o seu melhor e alcançar novos patamares.\n\n'
                                f'Em nome do clube BE | HUMBLE, queremos expressar nossa gratidão por ter você conosco. Sua presença torna nosso clube mais especial. Que este novo ano de vida seja cheio de felicidade, sucesso e momentos inesquecíveis.\n\n'
                                f'BE | HUMBLE 🏆🎂',
                    color=0xFFD700  # Cor dourada
                )

                # Substitua '123456789012345678' pelo ID do membro que você deseja marcar
                embed.add_field(name='', value=f'<@{member.id}>', inline=False)

                # Adicionar uma imagem ao embed (substitua pela URL da imagem desejada)
                embed.set_thumbnail(url='https://i.imgur.com/OefNYXb.png')

                # Enviar o embed
                await channel.send(embed=embed)

# Função para coamndo slash registro
async def iniciar_processo_registro(member):
    await member.send("👋Olá! Bem-vindo ao servidor. Por favor, digite seu nickname:")

    def check_nickname(msg):
        return msg.author == member and isinstance(msg.channel, discord.DMChannel)

    response_nickname = await bot.wait_for("message", check=check_nickname)

    # Pergunta sobre o nome pessoal
    await member.send("Qual é o seu nome pessoal?")

    # Função para coletar o nome pessoal
    def check_nome_pessoal(msg):
        return msg.author == member and isinstance(msg.channel, discord.DMChannel)

    response_nome_pessoal = await bot.wait_for("message", check=check_nome_pessoal)

    # Pergunta sobre a data de aniversário
    await member.send("Qual é a sua data de aniversário?📅 (Formato: DD/MM)")

    # Função para coletar a data de aniversário
    def check_aniversario(msg):
        return msg.author == member and isinstance(msg.channel, discord.DMChannel)

    response_aniversario = await bot.wait_for("message", check=check_aniversario)

    # Adiciona as informações à planilha
    new_data = {'Nome_discord': response_nickname.content, 'Aniversario': response_aniversario.content}
    global df
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

    # Pergunta sobre os horários disponíveis
    await member.send("Em quais períodos do dia você costuma estar disponível? Por exemplo, algo como 14h às 16h ou 20h às 00h🕒")

    # Função para coletar os horários disponíveis
    def check_schedule(msg):
        return msg.author == member and isinstance(msg.channel, discord.DMChannel)

    response_horarios = await bot.wait_for("message", check=check_schedule)

    await member.send(f"Obrigado por se registrar no servidor!😊🚀")

    # Envia a mensagem com as informações coletadas para um canal do servidor
    server = member.guild  # Obtém o servidor do membro
    channel_id = 1171884351269654560  # Substitua pelo ID do canal do servidor onde deseja enviar as mensagens

    # Envia a mensagem para o canal do servidor
    channel = server.get_channel(channel_id)
    if channel is not None:
        mensagem = f"**Dados de Usuário**\n\n- **Nickname:** {response_nickname.content}\n- **Nome Pessoal:** {response_nome_pessoal.content}\n- **Aniversário:** {response_aniversario.content}\n- **Horários disponíveis:** {response_horarios.content}\n\n---"
        await channel.send(mensagem)

    # Salva a planilha após coletar todas as informações
    df.to_excel('teste.xlsx', index=False, engine='openpyxl')


@bot.event
async def on_message(message):
    if message.content.startswith("/registro"):
        await iniciar_processo_registro(message.author)


@bot.tree.command(name="limpar", description="Limpa mensagens.")
async def limpar(interaction: discord.Interaction, quantidade: int):
    # Verifica se o autor da interação é um administrador
    if interaction.user.guild_permissions.administrator:
        # Limpar mensagens
        await interaction.response.send_message(f'{quantidade} mensagens foram removidas por {interaction.user.mention}.')
        await interaction.channel.purge(limit=quantidade)
    else:
        # Se o autor não for um administrador, enviar mensagem de erro
        await interaction.response.send_message('Você não tem permissão para usar este comando.')



# Comando slash ping
@bot.tree.command(name="ping", description="Informa o ping atual do bot.")
async def ping(interaction: discord.Interaction):
    bot_ping = round(bot.latency * 1000)  # Ping do bot em milissegundos
    await interaction.response.send_message(f'O ping do bot é: {bot_ping}ms')

# Comando slash registro
@bot.tree.command(name="registro", description="Inicia o processo de registro.")
async def registro(interaction: discord.Interaction):
    member = interaction.user
    await interaction.response.send_message(f'Olá {member.mention}! 😊 O seu cadastro foi iniciado. Por favor, responda à mensagem que enviei na sua DM para continuarmos.')
    await iniciar_processo_registro(member)

# Comando slash mensagem embed
@bot.tree.command(name="embed", description="Mensagem embed personalizada.")
async def embed(interaction: discord.Interaction):
    member = interaction.user

    # Envie uma mensagem inicial pedindo o título
    await interaction.response.send_message("Digite o título da mensagem embed:")

    # Espere pela resposta do usuário (título)
    title_msg = await bot.wait_for(
        "message",
        check=lambda m: m.author == member and m.channel == interaction.channel
    )

    # Envie uma mensagem pedindo a descrição
    await interaction.followup.send("Digite a descrição da mensagem embed:")

    # Espere pela resposta do usuário (descrição)
    description_msg = await bot.wait_for(
        "message",
        check=lambda m: m.author == member and m.channel == interaction.channel
    )

    # Envie uma mensagem pedindo a cor
    await interaction.followup.send("Digite a cor da mensagem embed (código hexadecimal):")

    # Espere pela resposta do usuário (cor)
    color_msg = await bot.wait_for(
        "message",
        check=lambda m: m.author == member and m.channel == interaction.channel
    )

    # Converta o código hexadecimal para inteiro e adicione à criação do Embed
    color = int(color_msg.content, 16)
    embed = discord.Embed(
        title=title_msg.content,
        description=description_msg.content,
        color=color
    )

    # Pergunte se o usuário deseja adicionar campos adicionais
    await interaction.followup.send("Deseja adicionar campos adicionais? Responda sim ou não:")

    # Espere pela resposta do usuário (sim ou não)
    fields_msg = await bot.wait_for(
        "message",
        check=lambda m: m.author == member and m.channel == interaction.channel and m.content.lower() in ["sim", "não"]
    )

    if fields_msg.content.lower() == "sim":
        # Solicite o número de campos que o usuário deseja adicionar
        await interaction.followup.send("Quantos campos você deseja adicionar?")
        
        # Espere pela resposta do usuário (número de campos)
        num_fields_msg = await bot.wait_for(
            "message",
            check=lambda m: m.author == member and m.channel == interaction.channel and m.content.isdigit()
        )

        num_fields = int(num_fields_msg.content)

        # Solicite os campos individuais e adicione-os ao Embed
        for _ in range(num_fields):
            await interaction.followup.send("Digite o nome do campo:")
            field_name_msg = await bot.wait_for(
                "message",
                check=lambda m: m.author == member and m.channel == interaction.channel
            )

            await interaction.followup.send("Escreva no campo:")
            field_value_msg = await bot.wait_for(
                "message",
                check=lambda m: m.author == member and m.channel == interaction.channel
            )

            embed.add_field(name=field_name_msg.content, value=field_value_msg.content, inline=False)

    # Adicione uma imagem ao embed (substitua pela URL da imagem desejada)
    embed.set_thumbnail(url='https://i.imgur.com/OefNYXb.png')

    # Envie o embed na mesma resposta
    await interaction.followup.send(embed=embed)


@bot.event
async def on_member_join(member):
    global df
    new_member_role = discord.utils.get(member.guild.roles, name="Membro Novo")
    member_role = discord.utils.get(member.guild.roles, name="Membro")

    if new_member_role is not None:
        await member.add_roles(new_member_role)

    await member.send("👋Olá! Que bom ter você aqui no servidor! Por favor, digite seu nickname:")

    def check_nickname(msg):
        return msg.author == member and isinstance(msg.channel, discord.DMChannel)

    response_nickname = await bot.wait_for("message", check=check_nickname)

    await member.send("Qual é o seu nome pessoal?")

    def check_nome_pessoal(msg):
        return msg.author == member and isinstance(msg.channel, discord.DMChannel)

    response_nome_pessoal = await bot.wait_for("message", check=check_nome_pessoal)

    await member.send("Qual é a sua data de aniversário?📅 (Formato: DD/MM)")

    def check_aniversario(msg):
        return msg.author == member and isinstance(msg.channel, discord.DMChannel)

    response_aniversario = await bot.wait_for("message", check=check_aniversario)

    new_data = {'Nome_discord': response_nickname.content, 'Aniversario': response_aniversario.content}
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

    await member.send("Em quais períodos do dia você costuma estar disponível? Por exemplo, algo como 14h às 16h ou 20h às 00h🕒")

    def check_schedule(msg):
        return msg.author == member and isinstance(msg.channel, discord.DMChannel)

    response_horarios = await bot.wait_for("message", check=check_schedule)

    if new_member_role is not None:
        await member.remove_roles(new_member_role)

    if member_role is not None:
        await member.add_roles(member_role)

    await member.send(f"Seu nickname foi definido como {response_nickname.content}. Bem-vindo ao servidor!😊🚀")

    await member.edit(nick=response_nickname.content)

    server = member.guild
    channel_id = 1171884351269654560

    channel = server.get_channel(channel_id)
    if channel is not None:
        mensagem = f"**Dados de Usuário**\n\n- **Nickname:** {response_nickname.content}\n- **Nome Pessoal:** {response_nome_pessoal.content}\n- **Aniversário:** {response_aniversario.content}\n- **Horários disponíveis:** {response_horarios.content}\n\n---"
        await channel.send(mensagem)

    df.to_excel('teste.xlsx', index=False, engine='openpyxl')

# Executa o bot
bot.run(bot_token)