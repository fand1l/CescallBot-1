import json
import disnake
from disnake.ext import commands
import sqlite3
import time as t
from random import randint as rdi
import asyncio
import sys
import traceback

bot = commands.Bot(command_prefix=["$", "!", "&"], intents=disnake.Intents.all())

with open("config.json", "r") as f:
    config = json.load(f)


async def BlackListMember(inter):
    with open("MemberBlackList.json", "r") as file:
        data = json.load(file)

    if str(inter.author.id) not in data["list"]:
        pass

    else:
        embed = disnake.Embed(title="Ошибка",
                                  description=f"Вы в черном списке бота!",
                                  color=0xff0000)
        await inter.send(embed=embed)
        raise commands.CommandError("BlackList error!")


async def BlackListAdmin(inter):
    with open("AdminsBlackList.json", "r") as file:
        data = json.load(file)

    if str(inter.author.id) not in data["list"]:
        pass

    else:
        embed = disnake.Embed(title="Ошибка",
                                  description=f"Вы в черном списке администраторов!",
                                  color=0xff0000)
        await inter.send(embed=embed)
        raise commands.CommandError("BlackListAdmin error!")


if __name__ == '__main__':
    for extension in disnake.utils.search_directory("cogs"):
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f'Failed to load extension {extension}', file=sys.stderr)
            errors = traceback.format_exception(type(error), error, error.__traceback__)


# async def send_message_to_channel():
#     channel = bot.get_channel(1116409461423214679)
#
#     while not bot.is_closed():
#         # Ваше сообщение, которое будет отправлено в канал
#         message_content0 = "https://discord.gg/ssumqfZESq"
#         message_content = disnake.Embed(title="Сервер поддержки",
#                                         description="У этого бота есть сервер поддержки! Если вы столкнулись с ошибкой, у вас есть идея или вопрос, то вам на Cescall Bot Server!")
#         await asyncio.sleep(rdi(7600, 17800))
#
#         await channel.send(message_content0)
#         await channel.send(embed=message_content)
#
#         print("Отправлено рекламное сообщение!")


# Bot on Ready
@bot.event
async def on_ready():
    print("Bot ready!")
    # bot.loop.create_task(send_message_to_channel())


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        embed = disnake.Embed(title="MissingRole",
                              description=f"Недостаточно ролей для выполнения команды!\n {error}",
                              color=0xff0000)
        await ctx.send(embed=embed)

    elif isinstance(error, commands.CommandNotFound):
        embed = disnake.Embed(title="CommandNotFound",
                              description=f"Нет данной команды!\n {error}",
                              color=0xff0000)
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingRequiredArgument):
        embed = disnake.Embed(title="MissingRequiredArgument",
                              description=f"Вы пропустили какой-то аргумент!\n {error}",
                              color=0xff0000)
        await ctx.send(embed=embed)

    elif isinstance(error, commands.BadArgument):
        embed = disnake.Embed(title="BadArgument",
                              description=f"Вы указали неверный аргумент!\n {error}",
                              color=0xff0000)
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingPermissions):
        embed = disnake.Embed(title="MissingPermissions",
                              description=f"Недостаточно прав для выполнения данной команды!\n {error}",
                              color=0xff0000)
        await ctx.send(embed=embed)

    elif isinstance(error, commands.NotOwner):
        embed = disnake.Embed(title="NotOwner",
                              description=f"Вы не владелец бота!\n {error}",
                              color=0xff0000)
        await ctx.send(embed=embed)

    else:
        embed = disnake.Embed(title="Error",
                              description=f"Ошибка при выполнении команды!\n {error}",
                              color=0xff0000)
        await ctx.send(embed=embed)


@bot.command()
@commands.is_owner()
async def load(inter):
    if __name__ == '__main__':
        for extension in disnake.utils.search_directory("cogs"):
            try:
                bot.load_extension(extension)
            except Exception as error:
                print(f'Failed to load extension {extension}', file=sys.stderr)
                errors = traceback.format_exception(type(error), error, error.__traceback__)


@bot.command(aliases=["reg"])
async def register(inter, ctype: str = None):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None or resid_org is not None:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы уже зарегестрированы! Вам не нужна повторная регистрация",
                              color=0xff0000)
        await inter.send(embed=embed)
        db.close()

    else:
        with open("BannedIDs.json", "r") as f:
            ban_pl_data = json.load(f)

        if str(inter.author.id) in ban_pl_data["list"]:
            embed = disnake.Embed(title="Бан",
                                  description="Регистрация не возможна! Вы забанены",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            if ctype == "country":
                c.execute(
                    f"INSERT INTO 'users-data' VALUES ('{inter.author.name}', {inter.author.id}, 0, 10000, 80, 'country', 40, 6000000, 4000000, 2000000)")
                c.execute(
                    f"INSERT INTO 'users-data-army' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-army-mod' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-infra' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-lctime' VALUES ('{inter.author.name}', {inter.author.id}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())})")
                c.execute(
                    f"INSERT INTO 'users-data-resdots' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-resources' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0, 0)")
                db.commit()

                embed = disnake.Embed(title="Успешно",
                                      description="Вы успешно зарегестрировались как страна! Приятной игры",
                                      color=0x00ff00)
                await inter.send(embed=embed)

                print(f"[{inter.author.name} | {inter.author.id}] $ registered as a country")

            elif ctype == "separatist":
                c.execute(
                    f"INSERT INTO 'users-data' VALUES ('{inter.author.name}', {inter.author.id}, 0, 9000, 70, 'separatist', 40, 6000000, 4000000, 2500000)")
                c.execute(
                    f"INSERT INTO 'users-data-army' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-army-mod' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-infra' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-lctime' VALUES ('{inter.author.name}', {inter.author.id}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())})")
                c.execute(
                    f"INSERT INTO 'users-data-resdots' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-resources' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0, 0)")
                db.commit()

                embed = disnake.Embed(title="Успешно",
                                      description="Вы успешно зарегестрировались как сепаратист! Приятного захвата власти",
                                      color=0x00ff00)
                await inter.send(embed=embed)

                print(f"[{inter.author.name} | {inter.author.id}] $ registered as a separatist")

            elif ctype == "organization":
                c.execute(
                    f"INSERT INTO 'users-data-org' VALUES ('{inter.author.name}', {inter.author.id}, 0, 10, 'organization', 5000000, 1000000, 50000, 4000000, 1)")
                c.execute(
                    f"INSERT INTO 'users-data-army' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-army-mod' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-infra' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-lctime' VALUES ('{inter.author.name}', {inter.author.id}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())})")
                c.execute(
                    f"INSERT INTO 'users-data-resdots' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-resources' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0, 0)")
                db.commit()

                embed = disnake.Embed(title="Успешно",
                                      description="Вы успешно зарегестрировались как организация! Приятной игры",
                                      color=0x00ff00)
                await inter.send(embed=embed)

                print(f"[{inter.author.name} | {inter.author.id}] $ registered as a organization")

            elif ctype is None:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы не указали тип государства! Доступные типы государства: country, organization, separatist",
                                      color=0xff0000)
                await inter.send(embed=embed)

            else:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали неверный тип государства! Доступные типы государства: country, organization, separatist",
                                      color=0xff0000)
                await inter.send(embed=embed)

        db.close()


