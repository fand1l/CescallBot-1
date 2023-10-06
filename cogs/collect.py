import disnake
from disnake.ext import commands
import sqlite3
import json
import time as t
from random import randint as rdi

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

class CollectCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    resources = commands.option_enum({
        "Газ": "1",
        "Золото": "2",
        "Уран": "3",
        "Титан": "4",
        "Железо": "5"
    })

    @commands.slash_command(name="collect", description="Команда для сбора денег")
    async def collect(self, inter: disnake.ApplicationCommandInteraction):
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

                await inter.send(embed=embed, ephemeral=True)

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
                await inter.send(embed=embed, ephemeral=True)


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

                await inter.send(embed=embed, ephemeral=True)

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
                await inter.send(embed=embed, ephemeral=True)


        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()

    @commands.slash_command(name="mine", description="Команда для сбор ресурсов")
    async def mine(self, inter: disnake.ApplicationCommandInteraction, resource: resources):
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

            if resource not in res_data:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали неверный ID ресурса",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

            elif resource == "6":
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы не можете добывать строительные материалы",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

            else:
                res_id = res_data[resource]["id"]

                c.execute(f"SELECT {res_id} FROM 'users-data-resdots' WHERE id={inter.author.id}")
                res_dot = c.fetchone()
                res_dot = res_dot[0]

                if res_dot == 0:
                    embed = disnake.Embed(title="Ошибка",
                                          description="У вас нет этой точки! Колонизируйте территорию",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

                else:
                    c.execute(f"SELECT {res_id} FROM 'users-data-lctime' WHERE id={inter.author.id}")
                    res_lctime = c.fetchone()
                    res_lctime = res_lctime[0]

                    min_coll = res_data[resource]["min"]
                    max_coll = res_data[resource]["max"]

                    res_coll = rdi(min_coll, max_coll) * res_dot

                    time_passed = int(t.time()) - res_lctime

                    if time_passed < 3600:
                        embed = disnake.Embed(title="Ошибка",
                                              description="Ещё рано! Попробуйте позже",
                                              color=0xff0000)
                        embed.add_field(name="Последний сбор", value=f"<t:{res_lctime}:R>")
                        await inter.send(embed=embed, ephemeral=True)

                    else:
                        c.execute(f"SELECT {res_id} FROM 'users-data-resources' WHERE id={inter.author.id}")
                        res_inv = c.fetchone()
                        res_inv = res_inv[0]
                        up_res_inv = res_inv + res_coll

                        c.execute(f"UPDATE 'users-data-resources' SET {res_id}=? WHERE id=?",
                                  (up_res_inv, inter.author.id))
                        c.execute(f"UPDATE 'users-data-lctime' SET {res_id}={int(t.time())} WHERE id={inter.author.id}")
                        db.commit()

                        res_name = res_data[resource]["name"]
                        embed = disnake.Embed(title="Успешно",
                                              description=f"Вы успешно собрали {res_name}!",
                                              color=0x00ff00)
                        embed.add_field(name="Ваш доход с этого сбора:", value=f"{int(res_coll):,}", inline=True)
                        embed.add_field(name=f"Кол-во {res_name}:", value=f"{int(up_res_inv):,}", inline=True)
                        await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()

    @commands.slash_command(name="make", description="Команда для сбора строительных материалов")
    async def make(self, inter: disnake.ApplicationCommandInteraction):
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

                await inter.send(embed=embed, ephemeral=True)

            else:
                up_build = build_res + build_coll

                c.execute(f"UPDATE 'users-data-resources' SET building_materials={up_build} WHERE id={inter.author.id}")
                c.execute(
                    f"UPDATE 'users-data-lctime' SET building_materials={int(t.time())} WHERE id={inter.author.id}")
                db.commit()

                embed = disnake.Embed(title="Успешно",
                                      description="Вы успешно собрали строительные материалы!",
                                      color=0x00ff00)
                embed.add_field(name="Ваш доход с этого сбора:", value=f"{int(build_coll):,}", inline=True)
                embed.add_field(name="Кол-во строительных материалов:", value=f"{int(up_build):,}", inline=True)
                await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()

    @commands.slash_command(name="mine_all", description="Команда для сбора всех доступных ресурсов")
    async def mine_all(self, inter: disnake.ApplicationCommandInteraction):
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

                            c.execute(f"UPDATE 'users-data-resources' SET {res_id}=? WHERE id=?",
                                      (up_res_inv, inter.author.id))
                            c.execute(
                                f"UPDATE 'users-data-lctime' SET {res_id}={int(t.time())} WHERE id={inter.author.id}")
                            db.commit()

                            resources_collected[res_info["name"]] = int(res_coll)

            if resources_collected:
                embed = disnake.Embed(title="Успешно", description="Вы успешно собрали следующие ресурсы:",
                                      color=0x00ff00)
                for res_name, res_coll in resources_collected.items():
                    embed.add_field(name=res_name, value=f"{res_coll:,}", inline=True)
                await inter.send(embed=embed, ephemeral=True)
            else:
                embed = disnake.Embed(title="Ошибка", description="У вас нет доступных ресурсов для сбора",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегистрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


def setup(bot: commands.Bot):
    print("CollectCommands is loaded")
    bot.add_cog(CollectCommands(bot))