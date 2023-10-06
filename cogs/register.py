import disnake
from disnake.ext import commands
import sqlite3
import json
import time as t

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

class RegisterCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    ctype_ch = commands.option_enum(["country", "organization", "separatist"])

    @commands.slash_command()
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        """Получить текущую задержку бота."""
        await inter.response.send_message(f"Понг! {round(self.bot.latency * 1000)}мс")
        
    @commands.command()
    async def test(inter):
        await inter.send("test")


    @commands.slash_command(name="register", description="Команда для регистрации в базе данных бота")
    async def register(self, inter: disnake.ApplicationCommandInteraction, ctype: ctype_ch):
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
            await inter.send(embed=embed, ephemeral=True)
            db.close()

        else:
            with open("BannedIDs.json", "r") as f:
                ban_pl_data = json.load(f)

            if str(inter.author.id) in ban_pl_data["list"]:
                embed = disnake.Embed(title="Бан",
                                      description="Регистрация не возможна! Вы забанены",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

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
                    await inter.send(embed=embed, ephemeral=True)

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
                    await inter.send(embed=embed, ephemeral=True)

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
                    await inter.send(embed=embed, ephemeral=True)

                    print(f"[{inter.author.name} | {inter.author.id}] $ registered as a organization")

                elif ctype is None:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Вы не указали тип государства! Доступные типы государства: country, organization, separatist",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

                else:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Вы указали неверный тип государства! Доступные типы государства: country, organization, separatist",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

            db.close()

    @commands.slash_command(name="unregister", description="Команда для удаления аккаунта в базе данных бота")
    async def unregister(self, inter: disnake.ApplicationCommandInteraction):
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
            await inter.send(embed=embed, ephemeral=True)

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
            await inter.send(embed=embed, ephemeral=True)

            print(f"[{inter.author.name} | {inter.author.id}] $ unregistered")

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


def setup(bot: commands.Bot):
    print("RegisterCommands is loaded")
    bot.add_cog(RegisterCommands(bot))