@bot.command(aliases=["unreg"])
async def unregister(inter):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()

    if resid is not None:
        c.execute(f"DELETE FROM 'users-data' WHERE id={inter.author.id}")
        c.execute(f"DELETE FROM 'users-data-army' WHERE id={inter.author.id}")
        c.execute(f"DELETE FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        c.execute(f"DELETE FROM 'users-data-infra' WHERE id={inter.author.id}")
        c.execute(f"DELETE FROM 'users-data-lctime' WHERE id={inter.author.id}")
        c.execute(f"DELETE FROM 'users-data-resdots' WHERE id={inter.author.id}")
        c.execute(f"DELETE FROM 'users-data-resources' WHERE id={inter.author.id}")
        db.commit()

        embed = disnake.Embed(title="Успешно",
                              description="Учетная запись успешно удалена!",
                              color=0x00ff00)
        await inter.send(embed=embed)

        print(f"[{inter.author.name} | {inter.author.id}] $ unregistered")

    elif resid_org is not None:
        c.execute(f"DELETE FROM 'users-data-org' WHERE id={inter.author.id}")
        c.execute(f"DELETE FROM 'users-data-army' WHERE id={inter.author.id}")
        c.execute(f"DELETE FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        c.execute(f"DELETE FROM 'users-data-infra' WHERE id={inter.author.id}")
        c.execute(f"DELETE FROM 'users-data-lctime' WHERE id={inter.author.id}")
        c.execute(f"DELETE FROM 'users-data-resdots' WHERE id={inter.author.id}")
        c.execute(f"DELETE FROM 'users-data-resources' WHERE id={inter.author.id}")
        db.commit()

        embed = disnake.Embed(title="Успешно",
                              description="Учетная запись успешно удалена!",
                              color=0x00ff00)
        await inter.send(embed=embed)

        print(f"[{inter.author.name} | {inter.author.id}] $ unregistered")

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command()
@commands.has_permissions(administrator=True)
async def money(inter, member: disnake.Member, amount: int = 0):
    await BlackListMember(inter)
    await BlackListAdmin(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()

    c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
    resid_user = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
    resid_user_org = c.fetchone()

    if amount > 999999999999999 or amount < -999999999999999:
        embed = disnake.Embed(title="Ошибка",
                              description="Указана неверная сумма",
                              color=0xff0000)
        await inter.send(embed=embed)
        return

    if resid_user is not None or resid_user_org is not None:
        if resid_user is not None:
            c.execute(f"SELECT money FROM 'users-data' WHERE id={member.id}")
            user_balance = c.fetchone()
            user_balance = user_balance[0]

            up_balance = user_balance + amount

            c.execute(f"UPDATE 'users-data' SET money={up_balance} WHERE id={member.id}")
            db.commit()

            embed = disnake.Embed(title="Успешно",
                                  description=f"Баланс игрока {member.name} успешно изменён!",
                                  color=0x00ff00)
            embed.add_field(name="Прошлый баланс", value=f"${user_balance:,}")
            embed.add_field(name="Баланс", value=f"${up_balance:,}")
            await inter.send(embed=embed)

        elif resid_user_org is not None:
            c.execute(f"SELECT money FROM 'users-data-org' WHERE id={member.id}")
            user_balance = c.fetchone()
            user_balance = user_balance[0]

            up_balance = user_balance + amount

            c.execute(f"UPDATE 'users-data-org' SET money={up_balance} WHERE id={member.id}")
            db.commit()

            embed = disnake.Embed(title="Успешно",
                                  description=f"Баланс игрока {member.name} успешно изменён!",
                                  color=0x00ff00)
            embed.add_field(name="Прошлый баланс", value=f"${user_balance:,}")
            embed.add_field(name="Баланс", value=f"${up_balance:,}")
            await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Данный пользователь не зарегистрирован!",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command()
@commands.has_permissions(administrator=True)
async def dot(inter, member: disnake.Member, action: str, dot):
    await BlackListMember(inter)
    await BlackListAdmin(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()

    c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
    resid_user = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
    resid_user_org = c.fetchone()

    if resid_user is not None or resid_user_org is not None:
        with open("ResData.json", "r", encoding="utf-8") as f:
            data_res = json.load(f)

        if dot not in data_res:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы ввели неверный ID точки!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            dot_dbid = data_res[str(dot)]["id"]
            dot_name = data_res[str(dot)]["name"]

            c.execute(f"SELECT {dot_dbid} FROM 'users-data-resdots' WHERE id={member.id}")
            need_dot = c.fetchone()
            need_dot = need_dot[0]

            if action == "add":
                up_dot = need_dot + 1
                c.execute(f"UPDATE 'users-data-resdots' SET {dot_dbid}={up_dot} WHERE id={member.id}")
                db.commit()

                embed = disnake.Embed(title="Успешно",
                                      description=f"Точка {dot_name} выдана игроку {member.mention}!",
                                      color=0x00ff00)
                embed.add_field(name="Кол-во точек", value=f"{dot_name}: {up_dot}")
                await inter.send(embed=embed)

            elif action == "remove":
                if need_dot == 0:
                    embed = disnake.Embed(title="Ошибка",
                                          description="У пользователя минимальное кол-во точек!",
                                          color=0xff0000)
                    await inter.send(embed=embed)
                else:
                    up_dot = need_dot - 1

                    c.execute(f"UPDATE 'users-data-resdots' SET {dot_dbid}={up_dot} WHERE id={member.id}")
                    db.commit()

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Точка {dot_name} забрана у игрока {member.mention}!",
                                          color=0x00ff00)
                    embed.add_field(name="Кол-во точек", value=f"{dot_name}: {up_dot}")
                    await inter.send(embed=embed)

            else:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали неверное действие!",
                                      color=0xff0000)
                await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Данный пользователь не зарегистрирован!",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command(aliases=["prof"])
async def profile(inter):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None:
        c.execute(f"SELECT money FROM 'users-data' WHERE id={inter.author.id}")
        usr_money = c.fetchone()

        c.execute(f"SELECT peoples FROM 'users-data' WHERE id={inter.author.id}")
        usr_peoples = c.fetchone()

        c.execute(f"SELECT happy FROM 'users-data' WHERE id={inter.author.id}")
        usr_happy = c.fetchone()

        c.execute(f"SELECT type FROM 'users-data' WHERE id={inter.author.id}")
        usr_type = c.fetchone()

        c.execute(f"SELECT earn_per_person FROM 'users-data' WHERE id={inter.author.id}")
        usr_earn = c.fetchone()

        c.execute(f"SELECT cost_up_eco FROM 'users-data' WHERE id={inter.author.id}")
        usr_cost_eco = c.fetchone()

        c.execute(f"SELECT cost_up_peoples FROM 'users-data' WHERE id={inter.author.id}")
        usr_cost_peop = c.fetchone()

        c.execute(f"SELECT cost_up_happy FROM 'users-data' WHERE id={inter.author.id}")
        usr_cost_happy = c.fetchone()

        c.execute(f"SELECT solider FROM 'users-data-army' WHERE id={inter.author.id}")
        usr_solider = c.fetchone()

        embed = disnake.Embed(title=f"Профиль участника {inter.author.name}",
                              description="Здесь написана вся информация о пользователе")
        embed.add_field(name="Баланс", value=f"${usr_money[0]:,}")
        embed.add_field(name="Население", value=f"{usr_peoples[0]:,} человек")
        embed.add_field(name="Счастье жителей", value=f"{usr_happy[0]}%")
        embed.add_field(name="Тип", value=f"{usr_type[0]}")
        embed.add_field(name="Сбор с 1 жителя", value=f"${usr_earn[0]:,}")
        embed.add_field(name="Стоимость прокачки экономики", value=f"${usr_cost_eco[0]:,}")
        embed.add_field(name="Стоимость прокачки населения", value=f"${usr_cost_peop[0]:,}")
        embed.add_field(name="Стоимость прокачки счастья", value=f"${usr_cost_happy[0]:,}")
        embed.add_field(name="Военнослужащих", value=f"{usr_solider[0]:,} солдат")

        await inter.send(embed=embed)


    elif resid_org is not None:
        c.execute(f"SELECT money FROM 'users-data-org' WHERE id={inter.author.id}")
        usr_money = c.fetchone()

        c.execute(f"SELECT goods_for_coll FROM 'users-data-org' WHERE id={inter.author.id}")
        usr_goods_coll = c.fetchone()

        c.execute(f"SELECT type FROM 'users-data-org' WHERE id={inter.author.id}")
        usr_type = c.fetchone()

        c.execute(f"SELECT cost_up_eco FROM 'users-data-org' WHERE id={inter.author.id}")
        usr_cost_eco = c.fetchone()

        c.execute(f"SELECT goods_count FROM 'users-data-org' WHERE id={inter.author.id}")
        usr_goods_count = c.fetchone()

        c.execute(f"SELECT cost_up_goods FROM 'users-data-org' WHERE id={inter.author.id}")
        usr_cost_goods = c.fetchone()

        c.execute(f"SELECT offices FROM 'users-data-org' WHERE id={inter.author.id}")
        offices = c.fetchone()

        c.execute(f"SELECT solider FROM 'users-data-army' WHERE id={inter.author.id}")
        usr_solider = c.fetchone()

        embed = disnake.Embed(title=f"Профиль участника {inter.author.name}",
                              description="Здесь написана вся информация о пользователе")
        embed.add_field(name="Баланс", value=f"${usr_money[0]:,}")
        embed.add_field(name="Тип", value=f"{usr_type[0]}")
        embed.add_field(name="Сбор с 1 товара", value=f"${usr_goods_coll[0]:,}")
        embed.add_field(name="Кол-во товара", value=f"{usr_goods_count[0]:,} шт.")
        embed.add_field(name="Стоимость прокачки экономики", value=f"${usr_cost_eco[0]:,}")

        embed.add_field(name="Стоимость прокачки кол-ва товара", value=f"${usr_cost_goods[0]:,}")
        embed.add_field(name="Кол-во офисов", value=f"{offices[0]:,}")
        embed.add_field(name="Военнослужащих", value=f"{usr_solider[0]:,} солдат")

        await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command(aliases=["res"])
async def resources(inter):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None or resid_org is not None:
        c.execute(f"SELECT gas FROM 'users-data-resources' WHERE id={inter.author.id}")
        usr_gas = c.fetchone()

        c.execute(f"SELECT gold FROM 'users-data-resources' WHERE id={inter.author.id}")
        usr_gold = c.fetchone()

        c.execute(f"SELECT uranium FROM 'users-data-resources' WHERE id={inter.author.id}")
        usr_uranium = c.fetchone()

        c.execute(f"SELECT titanium FROM 'users-data-resources' WHERE id={inter.author.id}")
        usr_titanium = c.fetchone()

        c.execute(f"SELECT iron FROM 'users-data-resources' WHERE id={inter.author.id}")
        usr_iron = c.fetchone()

        c.execute(f"SELECT building_materials FROM 'users-data-resources' WHERE id={inter.author.id}")
        usr_build = c.fetchone()

        c.execute(f"SELECT gas FROM 'users-data-resdots' WHERE id={inter.author.id}")
        usr_dot_gas = c.fetchone()

        c.execute(f"SELECT gold FROM 'users-data-resdots' WHERE id={inter.author.id}")
        usr_dot_gold = c.fetchone()

        c.execute(f"SELECT uranium FROM 'users-data-resdots' WHERE id={inter.author.id}")
        usr_dot_uranium = c.fetchone()

        c.execute(f"SELECT titanium FROM 'users-data-resdots' WHERE id={inter.author.id}")
        usr_dot_titanium = c.fetchone()

        c.execute(f"SELECT iron FROM 'users-data-resdots' WHERE id={inter.author.id}")
        usr_dot_iron = c.fetchone()

        embed = disnake.Embed(title=f"Ресурсы игрока {inter.author.name}",
                              description="Здесь указаны все ваши ресурсы и точки к ресурсам")
        embed.add_field(name="**Ресурсы**", value="", inline=False)

        embed.add_field(name="Газ", value=f"Кол-во: {usr_gas[0]:,} м²")
        embed.add_field(name="Золото", value=f"Кол-во: {usr_gold[0]:,}")
        embed.add_field(name="Уран", value=f"Кол-во: {usr_uranium[0]:,}")
        embed.add_field(name="Титан", value=f"Кол-во: {usr_titanium[0]:,}")
        embed.add_field(name="Железо", value=f"Кол-во: {usr_iron[0]:,}")
        embed.add_field(name="Строительные материалы", value=f"Кол-во: {usr_build[0]:,}")
        embed.add_field(name="ㅤ", value="")

        embed.add_field(name="**Точки с ресурсами**", value="", inline=False)
        embed.add_field(name="Газ", value=f"Точек: {usr_dot_gas[0]}")
        embed.add_field(name="Золото", value=f"Точек: {usr_dot_gold[0]}")
        embed.add_field(name="Уран", value=f"Точек: {usr_dot_uranium[0]}")
        embed.add_field(name="Титан", value=f"Точек: {usr_dot_titanium[0]}")
        embed.add_field(name="Железо", value=f"Точек: {usr_dot_iron[0]}")

        await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command(aliases=["infra"])
async def infrastructure(inter):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None:
        c.execute(f"SELECT house FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_house = c.fetchone()

        c.execute(f"SELECT multi_house FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_mul_house = c.fetchone()

        c.execute(f"SELECT com_shops FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_shops = c.fetchone()

        c.execute(f"SELECT com_electronics FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_electronics = c.fetchone()

        c.execute(f"SELECT com_cars FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_cars = c.fetchone()

        c.execute(f"SELECT com_it FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_it = c.fetchone()

        c.execute(f"SELECT com_army FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_army = c.fetchone()

        c.execute(f"SELECT com_buildings FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_build = c.fetchone()

        c.execute(f"SELECT com_hospitals FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_hospital = c.fetchone()

        c.execute(f"SELECT land_equipment_plant FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_land = c.fetchone()

        c.execute(f"SELECT aviation_factory FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_avia = c.fetchone()

        c.execute(f"SELECT shipyard FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_ship = c.fetchone()

        c.execute(f"SELECT nuclear_factory FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_nuke = c.fetchone()

        c.execute(f"SELECT chemical_factory FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_chemic = c.fetchone()

        embed = disnake.Embed(title=f"Инфраструктура участника {inter.author.name}",
                              description="Здесь показана вся ваша инфраструктура")
        embed.add_field(name="Дом", value=f"Кол-во: {usr_house[0]}")
        embed.add_field(name="Многоэтажный дом", value=f"Кол-во: {usr_mul_house[0]}")
        embed.add_field(name="Сеть продуктовых магазинов", value=f"Кол-во: {usr_shops[0]}")
        embed.add_field(name="Сеть магазинов электроники", value=f"Кол-во: {usr_electronics[0]}")
        embed.add_field(name="Сеть автосалонов", value=f"Кол-во: {usr_cars[0]}")
        embed.add_field(name="IT компании", value=f"Кол-во: {usr_it[0]}")
        embed.add_field(name="Сеть военных магазинов", value=f"Кол-во: {usr_army[0]}")
        embed.add_field(name="Сеть строительных компаний", value=f"Кол-во: {usr_build[0]}")
        embed.add_field(name="Сеть больниц", value=f"Кол-во: {usr_hospital[0]}")
        embed.add_field(name="Завод сухопутной техники", value=f"Кол-во: {usr_land[0]}")
        embed.add_field(name="Авиационный завод", value=f"Кол-во: {usr_avia[0]}")
        embed.add_field(name="Верфь", value=f"Кол-во: {usr_ship[0]}")
        embed.add_field(name="Ядерный завод", value=f"Кол-во: {usr_nuke[0]}")
        embed.add_field(name="Химический завод", value=f"Кол-во: {usr_chemic[0]}")
        await inter.send(embed=embed)

    elif resid_org is not None:
        c.execute(f"SELECT land_equipment_plant FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_land = c.fetchone()

        c.execute(f"SELECT aviation_factory FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_avia = c.fetchone()

        c.execute(f"SELECT shipyard FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_ship = c.fetchone()

        c.execute(f"SELECT nuclear_factory FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_nuke = c.fetchone()

        c.execute(f"SELECT chemical_factory FROM 'users-data-infra' WHERE id={inter.author.id}")
        usr_chemic = c.fetchone()

        embed = disnake.Embed(title=f"Инфраструктура участника {inter.author.name}",
                              description="Здесь показана вся ваша инфраструктура")
        embed.add_field(name="Завод сухопутной техники", value=f"Кол-во: {usr_land[0]}")
        embed.add_field(name="Авиационный завод", value=f"Кол-во: {usr_avia[0]}")
        embed.add_field(name="Верфь", value=f"Кол-во: {usr_ship[0]}")
        embed.add_field(name="Ядерный завод", value=f"Кол-во: {usr_nuke[0]}")
        embed.add_field(name="Химический завод", value=f"Кол-во: {usr_chemic[0]}")
        await inter.send(embed=embed)


    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command(aliases=["inv"])
async def inventory(inter):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None or resid_org is not None:
        # Normal
        c.execute(f"SELECT solider FROM 'users-data-army' WHERE id={inter.author.id}")
        solider = c.fetchone()

        c.execute(f"SELECT pams FROM 'users-data-army' WHERE id={inter.author.id}")
        pams = c.fetchone()

        c.execute(f"SELECT tank FROM 'users-data-army' WHERE id={inter.author.id}")
        tank = c.fetchone()

        c.execute(f"SELECT bmp FROM 'users-data-army' WHERE id={inter.author.id}")
        bmp = c.fetchone()

        c.execute(f"SELECT apc FROM 'users-data-army' WHERE id={inter.author.id}")
        apc = c.fetchone()

        c.execute(f"SELECT sam FROM 'users-data-army' WHERE id={inter.author.id}")
        sam = c.fetchone()

        c.execute(f"SELECT towed_howitzer FROM 'users-data-army' WHERE id={inter.author.id}")
        howitzer = c.fetchone()

        c.execute(f"SELECT mlrs FROM 'users-data-army' WHERE id={inter.author.id}")
        mlrs = c.fetchone()

        c.execute(f"SELECT transport_helicopter FROM 'users-data-army' WHERE id={inter.author.id}")
        trans_helicopter = c.fetchone()

        c.execute(f"SELECT attack_helicopter FROM 'users-data-army' WHERE id={inter.author.id}")
        att_heli = c.fetchone()

        c.execute(f"SELECT airborne_helicopter FROM 'users-data-army' WHERE id={inter.author.id}")
        air_heli = c.fetchone()

        c.execute(f"SELECT fighter FROM 'users-data-army' WHERE id={inter.author.id}")
        fighter = c.fetchone()

        c.execute(f"SELECT transport_aircraft FROM 'users-data-army' WHERE id={inter.author.id}")
        trans_air = c.fetchone()

        c.execute(f"SELECT airborne_aircraft FROM 'users-data-army' WHERE id={inter.author.id}")
        air_air = c.fetchone()

        c.execute(f"SELECT bomber FROM 'users-data-army' WHERE id={inter.author.id}")
        bomber = c.fetchone()

        c.execute(f"SELECT ruav FROM 'users-data-army' WHERE id={inter.author.id}")
        ruav = c.fetchone()

        c.execute(f"SELECT auav FROM 'users-data-army' WHERE id={inter.author.id}")
        auav = c.fetchone()

        c.execute(f"SELECT radar FROM 'users-data-army' WHERE id={inter.author.id}")
        radar = c.fetchone()

        c.execute(f"SELECT missile_system FROM 'users-data-army' WHERE id={inter.author.id}")
        missile_system = c.fetchone()

        c.execute(f"SELECT frigate FROM 'users-data-army' WHERE id={inter.author.id}")
        frigate = c.fetchone()

        c.execute(f"SELECT missile_cruiser FROM 'users-data-army' WHERE id={inter.author.id}")
        miss_cruis = c.fetchone()

        c.execute(f"SELECT transport_ship FROM 'users-data-army' WHERE id={inter.author.id}")
        trans_ship = c.fetchone()

        c.execute(f"SELECT landing_ship FROM 'users-data-army' WHERE id={inter.author.id}")
        land_ship = c.fetchone()

        c.execute(f"SELECT speedboat FROM 'users-data-army' WHERE id={inter.author.id}")
        speedb = c.fetchone()

        c.execute(f"SELECT missile FROM 'users-data-army' WHERE id={inter.author.id}")
        missile = c.fetchone()

        c.execute(f"SELECT ibm FROM 'users-data-army' WHERE id={inter.author.id}")
        ibm = c.fetchone()

        c.execute(f"SELECT bomb FROM 'users-data-army' WHERE id={inter.author.id}")
        bomb = c.fetchone()

        c.execute(f"SELECT artillery_shell FROM 'users-data-army' WHERE id={inter.author.id}")
        art_shell = c.fetchone()

        c.execute(f"SELECT rocket_projectile FROM 'users-data-army' WHERE id={inter.author.id}")
        rock_proj = c.fetchone()

        c.execute(f"SELECT nuclear_missile FROM 'users-data-army' WHERE id={inter.author.id}")
        nuke_miss = c.fetchone()

        c.execute(f"SELECT nuclear_bomb FROM 'users-data-army' WHERE id={inter.author.id}")
        nuke_bomb = c.fetchone()

        c.execute(f"SELECT chemical_bomb FROM 'users-data-army' WHERE id={inter.author.id}")
        chem_bomb = c.fetchone()

        c.execute(f"SELECT rifle FROM 'users-data-army' WHERE id={inter.author.id}")
        rifle = c.fetchone()

        c.execute(f"SELECT equipment FROM 'users-data-army' WHERE id={inter.author.id}")
        equipment = c.fetchone()

        c.execute(f"SELECT armored_car FROM 'users-data-army' WHERE id={inter.author.id}")
        arm_car = c.fetchone()

        c.execute(f"SELECT kuav FROM 'users-data-army' WHERE id={inter.author.id}")
        kuav = c.fetchone()

        c.execute(f"SELECT missile_submarine FROM 'users-data-army' WHERE id={inter.author.id}")
        miss_sub = c.fetchone()

        c.execute(f"SELECT nuclear_submarine FROM 'users-data-army' WHERE id={inter.author.id}")
        nuke_sub = c.fetchone()

        c.execute(f"SELECT aircraft_carrier FROM 'users-data-army' WHERE id={inter.author.id}")
        air_carrier = c.fetchone()

        # def
        c.execute(f"SELECT tank_def FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        tank_def = c.fetchone()

        c.execute(f"SELECT bmp_def FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        bmp_def = c.fetchone()

        c.execute(f"SELECT apc_def FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        apc_def = c.fetchone()

        c.execute(f"SELECT sam_def FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        sam_def = c.fetchone()

        c.execute(f"SELECT mlrs_def FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        mlrs_def = c.fetchone()

        c.execute(f"SELECT fighter_def FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        fighter_def = c.fetchone()

        c.execute(f"SELECT bomber_def FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        bomber_def = c.fetchone()

        c.execute(f"SELECT frigate_def FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        frigate_def = c.fetchone()

        c.execute(f"SELECT missile_cruiser_def FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        miss_cruis_def = c.fetchone()

        c.execute(f"SELECT transport_ship_def FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        trans_ship_def = c.fetchone()

        c.execute(f"SELECT landing_ship_def FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        land_ship_def = c.fetchone()

        c.execute(f"SELECT equipment_def FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        equipment_def = c.fetchone()
        c.execute(f"SELECT armored_car_def FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        arm_car_def = c.fetchone()

        # spd
        c.execute(f"SELECT tank_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        tank_spd = c.fetchone()

        c.execute(f"SELECT bmp_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        bmp_spd = c.fetchone()

        c.execute(f"SELECT apc_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        apc_spd = c.fetchone()

        c.execute(f"SELECT sam_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        sam_spd = c.fetchone()

        c.execute(f"SELECT mlrs_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        mlrs_spd = c.fetchone()

        c.execute(f"SELECT transport_helicopter_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        trans_helicopter_spd = c.fetchone()

        c.execute(f"SELECT attack_helicopter_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        att_heli_spd = c.fetchone()

        c.execute(f"SELECT airborne_helicopter_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        air_heli_spd = c.fetchone()

        c.execute(f"SELECT fighter_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        fighter_spd = c.fetchone()

        c.execute(f"SELECT transport_aircraft_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        trans_air_spd = c.fetchone()

        c.execute(f"SELECT airborne_aircraft_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        air_air_spd = c.fetchone()

        c.execute(f"SELECT bomber_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        bomber_spd = c.fetchone()

        c.execute(f"SELECT ruav_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        ruav_spd = c.fetchone()

        c.execute(f"SELECT auav_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        auav_spd = c.fetchone()

        c.execute(f"SELECT missile_system_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        missile_system_spd = c.fetchone()

        c.execute(f"SELECT frigate_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        frigate_spd = c.fetchone()

        c.execute(f"SELECT missile_cruiser_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        miss_cruis_spd = c.fetchone()

        c.execute(f"SELECT transport_ship_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        trans_ship_spd = c.fetchone()

        c.execute(f"SELECT landing_ship_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        land_ship_spd = c.fetchone()

        c.execute(f"SELECT missile_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        missile_spd = c.fetchone()

        c.execute(f"SELECT ibm_spd FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        ibm_spd = c.fetchone()

        # dmg
        c.execute(f"SELECT tank_dmg FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        tank_dmg = c.fetchone()

        c.execute(f"SELECT bmp_dmg FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        bmp_dmg = c.fetchone()

        c.execute(f"SELECT apc_dmg FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        apc_dmg = c.fetchone()

        c.execute(f"SELECT sam_dmg FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        sam_dmg = c.fetchone()

        c.execute(f"SELECT towed_howitzer_dmg FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        howitzer_dmg = c.fetchone()

        c.execute(f"SELECT mlrs_dmg FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        mlrs_dmg = c.fetchone()

        c.execute(f"SELECT attack_helicopter_dmg FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        att_heli_dmg = c.fetchone()

        c.execute(f"SELECT fighter_dmg FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        fighter_dmg = c.fetchone()

        c.execute(f"SELECT auav_dmg FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        auav_dmg = c.fetchone()

        c.execute(f"SELECT frigate_dmg FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        frigate_dmg = c.fetchone()

        c.execute(f"SELECT missile_dmg FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        missile_dmg = c.fetchone()

        c.execute(f"SELECT ibm_dmg FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        ibm_dmg = c.fetchone()

        c.execute(f"SELECT bomb_dmg FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        bomb_dmg = c.fetchone()

        c.execute(f"SELECT kuav_dmg FROM 'users-data-army-mod' WHERE id={inter.author.id}")
        kuav_dmg = c.fetchone()

        embed_land = disnake.Embed(title=f"Наземная техника игрока {inter.author.name}",
                                   description="В этом разделе инвентаря описана вся информация про вашу наземную технику. Построить данный тип техники можно с помощью завода сухопутной техники")
        embed_land.add_field(name="ПЗРК",
                             value=f'**Обычная:** {pams[0]:,}',
                             inline=True)
        embed_land.add_field(name="Танк",
                             value=f'**Обычная:** {tank[0]:,}\n**Модификации:** \nЗащита: {tank_def[0]:,}\nСкорость: {tank_spd[0]:,}\nУрон: {tank_dmg[0]:,}',
                             inline=True)
        embed_land.add_field(name="БМП",
                             value=f'**Обычная:** {bmp[0]:,}\n**Модификации:** \nЗащита: {bmp_def[0]:,}\nСкорость: {bmp_spd[0]:,}\nУрон: {bmp_dmg[0]:,}',
                             inline=True)
        embed_land.add_field(name="БТР",
                             value=f'**Обычная:** {apc[0]:,}\n**Модификации:** \nЗащита: {apc_def[0]:,}\nСкорость: {apc_spd[0]:,}\nУрон: {apc_dmg[0]:,}',
                             inline=True)
        embed_land.add_field(name="Бронеавтомобиль",
                             value=f'**Обычная:** {arm_car[0]:,}\n**Модификации:** \nЗащита: {arm_car_def[0]:,}',
                             inline=True)
        embed_land.add_field(name="САУ",
                             value=f'**Обычная:** {sam[0]:,}\n**Модификации:** \nЗащита: {sam_def[0]:,}\nСкорость: {sam_spd[0]:,}\nУрон: {sam_dmg[0]:,}',
                             inline=True)
        embed_land.add_field(name="Буксеруемая Гаубица",
                             value=f'**Обычная:** {howitzer[0]:,}\n**Модификации:** \nУрон: {howitzer_dmg[0]:,}',
                             inline=True)
        embed_land.add_field(name="РСЗО",
                             value=f'**Обычная:** {mlrs[0]:,}\n**Модификации:** \nЗащита: {mlrs_def[0]:,}\nСкорость: {mlrs_spd[0]:,}\nУрон: {mlrs_dmg[0]:,}',
                             inline=True)
        embed_land.add_field(name="РЛС", value=f'**Обычная:** {radar[0]:,}', inline=True)
        embed_land.add_field(name="Ракетный Комплекс",
                             value=f'**Обычная:** {missile_system[0]:,}\n**Модификации:** \nСкорость: {missile_system_spd[0]:,}',
                             inline=True)
        embed_land.add_field(name="Винтовка", value=f'**Обычная:** {rifle[0]:,}', inline=True)
        embed_land.add_field(name="Экипировка солдат",
                             value=f'**Обычная:** {equipment[0]:,}\n**Модификации:** \nЗащита: {equipment_def[0]:,}',
                             inline=True)

        embed_air = disnake.Embed(title=f"Воздушная техника игрока {inter.author.name}",
                                  description="В этом разделе инвентаря описана вся информация про вашу воздушную технику. Построить данный тип техники можно с помощью авиационного завода")
        embed_air.add_field(name="Транспортный Вертолёт",
                            value=f'**Обычная:** {trans_helicopter[0]:,}\n**Модификации:** \nСкорость: {trans_helicopter_spd[0]:,}',
                            inline=True)
        embed_air.add_field(name="Ударный Вертолёт",
                            value=f'**Обычная:** {att_heli[0]:,}\n**Модификации:** \nСкорость: {att_heli_spd[0]:,}\nУрон: {att_heli_dmg[0]:,}',
                            inline=True)
        embed_air.add_field(name="Десантный Вертолёт",
                            value=f'**Обычная:** {air_heli[0]:,}\n**Модификации:** \nСкорость: {air_heli_spd[0]:,}',
                            inline=True)
        embed_air.add_field(name="Истребитель",
                            value=f'**Обычная:** {fighter[0]:,}\n**Модификации:** \nЗащита: {fighter_def[0]:,}\nСкорость: {fighter_spd[0]:,}\nУрон: {fighter_dmg[0]:,}',
                            inline=True)
        embed_air.add_field(name="Транспортный Самолёт",
                            value=f'**Обычная:** {trans_air[0]:,}\n**Модификации:** \nСкорость: {trans_air_spd[0]:,}',
                            inline=True)
        embed_air.add_field(name="Десантный Самолёт",
                            value=f'**Обычная:** {air_air[0]}\n**Модификации:** \nСкорость: {air_air_spd[0]}',
                            inline=True)
        embed_air.add_field(name="Бомбардировщик",
                            value=f'**Обычная:** {bomber[0]:,}\n**Модификации:** \nЗащита: {bomber_def[0]:,}\nСкорость: {bomber_spd[0]:,}',
                            inline=True)
        embed_air.add_field(name="Разведовательный БПЛА",
                            value=f'**Обычная:** {ruav[0]:,}\n**Модификации:** \nСкорость: {ruav_spd[0]:,}',
                            inline=True)
        embed_air.add_field(name="Ударный БПЛА",
                            value=f'**Обычная:** {auav[0]:,}\n**Модификации:** \nСкорость: {auav_spd[0]:,}\nУрон: {auav_dmg[0]:,}',
                            inline=True)
        embed_air.add_field(name="Дрон Камикадзе",
                            value=f'**Обычная:** {kuav[0]:,}\n**Модификации:** \nУрон: {kuav_dmg[0]:,}',
                            inline=True)
        embed_air.add_field(name="Ракета",
                            value=f'**Обычная:** {missile[0]:,}\n**Модификации:** \nСкорость: {missile_spd[0]:,}\nУрон: {missile_dmg[0]:,}',
                            inline=True)
        embed_air.add_field(name="МБР",
                            value=f'**Обычная:** {ibm[0]:,}\n**Модификации:** \nСкорость: {ibm_spd[0]:,}\nУрон: {ibm_dmg[0]:,}',
                            inline=True)
        embed_air.add_field(name="Бомба",
                            value=f'**Обычная:** {bomb[0]:,}\n**Модификации:** \nУрон: {bomb_dmg[0]:,}',
                            inline=True)
        embed_air.add_field(name="Артиллерийский снаряд",
                            value=f'**Обычная:** {art_shell[0]:,}',
                            inline=True)
        embed_air.add_field(name="Реактивный снаряд",
                            value=f'**Обычная:** {rock_proj[0]:,}',
                            inline=True)

        embed_sea = disnake.Embed(title=f"Морская техника игрока {inter.author.name}",
                                  description="В этом разделе инвентаря описана вся информация про вашу морскую технику. Построить данный тип техники можно с помощью верфи")
        embed_sea.add_field(name="Фрегат",
                            value=f'**Обычная:** {frigate[0]:,}\n**Модификации:** \nЗащита: {frigate_def[0]:,}\nСкорость: {frigate_spd[0]:,}\nУрон: {frigate_dmg[0]:,}',
                            inline=True)
        embed_sea.add_field(name="Ракетный Крейсер",
                            value=f'**Обычная:** {miss_cruis[0]:,}\n**Модификации:** \nЗащита: {miss_cruis_def[0]:,}\nСкорость: {miss_cruis_spd[0]:,}',
                            inline=True)
        embed_sea.add_field(name="Транспортный Корабль",
                            value=f'**Обычная:** {trans_ship[0]:,}\n**Модификации:** \nЗащита: {trans_ship_def[0]:,}\nСкорость: {trans_ship_spd[0]:,}',
                            inline=True)
        embed_sea.add_field(name="Десантный Корабль",
                            value=f'**Обычная:** {land_ship[0]:,}\n**Модификации:** \nЗащита: {land_ship_def[0]:,}\nСкорость: {land_ship_spd[0]:,}',
                            inline=True)
        embed_sea.add_field(name="Катер", value=f'**Обычная:** {speedb[0]:,}', inline=True)
        embed_sea.add_field(name="Ракетная Подводная Лодка", value=f'**Обычная:** {miss_sub[0]:,}', inline=True)
        embed_sea.add_field(name="Ядерная Подводная Лодка", value=f'**Обычная:** {nuke_miss[0]:,}', inline=True)
        embed_sea.add_field(name="Авианосец", value=f'**Обычная:** {air_carrier[0]:,}', inline=True)

        embed_nuke_chem = disnake.Embed(title=f"Ядерная/Химическая техника игрока {inter.author.name}",
                                        description="В этом разделе инвентаря описана вся информация про вашу ядерную/химическую технику. Построить данный тип техники можно с помощью ядерного/химического завода")
        embed_nuke_chem.add_field(name="Ядерная Ракета", value=f'**Обычная:** {nuke_miss[0]:,}', inline=True)
        embed_nuke_chem.add_field(name="Ядерная Бомба", value=f'**Обычная:** {nuke_bomb[0]:,}', inline=True)
        embed_nuke_chem.add_field(name="Химическая Бомба", value=f'**Обычная:** {chem_bomb[0]:,}', inline=True)

        await inter.send(embed=embed_land)
        await inter.send(embed=embed_air)
        await inter.send(embed=embed_sea)
        await inter.send(embed=embed_nuke_chem)



    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command(aliases=["coll"])
async def collect(inter):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None:
        c.execute(f"SELECT money FROM 'users-data-lctime' WHERE id={inter.author.id}")
        lc_money = c.fetchone()
        lc_money = lc_money[0]

        c.execute(f"SELECT happy FROM 'users-data' WHERE id={inter.author.id}")
        happy = c.fetchone()
        happy = happy[0]

        c.execute(f"SELECT peoples FROM 'users-data' WHERE id={inter.author.id}")
        peoples = c.fetchone()
        peoples = peoples[0]

        c.execute(f"SELECT earn_per_person FROM 'users-data' WHERE id={inter.author.id}")
        earn_per_person = c.fetchone()
        earn_per_person = earn_per_person[0]

        c.execute(f"SELECT house FROM 'users-data-infra' WHERE id={inter.author.id}")
        house = c.fetchone()
        house = house[0]

        c.execute(f"SELECT multi_house FROM 'users-data-infra' WHERE id={inter.author.id}")
        multi_house = c.fetchone()
        multi_house = multi_house[0]

        c.execute(f"SELECT com_shops FROM 'users-data-infra' WHERE id={inter.author.id}")
        com_shops = c.fetchone()
        com_shops = com_shops[0]

        c.execute(f"SELECT com_electronics FROM 'users-data-infra' WHERE id={inter.author.id}")
        com_electronics = c.fetchone()
        com_electronics = com_electronics[0]

        c.execute(f"SELECT com_cars FROM 'users-data-infra' WHERE id={inter.author.id}")
        com_cars = c.fetchone()
        com_cars = com_cars[0]

        c.execute(f"SELECT com_it FROM 'users-data-infra' WHERE id={inter.author.id}")
        com_it = c.fetchone()
        com_it = com_it[0]

        c.execute(f"SELECT com_army FROM 'users-data-infra' WHERE id={inter.author.id}")
        com_army = c.fetchone()
        com_army = com_army[0]

        c.execute(f"SELECT com_buildings FROM 'users-data-infra' WHERE id={inter.author.id}")
        com_buildings = c.fetchone()
        com_buildings = com_buildings[0]

        c.execute(f"SELECT com_hospitals FROM 'users-data-infra' WHERE id={inter.author.id}")
        com_hospitals = c.fetchone()
        com_hospitals = com_hospitals[0]

        c.execute(f"SELECT money FROM 'users-data' WHERE id={inter.author.id}")
        old_balance = c.fetchone()
        old_balance = old_balance[0]

        coll_house = 10000
        coll_multi_house = 100000
        coll_com_shops = 30000
        coll_com_electronics = 42000
        coll_com_cars = 136000
        coll_com_it = 63000
        coll_com_army = 39000
        coll_com_buildings = 93000
        coll_com_hospitals = 72000

        usr_house = coll_house * house
        usr_multi_house = coll_multi_house * multi_house
        usr_com_shops = coll_com_shops * com_shops
        usr_com_electronics = coll_com_electronics * com_electronics
        usr_com_cars = coll_com_cars * com_cars
        usr_com_it = coll_com_it * com_it
        usr_com_army = coll_com_army * com_army
        usr_com_buildings = coll_com_buildings * com_buildings
        usr_com_hospitals = coll_com_hospitals * com_hospitals

        usr_coll_all = usr_com_hospitals + usr_com_buildings + usr_com_it + usr_com_army + usr_com_cars + usr_house + usr_com_electronics + usr_com_shops + usr_multi_house

        ltime = int(t.time()) - int(lc_money)

        if ltime < 1800:
            ltime1 = 1800 - int(ltime)
            ltime2 = ltime1 // 60

            embed = disnake.Embed(title="Ошибка",
                                  description=f"Ещё не прошло время до сбора денег! Подождите ещё {int(ltime2)} минут",
                                  color=0xff0000)
            embed.add_field(name="Последний сбор был:", value=f"<t:{lc_money}:R>")

            await inter.send(embed=embed)

        else:
            time_passed = int(t.time()) - int(lc_money)
            coll_count = time_passed // 1800

            taxes = peoples * earn_per_person
            collect = usr_coll_all + taxes

            with open("PremiumUsers.json", "r") as f:
                prem_usr_data = json.load(f)

            with open("VIPUsers.json", "r") as f:
                vip_usr_data = json.load(f)

            if str(inter.author.id) in prem_usr_data["list"]:
                collect += 1000000

            if str(inter.author.id) in vip_usr_data["list"]:
                collect *= 1.2 // 1

            collect = collect * coll_count
            collect = collect * 100 // happy

            balance = old_balance + collect

            lc_money = int(t.time())
            c.execute(f"UPDATE 'users-data-lctime' SET money={lc_money} WHERE id={inter.author.id}")
            c.execute(f"UPDATE 'users-data' SET money={balance} WHERE id={inter.author.id}")
            db.commit()

            embed = disnake.Embed(title="Успешно",
                                  description="Вы успешно собрали деньги!",
                                  color=0x00ff00)
            embed.add_field(name="Ваш доход с этого сбора:", value=f"${int(collect):,}", inline=True)
            embed.add_field(name="Ваш баланс составляет:", value=f"${int(balance):,}", inline=True)
            await inter.send(embed=embed)


    elif resid_org is not None:
        c.execute(f"SELECT goods_for_coll FROM 'users-data-org' WHERE id={inter.author.id}")
        goods_for_coll = c.fetchone()
        goods_for_coll = goods_for_coll[0]

        c.execute(f"SELECT money FROM 'users-data-org' WHERE id={inter.author.id}")
        old_balance = c.fetchone()
        old_balance = old_balance[0]

        c.execute(f"SELECT goods_count FROM 'users-data-org' WHERE id={inter.author.id}")
        goods_count = c.fetchone()
        goods_count = goods_count[0]

        c.execute(f"SELECT money FROM 'users-data-lctime' WHERE id={inter.author.id}")
        lc_money = c.fetchone()
        lc_money = lc_money[0]

        c.execute(f"SELECT offices FROM 'users-data-org' WHERE id={inter.author.id}")
        offices = c.fetchone()
        offices = offices[0]

        vip_role_id = 1123021947706548376
        role = disnake.utils.get(inter.guild.roles, id=vip_role_id)

        coll_offices = offices * 200000

        ltime = int(t.time()) - int(lc_money)

        if ltime < 1800:
            ltime1 = 1800 - int(ltime)
            ltime2 = ltime1 // 60

            embed = disnake.Embed(title="Ошибка",
                                  description=f"Ещё не прошло время до сбора денег! Подождите ещё {int(ltime2)} минут",
                                  color=0xff0000)
            embed.add_field(name="Последний сбор был:", value=f"<t:{lc_money}:R>")

            await inter.send(embed=embed)

        else:
            time_passed = int(t.time()) - int(lc_money)
            coll_count = time_passed // 1800

            collect = goods_count * goods_for_coll
            collect += coll_offices

            if role in inter.author.roles:
                collect += 2000000

            collect = collect * coll_count

            balance = old_balance + collect

            lc_money = int(t.time())
            c.execute(f"UPDATE 'users-data-lctime' SET money={lc_money} WHERE id={inter.author.id}")
            c.execute(f"UPDATE 'users-data-org' SET money={balance} WHERE id={inter.author.id}")
            db.commit()

            embed = disnake.Embed(title="Успешно",
                                  description="Вы успешно собрали деньги!",
                                  color=0x00ff00)
            embed.add_field(name="Ваш доход с этого сбора:", value=f"${int(collect):,}", inline=True)
            embed.add_field(name="Ваш баланс составляет:", value=f"${int(balance):,}", inline=True)
            await inter.send(embed=embed)


    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command()
async def call(inter, amount: int = 1):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None or resid_org is not None:
        c.execute(f"SELECT solider FROM 'users-data-army' WHERE id={inter.author.id}")
        soldier = c.fetchone()
        soldier = soldier[0]

        if amount <= 0:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы указали неверное кол-во солдат!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            if resid is not None:
                c.execute(f"SELECT money FROM 'users-data' WHERE id={inter.author.id}")
                balance = c.fetchone()
                balance = balance[0]

                c.execute(f"SELECT peoples FROM 'users-data' WHERE id={inter.author.id}")
                peoples = c.fetchone()
                peoples = peoples[0]

                c.execute(f"SELECT happy FROM 'users-data' WHERE id={inter.author.id}")
                happy = c.fetchone()
                happy = happy[0]

                max_peoples_for_call = peoples // 3

                if amount > max_peoples_for_call:
                    embed = disnake.Embed(title="Ошибка",
                                          description="У вас недостаточно населения для призыва!",
                                          color=0xff0000)
                    embed.add_field(name="Ваше население:", value=f"{peoples:,} человек")
                    embed.add_field(name="Доступно для призыва:", value=f"{max_peoples_for_call:,} человек")
                    await inter.send(embed=embed)

                else:
                    if balance < amount * 200:
                        embed = disnake.Embed(title="Ошибка",
                                              description="Недостаточно денег для призыва!",
                                              color=0xff0000)
                        embed.add_field(name="Ваш баланс", value=f"${balance:,}")
                        embed.add_field(name="Нужно для призыва", value=f"${(amount * 200):,}")
                        embed.add_field(name="Не хватает", value=f"${((amount * 200) - balance):,}")
                        await inter.send(embed=embed)

                    else:
                        up_money = balance - amount * 200
                        up_soldier = amount + soldier
                        up_happy = happy - 2
                        up_peoples = peoples - amount

                        c.execute(f"UPDATE 'users-data' SET money={up_money} WHERE id={inter.author.id}")
                        c.execute(f"UPDATE 'users-data-army' SET solider={up_soldier} WHERE id={inter.author.id}")
                        c.execute(f"UPDATE 'users-data' SET happy={up_happy} WHERE id={inter.author.id}")
                        c.execute(f"UPDATE 'users-data' SET peoples={up_peoples} WHERE id={inter.author.id}")
                        db.commit()

                        c.execute(f"SELECT solider FROM 'users-data-army' WHERE id={inter.author.id}")
                        soldier = c.fetchone()
                        soldier = soldier[0]

                        embed = disnake.Embed(title="Успешно",
                                              description="Вы призвали солдат!",
                                              color=0x00ff00)
                        embed.add_field(name="Ваш баланс", value=f"${(up_money):,}", inline=True)
                        embed.add_field(name="Кол-во солдат", value=f"{soldier:,} солдат", inline=True)
                        embed.add_field(name="Счастье", value=f"{up_happy}%")
                        embed.add_field(name="Население", value=f"{up_peoples:,} человек")
                        await inter.send(embed=embed)

            elif resid_org is not None:
                c.execute(f"SELECT money FROM 'users-data-org' WHERE id={inter.author.id}")
                balance = c.fetchone()
                balance = balance[0]

                c.execute(f"SELECT offices FROM 'users-data-org' WHERE id={inter.author.id}")
                offices = c.fetchone()
                offices = offices[0]

                c.execute(f"SELECT solider FROM 'users-data-army' WHERE id={inter.author.id}")
                soldier = c.fetchone()
                soldier = soldier[0]

                max_peoples_for_call = offices * 5000

                if soldier >= max_peoples_for_call:
                    c.execute(
                        f"UPDATE 'users-data-army' SET solider={max_peoples_for_call} WHERE id={inter.author.id}")
                    db.commit()

                    embed = disnake.Embed(title="Ошибка",
                                          description="У вас максимальное число солдат. Постройте больше офисов",
                                          color=0xff0000)
                    embed.add_field(name="Кол-во офисов", value=f"{offices:,} офисов")
                    embed.add_field(name="Максимальное кол-во солдат", value=f"{max_peoples_for_call:,} человек")
                    await inter.send(embed=embed)

                else:
                    if amount > max_peoples_for_call:
                        embed = disnake.Embed(title="Ошибка",
                                              description="У вас недостаточно людей для призыва!",
                                              color=0xff0000)
                        embed.add_field(name="Доступно для призыва:", value=f"{max_peoples_for_call:,} человек")
                        await inter.send(embed=embed)

                    else:
                        if balance < amount * 200:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="Недостаточно денег для призыва!",
                                                  color=0xff0000)
                            embed.add_field(name="Ваш баланс", value=f"${balance:,}")
                            embed.add_field(name="Нужно для призыва", value=f"${(amount * 5000):,}")
                            embed.add_field(name="Не хватает", value=f"${((amount * 5000) - balance):,}")
                            await inter.send(embed=embed)

                        else:
                            up_money = balance - amount * 5000
                            up_soldier = amount + soldier

                            c.execute(f"UPDATE 'users-data-org' SET money={up_money} WHERE id={inter.author.id}")
                            c.execute(
                                f"UPDATE 'users-data-army' SET solider={up_soldier} WHERE id={inter.author.id}")
                            db.commit()

                            c.execute(f"SELECT solider FROM 'users-data-army' WHERE id={inter.author.id}")
                            soldier = c.fetchone()
                            soldier = soldier[0]

                            embed = disnake.Embed(title="Успешно",
                                                  description="Вы призвали солдат!",
                                                  color=0x00ff00)
                            embed.add_field(name="Ваш баланс", value=f"${up_money:,}", inline=True)
                            embed.add_field(name="Кол-во солдат", value=f"{soldier:,} солдат", inline=True)
                            await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command(aliases=["mobil", "mobiliz", "mobi"])
async def mobilization(inter):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None:
        c.execute(f"SELECT solider FROM 'users-data-army' WHERE id={inter.author.id}")
        soldier = c.fetchone()
        soldier = soldier[0]

        c.execute(f"SELECT money FROM 'users-data' WHERE id={inter.author.id}")
        balance = c.fetchone()
        balance = balance[0]

        c.execute(f"SELECT peoples FROM 'users-data' WHERE id={inter.author.id}")
        peoples = c.fetchone()
        peoples = peoples[0]

        c.execute(f"SELECT happy FROM 'users-data' WHERE id={inter.author.id}")
        happy = c.fetchone()
        happy = happy[0]

        amount = peoples // 4

        if balance < amount * 50:
            embed = disnake.Embed(title="Ошибка",
                                  description="Недостаточно денег для призыва!",
                                  color=0xff0000)
            embed.add_field(name="Ваш баланс", value=f"${balance:,}")
            embed.add_field(name="Нужно для призыва", value=f"${(amount * 50):,}")
            embed.add_field(name="Не хватает", value=f"${((amount * 50) - balance):,}")
            await inter.send(embed=embed)

        else:
            up_solider = amount + soldier
            up_balance = balance - amount * 50
            up_happy = happy - 30
            up_peoples = peoples - amount

            if up_happy <= 10:
                if up_happy <= 0:
                    up_happy = 0
                embed = disnake.Embed(title="Ошибка",
                                      description="У вашего населения слишком маленькое счастье!",
                                      color=0xff0000)
                embed.add_field(name="Счастье", value=f"{up_happy}%")
                await inter.send(embed=embed)

                print(f"[{inter.author.name} | {inter.author.id}] $ happy <= 10%")

            c.execute(f"UPDATE 'users-data-army' SET solider={up_solider} WHERE id={inter.author.id}")
            c.execute(f"UPDATE 'users-data' SET money={up_balance} WHERE id={inter.author.id}")
            c.execute(f"UPDATE 'users-data' SET happy={up_happy} WHERE id={inter.author.id}")
            c.execute(f"UPDATE 'users-data' SET peoples={up_peoples} WHERE id={inter.author.id}")
            db.commit()

            c.execute(f"SELECT solider FROM 'users-data-army' WHERE id={inter.author.id}")
            soldier = c.fetchone()
            soldier = soldier[0]

            embed = disnake.Embed(title="Успешно",
                                  description="Вы успешно провели мобилизацию",
                                  color=0x00ff00)
            embed.add_field(name="Ваш баланс", value=f"${up_balance:,}", inline=True)
            embed.add_field(name="Кол-во солдат", value=f"{soldier:,} солдат", inline=True)
            embed.add_field(name="Счастье", value=f"{up_happy}%")
            embed.add_field(name="Население", value=f"{up_peoples:,} человек")
            await inter.send(embed=embed)

    elif resid_org is not None:
        embed = disnake.Embed(title="Ошибка",
                              description="Данная команда не доступна для организации",
                              color=0xff0000)
        await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command(aliases=["disb"])
async def disband(inter, amount: int = 1):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None:
        if amount <= 0:
            embed = disnake.Embed(title="Ошибка",
                                  description="Указано неверное кол-во солдат!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            c.execute(f"SELECT solider FROM 'users-data-army' WHERE id={inter.author.id}")
            soldier = c.fetchone()
            soldier = soldier[0]

            c.execute(f"SELECT peoples FROM 'users-data' WHERE id={inter.author.id}")
            peoples = c.fetchone()
            peoples = peoples[0]

            if amount < soldier:
                embed = disnake.Embed(title="Ошибка",
                                      description="Недостаточно солдат!",
                                      color=0xff0000)
                embed.add_field(name="Кол-во солдат", value=f"{soldier:,} солдат")
                await inter.send(embed=embed)

            else:
                up_soldier = soldier - amount
                up_peoples = peoples + amount

                c.execute(f"UPDATE 'users-data-army' SET solider={up_soldier} WHERE id={inter.author.id}")
                c.execute(f"UPDATE 'users-data' SET peoples={up_peoples} WHERE id={inter.author.id}")
                db.commit()

                embed = disnake.Embed(title="Успешно",
                                      description="Вы успешно распустили солдат!",
                                      color=0x00ff00)
                embed.add_field(name="Кол-во солдат", value=f"{up_soldier:,} солдат", inline=True)
                embed.add_field(name="Кол-во населения", value=f"{up_peoples:,} человек", inline=True)
                await inter.send(embed=embed)

    elif resid_org is not None:
        if amount <= 0:
            embed = disnake.Embed(title="Ошибка",
                                  description="Указано неверное кол-во солдат!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            c.execute(f"SELECT solider FROM 'users-data-army' WHERE id={inter.author.id}")
            soldier = c.fetchone()
            soldier = soldier[0]

            if amount < soldier:
                embed = disnake.Embed(title="Ошибка",
                                      description="Недостаточно солдат!",
                                      color=0xff0000)
                embed.add_field(name="Кол-во солдат", value=f"{soldier:,} солдат")
                await inter.send(embed=embed)

            else:
                up_soldier = soldier - amount

                c.execute(f"UPDATE 'users-data-army' SET solider={up_soldier} WHERE id={inter.author.id}")
                db.commit()

                embed = disnake.Embed(title="Успешно",
                                      description="Вы успешно распустили солдат!",
                                      color=0x00ff00)
                embed.add_field(name="Кол-во солдат", value=f"{up_soldier:,} солдат", inline=True)
                await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command()
async def pay(inter, member: disnake.Member, amount: int = 1):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
    resid_user = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
    resid_user_org = c.fetchone()

    if resid is not None or resid_org is not None:
        if resid is not None:
            c.execute(f"SELECT money FROM 'users-data' WHERE id={inter.author.id}")
            your_balance = c.fetchone()
            your_balance = your_balance[0]

        elif resid_org is not None:
            c.execute(f"SELECT money FROM 'users-data-org' WHERE id={inter.author.id}")
            your_balance = c.fetchone()
            your_balance = your_balance[0]

        if resid_user is not None or resid_user_org is not None:
            if resid_user is not None:
                c.execute(f"SELECT money FROM 'users-data' WHERE id={member.id}")
                user_balance = c.fetchone()
                user_balance = user_balance[0]

            elif resid_user_org is not None:
                c.execute(f"SELECT money FROM 'users-data-org' WHERE id={member.id}")
                user_balance = c.fetchone()
                user_balance = user_balance[0]
            if member == inter.author:

                    embed = disnake.Embed(title="Ошибка",

                                          description=f"Нельзя переводить деньги самому себе",

                                          color=0xff0000)

            else:
                if your_balance < amount:
                    embed = disnake.Embed(title="Ошибка",
                                      description=f"Недостаточно денег для перевода",
                                      color=0xff0000)
                    embed.add_field(name="Ваш баланс", value=f"${your_balance:,}")
                    await inter.send(embed=embed)

                else:
                    if amount <= 0:
                        embed = disnake.Embed(title="Ошибка",
                                          description=f"Вы указали неверную сумму!",
                                          color=0xff0000)
                        await inter.send(embed=embed)

                    else:
                        up_your_balance = your_balance - amount
                        up_user_balance = user_balance + amount

                        if resid is not None:
                            c.execute(f"UPDATE 'users-data' SET money={up_your_balance} WHERE id={inter.author.id}")

                        elif resid_org is not None:
                            c.execute(f"UPDATE 'users-data-org' SET money={up_your_balance} WHERE id={inter.author.id}")

                        if resid_user is not None:
                            c.execute(f"UPDATE 'users-data' SET money={up_user_balance} WHERE id={member.id}")

                        elif resid_user_org is not None:
                            c.execute(f"UPDATE 'users-data-org' SET money={up_user_balance} WHERE id={member.id}")

                        db.commit()

                        embed = disnake.Embed(title="Успешно",
                                          description=f"Вы успешно перевели пользователю <@{member.id}> ${amount:,}",
                                          color=0x00ff00)
                        embed.add_field(name="Ваш баланс", value=f"${up_your_balance:,}", inline=True)

                        await inter.send(embed=embed)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Данный пользователь не зарегистрирован!",
                                  color=0xff0000)
            await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command()
async def shop(inter):
    await BlackListMember(inter)

    embedland = disnake.Embed(title="Информация о предметах",
                              description="Здесь находится информация и цена на предметы наземной техники!")
    embedair = disnake.Embed(title="Информация о предметах",
                             description="Здесь находится информация и цена на предметы воздушной техники!")
    embedsea = disnake.Embed(title="Информация о предметах",
                             description="Здесь находится информация и цена на предметы морской техники!")
    embednuke = disnake.Embed(title="Информация о предметах",
                              description="Здесь находится информация и цена на предметы ядерной/химической техники!")

    with open("ArmyData.json", "r", encoding='utf-8') as f:
        data_army = json.load(f)
    for i in data_army:
        id = str(i)
        name = data_army[str(i)]["Name"]
        db_id = data_army[str(i)]["id"]
        typef = data_army[str(i)]["type"]
        cost_gold = data_army[str(i)]["ResNeed"]["gold"]
        cost_uranium = data_army[str(i)]["ResNeed"]["uranium"]
        cost_titanium = data_army[str(i)]["ResNeed"]["titanium"]
        cost_iron = data_army[str(i)]["ResNeed"]["iron"]
        cost_money = data_army[str(i)]["ResNeed"]["money"]
        modify_cost = data_army[str(i)]["Modify"]["Cost"]

        if typef == "ground":
            embedland.add_field(name=f"{name}",
                                value=f"ID - {id}\nТип - {typef}\nНужно золота - {cost_gold:,}\nНужно урана - {cost_uranium:,}\nНужно титана - {cost_titanium:,}\nНужно железа - {cost_iron:,}\nНужно денег - {cost_money:,}\nСтоимость модификации - {modify_cost:,}",
                                inline=False)

        elif typef == "air":
            embedair.add_field(name=f"{name}",
                               value=f"ID - {id}\nТип - {typef}\nНужно золота - {cost_gold:,}\nНужно урана - {cost_uranium:,}\nНужно титана - {cost_titanium:,}\nНужно железа - {cost_iron:,}\nНужно денег - {cost_money:,}\nСтоимость модификации - {modify_cost:,}",
                               inline=False)

        elif typef == "sea":
            embedsea.add_field(name=f"{name}",
                               value=f"ID - {id}\nТип - {typef}\nНужно золота - {cost_gold:,}\nНужно урана - {cost_uranium:,}\nНужно титана - {cost_titanium:,}\nНужно железа - {cost_iron:,}\nНужно денег - {cost_money:,}\nСтоимость модификации - {modify_cost:,}",
                               inline=False)

        elif typef == "nuke" or typef == "chemical":
            embednuke.add_field(name=f"{name}",
                                value=f"ID - {id}\nТип - {typef}\nНужно золота - {cost_gold:,}\nНужно урана - {cost_uranium:,}\nНужно титана - {cost_titanium:,}\nНужно железа - {cost_iron:,}\nНужно денег - {cost_money:,}\nСтоимость модификации - {modify_cost:,}",
                                inline=False)

    await inter.send(embed=embedland)
    await inter.send(embed=embedair)
    await inter.send(embed=embedsea)
    await inter.send(embed=embednuke)


@bot.command(aliases=["up"])
async def upgrade(inter, up: str):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None:
        c.execute(f"SELECT money FROM 'users-data' WHERE id={inter.author.id}")
        money = c.fetchone()
        money = money[0]

        if up == "eco" or up == "economy":
            c.execute(f"SELECT earn_per_person FROM 'users-data' WHERE id={inter.author.id}")
            earn_per_person = c.fetchone()
            earn_per_person = earn_per_person[0]

            if earn_per_person >= 500:
                up_earn_per_person = 500
                c.execute(
                    f"UPDATE 'users-data' SET earn_per_person={up_earn_per_person} WHERE id={inter.author.id}")
                db.commit()

                embed = disnake.Embed(title="Ошибка",
                                      description="Вы имеете максимальный доход с 1 человека!",
                                      color=0xff0000)
                embed.add_field(name="Доход с 1 человека", value=f"${up_earn_per_person:,}")
                await inter.send(embed=embed)

            else:
                c.execute(f"SELECT cost_up_eco FROM 'users-data' WHERE id={inter.author.id}")
                cost_up_eco = c.fetchone()
                cost_up_eco = cost_up_eco[0]

                if money < cost_up_eco:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Недостаточно денег для прокачки!",
                                          color=0xff0000)
                    embed.add_field(name="Баланс", value=f"${money}")
                    embed.add_field(name="Стоимость прокачки", value=f"${cost_up_eco:,}")
                    embed.add_field(name="Не хватает", value=f"${(cost_up_eco - money):,}")
                    await inter.send(embed=embed)

                else:
                    up_earn_per_person = earn_per_person * 1.1 // 1
                    up_cost_up_eco = cost_up_eco * 1.3 // 1
                    up_balance = money - cost_up_eco // 1

                    c.execute(
                        f"UPDATE 'users-data' SET earn_per_person={up_earn_per_person} WHERE id={inter.author.id}")
                    c.execute(f"UPDATE 'users-data' SET cost_up_eco={up_cost_up_eco} WHERE id={inter.author.id}")
                    c.execute(f"UPDATE 'users-data' SET money={up_balance} WHERE id={inter.author.id}")
                    db.commit()

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Вы успешно прокачали экономику",
                                          color=0x00ff00)
                    embed.add_field(name="Ваш баланс", value=f"${up_balance:,}", inline=True)
                    embed.add_field(name="Сбор с 1 человека", value=f"${up_earn_per_person:,}")
                    embed.add_field(name="Стоимость прокачки экономики", value=f"${up_cost_up_eco:,}")
                    await inter.send(embed=embed)

        elif up == "peop" or up == "peoples":
            c.execute(f"SELECT peoples FROM 'users-data' WHERE id={inter.author.id}")
            peoples = c.fetchone()
            peoples = peoples[0]

            if peoples >= 100000000:
                up_peoples = 100000000
                c.execute(f"UPDATE 'users-data' SET earn_per_person={up_peoples} WHERE id={inter.author.id}")
                db.commit()

                embed = disnake.Embed(title="Ошибка",
                                      description="Вы имеете максимальное население!",
                                      color=0xff0000)
                embed.add_field(name="Население", value=f"{up_peoples:,} человек")
                await inter.send(embed=embed)

            else:
                c.execute(f"SELECT cost_up_peoples FROM 'users-data' WHERE id={inter.author.id}")
                cost_up_peoples = c.fetchone()
                cost_up_peoples = cost_up_peoples[0]

                if money < cost_up_peoples:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Недостаточно денег для прокачки!",
                                          color=0xff0000)
                    embed.add_field(name="Баланс", value=f"${money:,}")
                    embed.add_field(name="Стоимость прокачки", value=f"${cost_up_peoples:,}")
                    embed.add_field(name="Не хватает", value=f"${(cost_up_peoples - money):,}")
                    await inter.send(embed=embed)

                else:
                    up_peoples = peoples * 1.15 // 1
                    up_cost_up_peoples = cost_up_peoples * 1.2 // 1
                    up_balance = money - cost_up_peoples // 1

                    c.execute(f"UPDATE 'users-data' SET peoples={up_peoples} WHERE id={inter.author.id}")
                    c.execute(
                        f"UPDATE 'users-data' SET cost_up_peoples={up_cost_up_peoples} WHERE id={inter.author.id}")
                    c.execute(f"UPDATE 'users-data' SET money={up_balance} WHERE id={inter.author.id}")
                    db.commit()

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Вы успешно прокачали население",
                                          color=0x00ff00)
                    embed.add_field(name="Ваш баланс", value=f"${up_balance:,}", inline=True)
                    embed.add_field(name="Население", value=f"{up_peoples:,} человек")
                    embed.add_field(name="Стоимость прокачки населения", value=f"${up_cost_up_peoples:,}")
                    await inter.send(embed=embed)

        elif up == "hap" or up == "happy":
            c.execute(f"SELECT happy FROM 'users-data' WHERE id={inter.author.id}")
            happy = c.fetchone()
            happy = happy[0]

            if happy >= 100:
                up_happy = 100
                c.execute(f"UPDATE 'users-data' SET happy={up_happy} WHERE id={inter.author.id}")
                db.commit()

                embed = disnake.Embed(title="Ошибка",
                                      description="Вы имеете максимальное счастье",
                                      color=0xff0000)
                embed.add_field(name="Счастье", value=f"{up_happy}%")
                await inter.send(embed=embed)

            else:
                c.execute(f"SELECT cost_up_happy FROM 'users-data' WHERE id={inter.author.id}")
                cost_up_happy = c.fetchone()
                cost_up_happy = cost_up_happy[0]

                if money < cost_up_happy:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Недостаточно денег для прокачки!",
                                          color=0xff0000)
                    embed.add_field(name="Баланс", value=f"${money:,}")
                    embed.add_field(name="Стоимость прокачки", value=f"${cost_up_happy:,}")
                    embed.add_field(name="Не хватает", value=f"${(cost_up_happy - money):,}")
                    await inter.send(embed=embed)

                else:
                    up_happy = happy + 1
                    up_balance = money - cost_up_happy

                    c.execute(f"UPDATE 'users-data' SET happy={up_happy} WHERE id={inter.author.id}")
                    c.execute(f"UPDATE 'users-data' SET money={up_balance} WHERE id={inter.author.id}")
                    db.commit()

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Вы успешно прокачали счастье жителей!",
                                          color=0x00ff00)
                    embed.add_field(name="Ваш баланс", value=f"${up_balance:,}", inline=True)
                    embed.add_field(name="Счастье", value=f"{up_happy}%")
                    embed.add_field(name="Стоимость прокачки счастья", value=f"${cost_up_happy:,}")
                    await inter.send(embed=embed)

        elif up == "product" or up == "prod":
            embed = disnake.Embed(title="Ошибка",
                                  description="Этот аргумент доступен только для организации!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        elif up == "count":
            embed = disnake.Embed(title="Ошибка",
                                  description="Этот аргумент доступен только для организации!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        elif up == None:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не ввели аргумент!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            pass

    elif resid_org is not None:
        if up == "eco" or up == "economy":
            embed = disnake.Embed(title="Ошибка",
                                  description="Этот аргумент доступен только для страны/сепаратиста!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        elif up == "peop" or up == "peoples":
            embed = disnake.Embed(title="Ошибка",
                                  description="Этот аргумент доступен только для страны/сепаратиста!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        elif up == "hap" or up == "happy":
            embed = disnake.Embed(title="Ошибка",
                                  description="Этот аргумент доступен только для страны/сепаратиста!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        elif up == "product" or up == "prod":
            c.execute(f"SELECT goods_for_coll FROM 'users-data-org' WHERE id={inter.author.id}")
            goods_for_coll = c.fetchone()
            goods_for_coll = goods_for_coll[0]

            c.execute(f"SELECT money FROM 'users-data-org' WHERE id={inter.author.id}")
            balance = c.fetchone()
            balance = balance[0]

            max_prod = 500

            if goods_for_coll == max_prod:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы имеете максимальный доход с 1 товара",
                                      color=0xff0000)
                await inter.send(embed=embed)

            elif goods_for_coll > max_prod:
                up_goods_for_coll = max_prod
                c.execute(
                    f"UPDATE 'users-data-org' SET goods_for_coll={up_goods_for_coll} WHERE id={inter.author.id}")
                db.commit()

                embed = disnake.Embed(title="Ошибка",
                                      description="Вы имеете максимальный доход с 1 товара",
                                      color=0xff0000)
                await inter.send(embed=embed)

            else:
                c.execute(f"SELECT cost_up_eco FROM 'users-data-org' WHERE id={inter.author.id}")
                cost_up_eco = c.fetchone()
                cost_up_eco = cost_up_eco[0]

                if balance < cost_up_eco:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Недостаточно денег для прокачки!",
                                          color=0xff0000)
                    embed.add_field(name="Баланс", value=f"${balance:,}")
                    embed.add_field(name="Стоимость прокачки", value=f"${cost_up_eco:,}")
                    embed.add_field(name="Не хватает", value=f"${(cost_up_eco - balance):,}")
                    await inter.send(embed=embed)

                else:
                    up_cost_up_eco = cost_up_eco * 1.15 // 1
                    up_balance = balance - cost_up_eco
                    up_goods_for_coll = goods_for_coll * 1.1 // 1

                    c.execute(
                        f"UPDATE 'users-data-org' SET goods_for_coll={up_goods_for_coll} WHERE id={inter.author.id}")
                    c.execute(f"UPDATE 'users-data-org' SET money={up_balance} WHERE id={inter.author.id}")
                    c.execute(
                        f"UPDATE 'users-data-org' SET cost_up_eco={up_cost_up_eco} WHERE id={inter.author.id}")
                    db.commit()

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Вы успешно прокачали сбор с 1 товара!",
                                          color=0x00ff00)
                    embed.add_field(name="Ваш баланс", value=f"${up_balance:,}", inline=True)
                    embed.add_field(name="Сбор с 1 товара", value=f"{up_goods_for_coll:,}")
                    embed.add_field(name="Стоимость прокачки", value=f"${up_cost_up_eco:,}")
                    await inter.send(embed=embed)

        elif up == "count":
            c.execute(f"SELECT goods_count FROM 'users-data-org' WHERE id={inter.author.id}")
            goods_count = c.fetchone()
            goods_count = goods_count[0]

            c.execute(f"SELECT offices FROM 'users-data-org' WHERE id={inter.author.id}")
            offices = c.fetchone()
            offices = offices[0]

            c.execute(f"SELECT money FROM 'users-data-org' WHERE id={inter.author.id}")
            balance = c.fetchone()
            balance = balance[0]

            max_prod = offices * 50000

            if goods_count == max_prod:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы имеете максимальное кол-во товара! Постройте больше офисов",
                                      color=0xff0000)
                embed.add_field(name="Офисы", value=f"{offices}")
                embed.add_field(name="Максимальное кол-во товара", value=f"{max_prod:,} шт.")
                await inter.send(embed=embed)

            elif goods_count > max_prod:
                up_goods_count = max_prod
                c.execute(f"UPDATE 'users-data-org' SET goods_count={up_goods_count} WHERE id={inter.author.id}")
                db.commit()

                embed = disnake.Embed(title="Ошибка",
                                      description="Вы имеете максимальное кол-во товара! Постройте больше офисов",
                                      color=0xff0000)
                embed.add_field(name="Офисы", value=f"{offices:,}")
                embed.add_field(name="Максимальное кол-во товара", value=f"{max_prod:,} шт.")
                await inter.send(embed=embed)

            else:
                c.execute(f"SELECT cost_up_goods FROM 'users-data-org' WHERE id={inter.author.id}")
                cost_up_goods = c.fetchone()
                cost_up_goods = cost_up_goods[0]

                if balance < cost_up_goods:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Недостаточно денег для прокачки!",
                                          color=0xff0000)
                    embed.add_field(name="Баланс", value=f"${balance:,}")
                    embed.add_field(name="Стоимость прокачки", value=f"${cost_up_goods:,}")
                    embed.add_field(name="Не хватает", value=f"${(cost_up_goods - balance):,}")
                    await inter.send(embed=embed)

                else:
                    up_cost_up_goods = cost_up_goods * 1.15 // 1
                    up_balance = balance - cost_up_goods
                    up_goods_count = goods_count * 1.1 // 1

                    c.execute(
                        f"UPDATE 'users-data-org' SET goods_count={up_goods_count} WHERE id={inter.author.id}")
                    c.execute(f"UPDATE 'users-data-org' SET money={up_balance} WHERE id={inter.author.id}")
                    c.execute(
                        f"UPDATE 'users-data-org' SET cost_up_goods={up_cost_up_goods} WHERE id={inter.author.id}")
                    db.commit()

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Вы успешно прокачали сбор с 1 товара!",
                                          color=0x00ff00)
                    embed.add_field(name="Ваш баланс", value=f"${up_balance:,}", inline=True)
                    embed.add_field(name="Кол-во товара", value=f"{up_goods_count:,} шт.")
                    embed.add_field(name="Стоимость прокачки", value=f"${up_cost_up_goods:,}")
                    await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command(aliases=["shopi", "shop-infra"])
async def shop_infrastructure(inter):
    await BlackListMember(inter)

    embed = disnake.Embed(title="Магазин инфраструктуры",
                          description="Здесь находится информация и цена на на инфраструктуру")
    with open("InfraData.json", "r", encoding='utf-8') as f:
        data_infra = json.load(f)

    for i in data_infra:
        id = str(i)
        name = data_infra[str(i)]["name"]
        maxf = data_infra[str(i)]["max"]
        cost_build = data_infra[str(i)]["building-materials"]

        embed.add_field(name=f"{name}",
                        value=f"ID - {id}\nМаксимально можно построить - {maxf:,}\nНужно строительных материалов - {cost_build:,}")

    await inter.send(embed=embed)


@bot.command(aliases=["top"])
async def leaderboard(inter):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()

    c.execute("SELECT id, money FROM 'users-data' UNION SELECT id, money FROM 'users-data-org'")
    player_data = c.fetchall()

    leaderboard_data = {}  # Создаем пустой словарь для хранения данных игроков

    # Заполняем словарь данными из базы данных
    for player in player_data:
        user_id = player[0]
        money = player[1]
        leaderboard_data[user_id] = money

    # Сортируем словарь по значению (балансу) и ограничиваем до топ-10
    sorted_leaderboard = dict(sorted(leaderboard_data.items(), key=lambda item: item[1], reverse=True)[:10])

    # Создаем embed для вывода топа игроков
    embed = disnake.Embed(title="Топ игроков по балансу", color=0xffd700)

    # Формируем поля (fields) для каждого игрока в топе
    for position, (user_id, money) in enumerate(sorted_leaderboard.items(), start=1):
        user = bot.get_user(user_id)
        name = user.name if user else f"Пользователь с ID {user_id}"
        embed.add_field(name=f"{position}. {name}", value=f"Баланс: {money} денег", inline=False)

    # Отправляем embed с топом игроков
    await inter.send(embed=embed)

    db.close()


@bot.command()
async def give(inter, member: disnake.Member, typef: str, amount: int, id: str, mod: str = None):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    if typef == "V" or typef == "v":
        with open("ArmyData.json", "r", encoding="utf-8") as f:
            army_data = json.load(f)

        if id not in army_data:
            embed = disnake.Embed(title="Ошибка",
                                  description="Такого предмета не существует!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            item_name_id = army_data[id]["id"]
            if mod is not None:
                c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
                resid = c.fetchone()

                c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
                resid_org = c.fetchone()

                c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
                resid_user = c.fetchone()

                c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
                resid_user_org = c.fetchone()

                if resid is not None or resid_org is not None:
                    if mod == "def":
                        item_name_id = item_name_id + "_def"
                        try:
                            c.execute(f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={inter.author.id}")
                            item = c.fetchone()
                            item = item[0]

                        except sqlite3.OperationalError:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У данного предмета нет этой модификации!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)
                            return

                    elif mod == "spd":
                        item_name_id = item_name_id + "_spd"
                        try:
                            c.execute(f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={inter.author.id}")
                            item = c.fetchone()
                            item = item[0]

                        except sqlite3.OperationalError:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У данного предмета нет этой модификации!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)
                            return

                    elif mod == "dmg":
                        item_name_id = item_name_id + "_dmg"
                        try:
                            c.execute(f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={inter.author.id}")
                            item = c.fetchone()
                            item = item[0]

                        except sqlite3.OperationalError:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У данного предмета нет этой модификации!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)
                            return

                    else:
                        embed = disnake.Embed(title="Ошибка", description="Вы указали неверную модификацию!",
                                              color=0xff0000)
                        await inter.send(embed=embed)
                        return

                    if resid_user is not None or resid_user_org is not None:
                        c.execute(f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={member.id}")
                        item_user = c.fetchone()
                        item_user = item_user[0]

                        if amount <= 0:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="Вы указали неверную сумму для передачи!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)

                        else:
                            if amount > item:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="Недостаточно пердметов для передачи!",
                                                      color=0xff0000)
                                await inter.send(embed=embed)

                            else:
                                up_item = item - amount
                                up_item_user = item_user + amount

                                c.execute(
                                    f"UPDATE 'users-data-army-mod' SET {item_name_id}={up_item} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-army-mod' SET {item_name_id}={up_item_user} WHERE id={member.id}")
                                db.commit()

                                item_name = army_data[id]["Name"]
                                embed = disnake.Embed(title="Успешно",
                                                      description=f"Вы передали пользователю {member.mention} {amount:,} {item_name} с модификацией {mod}!",
                                                      color=0x00ff00)
                                await inter.send(embed=embed)

                    else:
                        embed = disnake.Embed(title="Ошибка",
                                              description="Данный пользователь не зарегистрирован!",
                                              color=0xff0000)
                        await inter.send(embed=embed)

                else:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                          color=0xff0000)
                    await inter.send(embed=embed)

            elif mod is None:
                c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
                resid = c.fetchone()

                c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
                resid_org = c.fetchone()

                c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
                resid_user = c.fetchone()

                c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
                resid_user_org = c.fetchone()

                if resid is not None or resid_org is not None:
                    c.execute(f"SELECT {item_name_id} FROM 'users-data-army' WHERE id={inter.author.id}")
                    item = c.fetchone()
                    item = item[0]

                    if resid_user is not None or resid_user_org is not None:
                        c.execute(f"SELECT {item_name_id} FROM 'users-data-army' WHERE id={member.id}")
                        item_user = c.fetchone()
                        item_user = item_user[0]

                        if amount <= 0:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="Вы указали неверную сумму для передачи!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)

                        else:
                            if amount > item:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="Недостаточно пердметов для передачи!",
                                                      color=0xff0000)
                                await inter.send(embed=embed)

                            else:
                                up_item = item - amount
                                up_item_user = item_user + amount

                                c.execute(
                                    f"UPDATE 'users-data-army' SET {item_name_id}={up_item} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-army' SET {item_name_id}={up_item_user} WHERE id={member.id}")
                                db.commit()

                                item_name = army_data[id]["Name"]
                                embed = disnake.Embed(title="Успешно",
                                                      description=f"Вы передали пользователю {member.mention} {amount:,} {item_name}!",
                                                      color=0x00ff00)
                                await inter.send(embed=embed)

                    else:
                        embed = disnake.Embed(title="Ошибка",
                                              description="Данный пользователь не зарегистрирован!",
                                              color=0xff0000)
                        await inter.send(embed=embed)

                else:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Вы не зарегистрированы! Для регистрации на сервере используйте команду $reg <type>",
                                          color=0xff0000)
                    await inter.send(embed=embed)

    elif typef == "R" or typef == "r":
        with open("ResData.json", "r", encoding="utf-8") as f:
            res_data = json.load(f)

        if id not in res_data:
            embed = disnake.Embed(title="Ошибка",
                                  description="Такого ресурса не существует!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            if mod is not None:
                embed = disnake.Embed(title="Ошибка",
                                      description="Модификации не доступны для ресурсов!",
                                      color=0xff0000)
                await inter.send(embed=embed)

            else:
                item_name_id = res_data[id]["id"]
                c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
                resid = c.fetchone()

                c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
                resid_org = c.fetchone()

                c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
                resid_user = c.fetchone()

                c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
                resid_user_org = c.fetchone()

                if resid is not None or resid_org is not None:
                    c.execute(f"SELECT {item_name_id} FROM 'users-data-resources' WHERE id={inter.author.id}")
                    item = c.fetchone()
                    item = item[0]

                    if resid_user is not None or resid_user_org is not None:
                        c.execute(f"SELECT {item_name_id} FROM 'users-data-resources' WHERE id={member.id}")
                        item_user = c.fetchone()
                        item_user = item_user[0]

                        if amount <= 0:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="Вы указали неверную сумму для передачи!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)

                        else:
                            if amount > item:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="Недостаточно пердметов для передачи!",
                                                      color=0xff0000)
                                await inter.send(embed=embed)

                            else:
                                up_item = item - amount
                                up_item_user = item_user + amount

                                c.execute(
                                    f"UPDATE 'users-data-resources' SET {item_name_id}={up_item} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET {item_name_id}={up_item_user} WHERE id={member.id}")
                                db.commit()

                                item_name = res_data[id]["name"]
                                embed = disnake.Embed(title="Успешно",
                                                      description=f"Вы передали пользователю {member.mention} {amount:,} {item_name}!",
                                                      color=0x00ff00)
                                await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы ввели неверный вид!",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command()
@commands.has_permissions(administrator=True)
async def item(inter, member: disnake.Member, typef: str, amount: int, id: str, mod: str = None):
    await BlackListMember(inter)
    await BlackListAdmin(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    if amount > 9999999999 or amount < -9999999999:
        embed = disnake.Embed(title="Ошибка",
                              description="Указана неверное кол-во",
                              color=0xff0000)
        await inter.send(embed=embed)
        return
    if typef == "V" or typef == "v":
        with open("ArmyData.json", "r", encoding="utf-8") as f:
            army_data = json.load(f)

        if id not in army_data:
            embed = disnake.Embed(title="Ошибка",
                                  description="Такого предмета не существует!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            item_name_id = army_data[id]["id"]
            if mod is not None:
                c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
                resid_user = c.fetchone()

                c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
                resid_user_org = c.fetchone()

                if resid_user is not None or resid_user_org is not None:
                    if mod == "def":
                        item_name_id = item_name_id + "_def"
                        try:
                            c.execute(f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={member.id}")
                            item_user = c.fetchone()
                            item_user = item_user[0]

                        except sqlite3.OperationalError:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У данного предмета нет этой модификации!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)
                            return

                    elif mod == "spd":
                        item_name_id = item_name_id + "_spd"
                        try:
                            c.execute(f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={member.id}")
                            item_user = c.fetchone()
                            item_user = item_user[0]

                        except sqlite3.OperationalError:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У данного предмета нет этой модификации!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)
                            return

                    elif mod == "dmg":
                        item_name_id = item_name_id + "_dmg"
                        try:
                            c.execute(f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={member.id}")
                            item_user = c.fetchone()
                            item_user = item_user[0]

                        except sqlite3.OperationalError:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У данного предмета нет этой модификации!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)
                            return

                    else:
                        embed = disnake.Embed(title="Ошибка", description="Вы указали неверную модификацию!",
                                              color=0xff0000)
                        await inter.send(embed=embed)
                        return

                    c.execute(f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={member.id}")
                    item_user = c.fetchone()
                    item_user = item_user[0]

                    up_item_user = item_user + amount

                    c.execute(f"UPDATE 'users-data-army-mod' SET {item_name_id}={up_item_user} WHERE id={member.id}")
                    db.commit()

                    item_name = army_data[id]["Name"]
                    embed = disnake.Embed(title="Успешно",
                                          description=f"Вы выдали пользователю {member.mention} {amount:,} {item_name} с модификацией {mod}!",
                                          color=0x00ff00)
                    await inter.send(embed=embed)

                else:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Данный пользователь не зарегистрирован!",
                                          color=0xff0000)
                    await inter.send(embed=embed)

            elif mod is None:
                c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
                resid_user = c.fetchone()

                c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
                resid_user_org = c.fetchone()

                if resid_user is not None or resid_user_org is not None:
                    c.execute(f"SELECT {item_name_id} FROM 'users-data-army' WHERE id={member.id}")
                    item_user = c.fetchone()
                    item_user = item_user[0]

                    up_item_user = item_user + amount

                    c.execute(f"UPDATE 'users-data-army' SET {item_name_id}={up_item_user} WHERE id={member.id}")
                    db.commit()

                    item_name = army_data[id]["Name"]
                    embed = disnake.Embed(title="Успешно",
                                          description=f"Вы выдали пользователю {member.mention} {amount:,} {item_name}!",
                                          color=0x00ff00)
                    await inter.send(embed=embed)

                else:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Данный пользователь не зарегистрирован!",
                                          color=0xff0000)
                    await inter.send(embed=embed)

    elif typef == "R" or typef == "r":
        with open("ResData.json", "r", encoding="utf-8") as f:
            res_data = json.load(f)

        if id not in res_data:
            embed = disnake.Embed(title="Ошибка",
                                  description="Такого ресурса не существует!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            if mod is not None:
                embed = disnake.Embed(title="Ошибка",
                                      description="Модификации не доступны для ресурсов!",
                                      color=0xff0000)
                await inter.send(embed=embed)

            else:
                c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
                resid_user = c.fetchone()

                c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
                resid_user_org = c.fetchone()
                if resid_user is not None or resid_user_org is not None:
                    item_name_id = res_data[id]["id"]
                    c.execute(f"SELECT {item_name_id} FROM 'users-data-resources' WHERE id={member.id}")
                    item_user = c.fetchone()
                    item_user = item_user[0]

                    up_item_user = item_user + amount

                    c.execute(f"UPDATE 'users-data-resources' SET {item_name_id}={up_item_user} WHERE id={member.id}")
                    db.commit()

                    item_name = res_data[id]["name"]
                    embed = disnake.Embed(title="Успешно",
                                          description=f"Вы выдали пользователю {member.mention} {amount:,} {item_name}!",
                                          color=0x00ff00)
                    await inter.send(embed=embed)

                else:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Данный пользователь не зарегистрирован!",
                                          color=0xff0000)
                    await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы ввели неверный вид!",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command()
@commands.has_permissions(administrator=True)
async def soldier(inter, member: disnake.Member, amount: int):
    await BlackListMember(inter)
    await BlackListAdmin(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()

    c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
    resid_user = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
    resid_user_org = c.fetchone()

    if amount > 999999999 or amount < -999999999:
        embed = disnake.Embed(title="Ошибка",
                              description="Указано неверное кол-во солдат",
                              color=0xff0000)
        await inter.send(embed=embed)
        return

    if resid_user is not None or resid_user_org is not None:
        c.execute(f"SELECT solider FROM 'users-data-army' WHERE id={member.id}")
        user_soldier = c.fetchone()
        user_soldier = user_soldier[0]

        up_soldier = user_soldier + amount

        c.execute(f"UPDATE 'users-data-army' SET solider={up_soldier} WHERE id={member.id}")
        db.commit()

        embed = disnake.Embed(title="Успешно",
                              description=f"Кол-во солдат игрока {member.mention} успешно изменено!",
                              color=0x00ff00)
        embed.add_field(name="Солдаты", value=f"{up_soldier:,} солдат")
        await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Данный пользователь не зарегистрирован!",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command()
async def make(inter):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None or resid_org is not None:
        c.execute(f"SELECT building_materials FROM 'users-data-lctime' WHERE id={inter.author.id}")
        build_lctime = c.fetchone()
        build_lctime = build_lctime[0]

        c.execute(f"SELECT building_materials FROM 'users-data-resources' WHERE id={inter.author.id}")
        build_res = c.fetchone()
        build_res = build_res[0]

        with open("ResData.json", "r") as f:
            res_data = json.load(f)

        min_coll = res_data["6"]["min"]
        max_coll = res_data["6"]["max"]

        build_coll = rdi(min_coll, max_coll)

        time_now = int(t.time())
        time_passed = time_now - build_lctime

        if time_passed < 14400:
            ltime1 = 14400 - int(time_passed)
            ltime2 = ltime1 // 60
            embed = disnake.Embed(title="Ошибка",
                                  description=f"Ещё не прошло время до сбора строительных материалов! Подождите ещё {ltime2} минут",
                                  color=0xff0000)
            embed.add_field(name="Последний сбор был:", value=f"<t:{build_lctime}:R>")

            await inter.send(embed=embed)

        else:
            up_build = build_res + build_coll

            c.execute(f"UPDATE 'users-data-resources' SET building_materials={up_build} WHERE id={inter.author.id}")
            c.execute(f"UPDATE 'users-data-lctime' SET building_materials={int(t.time())} WHERE id={inter.author.id}")
            db.commit()

            embed = disnake.Embed(title="Успешно",
                                  description="Вы успешно собрали строительные материалы!",
                                  color=0x00ff00)
            embed.add_field(name="Ваш доход с этого сбора:", value=f"{int(build_coll):,}", inline=True)
            embed.add_field(name="Кол-во строительных материалов:", value=f"{int(up_build):,}", inline=True)
            await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command()
async def mine(inter, id: str):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None or resid_org is not None:
        with open("ResData.json", "r", encoding="utf-8") as f:
            res_data = json.load(f)

        if id not in res_data:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы указали неверный ID ресурса",
                                  color=0xff0000)
            await inter.send(embed=embed)

        elif id == "6":
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не можете добывать строительные материалы",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            res_id = res_data[id]["id"]

            c.execute(f"SELECT {res_id} FROM 'users-data-resdots' WHERE id={inter.author.id}")
            res_dot = c.fetchone()
            res_dot = res_dot[0]

            if res_dot == 0:
                embed = disnake.Embed(title="Ошибка",
                                      description="У вас нет этой точки! Колонизируйте территорию",
                                      color=0xff0000)
                await inter.send(embed=embed)

            else:
                c.execute(f"SELECT {res_id} FROM 'users-data-lctime' WHERE id={inter.author.id}")
                res_lctime = c.fetchone()
                res_lctime = res_lctime[0]

                min_coll = res_data[id]["min"]
                max_coll = res_data[id]["max"]

                res_coll = rdi(min_coll, max_coll) * res_dot

                time_passed = int(t.time()) - res_lctime

                if time_passed < 3600:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Ещё рано! Попробуйте позже",
                                          color=0xff0000)
                    embed.add_field(name="Последний сбор", value=f"<t:{res_lctime}:R>")
                    await inter.send(embed=embed)

                else:
                    c.execute(f"SELECT {res_id} FROM 'users-data-resources' WHERE id={inter.author.id}")
                    res_inv = c.fetchone()
                    res_inv = res_inv[0]
                    up_res_inv = res_inv + res_coll

                    c.execute(f"UPDATE 'users-data-resources' SET {res_id}=? WHERE id=?", (up_res_inv, inter.author.id))
                    c.execute(f"UPDATE 'users-data-lctime' SET {res_id}={int(t.time())} WHERE id={inter.author.id}")
                    db.commit()

                    res_name = res_data[id]["name"]
                    embed = disnake.Embed(title="Успешно",
                                          description=f"Вы успешно собрали {res_name}!",
                                          color=0x00ff00)
                    embed.add_field(name="Ваш доход с этого сбора:", value=f"{int(res_coll):,}", inline=True)
                    embed.add_field(name=f"Кол-во {res_name}:", value=f"{int(up_res_inv):,}", inline=True)
                    await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command()
async def build(inter, id: str):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None or resid_org is not None:
        with open("InfraData.json", "r", encoding="utf-8") as f:
            infra_data = json.load(f)

        if id not in infra_data:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы ввели неверный ID инфраструктуры",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            infra_id = infra_data[id]["id"]
            max_infra = infra_data[id]["max"]
            infra_name = infra_data[id]["name"]

            c.execute(f"SELECT {infra_id} FROM 'users-data-infra' WHERE id={inter.author.id}")
            infra_inv = c.fetchone()
            infra_inv = infra_inv[0]

            if infra_inv >= max_infra:
                embed = disnake.Embed(title="Ошибка",
                                      description=f"У вас максимальное кол-во {infra_name}",
                                      color=0xff0000)
                await inter.send(embed=embed)

            else:
                c.execute(f"SELECT building_materials FROM 'users-data-resources' WHERE id={inter.author.id}")
                build_m = c.fetchone()
                build_m = build_m[0]

                build_m_need = infra_data[id]["building-materials"]

                if build_m < build_m_need:
                    embed = disnake.Embed(title="Ошибка",
                                          description=f"Недостаточно строительных материалов",
                                          color=0xff0000)
                    embed.add_field(name="Нужно материалов", value=f"{build_m_need:,}")
                    embed.add_field(name="У вас есть", value=f"{build_m:,}")
                    embed.add_field(name="Ещё нужно", value=f"{(build_m_need - build_m):,}")
                    await inter.send(embed=embed)

                else:
                    up_build = infra_inv + 1
                    up_build_m = build_m - build_m_need

                    c.execute(f"UPDATE 'users-data-infra' SET {infra_id}={up_build} WHERE id={inter.author.id}")
                    c.execute(
                        f"UPDATE 'users-data-resources' SET building_materials={up_build_m} WHERE id={inter.author.id}")
                    db.commit()

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Вы успешно построили {infra_name}",
                                          color=0x00ff00)
                    embed.add_field(name="Кол-во строительных материалов:", value=f"{int(up_build_m):,}", inline=True)
                    embed.add_field(name=f"Кол-во {infra_name}:", value=f"{int(up_build):,}", inline=True)
                    await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command(aliases=["const"])
@commands.has_permissions(administrator=True)
async def construction(inter, member: disnake.Member, action: str, id: str):
    await BlackListMember(inter)
    await BlackListAdmin(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()

    c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
    resid_user = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
    resid_user_org = c.fetchone()

    if resid_user is not None or resid_user_org is not None:
        with open("InfraData.json", "r", encoding="utf-8") as f:
            infra_data = json.load(f)

        if id not in infra_data:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы ввели неверный ID инфраструктуры",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            if action == "add":
                infra_id = infra_data[id]["id"]
                max_infra = infra_data[id]["max"]
                infra_name = infra_data[id]["name"]

                c.execute(f"SELECT {infra_id} FROM 'users-data-infra' WHERE id={member.id}")
                infra_inv = c.fetchone()
                infra_inv = infra_inv[0]

                if infra_inv >= max_infra:
                    embed = disnake.Embed(title="Ошибка",
                                          description=f"У {member.mention} максимальное кол-во {infra_name}",
                                          color=0xff0000)
                    await inter.send(embed=embed)

                else:
                    up_build = infra_inv + 1

                    c.execute(f"UPDATE 'users-data-infra' SET {infra_id}={up_build} WHERE id={member.id}")
                    db.commit()

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Вы успешно построили {infra_name}",
                                          color=0x00ff00)
                    embed.add_field(name=f"Кол-во {infra_name}:", value=f"{int(up_build):,}", inline=True)
                    await inter.send(embed=embed)

            elif action == "remove":
                infra_id = infra_data[id]["id"]
                infra_name = infra_data[id]["name"]

                c.execute(f"SELECT {infra_id} FROM 'users-data-infra' WHERE id={member.id}")
                infra_inv = c.fetchone()
                infra_inv = infra_inv[0]

                if infra_inv == 0:
                    embed = disnake.Embed(title="Ошибка",
                                          description=f"У {member.mention} минимальное кол-во {infra_name}",
                                          color=0xff0000)
                    await inter.send(embed=embed)

                else:
                    up_build = infra_inv - 1

                    c.execute(f"UPDATE 'users-data-infra' SET {infra_id}={up_build} WHERE id={member.id}")
                    db.commit()

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Вы успешно построили {infra_name}",
                                          color=0x00ff00)
                    embed.add_field(name=f"Кол-во {infra_name}:", value=f"{int(up_build):,}", inline=True)
                    await inter.send(embed=embed)

            else:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали неверное действие",
                                      color=0xff0000)
                await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Данный пользователь не зарегистрирован!",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command()
async def destroy(inter, typef: str, id: str, amount: int = 1, *args):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None or resid_org is not None:
        if typef == "infrastructure" or typef == "I" or typef == "i":
            with open("InfraData.json", "r", encoding="utf-8") as f:
                infra_data = json.load(f)

            if id not in infra_data:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали неверный ID инфраструктуры!",
                                      color=0xff0000)
                await inter.send(embed=embed)

            else:
                infra_id = infra_data[id]["id"]
                infra_name = infra_data[id]["name"]

                c.execute(f"SELECT {infra_id} FROM 'users-data-infra' WHERE id={inter.author.id}")
                infra_inv = c.fetchone()
                infra_inv = infra_inv[0]

                if infra_inv == 0:
                    embed = disnake.Embed(title="Ошибка",
                                          description="У вас нет данной постройки!",
                                          color=0xff0000)
                    await inter.send(embed=embed)

                else:
                    if infra_inv < amount:
                        embed = disnake.Embed(title="Ошибка",
                                              description="Недостаточно инфраструктуры для уничтожения!",
                                              color=0xff0000)
                        await inter.send(embed=embed)

                    else:
                        up_build = infra_inv - amount

                        c.execute(f"UPDATE 'users-data-infra' SET {infra_id}={up_build} WHERE id={inter.author.id}")
                        db.commit()

                        embed = disnake.Embed(title="Успешно",
                                              description=f"Вы успешно уничтожили {infra_name} в количестве {amount:,}!",
                                              color=0x00ff00)
                        embed.add_field(name=f"Кол-во {infra_name}:", value=f"{int(up_build)}", inline=True)
                        await inter.send(embed=embed)

        elif typef == "vehicle" or typef == "V" or typef == "v":
            with open("ArmyData.json", "r", encoding="utf-8") as f:
                army_data = json.load(f)

            if id not in army_data:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали неверный ID техники!",
                                      color=0xff0000)
                await inter.send(embed=embed)

            else:
                if args:
                    if args[0] == "def":
                        army_id = f"{army_data[id]['id']}_def"
                        army_name = army_data[id]["Name"]

                        c.execute(f"SELECT {army_id} FROM 'users-data-army-mod' WHERE id={inter.author.id}")
                        army_inv = c.fetchone()
                        army_inv = army_inv[0]

                        if army_inv == 0:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У вас нет данной техники!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)

                        elif army_inv < amount:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У вас недостаточно техники для уничтожения!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)

                        else:
                            up_army = army_inv - amount

                            c.execute(
                                f"UPDATE 'users-data-army-mod' SET {army_id}={up_army} WHERE id={inter.author.id}")
                            db.commit()

                            embed = disnake.Embed(title="Успешно",
                                                  description=f"Вы успешно уничтожили {army_name} в количестве {amount:,} с модификацией def!",
                                                  color=0x00ff00)
                            embed.add_field(name=f"Кол-во {army_name}:", value=f"{int(up_army)}", inline=True)
                            await inter.send(embed=embed)

                    elif args[0] == "spd":
                        army_id = f"{army_data[id]['id']}_spd"
                        army_name = army_data[id]["Name"]

                        c.execute(f"SELECT {army_id} FROM 'users-data-army-mod' WHERE id={inter.author.id}")
                        army_inv = c.fetchone()
                        army_inv = army_inv[0]

                        if army_inv == 0:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У вас нет данной техники!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)

                        elif army_inv < amount:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У вас недостаточно техники для уничтожения!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)

                        else:
                            up_army = army_inv - amount

                            c.execute(
                                f"UPDATE 'users-data-army-mod' SET {army_id}={up_army} WHERE id={inter.author.id}")
                            db.commit()

                            embed = disnake.Embed(title="Успешно",
                                                  description=f"Вы успешно уничтожили {army_name} в количестве {amount:,} с модификацией spd!",
                                                  color=0x00ff00)
                            embed.add_field(name=f"Кол-во {army_name}:", value=f"{int(up_army)}", inline=True)
                            await inter.send(embed=embed)

                    elif args[0] == "dmg":
                        army_id = f"{army_data[id]['id']}_dmg"
                        army_name = army_data[id]["Name"]

                        c.execute(f"SELECT {army_id} FROM 'users-data-army-mod' WHERE id={inter.author.id}")
                        army_inv = c.fetchone()
                        army_inv = army_inv[0]

                        if army_inv == 0:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У вас нет данной техники!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)

                        elif army_inv < amount:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У вас недостаточно техники для уничтожения!",
                                                  color=0xff0000)
                            await inter.send(embed=embed)

                        else:
                            up_army = army_inv - amount

                            c.execute(
                                f"UPDATE 'users-data-army-mod' SET {army_id}={up_army} WHERE id={inter.author.id}")
                            db.commit()

                            embed = disnake.Embed(title="Успешно",
                                                  description=f"Вы успешно уничтожили {army_name} в количестве {amount:,} с модификацией dmg!",
                                                  color=0x00ff00)
                            embed.add_field(name=f"Кол-во {army_name}:", value=f"{int(up_army)}", inline=True)
                            await inter.send(embed=embed)

                else:
                    army_id = army_data[id]["id"]
                    army_name = army_data[id]["Name"]

                    c.execute(f"SELECT {army_id} FROM 'users-data-army' WHERE id={inter.author.id}")
                    army_inv = c.fetchone()
                    army_inv = army_inv[0]

                    if army_inv == 0:
                        embed = disnake.Embed(title="Ошибка",
                                              description="У вас нет данной техники!",
                                              color=0xff0000)
                        await inter.send(embed=embed)

                    elif army_inv < amount:
                        embed = disnake.Embed(title="Ошибка",
                                              description="У вас недостаточно техники для уничтожения!",
                                              color=0xff0000)
                        await inter.send(embed=embed)

                    else:
                        up_army = army_inv - amount

                        c.execute(f"UPDATE 'users-data-army' SET {army_id}={up_army} WHERE id={inter.author.id}")
                        db.commit()

                        embed = disnake.Embed(title="Успешно",
                                              description=f"Вы успешно уничтожили {army_name} в количестве {amount:,}!",
                                              color=0x00ff00)
                        embed.add_field(name=f"Кол-во {army_name}:", value=f"{int(up_army)}", inline=True)
                        await inter.send(embed=embed)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы указали неверный тип!",
                                  color=0xff0000)
            await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command(aliases=["cr"])
async def create(inter, id: str, amount: int = 1):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None or resid_org is not None:
        with open("ArmyData.json", "r", encoding="utf-8") as f:
            army_data = json.load(f)

        if id not in army_data:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы указали неверный ID техники!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            army_id = army_data[id]["id"]
            army_name = army_data[id]["Name"]
            army_type = army_data[id]["type"]

            c.execute(f"SELECT land_equipment_plant FROM 'users-data-infra' WHERE id={inter.author.id}")
            land_equipment_plant = c.fetchone()
            land_equipment_plant = land_equipment_plant[0]

            c.execute(f"SELECT aviation_factory FROM 'users-data-infra' WHERE id={inter.author.id}")
            aviation_factory = c.fetchone()
            aviation_factory = aviation_factory[0]

            c.execute(f"SELECT shipyard FROM 'users-data-infra' WHERE id={inter.author.id}")
            shipyard = c.fetchone()
            shipyard = shipyard[0]

            c.execute(f"SELECT nuclear_factory FROM 'users-data-infra' WHERE id={inter.author.id}")
            nuclear_factory = c.fetchone()
            nuclear_factory = nuclear_factory[0]

            c.execute(f"SELECT chemical_factory FROM 'users-data-infra' WHERE id={inter.author.id}")
            chemical_factory = c.fetchone()
            chemical_factory = chemical_factory[0]

            with open("ResData.json", "r", encoding="utf-8") as f:
                res_data = json.load(f)

            if amount <= 0:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали неверную кол-во!",
                                      color=0xff0000)
                await inter.send(embed=embed)

            else:
                if army_type == "ground":
                    if land_equipment_plant == 0:
                        embed = disnake.Embed(title="Ошибка",
                                              description="У вас нет завода сухопутной техники!",
                                              color=0xff0000)
                        await inter.send(embed=embed)

                    else:
                        reach = 0
                        embed = disnake.Embed(title="Ошибка", description="Не хватает некоторых ресурсов!")
                        i = 1
                        for i in range(6):
                            if i == 0 or i == 1:
                                pass
                            else:
                                idf = str(i)
                                res_id = res_data[idf]["id"]
                                res_name = res_data[idf]["name"]

                                res_need = army_data[id]["ResNeed"][res_id] * amount

                                c.execute(f"SELECT {res_id} FROM 'users-data-resources' WHERE id={inter.author.id}")
                                res_inv = c.fetchone()
                                res_inv = res_inv[0]

                                if res_need > res_inv:
                                    embed.add_field(name=res_name, value="Не достаточно!")

                                else:
                                    reach += 1

                        if reach < 4:
                            await inter.send(embed=embed)

                        elif reach == 4:
                            if resid is not None:
                                c.execute(f"SELECT money FROM 'users-data' WHERE id={inter.author.id}")
                                balance = c.fetchone()
                                balance = balance[0]

                            elif resid_org is not None:
                                c.execute(f"SELECT money FROM 'users-data-org' WHERE id={inter.author.id}")
                                balance = c.fetchone()
                                balance = balance[0]

                            if balance < army_data[id]["ResNeed"]["money"] * amount:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="Не достаточно денег!",
                                                      color=0xff0000)
                                embed.add_field(name="Ваш баланс", value=f"${balance:,}")
                                embed.add_field(name="Нужно денег",
                                                value=f"${(army_data[id]['ResNeed']['money'] * amount):,}")
                                embed.add_field(name="Не хватает",
                                                value=f"${((army_data[id]['ResNeed']['money'] * amount) - balance):,}")
                                await inter.send(embed=embed)

                            else:
                                c.execute(f"SELECT {army_id} FROM 'users-data-army' WHERE id={inter.author.id}")
                                army_inv = c.fetchone()
                                army_inv = army_inv[0]

                                c.execute(f"SELECT gold FROM 'users-data-resources' WHERE id={inter.author.id}")
                                gold = c.fetchone()
                                gold = gold[0]

                                c.execute(f"SELECT titanium FROM 'users-data-resources' WHERE id={inter.author.id}")
                                titanium = c.fetchone()
                                titanium = titanium[0]

                                c.execute(f"SELECT uranium FROM 'users-data-resources' WHERE id={inter.author.id}")
                                uranium = c.fetchone()
                                uranium = uranium[0]

                                c.execute(f"SELECT iron FROM 'users-data-resources' WHERE id={inter.author.id}")
                                iron = c.fetchone()
                                iron = iron[0]

                                up_gold = gold - army_data[id]["ResNeed"]["gold"]
                                up_uranium = uranium - army_data[id]["ResNeed"]["uranium"]
                                up_titanium = titanium - army_data[id]["ResNeed"]["titanium"]
                                up_iron = iron - army_data[id]["ResNeed"]["iron"]
                                up_money = balance - army_data[id]["ResNeed"]["money"] * amount
                                up_army = army_inv + amount

                                if resid is not None:
                                    c.execute(f"UPDATE 'users-data' SET money={up_money} WHERE id={inter.author.id}")

                                elif resid_org is not None:
                                    c.execute(
                                        f"UPDATE 'users-data-org' SET money={up_money} WHERE id={inter.author.id}")

                                c.execute(
                                    f"UPDATE 'users-data-resources' SET gold={up_gold} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET titanium={up_titanium} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET uranium={up_uranium} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET iron={up_iron} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-army' SET {army_id}={up_army} WHERE id={inter.author.id}")
                                db.commit()

                                embed = disnake.Embed(title="Успешно",
                                                      description=f"Вы успешно создали {army_name} в количестве {amount:,}!",
                                                      color=0x00ff00)
                                embed.add_field(name=f"Кол-во {army_name}:", value=f"{int(up_army)}", inline=True)
                                await inter.send(embed=embed)

                elif army_type == "air":
                    if aviation_factory == 0:
                        embed = disnake.Embed(title="Ошибка",
                                              description="У вас нет авиационного завода!",
                                              color=0xff0000)
                        await inter.send(embed=embed)

                    else:
                        reach = 0
                        embed = disnake.Embed(title="Ошибка", description="Не хватает некоторых ресурсов!")
                        i = 1
                        for i in range(6):
                            if i == 0 or i == 1:
                                pass
                            else:
                                idf = str(i)
                                res_id = res_data[idf]["id"]
                                res_name = res_data[idf]["name"]

                                res_need = army_data[id]["ResNeed"][res_id] * amount

                                c.execute(f"SELECT {res_id} FROM 'users-data-resources' WHERE id={inter.author.id}")
                                res_inv = c.fetchone()
                                res_inv = res_inv[0]

                                if res_need > res_inv:
                                    embed.add_field(name=res_name, value="Не достаточно!")

                                else:
                                    reach += 1

                        if reach < 4:
                            await inter.send(embed=embed)

                        elif reach == 4:
                            if resid is not None:
                                c.execute(f"SELECT money FROM 'users-data' WHERE id={inter.author.id}")
                                balance = c.fetchone()
                                balance = balance[0]

                            elif resid_org is not None:
                                c.execute(f"SELECT money FROM 'users-data-org' WHERE id={inter.author.id}")
                                balance = c.fetchone()
                                balance = balance[0]

                            if balance < army_data[id]["ResNeed"]["money"] * amount:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="Не достаточно денег!",
                                                      color=0xff0000)
                                embed.add_field(name="Ваш баланс", value=f"${balance:,}")
                                embed.add_field(name="Нужно денег",
                                                value=f"${(army_data[id]['ResNeed']['money'] * amount)}")
                                embed.add_field(name="Не хватает",
                                                value=f"${((army_data[id]['ResNeed']['money'] * amount) - balance):,}")
                                await inter.send(embed=embed)

                            else:
                                c.execute(f"SELECT {army_id} FROM 'users-data-army' WHERE id={inter.author.id}")
                                army_inv = c.fetchone()
                                army_inv = army_inv[0]

                                c.execute(f"SELECT gold FROM 'users-data-resources' WHERE id={inter.author.id}")
                                gold = c.fetchone()
                                gold = gold[0]

                                c.execute(f"SELECT titanium FROM 'users-data-resources' WHERE id={inter.author.id}")
                                titanium = c.fetchone()
                                titanium = titanium[0]

                                c.execute(f"SELECT uranium FROM 'users-data-resources' WHERE id={inter.author.id}")
                                uranium = c.fetchone()
                                uranium = uranium[0]

                                c.execute(f"SELECT iron FROM 'users-data-resources' WHERE id={inter.author.id}")
                                iron = c.fetchone()
                                iron = iron[0]

                                up_gold = gold - army_data[id]["ResNeed"]["gold"]
                                up_uranium = uranium - army_data[id]["ResNeed"]["uranium"]
                                up_titanium = titanium - army_data[id]["ResNeed"]["titanium"]
                                up_iron = iron - army_data[id]["ResNeed"]["iron"]
                                up_money = balance - army_data[id]["ResNeed"]["money"] * amount
                                up_army = army_inv + amount

                                if resid is not None:
                                    c.execute(f"UPDATE 'users-data' SET money={up_money} WHERE id={inter.author.id}")

                                elif resid_org is not None:
                                    c.execute(
                                        f"UPDATE 'users-data-org' SET money={up_money} WHERE id={inter.author.id}")

                                c.execute(
                                    f"UPDATE 'users-data-resources' SET gold={up_gold} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET titanium={up_titanium} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET uranium={up_uranium} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET iron={up_iron} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-army' SET {army_id}={up_army} WHERE id={inter.author.id}")
                                db.commit()

                                embed = disnake.Embed(title="Успешно",
                                                      description=f"Вы успешно создали {army_name} в количестве {amount:,}!",
                                                      color=0x00ff00)
                                embed.add_field(name=f"Кол-во {army_name}:", value=f"{int(up_army)}", inline=True)
                                await inter.send(embed=embed)

                elif army_type == "sea":
                    if shipyard == 0:
                        embed = disnake.Embed(title="Ошибка",
                                              description="У вас нет верфи!",
                                              color=0xff0000)
                        await inter.send(embed=embed)

                    else:
                        reach = 0
                        embed = disnake.Embed(title="Ошибка", description="Не хватает некоторых ресурсов!")
                        i = 1
                        for i in range(6):
                            if i == 0 or i == 1:
                                pass
                            else:
                                idf = str(i)
                                res_id = res_data[idf]["id"]
                                res_name = res_data[idf]["name"]

                                res_need = army_data[id]["ResNeed"][res_id] * amount

                                c.execute(f"SELECT {res_id} FROM 'users-data-resources' WHERE id={inter.author.id}")
                                res_inv = c.fetchone()
                                res_inv = res_inv[0]

                                if res_need > res_inv:
                                    embed.add_field(name=res_name, value="Не достаточно!")

                                else:
                                    reach += 1

                        if reach < 4:
                            await inter.send(embed=embed)

                        elif reach == 4:
                            if resid is not None:
                                c.execute(f"SELECT money FROM 'users-data' WHERE id={inter.author.id}")
                                balance = c.fetchone()
                                balance = balance[0]

                            elif resid_org is not None:
                                c.execute(f"SELECT money FROM 'users-data-org' WHERE id={inter.author.id}")
                                balance = c.fetchone()
                                balance = balance[0]

                            if balance < army_data[id]["ResNeed"]["money"] * amount:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="Не достаточно денег!",
                                                      color=0xff0000)
                                embed.add_field(name="Ваш баланс", value=f"${balance:,}")
                                embed.add_field(name="Нужно денег",
                                                value=f"${(army_data[id]['ResNeed']['money'] * amount):,}")
                                embed.add_field(name="Не хватает",
                                                value=f"${((army_data[id]['ResNeed']['money'] * amount) - balance):,}")
                                await inter.send(embed=embed)

                            else:
                                c.execute(f"SELECT {army_id} FROM 'users-data-army' WHERE id={inter.author.id}")
                                army_inv = c.fetchone()
                                army_inv = army_inv[0]

                                c.execute(f"SELECT gold FROM 'users-data-resources' WHERE id={inter.author.id}")
                                gold = c.fetchone()
                                gold = gold[0]

                                c.execute(f"SELECT titanium FROM 'users-data-resources' WHERE id={inter.author.id}")
                                titanium = c.fetchone()
                                titanium = titanium[0]

                                c.execute(f"SELECT uranium FROM 'users-data-resources' WHERE id={inter.author.id}")
                                uranium = c.fetchone()
                                uranium = uranium[0]

                                c.execute(f"SELECT iron FROM 'users-data-resources' WHERE id={inter.author.id}")
                                iron = c.fetchone()
                                iron = iron[0]

                                up_gold = gold - army_data[id]["ResNeed"]["gold"]
                                up_uranium = uranium - army_data[id]["ResNeed"]["uranium"]
                                up_titanium = titanium - army_data[id]["ResNeed"]["titanium"]
                                up_iron = iron - army_data[id]["ResNeed"]["iron"]
                                up_money = balance - army_data[id]["ResNeed"]["money"] * amount
                                up_army = army_inv + amount

                                if resid is not None:
                                    c.execute(f"UPDATE 'users-data' SET money={up_money} WHERE id={inter.author.id}")

                                elif resid_org is not None:
                                    c.execute(
                                        f"UPDATE 'users-data-org' SET money={up_money} WHERE id={inter.author.id}")

                                c.execute(
                                    f"UPDATE 'users-data-resources' SET gold={up_gold} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET titanium={up_titanium} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET uranium={up_uranium} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET iron={up_iron} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-army' SET {army_id}={up_army} WHERE id={inter.author.id}")
                                db.commit()

                                embed = disnake.Embed(title="Успешно",
                                                      description=f"Вы успешно создали {army_name} в количестве {amount:,}!",
                                                      color=0x00ff00)
                                embed.add_field(name=f"Кол-во {army_name}:", value=f"{int(up_army)}", inline=True)
                                await inter.send(embed=embed)

                elif army_type == "nuke":
                    if nuclear_factory == 0:
                        embed = disnake.Embed(title="Ошибка",
                                              description="У вас нет ядерного завода!",
                                              color=0xff0000)
                        await inter.send(embed=embed)

                    else:
                        reach = 0
                        embed = disnake.Embed(title="Ошибка", description="Не хватает некоторых ресурсов!")
                        i = 1
                        for i in range(6):
                            if i == 0 or i == 1:
                                pass
                            else:
                                idf = str(i)
                                res_id = res_data[idf]["id"]
                                res_name = res_data[idf]["name"]

                                res_need = army_data[id]["ResNeed"][res_id] * amount

                                c.execute(f"SELECT {res_id} FROM 'users-data-resources' WHERE id={inter.author.id}")
                                res_inv = c.fetchone()
                                res_inv = res_inv[0]

                                if res_need > res_inv:
                                    embed.add_field(name=res_name, value="Не достаточно!")

                                else:
                                    reach += 1

                        if reach < 4:
                            await inter.send(embed=embed)

                        elif reach == 4:
                            if resid is not None:
                                c.execute(f"SELECT money FROM 'users-data' WHERE id={inter.author.id}")
                                balance = c.fetchone()
                                balance = balance[0]

                            elif resid_org is not None:
                                c.execute(f"SELECT money FROM 'users-data-org' WHERE id={inter.author.id}")
                                balance = c.fetchone()
                                balance = balance[0]

                            if balance < army_data[id]["ResNeed"]["money"] * amount:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="Не достаточно денег!",
                                                      color=0xff0000)
                                embed.add_field(name="Ваш баланс", value=f"${balance:,}")
                                embed.add_field(name="Нужно денег",
                                                value=f"${(army_data[id]['ResNeed']['money'] * amount):,}")
                                embed.add_field(name="Не хватает",
                                                value=f"${((army_data[id]['ResNeed']['money'] * amount) - balance):,}")
                                await inter.send(embed=embed)

                            else:
                                c.execute(f"SELECT {army_id} FROM 'users-data-army' WHERE id={inter.author.id}")
                                army_inv = c.fetchone()
                                army_inv = army_inv[0]

                                c.execute(f"SELECT gold FROM 'users-data-resources' WHERE id={inter.author.id}")
                                gold = c.fetchone()
                                gold = gold[0]

                                c.execute(f"SELECT titanium FROM 'users-data-resources' WHERE id={inter.author.id}")
                                titanium = c.fetchone()
                                titanium = titanium[0]

                                c.execute(f"SELECT uranium FROM 'users-data-resources' WHERE id={inter.author.id}")
                                uranium = c.fetchone()
                                uranium = uranium[0]

                                c.execute(f"SELECT iron FROM 'users-data-resources' WHERE id={inter.author.id}")
                                iron = c.fetchone()
                                iron = iron[0]

                                up_gold = gold - army_data[id]["ResNeed"]["gold"]
                                up_uranium = uranium - army_data[id]["ResNeed"]["uranium"]
                                up_titanium = titanium - army_data[id]["ResNeed"]["titanium"]
                                up_iron = iron - army_data[id]["ResNeed"]["iron"]
                                up_money = balance - army_data[id]["ResNeed"]["money"] * amount
                                up_army = army_inv + amount

                                if resid is not None:
                                    c.execute(f"UPDATE 'users-data' SET money={up_money} WHERE id={inter.author.id}")

                                elif resid_org is not None:
                                    c.execute(
                                        f"UPDATE 'users-data-org' SET money={up_money} WHERE id={inter.author.id}")

                                c.execute(
                                    f"UPDATE 'users-data-resources' SET gold={up_gold} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET titanium={up_titanium} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET uranium={up_uranium} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET iron={up_iron} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-army' SET {army_id}={up_army} WHERE id={inter.author.id}")
                                db.commit()

                                embed = disnake.Embed(title="Успешно",
                                                      description=f"Вы успешно создали {army_name} в количестве {amount:,}!",
                                                      color=0x00ff00)
                                embed.add_field(name=f"Кол-во {army_name}:", value=f"{int(up_army)}", inline=True)
                                await inter.send(embed=embed)

                elif army_type == "chemical":
                    if chemical_factory == 0:
                        embed = disnake.Embed(title="Ошибка",
                                              description="У вас нет химического завода!",
                                              color=0xff0000)
                        await inter.send(embed=embed)

                    else:
                        reach = 0
                        embed = disnake.Embed(title="Ошибка", description="Не хватает некоторых ресурсов!")
                        i = 1
                        for i in range(6):
                            if i == 0 or i == 1:
                                pass
                            else:
                                idf = str(i)
                                res_id = res_data[idf]["id"]
                                res_name = res_data[idf]["name"]

                                res_need = army_data[id]["ResNeed"][res_id] * amount

                                c.execute(f"SELECT {res_id} FROM 'users-data-resources' WHERE id={inter.author.id}")
                                res_inv = c.fetchone()
                                res_inv = res_inv[0]

                                if res_need > res_inv:
                                    embed.add_field(name=res_name, value="Не достаточно!")

                                else:
                                    reach += 1

                        if reach < 4:
                            await inter.send(embed=embed)

                        elif reach == 4:
                            if resid is not None:
                                c.execute(f"SELECT money FROM 'users-data' WHERE id={inter.author.id}")
                                balance = c.fetchone()
                                balance = balance[0]

                            elif resid_org is not None:
                                c.execute(f"SELECT money FROM 'users-data-org' WHERE id={inter.author.id}")
                                balance = c.fetchone()
                                balance = balance[0]

                            if balance < army_data[id]["ResNeed"]["money"] * amount:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="Не достаточно денег!",
                                                      color=0xff0000)
                                embed.add_field(name="Ваш баланс", value=f"${balance:,}")
                                embed.add_field(name="Нужно денег",
                                                value=f"${(army_data[id]['ResNeed']['money'] * amount):,}")
                                embed.add_field(name="Не хватает",
                                                value=f"${((army_data[id]['ResNeed']['money'] * amount) - balance):,}")
                                await inter.send(embed=embed)

                            else:
                                c.execute(f"SELECT {army_id} FROM 'users-data-army' WHERE id={inter.author.id}")
                                army_inv = c.fetchone()
                                army_inv = army_inv[0]

                                c.execute(f"SELECT gold FROM 'users-data-resources' WHERE id={inter.author.id}")
                                gold = c.fetchone()
                                gold = gold[0]

                                c.execute(f"SELECT titanium FROM 'users-data-resources' WHERE id={inter.author.id}")
                                titanium = c.fetchone()
                                titanium = titanium[0]

                                c.execute(f"SELECT uranium FROM 'users-data-resources' WHERE id={inter.author.id}")
                                uranium = c.fetchone()
                                uranium = uranium[0]

                                c.execute(f"SELECT iron FROM 'users-data-resources' WHERE id={inter.author.id}")
                                iron = c.fetchone()
                                iron = iron[0]

                                up_gold = gold - army_data[id]["ResNeed"]["gold"]
                                up_uranium = uranium - army_data[id]["ResNeed"]["uranium"]
                                up_titanium = titanium - army_data[id]["ResNeed"]["titanium"]
                                up_iron = iron - army_data[id]["ResNeed"]["iron"]
                                up_money = balance - army_data[id]["ResNeed"]["money"] * amount
                                up_army = army_inv + amount

                                if resid is not None:
                                    c.execute(f"UPDATE 'users-data' SET money={up_money} WHERE id={inter.author.id}")

                                elif resid_org is not None:
                                    c.execute(
                                        f"UPDATE 'users-data-org' SET money={up_money} WHERE id={inter.author.id}")

                                c.execute(
                                    f"UPDATE 'users-data-resources' SET gold={up_gold} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET titanium={up_titanium} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET uranium={up_uranium} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-resources' SET iron={up_iron} WHERE id={inter.author.id}")
                                c.execute(
                                    f"UPDATE 'users-data-army' SET {army_id}={up_army} WHERE id={inter.author.id}")
                                db.commit()

                                embed = disnake.Embed(title="Успешно",
                                                      description=f"Вы успешно создали {army_name} в количестве {amount:,}!",
                                                      color=0x00ff00)
                                embed.add_field(name=f"Кол-во {army_name}:", value=f"{int(up_army)}", inline=True)
                                await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command(aliases=["mod"])
async def modify(inter, vehicle_id: str, mod: str, amount: int = 1):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()
    if resid is not None or resid_org is not None:
        with open("ArmyData.json", "r", encoding="utf-8") as f:
            army_data = json.load(f)

        if vehicle_id not in army_data:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы указали неверный ID техники!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            army_id = army_data[vehicle_id]["id"]
            army_cost = army_data[vehicle_id]["Modify"]["Cost"]

            if mod == "def":
                army_id_mod = f"{army_id}_def"

            elif mod == "spd":
                army_id_mod = f"{army_id}_spd"

            elif mod == "dmg":
                army_id_mod = f"{army_id}_dmg"

            else:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали неверную модификацию техники!",
                                      color=0xff0000)
                await inter.send(embed=embed)

            c.execute(f"SELECT {army_id} FROM 'users-data-army' WHERE id={inter.author.id}")
            army_inv = c.fetchone()
            army_inv = army_inv[0]

            try:
                c.execute(f"SELECT {army_id_mod} FROM 'users-data-army-mod' WHERE id={inter.author.id}")
                army_mod_inv = c.fetchone()
                army_mod_inv = army_mod_inv[0]

            except:
                embed = disnake.Embed(title="Ошибка",
                                      description="У данной техники нет такой модификации!",
                                      color=0xff0000)
                await inter.send(embed=embed)
                return

            if army_inv == 0:
                embed = disnake.Embed(title="Ошибка",
                                      description="У вас нет техники для модификации!",
                                      color=0xff0000)
                await inter.send(embed=embed)

            elif army_inv < amount:
                embed = disnake.Embed(title="Ошибка",
                                      description="Не достаточно техники для модификации",
                                      color=0xff0000)
                await inter.send(embed=embed)

            else:
                if resid is not None:
                    c.execute(f"SELECT money FROM 'users-data' WHERE id={inter.author.id}")
                    balance = c.fetchone()
                    balance = balance[0]

                elif resid_org is not None:
                    c.execute(f"SELECT money FROM 'users-data-org' WHERE id={inter.author.id}")
                    balance = c.fetchone()
                    balance = balance[0]

                if balance < army_cost * amount:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Вам не хватает денег для модификации!",
                                          color=0xff0000)
                    embed.add_field(name="Ваш баланс", value=f"${balance:,}")
                    embed.add_field(name="Нужно денег", value=f"${(army_cost * amount):,}")
                    embed.add_field(name="Не хватает", value=f"${(army_cost * amount - balance):,}")
                    await inter.send(embed=embed)

                else:
                    up_balance = balance - army_cost * amount
                    up_army = army_inv - amount
                    up_army_mod = army_mod_inv + amount

                    c.execute(f"UPDATE 'users-data-army' SET {army_id}={up_army} WHERE id={inter.author.id}")
                    c.execute(
                        f"UPDATE 'users-data-army-mod' SET {army_id_mod}={up_army_mod} WHERE id={inter.author.id}")
                    if resid is not None:
                        c.execute(f"UPDATE 'users-data' SET money={up_balance} WHERE id={inter.author.id}")

                    elif resid_org is not None:
                        c.execute(f"UPDATE 'users-data-org' SET money={up_balance} WHERE id={inter.author.id}")

                    db.commit()

                    army_name = army_data[vehicle_id]["Name"]
                    embed = disnake.Embed(title="Успешно",
                                          description=f"Вы успешно модифицироали {army_name} в количестве {amount:,}!",
                                          color=0x00ff00)
                    embed.add_field(name=f"Кол-во {army_name}", value=f"{int(up_army):,}", inline=True)
                    embed.add_field(name=f"Кол-во {army_name} с модификацией {mod}", value=f"{int(up_army_mod):,}",
                                    inline=True)
                    await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command(aliases=["offi"])
@commands.has_permissions(administrator=True)
async def office(inter, member: disnake.Member, action: str, amount: int = 1):
    await BlackListMember(inter)
    await BlackListAdmin(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()

    c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
    resid_user = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
    resid_user_org = c.fetchone()

    if resid_user is not None:
        embed = disnake.Embed(title="Ошибка",
                              description="Пользователь не является организацией!",
                              color=0xff0000)
        await inter.send(embed=embed)

    elif resid_user_org is not None:
        if amount > 99 or amount < 1:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы указали неверное кол-во!",
                                  color=0xff0000)
            await inter.send(embed=embed)
        else:
            c.execute(f"SELECT offices FROM 'users-data-org' WHERE id={member.id}")
            has_off = c.fetchone()
            has_off = has_off[0]

            if action == "add":
                up_off = has_off + amount
                c.execute(f"UPDATE 'users-data-org' SET offices={up_off} WHERE id={member.id}")
                db.commit()

                embed = disnake.Embed(title="Успешно",
                                      description=f"Офис выдан игроку {member.mention} в количестве {amount}!",
                                      color=0x00ff00)
                embed.add_field(name="Кол-во офисов", value=f"{up_off}")
                await inter.send(embed=embed)

            elif action == "remove":
                if has_off == 1:
                    embed = disnake.Embed(title="Ошибка",
                                          description="У пользователя минимальное кол-во офисов!",
                                          color=0xff0000)
                    await inter.send(embed=embed)
                else:
                    if has_off - amount < 1:
                        embed = disnake.Embed(title="Ошибка",
                                              description="У пользователя недостаточно офисов для удаления!",
                                              color=0xff0000)
                        await inter.send(embed=embed)
                    else:
                        up_off = has_off - amount

                        c.execute(f"UPDATE 'users-data-org' SET offices={up_off} WHERE id={member.id}")
                        db.commit()

                        embed = disnake.Embed(title="Успешно",
                                              description=f"Офис удалён у игрока {member.mention} в количестве {amount}!",
                                              color=0x00ff00)
                        embed.add_field(name="Кол-во офисов", value=f"{up_off}")
                        await inter.send(embed=embed)

            else:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали неверное действие!",
                                      color=0xff0000)
                await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Данный пользователь не зарегистрирован!",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


@bot.command(aliases=["areg"])
@commands.has_permissions(administrator=True)
async def admin_register(inter, member: disnake.Member, ctype: str):
    await BlackListMember(inter)
    await BlackListAdmin(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()
    c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
    resid_org = c.fetchone()
    if resid is not None or resid_org is not None:
        embed = disnake.Embed(title="Ошибка",
                              description="Пользователь уже зарегистрирован!",
                              color=0xff0000)
        await inter.send(embed=embed)
        db.close()

    else:
        with open("BannedIDs.json", "r") as f:
            ban_pl_data = json.load(f)

        if str(member.id) in ban_pl_data["list"]:
            embed = disnake.Embed(title="Бан",
                                  description="Регистрация не возможна! Пользователь забанен",
                                  color=0xff0000)
            await inter.send(embed=embed)

        else:
            if ctype == "country":
                c.execute(
                    f"INSERT INTO 'users-data' VALUES ('{member.name}', {member.id}, 0, 10000, 80, 'country', 40, 6000000, 4000000, 2000000)")
                c.execute(
                    f"INSERT INTO 'users-data-army' VALUES ('{member.name}', {member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-army-mod' VALUES ('{member.name}', {member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-infra' VALUES ('{member.name}', {member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-lctime' VALUES ('{member.name}', {member.id}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())})")
                c.execute(
                    f"INSERT INTO 'users-data-resdots' VALUES ('{member.name}', {member.id}, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-resources' VALUES ('{member.name}', {member.id}, 0, 0, 0, 0, 0, 0)")
                db.commit()

                embed = disnake.Embed(title="Успешно",
                                      description="Пользователь успешно зарегестрировался как страна!",
                                      color=0x00ff00)
                await inter.send(embed=embed)

                print(f"[{member.name} | {member.id}] $ registered as a country")

            elif ctype == "separatist":
                c.execute(
                    f"INSERT INTO 'users-data' VALUES ('{member.name}', {member.id}, 0, 9000, 70, 'separatist', 40, 6000000, 4000000, 2500000)")
                c.execute(
                    f"INSERT INTO 'users-data-army' VALUES ('{member.name}', {member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-army-mod' VALUES ('{member.name}', {member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-infra' VALUES ('{member.name}', {member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-lctime' VALUES ('{member.name}', {member.id}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())})")
                c.execute(
                    f"INSERT INTO 'users-data-resdots' VALUES ('{member.name}', {member.id}, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-resources' VALUES ('{member.name}', {member.id}, 0, 0, 0, 0, 0, 0)")
                db.commit()

                embed = disnake.Embed(title="Успешно",
                                      description="Пользователь успешно зарегестрировался как сепаратист!",
                                      color=0x00ff00)
                await inter.send(embed=embed)

                print(f"[{member.name} | {member.id}] $ registered as a separatist")

            elif ctype == "organization":
                c.execute(
                    f"INSERT INTO 'users-data-org' VALUES ('{member.name}', {member.id}, 0, 10, 'organization', 5000000, 1000000, 50000, 4000000, 1)")
                c.execute(
                    f"INSERT INTO 'users-data-army' VALUES ('{member.name}', {member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-army-mod' VALUES ('{member.name}', {member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-infra' VALUES ('{member.name}', {member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-lctime' VALUES ('{member.name}', {member.id}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())}, {int(t.time())})")
                c.execute(
                    f"INSERT INTO 'users-data-resdots' VALUES ('{member.name}', {member.id}, 0, 0, 0, 0, 0)")
                c.execute(
                    f"INSERT INTO 'users-data-resources' VALUES ('{inter.author.name}', {inter.author.id}, 0, 0, 0, 0, 0, 0)")
                db.commit()

                embed = disnake.Embed(title="Успешно",
                                      description="Пользователь успешно зарегестрировался как организация!",
                                      color=0x00ff00)
                await inter.send(embed=embed)

                print(f"[{member.name} | {member.id}] $ registered as a organization")

            elif ctype is None:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы не указали тип государства! Доступные типы государства: country, organization, separatist",
                                      color=0xff0000)
                await inter.send(embed=embed)

            else:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали неверный тип государства! Доступные типы государства: country, organization, separatist",
                                      color=0xff0000)
                await inter.send(embed=embed)

        db.close()


@bot.command(aliases=["priv"])
async def privileges(inter):
    await BlackListMember(inter)

    with open("VIPUsers.json", "r") as f:
        vip_data = json.load(f)

    with open("PremiumUsers.json", "r") as f:
        premium_data = json.load(f)

    if str(inter.author.id) not in premium_data["list"]:
        prem_tf = "Нет"

    else:
        prem_tf = "Да"

    if str(inter.author.id) not in vip_data["list"]:
        vip_tf = "Нет"

    else:
        vip_tf = "Да"

    embed = disnake.Embed(title="Ваши привилегии")
    embed.add_field(name="Premium", value=f"{prem_tf}")
    embed.add_field(name="VIP", value=f"{vip_tf}")

    await inter.send(embed=embed)


@bot.command(aliases=["logch", "logc"])
async def log_channel(inter, action, channelf: disnake.TextChannel):
    await BlackListMember(inter)

    if inter.author == inter.guild.owner:
        with open("LogChannels.json", "r") as f:
            log_data = json.load(f)

        if action == "add":
            if str(channelf.id) in log_data["list"]:
                embed = disnake.Embed(title="Ошибка",
                                      description="Канал уже добавлен",
                                      color=0xff0000)
                await inter.send(embed=embed)

            else:
                log_data["list"].append(str(channelf.id))

                with open("LogChannels.json", "w") as f:
                    json.dump(log_data, f, indent=4)

                embed = disnake.Embed(title="Успешно",
                                      description="Канал добавлен в список!",
                                      color=0x00ff00)
                await inter.send(embed=embed)

        elif action == "remove":
            if str(channelf.id) not in log_data["list"]:
                embed = disnake.Embed(title="Ошибка",
                                      description="Канала нет в списке",
                                      color=0xff0000)
                await inter.send(embed=embed)

            else:
                del log_data["list"][str(channelf.id)]

                with open("LogChannels.json", "w") as f:
                    json.dump(log_data, f, indent=4)

                embed = disnake.Embed(title="Успешно",
                                      description="Канал удалён со списка",
                                      color=0x00ff00)
                await inter.send(embed=embed)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы указали не верное действие",
                                  color=0xff0000)
            await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не являетесь владельцем сервера",
                              color=0xff0000)
        await inter.send(embed=embed)


@bot.command()
async def mine_all(inter):
    await BlackListMember(inter)

    db = sqlite3.connect('CescallBotDB.db')
    c = db.cursor()

    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
    resid = c.fetchone()

    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
    resid_org = c.fetchone()

    if resid is not None or resid_org is not None:
        with open("ResData.json", "r", encoding="utf-8") as f:
            res_data = json.load(f)

        resources_collected = {}

        for id, res_info in res_data.items():
            if id != "6":  # Skip the "6" resource (building materials)
                res_id = res_info["id"]

                c.execute(f"SELECT {res_id} FROM 'users-data-resdots' WHERE id={inter.author.id}")
                res_dot = c.fetchone()[0]

                if res_dot > 0:
                    c.execute(f"SELECT {res_id} FROM 'users-data-lctime' WHERE id={inter.author.id}")
                    res_lctime = c.fetchone()[0]

                    min_coll = res_info["min"]
                    max_coll = res_info["max"]

                    res_coll = rdi(min_coll, max_coll) * res_dot

                    time_passed = int(t.time()) - res_lctime

                    if time_passed >= 3600:
                        c.execute(f"SELECT {res_id} FROM 'users-data-resources' WHERE id={inter.author.id}")
                        res_inv = c.fetchone()[0]
                        up_res_inv = res_inv + res_coll

                        c.execute(f"UPDATE 'users-data-resources' SET {res_id}=? WHERE id=?", (up_res_inv, inter.author.id))
                        c.execute(f"UPDATE 'users-data-lctime' SET {res_id}={int(t.time())} WHERE id={inter.author.id}")
                        db.commit()

                        resources_collected[res_info["name"]] = int(res_coll)

        if resources_collected:
            embed = disnake.Embed(title="Успешно", description="Вы успешно собрали следующие ресурсы:", color=0x00ff00)
            for res_name, res_coll in resources_collected.items():
                embed.add_field(name=res_name, value=f"{res_coll:,}", inline=True)
            await inter.send(embed=embed)
        else:
            embed = disnake.Embed(title="Ошибка", description="У вас нет доступных ресурсов для сбора", color=0xff0000)
            await inter.send(embed=embed)

    else:
        embed = disnake.Embed(title="Ошибка",
                              description="Вы не зарегистрированы! Для регистрации на сервере используйте команду $reg <type>",
                              color=0xff0000)
        await inter.send(embed=embed)

    db.close()


bot.run(config["TOKEN"])
