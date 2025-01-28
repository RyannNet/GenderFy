import discord
from discord.ext import commands

TOKEN = "MTMzMzY5MTcwMzMwMzA3NzkzOA.Gn9odD.0bN2hLwiDgFYR_G4mpn5WfG3iwxLkJey8GmO3I"
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Lista de administradores permitidos
ADMINS = {
    "kk_dv": 1130254273620488353,  # Substitua pelo nome e ID do admin
    "jootaka7": 818488622252032040
}

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# Comando para iniciar a verificação
@bot.command()
async def verificar(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("❌ Este comando deve ser usado no servidor.")
        return

    admin_names = "\n".join([f"- {name}" for name in ADMINS.keys()])
    await ctx.send(
        f"{ctx.author.mention}, verificação iniciada! Escolha um administrador para realizar sua verificação:\n\n"
        f"{admin_names}\n\n"
        "Digite o comando **!escolher <nome_do_admin>** para selecionar o administrador."
    )

# Comando para selecionar o administrador e criar o canal temporário
@bot.command()
async def escolher(ctx, admin_name: str):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("❌ Este comando só pode ser usado no servidor.")
        return

    admin_id = ADMINS.get(admin_name)
    if not admin_id:
        await ctx.send("❌ Administrador não encontrado. Certifique-se de digitar o nome corretamente.")
        return

    admin = bot.get_user(admin_id)
    if not admin:
        await ctx.send("❌ O administrador selecionado não está disponível no momento.")
        return

    # Criar um canal temporário para o membro e o administrador
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True),
        admin: discord.PermissionOverwrite(read_messages=True)
    }

    temp_channel = await guild.create_text_channel(
        f"verificacao-{ctx.author.name}",
        overwrites=overwrites
    )

    # Notificar o administrador no servidor
    await ctx.send(
        f"👮 **Nova solicitação de verificação!**\n\n"
        f"O membro {ctx.author.mention} selecionou você para realizar a verificação de voz. "
        f"Acesse o canal: {temp_channel.mention} para começar."
    )

    # Informar o membro que a solicitação foi enviada
    await ctx.send(
        f"✅ Sua solicitação foi enviada para {admin_name}. "
        f"Aguarde o contato do administrador no canal {temp_channel.mention} para continuar a verificação."
    )

    # Esperar o comando para fechar o canal (opcional)
    def check(message):
        return message.content.lower() == "!fechar" and message.author in [ctx.author, admin]

    # Aguardar a confirmação para fechar o canal
    await bot.wait_for("message", check=check)
    await temp_channel.delete()
    await ctx.send(f"O canal {temp_channel.name} foi fechado.")

# Comando para listar administradores disponíveis
@bot.command()
async def admins(ctx):
    admin_list = "\n".join([f"- {name}" for name in ADMINS.keys()])
    await ctx.send(f"**Administradores disponíveis:**\n{admin_list}")

bot.run(TOKEN)