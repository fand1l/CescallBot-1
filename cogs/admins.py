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

class AdminCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    actions = commands.option_enum({
        "Добавить": "add",
        "Удалить": "remove"
    })

    dots = commands.option_enum({
        "Газ": "1",
        "Золото": "2",
        "Уран": "3",
        "Титан": "4",
        "Железо": "5"
    })

    types = commands.option_enum({"Техника": "V", "Ресурсы": "R"})

    infras = commands.option_enum({
        "Дом": "1",
        "Многоэтажний Дом": "2",
        "Сеть Продуктовых Магазинов": "3",
        "Сеть Магазинов Электронники": "4",
        "Сеть Автосалонов": "5",
        "IT Компании": "6",
        "Сеть Военных Магазинов": "7",
        "Сеть Строительних Компаний": "8",
        "Сеть Больниц": "9",
        "Завод Сухопутной Техники": "10",
        "Авиационный Завод": "11",
        "Верфь": "12",
        "Ядерный завод": "13",
        "Химический завод": "14"

    })

    ctype_ch = commands.option_enum(["country", "organization", "separatist"])

    @commands.slash_command(name="dot", description="Команда для выдачи точек с ресурсами")
    @commands.has_permissions(administrator=True)
    async def dot(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, action: actions, dot: dots):
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
                await inter.send(embed=embed, ephemeral=True)

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
                    await inter.send(embed=embed, ephemeral=True)

                    with open("LogChannels.json", "r") as f:
                        log_channels_data = json.load(f)

                    for channel_id in log_channels_data["list"]:
                        channel_id = int(channel_id)
                        channelf = self.bot.get_channel(channel_id)
                        embed = disnake.Embed(title="Точки с ресурсами")
                        embed.add_field(name="Действие", value="Добавление")
                        embed.add_field(name="Ресурс", value=f"{dot_name}")
                        embed.add_field(name="Участник", value=f"{member.mention}")
                        embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                        await channelf.send(embed=embed)

                elif action == "remove":
                    if need_dot == 0:
                        embed = disnake.Embed(title="Ошибка",
                                              description="У пользователя минимальное кол-во точек!",
                                              color=0xff0000)
                        await inter.send(embed=embed, ephemeral=True)
                    else:
                        up_dot = need_dot - 1

                        c.execute(f"UPDATE 'users-data-resdots' SET {dot_dbid}={up_dot} WHERE id={member.id}")
                        db.commit()

                        embed = disnake.Embed(title="Успешно",
                                              description=f"Точка {dot_name} забрана у игрока {member.mention}!",
                                              color=0x00ff00)
                        embed.add_field(name="Кол-во точек", value=f"{dot_name}: {up_dot}")
                        await inter.send(embed=embed, ephemeral=True)

                        with open("LogChannels.json", "r") as f:
                            log_channels_data = json.load(f)

                        for channel_id in log_channels_data["list"]:
                            channel_id = int(channel_id)
                            channelf = self.bot.get_channel(channel_id)
                            embed = disnake.Embed(title="Точки с ресурсами")
                            embed.add_field(name="Действие", value="Удаление")
                            embed.add_field(name="Ресурс", value=f"{dot_name}")
                            embed.add_field(name="Участник", value=f"{member.mention}")
                            embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                            await channelf.send(embed=embed)

                else:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Вы указали неверное действие!",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Данный пользователь не зарегистрирован!",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


    @commands.slash_command(name="money", description="Команда для выдачи денег игроку")
    @commands.has_permissions(administrator=True)
    async def money(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, amount: int = 0):
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
            await inter.send(embed=embed, ephemeral=True)
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
                await inter.send(embed=embed, ephemeral=True)

                with open("LogChannels.json", "r") as f:
                    log_channels_data = json.load(f)

                for channel_id in log_channels_data["list"]:
                    channel_id = int(channel_id)
                    channelf = self.bot.get_channel(channel_id)
                    embed = disnake.Embed(title="Деньги")
                    embed.add_field(name="Действие", value="Добавление")
                    embed.add_field(name="Кол-во", value=f"{amount}")
                    embed.add_field(name="Участник", value=f"{member.mention}")
                    embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                    await channelf.send(embed=embed)

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
                await inter.send(embed=embed, ephemeral=True)

                with open("LogChannels.json", "r") as f:
                    log_channels_data = json.load(f)

                for channel_id in log_channels_data["list"]:
                    channel_id = int(channel_id)
                    channelf = self.bot.get_channel(channel_id)
                    embed = disnake.Embed(title="Деньги")
                    embed.add_field(name="Действие", value="Добавление")
                    embed.add_field(name="Кол-во", value=f"{amount}")
                    embed.add_field(name="Участник", value=f"{member.mention}")
                    embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                    await channelf.send(embed=embed)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Данный пользователь не зарегистрирован!",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


    @commands.slash_command(name="item", description="Команда для выдачи предметов игроку")
    @commands.has_permissions(administrator=True)
    async def item(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, typef: types, amount: int, id: str, modification: str = None):
        await BlackListMember(inter)
        await BlackListAdmin(inter)

        db = sqlite3.connect('CescallBotDB.db')
        c = db.cursor()
        if amount > 9999999999 or amount < -9999999999:
            embed = disnake.Embed(title="Ошибка",
                                  description="Указана неверное кол-во",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)
            return
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
                    c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
                    resid_user = c.fetchone()

                    c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
                    resid_user_org = c.fetchone()

                    if resid_user is not None or resid_user_org is not None:
                        if modification == "def":
                            item_name_id = item_name_id + "_def"
                            try:
                                c.execute(f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={member.id}")
                                item_user = c.fetchone()
                                item_user = item_user[0]

                            except sqlite3.OperationalError:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="У данного предмета нет этой модификации!",
                                                      color=0xff0000)
                                await inter.send(embed=embed, ephemeral=True)
                                return

                        elif modification == "spd":
                            item_name_id = item_name_id + "_spd"
                            try:
                                c.execute(f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={member.id}")
                                item_user = c.fetchone()
                                item_user = item_user[0]

                            except sqlite3.OperationalError:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="У данного предмета нет этой модификации!",
                                                      color=0xff0000)
                                await inter.send(embed=embed, ephemeral=True)
                                return

                        elif modification == "dmg":
                            item_name_id = item_name_id + "_dmg"
                            try:
                                c.execute(f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={member.id}")
                                item_user = c.fetchone()
                                item_user = item_user[0]

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

                        c.execute(f"SELECT {item_name_id} FROM 'users-data-army-mod' WHERE id={member.id}")
                        item_user = c.fetchone()
                        item_user = item_user[0]

                        up_item_user = item_user + amount

                        c.execute(
                            f"UPDATE 'users-data-army-mod' SET {item_name_id}={up_item_user} WHERE id={member.id}")
                        db.commit()

                        item_name = army_data[id]["Name"]
                        embed = disnake.Embed(title="Успешно",
                                              description=f"Вы выдали пользователю {member.mention} {amount:,} {item_name} с модификацией {modification}!",
                                              color=0x00ff00)
                        await inter.send(embed=embed, ephemeral=True)

                        with open("LogChannels.json", "r") as f:
                            log_channels_data = json.load(f)

                        for channel_id in log_channels_data["list"]:
                            channel_id = int(channel_id)
                            channelf = self.bot.get_channel(channel_id)
                            embed = disnake.Embed(title="Техника")
                            embed.add_field(name="Техника", value=f"{item_name} {modification}")
                            embed.add_field(name="Кол-во", value=f"{amount}")
                            embed.add_field(name="Участник", value=f"{member.mention}")
                            embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                            await channelf.send(embed=embed)

                    else:
                        embed = disnake.Embed(title="Ошибка",
                                              description="Данный пользователь не зарегистрирован!",
                                              color=0xff0000)
                        await inter.send(embed=embed, ephemeral=True)

                elif modification is None:
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
                        await inter.send(embed=embed, ephemeral=True)

                        with open("LogChannels.json", "r") as f:
                            log_channels_data = json.load(f)

                        for channel_id in log_channels_data["list"]:
                            channel_id = int(channel_id)
                            channelf = self.bot.get_channel(channel_id)
                            embed = disnake.Embed(title="Техника")
                            embed.add_field(name="Техника", value=f"{item_name}")
                            embed.add_field(name="Кол-во", value=f"{amount}")
                            embed.add_field(name="Участник", value=f"{member.mention}")
                            embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                            await channelf.send(embed=embed)

                    else:
                        embed = disnake.Embed(title="Ошибка",
                                              description="Данный пользователь не зарегистрирован!",
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

                        c.execute(
                            f"UPDATE 'users-data-resources' SET {item_name_id}={up_item_user} WHERE id={member.id}")
                        db.commit()

                        item_name = res_data[id]["name"]
                        embed = disnake.Embed(title="Успешно",
                                              description=f"Вы выдали пользователю {member.mention} {amount:,} {item_name}!",
                                              color=0x00ff00)
                        await inter.send(embed=embed, ephemeral=True)

                        with open("LogChannels.json", "r") as f:
                            log_channels_data = json.load(f)

                        for channel_id in log_channels_data["list"]:
                            channel_id = int(channel_id)
                            channelf = self.bot.get_channel(channel_id)
                            embed = disnake.Embed(title="Ресурсы")
                            embed.add_field(name="Ресурс", value=f"{item_name}")
                            embed.add_field(name="Кол-во", value=f"{amount}")
                            embed.add_field(name="Участник", value=f"{member.mention}")
                            embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                            await channelf.send(embed=embed)

                    else:
                        embed = disnake.Embed(title="Ошибка",
                                              description="Данный пользователь не зарегистрирован!",
                                              color=0xff0000)
                        await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы ввели неверный вид!",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


    @commands.slash_command(name="construction", description="Команда для выдачи инфраструктуры игроку")
    @commands.has_permissions(administrator=True)
    async def construction(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, action: actions, id: infras):
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
                await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

                    else:
                        up_build = infra_inv + 1

                        c.execute(f"UPDATE 'users-data-infra' SET {infra_id}={up_build} WHERE id={member.id}")
                        db.commit()

                        embed = disnake.Embed(title="Успешно",
                                              description=f"Вы успешно построили {infra_name}",
                                              color=0x00ff00)
                        embed.add_field(name=f"Кол-во {infra_name}:", value=f"{int(up_build):,}", inline=True)
                        await inter.send(embed=embed, ephemeral=True)

                        with open("LogChannels.json", "r") as f:
                            log_channels_data = json.load(f)

                        for channel_id in log_channels_data["list"]:
                            channel_id = int(channel_id)
                            channelf = self.bot.get_channel(channel_id)
                            embed = disnake.Embed(title="Инфраструктура")
                            embed.add_field(name="Действие", value="Добавление")
                            embed.add_field(name="Инфраструктура", value=f"{infra_name}")
                            embed.add_field(name="Участник", value=f"{member.mention}")
                            embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                            await channelf.send(embed=embed)

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
                        await inter.send(embed=embed, ephemeral=True)

                    else:
                        up_build = infra_inv - 1

                        c.execute(f"UPDATE 'users-data-infra' SET {infra_id}={up_build} WHERE id={member.id}")
                        db.commit()

                        embed = disnake.Embed(title="Успешно",
                                              description=f"Вы успешно уничтожили {infra_name}",
                                              color=0x00ff00)
                        embed.add_field(name=f"Кол-во {infra_name}:", value=f"{int(up_build):,}", inline=True)
                        await inter.send(embed=embed, ephemeral=True)

                        with open("LogChannels.json", "r") as f:
                            log_channels_data = json.load(f)

                        for channel_id in log_channels_data["list"]:
                            channel_id = int(channel_id)
                            channelf = self.bot.get_channel(channel_id)
                            embed = disnake.Embed(title="Инфраструктура")
                            embed.add_field(name="Действие", value="Удаление")
                            embed.add_field(name="Инфраструктура", value=f"{infra_name}")
                            embed.add_field(name="Участник", value=f"{member.mention}")
                            embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                            await channelf.send(embed=embed)

                else:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Вы указали неверное действие",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Данный пользователь не зарегистрирован!",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


    @commands.slash_command(name="soldier", description="Команда для выдачи солдат")
    @commands.has_permissions(administrator=True)
    async def soldier(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, amount: int):
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
            await inter.send(embed=embed, ephemeral=True)
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
            await inter.send(embed=embed, ephemeral=True)

            with open("LogChannels.json", "r") as f:
                log_channels_data = json.load(f)

            for channel_id in log_channels_data["list"]:
                channel_id = int(channel_id)
                channelf = self.bot.get_channel(channel_id)
                embed = disnake.Embed(title="Солдаты")
                embed.add_field(name="Кол-во", value=f"{amount}")
                embed.add_field(name="Участник", value=f"{member.mention}")
                embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                await channelf.send(embed=embed)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Данный пользователь не зарегистрирован!",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()

    @commands.slash_command(name="admin_unregister", description="Команда для удаления аккаунта пользователя")
    @commands.has_permissions(administrator=True)
    async def admin_unregister(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        await BlackListMember(inter)
        await BlackListAdmin(inter)

        db = sqlite3.connect('CescallBotDB.db')
        c = db.cursor()
        c.execute(f"SELECT id FROM 'users-data' WHERE id={member.id}")
        resid = c.fetchone()

        c.execute(f"SELECT id FROM 'users-data-org' WHERE id={member.id}")
        resid_org = c.fetchone()

        if resid is not None:
            c.execute(f"DELETE FROM 'users-data' WHERE id={member.id}")
            c.execute(f"DELETE FROM 'users-data-army' WHERE id={member.id}")
            c.execute(f"DELETE FROM 'users-data-army-mod' WHERE id={member.id}")
            c.execute(f"DELETE FROM 'users-data-infra' WHERE id={member.id}")
            c.execute(f"DELETE FROM 'users-data-lctime' WHERE id={member.id}")
            c.execute(f"DELETE FROM 'users-data-resdots' WHERE id={member.id}")
            c.execute(f"DELETE FROM 'users-data-resources' WHERE id={member.id}")
            db.commit()

            embed = disnake.Embed(title="Успешно",
                                  description="Учетная запись успешно удалена!",
                                  color=0x00ff00)
            await inter.send(embed=embed)

            with open("LogChannels.json", "r") as f:
                log_channels_data = json.load(f)

            for channel_id in log_channels_data["list"]:
                channel_id = int(channel_id)
                channelf = self.bot.get_channel(channel_id)
                embed = disnake.Embed(title="Аккаунты")
                embed.add_field(name="Действие", value="Удаление аккаунта")
                embed.add_field(name="Участник", value=f"{member.mention}")
                embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                await channelf.send(embed=embed)

            print(f"[{inter.author.name} | {inter.author.id}] $ unregistered")

        elif resid_org is not None:
            c.execute(f"DELETE FROM 'users-data-org' WHERE id={member.id}")
            c.execute(f"DELETE FROM 'users-data-army' WHERE id={member.id}")
            c.execute(f"DELETE FROM 'users-data-army-mod' WHERE id={member.id}")
            c.execute(f"DELETE FROM 'users-data-infra' WHERE id={member.id}")
            c.execute(f"DELETE FROM 'users-data-lctime' WHERE id={member.id}")
            c.execute(f"DELETE FROM 'users-data-resdots' WHERE id={member.id}")
            c.execute(f"DELETE FROM 'users-data-resources' WHERE id={member.id}")
            db.commit()

            embed = disnake.Embed(title="Успешно",
                                  description="Учетная запись успешно удалена!",
                                  color=0x00ff00)
            await inter.send(embed=embed)

            with open("LogChannels.json", "r") as f:
                log_channels_data = json.load(f)

            for channel_id in log_channels_data["list"]:
                channel_id = int(channel_id)
                channelf = self.bot.get_channel(channel_id)
                embed = disnake.Embed(title="Аккаунты")
                embed.add_field(name="Действие", value="Удаление аккаунта")
                embed.add_field(name="Участник", value=f"{member.mention}")
                embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                await channelf.send(embed=embed)

            print(f"[{member.name} | {member.id}] $ unregistered")

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Пользователь не зарегестрирован!",
                                  color=0xff0000)
            await inter.send(embed=embed)

        db.close()

    @commands.slash_command(name="office", description="Команда для выдачи офисов игроку")
    @commands.has_permissions(administrator=True)
    async def office(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, action: actions, amount: int = 1):
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
            await inter.send(embed=embed, ephemeral=True)

        elif resid_user_org is not None:
            if amount > 99 or amount < 1:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали неверное кол-во!",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)
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
                    await inter.send(embed=embed, ephemeral=True)

                    with open("LogChannels.json", "r") as f:
                        log_channels_data = json.load(f)

                    for channel_id in log_channels_data["list"]:
                        channel_id = int(channel_id)
                        channelf = self.bot.get_channel(channel_id)
                        embed = disnake.Embed(title="Офисы")
                        embed.add_field(name="Действие", value="Добавление")
                        embed.add_field(name="Кол-во", value=f"{amount}")
                        embed.add_field(name="Участник", value=f"{member.mention}")
                        embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                        await channelf.send(embed=embed)

                elif action == "remove":
                    if has_off == 1:
                        embed = disnake.Embed(title="Ошибка",
                                              description="У пользователя минимальное кол-во офисов!",
                                              color=0xff0000)
                        await inter.send(embed=embed, ephemeral=True)
                    else:
                        if has_off - amount < 1:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У пользователя недостаточно офисов для удаления!",
                                                  color=0xff0000)
                            await inter.send(embed=embed, ephemeral=True)
                        else:
                            up_off = has_off - amount

                            c.execute(f"UPDATE 'users-data-org' SET offices={up_off} WHERE id={member.id}")
                            db.commit()

                            embed = disnake.Embed(title="Успешно",
                                                  description=f"Офис удалён у игрока {member.mention} в количестве {amount}!",
                                                  color=0x00ff00)
                            embed.add_field(name="Кол-во офисов", value=f"{up_off}")
                            await inter.send(embed=embed, ephemeral=True)

                            with open("LogChannels.json", "r") as f:
                                log_channels_data = json.load(f)

                            for channel_id in log_channels_data["list"]:
                                channel_id = int(channel_id)
                                channelf = self.bot.get_channel(channel_id)
                                embed = disnake.Embed(title="Офисы")
                                embed.add_field(name="Действие", value="Удаление")
                                embed.add_field(name="Кол-во", value=f"{amount}")
                                embed.add_field(name="Участник", value=f"{member.mention}")
                                embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                                await channelf.send(embed=embed)

                else:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Вы указали неверное действие!",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Данный пользователь не зарегистрирован!",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()

    @commands.slash_command(name="admin-register", description="Команда для регистрации игроков на сервере")
    @commands.has_permissions(administrator=True)
    async def admin_register(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, ctype: ctype_ch):
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
            await inter.send(embed=embed, ephemeral=True)
            db.close()

        else:
            with open("BannedIDs.json", "r") as f:
                ban_pl_data = json.load(f)

            if str(member.id) in ban_pl_data["list"]:
                embed = disnake.Embed(title="Бан",
                                      description="Регистрация не возможна! Пользователь забанен",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

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
                    await inter.send(embed=embed, ephemeral=True)

                    with open("LogChannels.json", "r") as f:
                        log_channels_data = json.load(f)

                    for channel_id in log_channels_data["list"]:
                        channel_id = int(channel_id)
                        channelf = self.bot.get_channel(channel_id)
                        embed = disnake.Embed(title="Аккаунты")
                        embed.add_field(name="Действие", value="Регистрация")
                        embed.add_field(name="Участник", value=f"{member.mention}")
                        embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                        await channelf.send(embed=embed)

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
                    await inter.send(embed=embed, ephemeral=True)

                    with open("LogChannels.json", "r") as f:
                        log_channels_data = json.load(f)

                    for channel_id in log_channels_data["list"]:
                        channel_id = int(channel_id)
                        channelf = self.bot.get_channel(channel_id)
                        embed = disnake.Embed(title="Аккаунты")
                        embed.add_field(name="Действие", value="Регистрация")
                        embed.add_field(name="Участник", value=f"{member.mention}")
                        embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                        await channelf.send(embed=embed)

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
                    await inter.send(embed=embed, ephemeral=True)

                    with open("LogChannels.json", "r") as f:
                        log_channels_data = json.load(f)

                    for channel_id in log_channels_data["list"]:
                        channel_id = int(channel_id)
                        channelf = self.bot.get_channel(channel_id)
                        embed = disnake.Embed(title="Аккаунты")
                        embed.add_field(name="Действие", value="Регистрация")
                        embed.add_field(name="Участник", value=f"{member.mention}")
                        embed.add_field(name="Администратор", value=f"{inter.author.mention}")
                        await channelf.send(embed=embed)

                    print(f"[{member.name} | {member.id}] $ registered as a organization")

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

    @commands.slash_command(name="log_channel", description="Команда для добавления канала в список каналов логирования админских команд")
    async def log_channel(self, inter: disnake.ApplicationCommandInteraction, action: actions, channelf: disnake.TextChannel):
        await BlackListMember(inter)
        await BlackListAdmin(inter)

        if inter.author == inter.guild.owner:
            with open("LogChannels.json", "r") as f:
                log_data = json.load(f)

            if action == "add":
                if str(channelf.id) in log_data["list"]:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Канал уже добавлен",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

                else:
                    log_data["list"].append(str(channelf.id))

                    with open("LogChannels.json", "w") as f:
                        json.dump(log_data, f, indent=4)

                    embed = disnake.Embed(title="Успешно",
                                          description="Канал добавлен в список!",
                                          color=0x00ff00)
                    await inter.send(embed=embed, ephemeral=True)

            elif action == "remove":
                if str(channelf.id) not in log_data["list"]:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Канала нет в списке",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

                else:
                    log_data["list"].remove(str(channelf.id))

                    with open("LogChannels.json", "w") as f:
                        json.dump(log_data, f, indent=4)

                    embed = disnake.Embed(title="Успешно",
                                          description="Канал удалён со списка",
                                          color=0x00ff00)
                    await inter.send(embed=embed, ephemeral=True)

            else:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали не верное действие",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не являетесь владельцем сервера",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

def setup(bot: commands.Bot):
    print("AdminCommands is loaded")
    bot.add_cog(AdminCommands(bot))