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

class ProfileCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="profile", description="Команда для просмотра своего профиля")
    async def profile(self, inter: disnake.ApplicationCommandInteraction):
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

            await inter.send(embed=embed, ephemeral=True)


        elif resid_org is not None:
            c.execute(f"SELECT money FROM 'users-data-org' WHERE id={inter.author.id}")
            usr_money = c.fetchone()

            c.execute(f"SELECT goods_for_coll FROM 'users-data-org' WHERE id={inter.author.id}")
            usr_goods_coll = c.fetchone()

            c.execute(f"SELECT type FROM 'users-data-org' WHERE id={inter.author.id}")
            usr_type = c.fetchone()

            c.execute(f"SELECT cost_up_eco FROM 'users-data-org' WHERE id={inter.author.id}")
            usr_cost_eco = c.fetchone()

            c.execute(f"SELECT cost_up_happy FROM 'users-data-org' WHERE id={inter.author.id}")
            usr_cost_happy = c.fetchone()

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

            await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


    @commands.slash_command(name="inventory", description="Команда для просмотра инвентаря")
    async def inventory(self, inter: disnake.ApplicationCommandInteraction):
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

            await inter.send(embed=embed_land, ephemeral=True)
            await inter.send(embed=embed_air, ephemeral=True)
            await inter.send(embed=embed_sea, ephemeral=True)
            await inter.send(embed=embed_nuke_chem, ephemeral=True)



        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


    @commands.slash_command(name="resources", description="Команда для просмотра ресурсов и точек")
    async def resources(self, inter: disnake.ApplicationCommandInteraction):
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

            await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


    @commands.slash_command(name="infrastructure", description="Команда для просмотра вашей инфраструктуры")
    async def infrastructure(self, inter: disnake.ApplicationCommandInteraction):
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
            await inter.send(embed=embed, ephemeral=True)

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
            await inter.send(embed=embed, ephemeral=True)


        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы не зарегестрированы! Для регистрации на сервере используйте команду $reg <type>",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        db.close()


    @commands.slash_command(name="shop", description="Команда для просмотра цен на технику")
    async def shop(self, inter: disnake.ApplicationCommandInteraction):
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

        await inter.send(embed=embedland, ephemeral=True)
        await inter.send(embed=embedair, ephemeral=True)
        await inter.send(embed=embedsea, ephemeral=True)
        await inter.send(embed=embednuke, ephemeral=True)


    @commands.slash_command(name="shop_infrastructure", description="Команда для просмотра цен на инфраструктуру")
    async def shop_infrastructure(self, inter: disnake.ApplicationCommandInteraction):
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

        await inter.send(embed=embed, ephemeral=True)


    @commands.slash_command(name="leaderboard", description="Команда для просмотра топ игроков по балансу")
    async def leaderboard(self, inter: disnake.ApplicationCommandInteraction):
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
            user = self.bot.get_user(user_id)
            name = user.name if user else f"Пользователь с ID {user_id}"
            embed.add_field(name=f"{position}. {name}", value=f"Баланс: {money} денег", inline=False)

        # Отправляем embed с топом игроков
        await inter.send(embed=embed, ephemeral=True)

        db.close()

    @commands.slash_command(name="privileges", description="Команда для просмотра привилегий игрока")
    async def privileges(self, inter: disnake.ApplicationCommandInteraction):
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

        await inter.send(embed=embed, ephemeral=True)

    @commands.slash_command(name="info", description="Bot info")
    async def info(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(title="Information",
                              description="Bot created by fand1l in Ukraine!\n War-Political Game bot",
                              color=0x00ff00)
        await inter.send(embed=embed)


def setup(bot: commands.Bot):
    print("ProfileCommands is loaded")
    bot.add_cog(ProfileCommands(bot))