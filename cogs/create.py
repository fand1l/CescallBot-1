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

class CreateCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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

    types = commands.option_enum({"Техника": "V", "Ресурсы": "R"})

    @commands.slash_command(name="create", description="Команда для создания техники")
    async def create(self, inter: disnake.ApplicationCommandInteraction, id: str, amount: int = 1):
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
                await inter.send(embed=embed, ephemeral=True)

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
                    await inter.send(embed=embed, ephemeral=True)

                else:
                    if army_type == "ground":
                        if land_equipment_plant == 0:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У вас нет завода сухопутной техники!",
                                                  color=0xff0000)
                            await inter.send(embed=embed, ephemeral=True)

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
                                await inter.send(embed=embed, ephemeral=True)

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
                                    await inter.send(embed=embed, ephemeral=True)

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
                                        c.execute(
                                            f"UPDATE 'users-data' SET money={up_money} WHERE id={inter.author.id}")

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
                                    await inter.send(embed=embed, ephemeral=True)

                    elif army_type == "air":
                        if aviation_factory == 0:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У вас нет авиационного завода!",
                                                  color=0xff0000)
                            await inter.send(embed=embed, ephemeral=True)

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
                                await inter.send(embed=embed, ephemeral=True)

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
                                    await inter.send(embed=embed, ephemeral=True)

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
                                        c.execute(
                                            f"UPDATE 'users-data' SET money={up_money} WHERE id={inter.author.id}")

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
                                    await inter.send(embed=embed, ephemeral=True)

                    elif army_type == "sea":
                        if shipyard == 0:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У вас нет верфи!",
                                                  color=0xff0000)
                            await inter.send(embed=embed, ephemeral=True)

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
                                await inter.send(embed=embed, ephemeral=True)

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
                                    await inter.send(embed=embed, ephemeral=True)

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
                                        c.execute(
                                            f"UPDATE 'users-data' SET money={up_money} WHERE id={inter.author.id}")

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
                                    await inter.send(embed=embed, ephemeral=True)

                    elif army_type == "nuke":
                        if nuclear_factory == 0:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У вас нет ядерного завода!",
                                                  color=0xff0000)
                            await inter.send(embed=embed, ephemeral=True)

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
                                await inter.send(embed=embed, ephemeral=True)

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
                                    await inter.send(embed=embed, ephemeral=True)

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
                                        c.execute(
                                            f"UPDATE 'users-data' SET money={up_money} WHERE id={inter.author.id}")

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
                                    await inter.send(embed=embed, ephemeral=True)

                    elif army_type == "chemical":
                        if chemical_factory == 0:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У вас нет химического завода!",
                                                  color=0xff0000)
                            await inter.send(embed=embed, ephemeral=True)

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
                                await inter.send(embed=embed, ephemeral=True)

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
                                    await inter.send(embed=embed, ephemeral=True)

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
                                        c.execute(
                                            f"UPDATE 'users-data' SET money={up_money} WHERE id={inter.author.id}")

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
                                    await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


    @commands.slash_command(name="build", description="Команда для постройки инфраструктуры")
    async def build(self, inter: disnake.ApplicationCommandInteraction, id: infras):
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
                await inter.send(embed=embed, ephemeral=True)

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
                    await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

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
                        embed.add_field(name="Кол-во строительных материалов:", value=f"{int(up_build_m):,}",
                                        inline=True)
                        embed.add_field(name=f"Кол-во {infra_name}:", value=f"{int(up_build):,}", inline=True)
                        await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


    @commands.slash_command(name="destroy", description="Команда для уничтожения техники/инфраструктуры")
    async def destroy(self, inter: disnake.ApplicationCommandInteraction, typef: types, id: str, amount: int, mod: str):
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
                    await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

                    else:
                        if infra_inv < amount:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="Недостаточно инфраструктуры для уничтожения!",
                                                  color=0xff0000)
                            await inter.send(embed=embed, ephemeral=True)

                        else:
                            up_build = infra_inv - amount

                            c.execute(f"UPDATE 'users-data-infra' SET {infra_id}={up_build} WHERE id={inter.author.id}")
                            db.commit()

                            embed = disnake.Embed(title="Успешно",
                                                  description=f"Вы успешно уничтожили {infra_name} в количестве {amount:,}!",
                                                  color=0x00ff00)
                            embed.add_field(name=f"Кол-во {infra_name}:", value=f"{int(up_build)}", inline=True)
                            await inter.send(embed=embed, ephemeral=True)

            elif typef == "vehicle" or typef == "V" or typef == "v":
                with open("ArmyData.json", "r", encoding="utf-8") as f:
                    army_data = json.load(f)

                if id not in army_data:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Вы указали неверный ID техники!",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

                else:
                    if mod:
                        if mod == "def":
                            army_id = f"{army_data[id]['id']}_def"
                            army_name = army_data[id]["Name"]

                            c.execute(f"SELECT {army_id} FROM 'users-data-army-mod' WHERE id={inter.author.id}")
                            army_inv = c.fetchone()
                            army_inv = army_inv[0]

                            if army_inv == 0:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="У вас нет данной техники!",
                                                      color=0xff0000)
                                await inter.send(embed=embed, ephemeral=True)

                            elif army_inv < amount:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="У вас недостаточно техники для уничтожения!",
                                                      color=0xff0000)
                                await inter.send(embed=embed, ephemeral=True)

                            else:
                                up_army = army_inv - amount

                                c.execute(
                                    f"UPDATE 'users-data-army-mod' SET {army_id}={up_army} WHERE id={inter.author.id}")
                                db.commit()

                                embed = disnake.Embed(title="Успешно",
                                                      description=f"Вы успешно уничтожили {army_name} в количестве {amount:,} с модификацией def!",
                                                      color=0x00ff00)
                                embed.add_field(name=f"Кол-во {army_name}:", value=f"{int(up_army)}", inline=True)
                                await inter.send(embed=embed, ephemeral=True)

                        elif mod == "spd":
                            army_id = f"{army_data[id]['id']}_spd"
                            army_name = army_data[id]["Name"]

                            c.execute(f"SELECT {army_id} FROM 'users-data-army-mod' WHERE id={inter.author.id}")
                            army_inv = c.fetchone()
                            army_inv = army_inv[0]

                            if army_inv == 0:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="У вас нет данной техники!",
                                                      color=0xff0000)
                                await inter.send(embed=embed, ephemeral=True)

                            elif army_inv < amount:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="У вас недостаточно техники для уничтожения!",
                                                      color=0xff0000)
                                await inter.send(embed=embed, ephemeral=True)

                            else:
                                up_army = army_inv - amount

                                c.execute(
                                    f"UPDATE 'users-data-army-mod' SET {army_id}={up_army} WHERE id={inter.author.id}")
                                db.commit()

                                embed = disnake.Embed(title="Успешно",
                                                      description=f"Вы успешно уничтожили {army_name} в количестве {amount:,} с модификацией spd!",
                                                      color=0x00ff00)
                                embed.add_field(name=f"Кол-во {army_name}:", value=f"{int(up_army)}", inline=True)
                                await inter.send(embed=embed, ephemeral=True)

                        elif mod == "dmg":
                            army_id = f"{army_data[id]['id']}_dmg"
                            army_name = army_data[id]["Name"]

                            c.execute(f"SELECT {army_id} FROM 'users-data-army-mod' WHERE id={inter.author.id}")
                            army_inv = c.fetchone()
                            army_inv = army_inv[0]

                            if army_inv == 0:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="У вас нет данной техники!",
                                                      color=0xff0000)
                                await inter.send(embed=embed, ephemeral=True)

                            elif army_inv < amount:
                                embed = disnake.Embed(title="Ошибка",
                                                      description="У вас недостаточно техники для уничтожения!",
                                                      color=0xff0000)
                                await inter.send(embed=embed, ephemeral=True)

                            else:
                                up_army = army_inv - amount

                                c.execute(
                                    f"UPDATE 'users-data-army-mod' SET {army_id}={up_army} WHERE id={inter.author.id}")
                                db.commit()

                                embed = disnake.Embed(title="Успешно",
                                                      description=f"Вы успешно уничтожили {army_name} в количестве {amount:,} с модификацией dmg!",
                                                      color=0x00ff00)
                                embed.add_field(name=f"Кол-во {army_name}:", value=f"{int(up_army)}", inline=True)
                                await inter.send(embed=embed, ephemeral=True)

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
                            await inter.send(embed=embed, ephemeral=True)

                        elif army_inv < amount:
                            embed = disnake.Embed(title="Ошибка",
                                                  description="У вас недостаточно техники для уничтожения!",
                                                  color=0xff0000)
                            await inter.send(embed=embed, ephemeral=True)

                        else:
                            up_army = army_inv - amount

                            c.execute(f"UPDATE 'users-data-army' SET {army_id}={up_army} WHERE id={inter.author.id}")
                            db.commit()

                            embed = disnake.Embed(title="Успешно",
                                                  description=f"Вы успешно уничтожили {army_name} в количестве {amount:,}!",
                                                  color=0x00ff00)
                            embed.add_field(name=f"Кол-во {army_name}:", value=f"{int(up_army)}", inline=True)
                            await inter.send(embed=embed, ephemeral=True)

            else:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали неверный тип!",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


def setup(bot: commands.Bot):
    bot.add_cog(CreateCommands(bot))