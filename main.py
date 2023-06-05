import os
import json
import time
import random
import discord
import requests
# from google.colab import drive
from dotenv import load_dotenv
from discord.ext import commands


dotenv_path = os.path.join(os.path.dirname(__file__), '.env') # Путь до файла с переменными окружения
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


settings = {
    "token": YADB_TOKEN, # Discord bot token
    "bot": YADB_NAME,
    "id": YADB_ID, # Discord bot ID
    "prefix": YADB_PREFIX,
    "weatherapi": YADB_WEATHERAPITOKEN # www.weatherapi.com token
}


bot = commands.Bot(command_prefix = "/q ") # Префикс


@bot.command()
async def about(ctx: commands.Context):
    message = "Бот написан студентами ФИТ-221 Калицким Никитой и Александром Задорожным"
    await ctx.send(message)


@bot.command()
async def hello(ctx: commands.Context):
    author = ctx.message.author
    await ctx.send(f"Hello, {author.mention}!") # Выводим сообщение с упоминанием автора


@bot.command()
async def dice(ctx: commands.Context): # Подбросить кубик
    result = "Результат: " + str(random.randint(1, 7))
    await ctx.send(result)


@bot.command()
async def userinfo(ctx: commands.Context, user: discord.User):
    """Вывод информации о пользователе"""
    user_id = user.id
    username = user.name
    avatar = user.avatar_url
    
    await ctx.send(f"Пользователь найден: {user_id} -- {username}\n{avatar}")


@bot.command()
async def selfinfo(ctx: commands.Context):
    """Вывод информации о самом себе"""
    user = ctx.message.author
    user_id = user.id
    username = user.name
    avatar = user.avatar_url
    
    await ctx.send(f"Пользователь найден: {user_id} -- {username}\n{avatar}")


@bot.command()
async def serverinfo(ctx: commands.Context):
    """Вывод информации о сервере"""
    server = ctx.guild
    server_name = server.name
    total_members = server.member_count
    creation_date = server.created_at

    await ctx.send(f"Имя сервера: {server_name}\nВсего участников: {total_members}\nСоздан: {creation_date}")


async def weather(ctx: commands.Context, location: str):
    """Погода в указанном городе"""
    api_key = settings["weatherapi"]
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    
    response = requests.get(url)
    data = response.json()
    
    # Выцепим только нужную нам информацию
    current_temp = data["current"]["temp_c"]
    condition = data["current"]["condition"]["text"]
    
    await ctx.send(f"Текущая погода в {location}: {condition}, {current_temp}°C")


@bot.command()
async def quote(ctx: commands.Context):
    """Случайная цитата"""
    response = response = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=ru")
    data = response.json()
    
    quote = data["quoteText"]
    author = data["quoteAuthor"]
    
    await ctx.send(f"\"{quote}\" - {author}")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx: commands.Context, member: discord.Member, *, reason=None):
    """Кик пользователя"""
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} кикнут с сервера.")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx: commands.Context, member: discord.Member, *, reason=None):
    """Бан пользователя"""
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} забанен на этом сервере.")

  
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx: commands.Context, amount=5):
    """Удаление последних N сообщений"""
    await ctx.channel.purge(limit = amount + 1)
    await ctx.send(f"{amount} сообщений удалено.")


@bot.command()
async def play(ctx: commands.Context, url: str):
    """Примитивный проигрыватель музыки"""
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()
    voice_client.play(discord.FFmpegPCMAudio(url))


@bot.command()
async def leave(ctx: commands.Context):
    """"Покинуть войсчат"""
    voice_client = ctx.voice_client
    await voice_client.disconnect()


@bot.command()
async def poll(ctx: commands.Context, question: str, *options: list[str]):
    """Создать опрос"""
    if len(options) < 2:
        await ctx.send("Добавьте больше вариантов выбора")
        return

    formatted_options = [f"{chr(0x1F1E6 + index)}: {option}" for index, option in enumerate(options)] # Добавляет эмодзи-буквы A, B, C...
    poll_message = await ctx.send(f"**{question}**\n\n{"\n".join(formatted_options)}")

    for index in range(len(options)):
        await poll_message.add_reaction(chr(0x1F1E6 + index)) # Добавляет реакцию на сообщение


@bot.command()
async def cat(ctx: commands.Context):
    """Случайный кот (возможно даже кошка)"""
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    data = response.json()
    image_url = data[0]['url']
    
    embed = discord.Embed(title="Ваш случайный кот:")
    embed.set_image(url=image_url)
    
    await ctx.send(embed=embed)


@bot.command()
async def remindme(ctx: commands.Context, time, reminder):
    """Функция напоминания"""
    await ctx.send(f"Таймер сработает через {time} секунд.")
    await asyncio.sleep(int(time))
    await ctx.send(f"Таймер: {reminder}, {ctx.author.mention}")


@bot.command()
async def bitcoin(ctx: commands.Context):
    """Вывод курса биткоина"""
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice/BTC.json')
    data = response.json()
    
    price_usd = data['bpi']['USD']['rate']
    price_eur = data['bpi']['EUR']['rate']
    
    await ctx.send(f"Стоимость биткоина:\nUSD: {price_usd}\nEUR: {price_eur}")


@bot.command()
async def catstatus(ctx: commands.Context, url: str):
    """Вывод картинки с котом соотвествующей статусу ответа запроса"""
    request = requests.get(url)
    status_code = request.status_code

    cat_image_url = f"https://http.cat/{status_code}"
    
    embed = discord.Embed(title="Котостатус:")
    embed.set_image(url=cat_image)
    
    await ctx.send(embed=embed)


@bot.command()
async def yesorno(ctx: commands.Context, question: str):
    """Отвечает на вопрос (да, нет, наверное)"""
    request = requests.get("https://yesno.wtf/api")
    data = request.json()

    answer = data["answer"]
    image_url = data["image"]

    embed = discord.Embed(title=answer)
    embed.set_image(url=image_url)

    await ctx.send(embed=embed)


bot.run(settings["token"])
