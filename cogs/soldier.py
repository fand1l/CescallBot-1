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

class SoldierCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="call", description="Команда для призыва войск")
    async def call(self, inter: disnake.ApplicationCommandInteraction, amount: int = 1):
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
                await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

                    else:
                        if balance < amount * 200:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="Недостаточно денег для призыва!",
                                                  color=0xff0000)
                            embed.add_field(name="Ваш баланс", value=f"${balance:,}")
                            embed.add_field(name="Нужно для призыва", value=f"${(amount * 200):,}")
                            embed.add_field(name="Не хватает", value=f"${((amount * 200) - balance):,}")
                            await inter.send(embed=embed, ephemeral=True)

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
                            await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

                    else:
                        if amount > max_peoples_for_call:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У вас недостаточно людей для призыва!",
                                                  color=0xff0000)
                            embed.add_field(name="Доступно для призыва:", value=f"{max_peoples_for_call:,} человек")
                            await inter.send(embed=embed, ephemeral=True)

                        else:
                            if balance < amount * 200:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="Недостаточно денег для призыва!",
                                                      color=0xff0000)
                                embed.add_field(name="Ваш баланс", value=f"${balance:,}")
                                embed.add_field(name="Нужно для призыва", value=f"${(amount * 5000):,}")
                                embed.add_field(name="Не хватает", value=f"${((amount * 5000) - balance):,}")
                                await inter.send(embed=embed, ephemeral=True)

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
                                await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()

    @commands.slash_command(name="mobilization", description="Команда для мобилизации населения")
    async def mobilization(self, inter: disnake.ApplicationCommandInteraction):
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
                await inter.send(embed=embed, ephemeral=True)

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
                    await inter.send(embed=embed, ephemeral=True)

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
                await inter.send(embed=embed, ephemeral=True)

        elif resid_org is not None:
            embed = disnake.Embed(title="Ошибка",
                                  description="Данная команда не доступна для организации",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()

    @commands.slash_command(name="disband", description="Команда для розпуска армии")
    async def disband(self, inter: disnake.ApplicationCommandInteraction, amount: int = 1):
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
                await inter.send(embed=embed, ephemeral=True)

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
                    await inter.send(embed=embed, ephemeral=True)

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
                    await inter.send(embed=embed, ephemeral=True)

        elif resid_org is not None:
            if amount <= 0:
                embed = disnake.Embed(title="Ошибка",
                                      description="Указано неверное кол-во солдат!",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

            else:
                c.execute(f"SELECT solider FROM 'users-data-army' WHERE id={inter.author.id}")
                soldier = c.fetchone()
                soldier = soldier[0]

                if amount < soldier:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Недостаточно солдат!",
                                          color=0xff0000)
                    embed.add_field(name="Кол-во солдат", value=f"{soldier:,} солдат")
                    await inter.send(embed=embed, ephemeral=True)

                else:
                    up_soldier = soldier - amount

                    c.execute(f"UPDATE 'users-data-army' SET solider={up_soldier} WHERE id={inter.author.id}")
                    db.commit()

                    embed = disnake.Embed(title="Успешно",
                                          description="Вы успешно распустили солдат!",
                                          color=0x00ff00)
                    embed.add_field(name="Кол-во солдат", value=f"{up_soldier:,} солдат", inline=True)
                    await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


def setup(bot: commands.Bot):
    print("SoldierCommands is loaded")
    bot.add_cog(SoldierCommands(bot))
