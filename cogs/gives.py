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

class GiveCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    types = commands.option_enum({"Техника": "V", "Ресурсы": "R"})

    @commands.slash_command(name="pay", description="Команда для передачи денег другому игроку")
    async def pay(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, amount: int):
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
                        await inter.send(embed=embed, ephemeral=True)

                    else:
                        if amount <= 0:
                            embed = disnake.Embed(title="Ошибка",
                                              description=f"Вы указали неверную сумму!",
                                              color=0xff0000)
                            await inter.send(embed=embed, ephemeral=True)

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

                            await inter.send(embed=embed, ephemeral=True)

            else:
                embed = disnake.Embed(title="Ошибка",
                                      description="Данный пользователь не зарегистрирован!",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


    @commands.slash_command(name="give", description="Команда для передачи предметов другому игроку")
    async def give(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, typef: types, amount: int, id: str, modification: str = None):
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
                await inter.send(embed=embed, ephemeral=True)

            else:
                item_name_id = army_data[id]["id"]
                if modification is not None:
                    c.execute(f"SELECT id FROM 'users-data' WHERE id={inter.author.id}")
                    resid = c.fetchone()

                    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={inter.author.id}")
                    resid_org = c.fetchone()

                    c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
                    resid_user = c.fetchone()

                    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
                    resid_user_org = c.fetchone()

                    if resid is not None or resid_org is not None:
                        if modification == "def":
                            item_name_id = item_name_id + "_def"
                            try:
                                c.execute(
                                    f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={inter.author.id}")
                                item = c.fetchone()
                                item = item[0]

                            except sqlite3.OperationalError:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="У данного предмета нет этой модификации!",
                                                      color=0xff0000)
                                await inter.send(embed=embed, ephemeral=True)
                                return

                        elif modification == "spd":
                            item_name_id = item_name_id + "_spd"
                            try:
                                c.execute(
                                    f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={inter.author.id}")
                                item = c.fetchone()
                                item = item[0]

                            except sqlite3.OperationalError:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="У данного предмета нет этой модификации!",
                                                      color=0xff0000)
                                await inter.send(embed=embed, ephemeral=True)
                                return

                        elif modification == "dmg":
                            item_name_id = item_name_id + "_dmg"
                            try:
                                c.execute(
                                    f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={inter.author.id}")
                                item = c.fetchone()
                                item = item[0]

                            except sqlite3.OperationalError:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="У данного предмета нет этой модификации!",
                                                      color=0xff0000)
                                await inter.send(embed=embed, ephemeral=True)
                                return

                        else:
                            embed = disnake.Embed(title="Ошибка", description="Вы указали неверную модификацию!",
                                                  color=0xff0000)
                            await inter.send(embed=embed, ephemeral=True)
                            return

                        if resid_user is not None or resid_user_org is not None:
                            c.execute(f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={member.id}")
                            item_user = c.fetchone()
                            item_user = item_user[0]

                            if amount <= 0:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="Вы указали неверную сумму для передачи!",
                                                      color=0xff0000)
                                await inter.send(embed=embed, ephemeral=True)

                            else:
                                if amount > item:
                                    embed = disnake.Embed(title="Ошибка",
                                                          description="Недостаточно пердметов для передачи!",
                                                          color=0xff0000)
                                    await inter.send(embed=embed, ephemeral=True)

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
                                                          description=f"Вы передали пользователю {member.mention} {amount:,} {item_name} с модификацией {modification}!",
                                                          color=0x00ff00)
                                    await inter.send(embed=embed, ephemeral=True)

                        else:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="Данный пользователь не зарегистрирован!",
                                                  color=0xff0000)
                            await inter.send(embed=embed, ephemeral=True)

                    else:
                        embed = disnake.Embed(title="Ошибка",
                                              description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                              color=0xff0000)
                        await inter.send(embed=embed, ephemeral=True)

                elif modification is None:
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
                                await inter.send(embed=embed, ephemeral=True)

                            else:
                                if amount > item:
                                    embed = disnake.Embed(title="Ошибка",
                                                          description="Недостаточно пердметов для передачи!",
                                                          color=0xff0000)
                                    await inter.send(embed=embed, ephemeral=True)

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
                                    await inter.send(embed=embed, ephemeral=True)

                        else:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="Данный пользователь не зарегистрирован!",
                                                  color=0xff0000)
                            await inter.send(embed=embed, ephemeral=True)

                    else:
                        embed = disnake.Embed(title="Ошибка",
                                              description="Вы не зарегистрированы! Для регистрации на сервере используйте команду $reg <type>",
                                              color=0xff0000)
                        await inter.send(embed=embed, ephemeral=True)

        elif typef == "R" or typef == "r":
            with open("ResData.json", "r", encoding="utf-8") as f:
                res_data = json.load(f)

            if id not in res_data:
                embed = disnake.Embed(title="Ошибка",
                                      description="Такого ресурса не существует!",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

            else:
                if modification is not None:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Модификации не доступны для ресурсов!",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

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
                                await inter.send(embed=embed, ephemeral=True)

                            else:
                                if amount > item:
                                    embed = disnake.Embed(title="Ошибка",
                                                          description="Недостаточно пердметов для передачи!",
                                                          color=0xff0000)
                                    await inter.send(embed=embed, ephemeral=True)

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
                                    await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы ввели неверный вид!",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()



def setup(bot: commands.Bot):
    print("GiveCommands is loaded")
    bot.add_cog(GiveCommands(bot))