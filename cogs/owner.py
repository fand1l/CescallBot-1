import disnake
from disnake.ext import commands
import sqlite3
import json
import time as t
import os


class OwnerCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    actions = commands.option_enum({
        "Бан": "ban",
        "Разбан": "unban",
        "Премиум": "premium",
        "VIP": "vip",
        "Отключить": "off",
        "Отключить (публично)": "offwoe"
    })

    actions2 = commands.option_enum({
        "Список": "list",
        "Добавить в список": "add",
        "Удалить из списка": "remove"
    })

    lists = commands.option_enum({
        "Администраторы": "admins",
        "Пользователи": "member"
    })

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        bot_mention = message.guild.get_member(self.bot.user.id).mention
        if bot_mention in message.content:
            await message.channel.send(f"? ? ?")

    @commands.slash_command(name="bot", description="Команда для управления ботом")
    @commands.is_owner()
    async def botf(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, action: actions, args: str):
        with open("BannedIDs.json", "r", encoding="utf-8") as f:
            ban_pl_data = json.load(f)

        with open("PremiumUsers.json", "r", encoding="utf-8") as f:
            prem_usr_data = json.load(f)

        with open("VIPUsers.json", "r", encoding="utf-8") as f:
            vip_usr_data = json.load(f)

        if action == "ban":
            if str(member.id) in ban_pl_data["list"]:
                embed = disnake.Embed(title="Ошибка",
                                      description="Этот пользователь забанен!",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

            else:
                ban_pl_data["list"][str(member.id)] = f"{args}"

                with open("BannedIDs.json", "w", encoding="utf-8") as f:
                    json.dump(ban_pl_data, f, indent=4)

                embed = disnake.Embed(title="Успешно",
                                      description=f"Пользователь {member.mention} был забанен",
                                      color=0x00ff00)
                embed.add_field(name="Причина", value=f"{args}")
                await inter.send(embed=embed, ephemeral=True)
                await member.send(f"Вы были забанены по причине: {args}")

        elif action == "unban":
            if str(member.id) not in ban_pl_data["list"]:
                embed = disnake.Embed(title="Ошибка",
                                      description="Этот пользователь не забанен!",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

            else:
                del ban_pl_data["list"][str(member.id)]

                with open("BannedIDs.json", "w", encoding="utf-8") as f:
                    json.dump(ban_pl_data, f, indent=4)

                embed = disnake.Embed(title="Успешно",
                                      description=f"Пользователь {member.mention} был разбанен",
                                      color=0x00ff00)
                await inter.send(embed=embed, ephemeral=True)
                await member.send("Вы были разбанены")

        elif action == "premium" or action == "prem":
            if args == "add":
                if str(inter.author.id) in prem_usr_data["list"]:
                    embed = disnake.Embed(title="Ошибка",
                                          description="У данного пользователя уже есть эта привилегия",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)
                else:
                    prem_usr_data["list"].append(str(member.id))

                    with open("PremiumUsers.json", "w", encoding="utf-8") as f:
                        json.dump(prem_usr_data, f, indent=4)

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Пользователь {member.mention} получил привилегию Premium",
                                          color=0x00ff00)
                    await inter.send(embed=embed, ephemeral=True)
                    await member.send("Вы получили привилегию Premium")

            elif args == "remove":
                if str(inter.author.id) not in prem_usr_data["list"]:
                    embed = disnake.Embed(title="Ошибка",
                                          description="У данного пользователя нет этой привилегии!",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)
                else:
                    prem_usr_data["list"].append(str(member.id))

                    with open("PremiumUsers.json", "w", encoding="utf-8") as f:
                        json.dump(prem_usr_data, f, indent=4)

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Пользователь {member.mention} потерял привилегию Premium",
                                          color=0x00ff00)
                    await inter.send(embed=embed, ephemeral=True)
                    await member.send("Вы потеряли привилегию Premium")

            else:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали не верное действие2",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

        elif action == "vip":
            if args == "add":
                if str(inter.author.id) in vip_usr_data["list"]:
                    embed = disnake.Embed(title="Ошибка",
                                          description="У данного пользователя уже есть эта привилегия!",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)
                else:
                    vip_usr_data["list"].append(str(member.id))

                    with open("VIPUsers.json", "w", encoding="utf-8") as f:
                        json.dump(vip_usr_data, f, indent=4)

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Пользователь {member.mention} получил привилегию VIP",
                                          color=0x00ff00)
                    await inter.send(embed=embed, ephemeral=True)
                    await member.send("Вы получили привилегию VIP")

            elif args == "remove":
                if str(inter.author.id) not in vip_usr_data["list"]:
                    embed = disnake.Embed(title="Ошибка",
                                          description="У данного пользователя нет этой привилегии!",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)
                else:
                    vip_usr_data["list"].remove(str(member.id))

                    with open("VIPUsers.json", "w", encoding="utf-8") as f:
                        json.dump(vip_usr_data, f, indent=4)

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Пользователь {member.mention} потерял привилегию VIP",
                                          color=0x00ff00)
                    await inter.send(embed=embed, ephemeral=True)
                    await member.send("Вы потеряли привилегию VIP")

            else:
                embed = disnake.Embed(title="Ошибка",
                                      description="Вы указали не верное действие2",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)
                
        elif action == "off":
            embed = disnake.Embed(title="Отключение",
                                      description="Отключение бота!",
                                      color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)
            
            os._exit(0)
            
        elif action == "offwoe":
            embed = disnake.Embed(title="Отключение",
                                      description="Отключение бота!",
                                      color=0xff0000)
            await inter.send(embed=embed)
            
            os._exit(0)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Вы ввели неверное действие!",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

    @commands.slash_command(name="sql", description="Команда для управления базой данных")
    @commands.is_owner()
    async def sql(self, inter: disnake.ApplicationCommandInteraction, request: str):
        db = sqlite3.connect('CescallBotDB.db')
        c = db.cursor()
        c.execute(request)
        db.commit()
        rows = c.fetchall()
        await inter.send(rows, ephemeral=True)
        db.close()

    @commands.slash_command(name="banlist", description="Команда для просмотра забаненых игроков")
    @commands.is_owner()
    async def banlist(self, inter: disnake.ApplicationCommandInteraction):
        with open("BannedIDs.json", "r") as f:
            ban_pl_data = json.load(f)

        embed = disnake.Embed(title="Список забаненых игроков", description="Здесь показаны все забаненые игроки")

        for player_id in ban_pl_data["list"]:
            player = self.bot.get_user(int(player_id))
            if player is None:
                player_name = f"Unknown User ({player_id})"
            else:
                player_name = player.name

            embed.add_field(name=f"{player_name} | {player_id}", value=f"Причина: {ban_pl_data['list'][player_id]}")

        await inter.send(embed=embed, ephemeral=True)
        
    @commands.slash_command(name="server_list", description="Команда для просмотра серверов на которых есть данных бот")
    @commands.is_owner()
    async def server_list(self, inter: disnake.ApplicationCommandInteraction):
        bot_servers = self.bot.guilds
        response = "\n".join([f"{server.id}: {server.name}" for server in bot_servers])
        await inter.send(f"Серверы, на которых присутствует бот:\n{response}", ephemeral=True)
        
    @commands.slash_command(name="leave_s", description="Команда для удаления сервера с бота")
    @commands.is_owner()
    async def leave_s(self, inter: disnake.ApplicationCommandInteraction, server_id):
        guild = self.bot.get_guild(int(server_id))
        await inter.send(f"Successfully left the server {guild.name}.", ephemeral=True)
        channeln = self.bot.get_channel(1116409459749695575)
        await channeln.send("Бот покидает данный сервер")
        await guild.leave()

    @commands.slash_command(name="privileges_list", description="Команда для просмотра списка привилегий игроков")
    @commands.is_owner()
    async def privileges_list(self, inter: disnake.ApplicationCommandInteraction):
        with open("PremiumUsers.json", "r") as f:
            premium_data = json.load(f)

        with open("VIPUsers.json", "r") as f:
            vip_data = json.load(f)

        embed = disnake.Embed(title="Список привилегий игроков")

        for player_id in premium_data["list"]:
            player = self.bot.get_user(int(player_id))
            if player is None:
                player_name = f"Unknown User ({player_id})"
            else:
                player_name = player.name

            embed.add_field(name=f"{player_name} | {player_id}", value=f"Premium")

        for player_id in vip_data["list"]:
            player = self.bot.get_user(int(player_id))
            if player is None:
                player_name = f"Unknown User ({player_id})"
            else:
                player_name = player.name

            embed.add_field(name=f"{player_name} | {player_id}", value=f"VIP")

        await inter.send(embed=embed, ephemeral=True)

    @commands.slash_command(name="blacklist", description="Команда для управления черным списком")
    @commands.is_owner()
    async def blacklist(
            self,
            inter: disnake.ApplicationCommandInteraction,
            action: actions2,
            lists: lists = disnake.Option(name="list", required=False),
            member: disnake.Member = disnake.Option(name="member", required=False)):

        with open("MemberBlackList.json", "r") as file:
            member_data = json.load(file)

        with open("AdminsBlackList.json", "r") as file:
            admins_data = json.load(file)

        if action == "list":
            embed_member = disnake.Embed(title="Пользователи в черном списке")

            for user_id in admins_data["list"]:
                user_id = int(user_id)

                user = self.bot.get_user(user_id)

                embed_member.add_field(name=f"{user.name}", value="Черный список администрации")

            embed_member.add_field(name=" ", value=" ", inline=False)

            for user_id in member_data["list"]:
                user_id = int(user_id)

                user = self.bot.get_user(user_id)

                embed_member.add_field(name=f"{user.name}", value="Черный список пользователей")

            await inter.send(embed=embed_member, ephemeral=True)

        elif action == "add":
            if lists == "admins":
                if str(member.id) in admins_data["list"]:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Админ уже в черном списке",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

                else:
                    admins_data["list"].append(str(member.id))

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Пользователь {member.name} был занесен в черный список администраторов",
                                          color=0x00ff00)
                    await inter.send(embed=embed, ephemeral=True)
                    await member.send("Вы были занесены в черный список администраторов!")

            elif lists == "member":
                if str(member.id) in member_data["list"]:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Пользователь уже в черном списке",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

                else:
                    member_data["list"].append(str(member.id))

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Пользователь {member.name} был занесен в черный список пользователей",
                                          color=0x00ff00)
                    await inter.send(embed=embed, ephemeral=True)
                    await member.send("Вы были занесены в черный список пользователей!")

            else:
                embed = disnake.Embed(title="Ошибка",
                                      description="Неверный список",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

        elif action == "remove":
            if lists == "admins":
                if str(member.id) not in admins_data["list"]:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Админа нет в черном списке",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

                else:
                    admins_data["list"].remove(str(member.id))

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Пользователь {member.name} был удалён из черного списка администраторов!",
                                          color=0x00ff00)
                    await inter.send(embed=embed, ephemeral=True)
                    await member.send("Вы были удалёны из черного списка администраторов!")

            elif lists == "member":
                if str(member.id) not in member_data["list"]:
                    embed = disnake.Embed(title="Ошибка",
                                          description="Пользовател нет в черном списке",
                                          color=0xff0000)
                    await inter.send(embed=embed, ephemeral=True)

                else:
                    member_data["list"].remove(str(member.id))

                    embed = disnake.Embed(title="Успешно",
                                          description=f"Пользователь {member.name} был удалён из черного списка пользователей",
                                          color=0x00ff00)
                    await inter.send(embed=embed, ephemeral=True)
                    await member.send("Вы были удалёны из черного списка пользователей!")

            else:
                embed = disnake.Embed(title="Ошибка",
                                      description="Неверный список",
                                      color=0xff0000)
                await inter.send(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(title="Ошибка",
                                  description="Неверное действие!",
                                  color=0xff0000)
            await inter.send(embed=embed, ephemeral=True)

        with open("MemberBlackList.json", "w") as file:
            json.dump(member_data, file, indent=4)

        with open("AdminsBlackList.json", "w") as file:
            json.dump(admins_data, file, indent=4)


def setup(bot: commands.Bot):
    print("OwnerCommands is loaded")
    bot.add_cog(OwnerCommands(bot))