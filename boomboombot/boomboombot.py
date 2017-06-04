import discord
import os
import traceback
import pdb
import random
import asyncio


def discord_discussion():
    TOKEN =  os.environ['TOKEN']
    client = discord.Client()

    players = []
    word = '#'
    words = []
    game_start = False
    with open('./liste_mots.txt','r') as f:
        words = f.read().splitlines()
    index_player = 0


    async def send_word(msg):
        global word
        index = random.randint(0,len(words)-1)
        word = words[index]
        answer = " Le mot est '" + word + "'"
        await client.send_message(msg.channel, answer)

    async def start_round(msg):
        index_player = 0
        await send_word(msg)

    async def end_round(msg):
        for player in players:
            answer = player[0] + " : " + str(player[2]) + " points"
            await client.send_message(msg.channel, answer)
            player[2] = 0
            player[3] = 3

    async def verify_end(msg):
        player_with_life = 0
        for player in players:
            if player[3] > 0:
                 player_with_life += 1

        if player_with_life <= 1:
            await end_round(msg)


    @client.event
    async def on_message(message):
        global word
        if message.content.startswith("!start"):
            if len(players) > 0:
                await client.send_message(message.channel, "Le jeu va commencer !")
                await start_round(message)
            else:
                await client.send_message(message.channel, "Vous devez ajouter au moin un utilisateur")
        elif message.content.startswith("!end"):
            await end_round(message)
        elif message.content.startswith("!join"):
            name = message.author.name
            idNumber = message.author.id
            already_add = False
            for player in players:
                if idNumber in player[1]:
                    already_add = True
            if already_add:
                await client.send_message(message.channel,"Joueur déjà ajouté !")
            else:
                players.append([name, idNumber, 0, 3])
                await client.send_message(message.channel,"Joueur " + name + " ajouté au jeu !")
        elif message.content.startswith("!remove"):
            name = message.author.name
            idNumber = message.author.id
            for player in players:
                if idNumber in player[1]:
                    players.remove(player)
                    await client.send_message(message.channel,"Joueur " + name + " retiré du jeu !")
        elif message.content.startswith("!players"):
            for player in players:
                await client.send_message(message.channel, player[0])
        elif message.content.startswith("!help"):
            await client.send_message(message.channel,"'!join' pour s'inscrire à la partie.")
            await client.send_message(message.channel,"'!remove' pour se retirer de la partie.")
            await client.send_message(message.channel,"'!players' liste les différents joueurs inscrits.")
            await client.send_message(message.channel,"'!start' pour commencer à la partie.")
            await client.send_message(message.channel,"'!end' pour terminer à la partie.")
            await client.send_message(message.channel,"Des mots vont être envoyé par le bot, le premier à réécrire le mot gagne 10 points, si vous vous trompez vous perdez une vie, en sachant que vous commencez la partie avec 3 vies.")
            await client.send_message(message.channel,"Quand il ne reste plus qu'un joueur avec des vies, le tableau des scores s'affichent.")
        elif message.content.startswith(word):
            for player in players:
                if player[1] == message.author.id:
                    if player[3] > 0:
                        player[2] += 10
                        await client.send_message(message.channel,player[0] + " gagne 10 points")
                        await send_word(message)
        elif not message.content.startswith(word):
            if message.author.id != client.user.id:
                for player in players:
                    if player[1] == message.author.id:
                        if player[3] > 0:
                            player[3] -= 1
                            if player[3] <= 0:
                                await client.send_message(message.channel,player[0] + " n'à plus de vie !")
                                await verify_end(message)
                            else:
                                await client.send_message(message.channel,player[0] + " perds 1 vie")
    client.run(TOKEN)


main = discord_discussion()
