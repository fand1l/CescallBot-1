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

class UpgradeCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    upgrades = commands.option_enum({"Сбор с 1 жителя": "eco", "Население": "peoples", "Счастье": "happy", "Сбор с 1 товара": "prod", "Кол-во товара": "count"})
    vehicles = commands.option_enum({
        "Танк": "2",
        "БМП": "3",
        "БТР": "4",
        "Бронеавтомобиль": "5",
        "САУ": "6",
        "Буксеруемая Гаубица": "7",
        "РСЗО": "8",
        "Транспортный Вертолёт": "9",
        "Ударный Вертолёт": "10",
        "Десантный Вертолёт": "11",
        "Истребитель": "12",
        "Транспортный Самолёт": "13",
        "Десантный Самолёт": "14",
        "Бомбардировщик": "15",
        "Разведовательный БПЛА": "16",
        "Ударный БПЛА": "17",
        "Дрон Камикадзе": "18",
        "Ракетный Комплекс": "20",
        "Транспортный Корабль": "21",
        "Десантный Корабль": "22",
        "Ракета": "27",
        "МБР": "28",
        "Бомба": "29",
        "Экипировка": "36"
    })
    modifys = commands.option_enum({"Урон": "dmg", "Защита": "def", "Скорость": "spd"})
    @commands.slash_command(name="upgrade", description="Команда для улучшения экономики")
    async def upgrade(self, inter: disnake.ApplicationCommandInteraction, up: upgrades):
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
                    await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

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
                    await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

            elif up == "hap" or up == "happy":
                c.execute(f"SELECT happy FROM 'users-data' WHERE id={inter.author.id}")
                happy = c.fetchone()
                happy = happy[0]

                if happy >= 100:
                    up_happy = 100000000
                    c.execute(f"UPDATE 'users-data' SET happy={up_happy} WHERE id={inter.author.id}")
                    db.commit()

                    embed = disnake.Embed(title="Ошибка",
                                          description="Вы имеете максимальное счастье",
                                          color=0xff0000)
                    embed.add_field(name="Счастье", value=f"{up_happy}%")
                    await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

            elif up == "product" or up == "prod":
                embed = disnake.Embed(title="Ошибка",
                                      description="Этот аргумент доступен только для организации!",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

            elif up == "count":
                embed = disnake.Embed(title="Ошибка",
                                      description="Этот аргумент доступен только для организации!",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

            elif up == None:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы не ввели аргумент!",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

            else:
                pass

        elif resid_org is not None:
            if up == "eco" or up == "economy":
                embed = disnake.Embed(title="Ошибка",
                                      description="Этот аргумент доступен только для страны/сепаратиста!",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

            elif up == "peop" or up == "peoples":
                embed = disnake.Embed(title="Ошибка",
                                      description="Этот аргумент доступен только для страны/сепаратиста!",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

            elif up == "hap" or up == "happy":
                embed = disnake.Embed(title="Ошибка",
                                      description="Этот аргумент доступен только для страны/сепаратиста!",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

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
                    await inter.send(embed=embed, ephemeral=True)

                elif goods_for_coll > max_prod:
                    up_goods_for_coll = max_prod
                    c.execute(
                        f"UPDATE 'users-data-org' SET goods_for_coll={up_goods_for_coll} WHERE id={inter.author.id}")
                    db.commit()

                    embed = disnake.Embed(title="Ошибка",
                                          description="Вы имеете максимальный доход с 1 товара",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

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
                    await inter.send(embed=embed, ephemeral=True)

                elif goods_count > max_prod:
                    up_goods_count = max_prod
                    c.execute(f"UPDATE 'users-data-org' SET goods_count={up_goods_count} WHERE id={inter.author.id}")
                    db.commit()

                    embed = disnake.Embed(title="Ошибка",
                                          description="Вы имеете максимальное кол-во товара! Постройте больше офисов",
                                          color=0xff0000)
                    embed.add_field(name="Офисы", value=f"{offices:,}")
                    embed.add_field(name="Максимальное кол-во товара", value=f"{max_prod:,} шт.")
                    await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


    @commands.slash_command(name="modify", description="Команда для модификации техники")
    async def modify(self, inter: disnake.ApplicationCommandInteraction, vehicle_id: vehicles, modify: modifys, amount: int = 1):
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
                await inter.send(embed=embed, ephemeral=True)

            else:
                army_id = army_data[vehicle_id]["id"]
                army_cost = army_data[vehicle_id]["Modify"]["Cost"]

                if modify == "def":
                    army_id_mod = f"{army_id}_def"

                elif modify == "spd":
                    army_id_mod = f"{army_id}_spd"

                elif modify == "dmg":
                    army_id_mod = f"{army_id}_dmg"

                else:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Вы указали неверную модификацию техники!",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

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
                    await inter.send(embed=embed, ephemeral=True)
                    return

                if army_inv == 0:
                    embed = disnake.Embed(title="Ошибка",
                                          description="У вас нет техники для модификации!",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

                elif army_inv < amount:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Не достаточно техники для модификации",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

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
                        await inter.send(embed=embed, ephemeral=True)

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
                        embed.add_field(name=f"Кол-во {army_name} с модификацией {modify}", value=f"{int(up_army_mod):,}",
                                        inline=True)
                        await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


def setup(bot: commands.Bot):
    print("UpgradeCommands is loaded")
    bot.add_cog(UpgradeCommands(bot))