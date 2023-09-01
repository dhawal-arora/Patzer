from typing import Optional
import discord
import os
from discord.ext import commands
import requests
import json
import berserk

lichesstoken ="xyz"
session = berserk.TokenSession(lichesstoken)
lichess= berserk.Client(session=session)
tournaments = lichess.tournaments.get()
lengthinfo=len(tournaments['created'])
lengthstarted=len(tournaments['started'])
headers = {'User-Agent':'dhawalplaysd4'}
#updatedgamelink=""

TESTINGTOKEN="xyz"
TOKEN="xyz"
client = commands.Bot(command_prefix=['Ptz.','ptz.','p.','P.'], intents=discord.Intents.all())
#intents=discord.Intents.all()
client.remove_command("help")

@client.event
async def on_ready():
  print ('We have logged in as {0.user}' .format (client))
  await client.wait_until_ready()
  #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))
  await client.tree.sync()


@client.tree.command(name="help", description="Basic help command")
@commands.cooldown(1,5,commands.BucketType.user)
async def help(content: discord.Interaction):
   myEmbed = discord.Embed(title="Patzer Bot", description="Your One-Stop Chess Data Retrieval Tool\n\n \
    **Lichess:**\n\
    </score:1116564750080421959>: Score between two players.\n\
    </userinfo:1116564750080421960>: Player profile.\n\
    </variantratings:1116564750080421961>: Player variant ratings.\n\
    </gamegif:1146189138387816499>: Generates a GIF of game link entered.\n\
    </swissrankings:1116564750080421963>: Shows swiss tournament results.\n\
    </arenarankings:1116564750080421964>: Shows arena tournament results.\n\
    </teamrankings:1116564750080421965>: Shows team tournament results.\n\
    </arenabyuser:1116564750080421966>: Upcoming arena tournaments by a user.\n\
    </downloadgames:1116564750080421967>: Download games of a player.\n\n\
    **Chess.com:**\n\
    </chesscomclub:1116564750512423063>: Chess.com club details\n\
    </chesscomuserinfo:1116564750512423064>: Chess.com player profile\n\
    </chesscomdownload:1116564750512423065>: Download Chess.com games of a player\n\
    </chesscomleaderboard:1116564750512423066>: Chess.com all time leaderboards", color=0x00ff00)
   buttons=Empty()
   buttons.add_item(discord.ui.Button(label="Invite Bot",style=discord.ButtonStyle.link,url="https://discord.com/api/oauth2/authorize?client_id=803120439550279690&permissions=519233&scope=bot"))
   buttons.add_item(discord.ui.Button(label="Support Server",style=discord.ButtonStyle.link,url="https://discord.gg/cdfUp5Zqs7"))
   buttons.add_item(discord.ui.Button(label="Write Review",style=discord.ButtonStyle.link,url="https://top.gg/bot/803120439550279690"))
   await content.response.send_message(embed=myEmbed, view=buttons)

@client.tree.command(name="score", description="Score between two players")
@commands.cooldown(1,5,commands.BucketType.user)
async def score(content: discord.Interaction, player1:str, player2:str):
  if player1!=player2:
    response3=requests.get(f"https://lichess.org/api/crosstable/{player1}/{player2}")
    Total=(f"Total Games Played: {response3.json().get('nbGames')}")
    Player1 = list(response3.json().get('users').keys())[0]
    Player1Score = list(response3.json().get('users').values())[0]
    Player2= list(response3.json().get('users').keys())[1] 
    Player2Score= list(response3.json().get('users').values())[1] 
    whole=(f"Current Scores:\n\n**{Player1}** {Player1Score}-{Player2Score} **{Player2}**\n\n{Total}")
    myEmbed = discord.Embed(title="Patzer Bot", description=whole,color=0x00ff00)
  else:
    myEmbed = discord.Embed(title="Patzer Bot", description="Same player entered twice, please try again.",color=0x00ff00)
  await content.response.send_message(embed=myEmbed)


# @client.tree.command(name="lichessupcoming", description="Upcoming lichess tournament")
# @commands.cooldown(1,60,commands.BucketType.user)
# async def lichessupcoming(content:discord.Interaction):
#   myEmbed = discord.Embed(title="Patzer Bot", description="All tournaments shown below will have a minimum of 15 players.\n Only the top 4 events according to the number of players are shown.\n If nothing is shown it indicates that no tournaments meet the requirements.\n\nList of upcoming arena tournaments hosted by lichess:",color=0x00ff00)
#   maxRecord = min(4,lengthinfo)
#   for i in range(maxRecord):
#    dict = tournaments['created'][i]
#    if dict['nbPlayers'] > 15:
#     if dict['clock']['limit'] < 60:
#       timecontrolduration=str(dict['clock']['limit'])+'+'+str(dict['clock']['increment'])
#     else:
#       timecontrolduration=str(int(dict['clock']['limit']/60))+'+'+str(dict['clock']['increment'])
#     duration=timecontrolduration+' Matches for '+str(dict['minutes'])+' minutes'
#     timing=str(dict['startsAt'])+' (Add 5:30 for IST)'
#     str1 = 'https://lichess.org/tournament/'.strip()+dict['id']+'\n'
#     lichessupcomingt='**Tournament Name:** '+str(dict['fullName'])+'**\nStarting Date/Time:** '+str(timing)+'**\nDuration:** '+str(duration)+'\n**Tournament Link:** '+str(str1)
#     myEmbed.add_field(name="\u200b", value=lichessupcomingt,inline=False)
#   await content.response.send_message(embed=myEmbed)


# @client.tree.command(name="lichessstarted", description="Started lichess tournament")
# @commands.cooldown(1,60,commands.BucketType.user)
# async def lichessstarted(content:discord.Interaction):
#   myEmbed = discord.Embed(title="Patzer Bot", description="All tournaments shown below will have a minimum of 20 players.\n Only the top 4 events according to the number of players are shown.\n If nothing is shown it indicates that no tournaments meet the requirements.\n\nList of started arena tournaments hosted by lichess:",color=0x00ff00)
#   maxRecord = min(4,lengthstarted)
#   for i in range(maxRecord):
#    dict = tournaments['started'][i]
#    if dict['nbPlayers'] > 20:
#     if dict['clock']['limit'] < 60:
#      timecontrolduration=str(dict['clock']['limit'])+'sec+'+str(dict['clock']['increment'])
#     else:
#      timecontrolduration=str(int(dict['clock']['limit']/60))+'+'+str(dict['clock']['increment'])
#    duration=timecontrolduration+' Matches for '+str(dict['minutes'])+' minutes'
#    str1 = 'https://lichess.org/tournament/'.strip()+dict['id']+'\n'
#    newlichess='**Tournament Name: **'+str(dict['fullName'])+'\n**Finishes At: **'+str(dict['finishesAt'])+' (Add 5:30 for IST)''\n**Duration: **'+str(duration)+'\n**Tournament Link: **'+str(str1)
#    myEmbed.add_field(name='\u200b', value=newlichess,inline=False)
#   await content.response.send_message(embed=myEmbed)

@client.tree.command(name="userinfo", description="Lichess user info")
async def userinfo(content:discord.Interaction, username:str):
  response3=requests.get (str(f'https://lichess.org/api/user/{username}'))
  if response3.json().get("error")!="Not found":
    allinfo=str(
    'Username: '+str(response3.json().get('username'))+'\n'+
    'Title: '+str(response3.json().get('title'))+'\n'+
    'Lichess Patron: '+str(response3.json().get('patron'))+'\n'+
    'Profile Link: '+str(response3.json().get('url'))+'\n'+
    'Online Status: '+str(response3.json().get('online'))+'\n\n'+
    'All Games Played: '+str(response3.json().get('count')['all'])+'\n'+
    'Rated Games: '+str(response3.json().get('count')['rated'])+'\n'+
    'Wins: '+str(response3.json().get('count')['win'])+'\n'+
    'Draws: '+str(response3.json().get('count')['draw'])+'\n'+
    'Losses: '+str(response3.json().get('count')['loss'])+'\n'+
    'Games Playing Now: '+str(response3.json().get('count')['playing'])+'\n\u200b\n')
  else:
    allinfo="User Not Found"
  myEmbed1 = discord.Embed(title="Patzer Bot", description=allinfo,color=0x00ff00)
  ratings=''
  if 'perfs' in response3.json():
    if 'ultraBullet' in response3.json().get('perfs'):
      ratings='Games: '+str((response3.json().get('perfs')['ultraBullet']['games']))+'\n'
      ratings=str(ratings)+'Rating: '+str((response3.json().get('perfs')['ultraBullet']['rating']))+'\n\n'
      myEmbed1.add_field(name="UltraBullet", value = ratings, inline=True)
    if 'bullet' in response3.json().get('perfs'):
      ratings='Games: '+str((response3.json().get('perfs')['bullet']['games']))+'\n'
      ratings=str(ratings)+'Rating: '+str((response3.json().get('perfs')['bullet']['rating']))+'\n\n'
      myEmbed1.add_field(name="Bullet", value = ratings, inline=True)
    if 'blitz' in (response3.json().get('perfs')):
      ratings='Games: '+str((response3.json().get('perfs')['blitz']['games']))+'\n'
      ratings=str(ratings)+'Rating: '+str((response3.json().get('perfs')['blitz']['rating']))+'\n\n'
      myEmbed1.add_field(name="Blitz", value = ratings, inline=True)
    if 'rapid' in response3.json().get('perfs'):
      ratings='Games: '+str((response3.json().get('perfs')['rapid']['games']))+'\n'
      ratings=str(ratings)+'Rating: '+str((response3.json().get('perfs')['rapid']['rating']))+'\n\n'
      myEmbed1.add_field(name="Rapid", value = ratings, inline=True)
    if 'classical' in response3.json().get('perfs'):
      ratings='Games: '+str((response3.json().get('perfs')['classical']['games']))+'\n'
      ratings=str(ratings)+'Rating: '+str((response3.json().get('perfs')['classical']['rating']))+'\n\n'
      myEmbed1.add_field(name="Classical", value = ratings, inline=True)
    if 'correspondence' in response3.json().get('perfs'):
      ratings='Games: '+str((response3.json().get('perfs')['correspondence']['games']))+'\n'
      ratings=str(ratings)+'Rating: '+str((response3.json().get('perfs')['correspondence']['rating']))+'\n\n'
      myEmbed1.add_field(name="Correspondence", value = ratings, inline=True)
    if 'puzzle' in response3.json().get('perfs'):
      puzzles='Puzzles: '+str((response3.json().get('perfs')['puzzle']['games']))+'\n'
      puzzles=str(puzzles)+'Rating: '+str((response3.json().get('perfs')['puzzle']['rating']))+'\n\n'
      myEmbed1.add_field(name="Puzzles", value = puzzles, inline=True)
    if 'storm' in response3.json().get('perfs'):
      puzzles='Runs: '+str((response3.json().get('perfs')['storm']['runs']))+'\n'
      puzzles=str(puzzles)+'Score: '+str((response3.json().get('perfs')['storm']['score']))
      myEmbed1.add_field(name="Puzzle Storm", value = puzzles, inline=True)
    myEmbed1.set_footer(text="For variant ratings use /variantratings")
  await content.response.send_message(embed=myEmbed1)

@client.tree.command(name="variantratings", description="Lichess variant ratings")
async def variantratings(content:discord.Interaction , username:str):
  response3=requests.get (str(f'https://lichess.org/api/user/{username}'))
  otherr=''
  if response3.json().get("error")!="Not found":
      myEmbed1 = discord.Embed(title="Patzer Bot", description="User variant ratings (if any)",color=0x00ff00)
      if 'chess960' in response3.json().get('perfs'):
        otherr='Games: '+str((response3.json().get('perfs')['chess960']['games']))+'\n'
        otherr=str(otherr)+'Rating: '+str((response3.json().get('perfs')['chess960']['rating']))+'\n\n'
        myEmbed1.add_field(name="Chess960", value = otherr, inline=True)
      if 'crazyhouse' in response3.json().get('perfs'):
        otherr='Games: '+str((response3.json().get('perfs')['crazyhouse']['games']))+'\n'
        otherr=str(otherr)+'Rating: '+str((response3.json().get('perfs')['crazyhouse']['rating']))+'\n\n'
        myEmbed1.add_field(name="Crazyhouse", value = otherr, inline=True)
      if 'antichess' in response3.json().get('perfs'):
        otherr='Games: '+str((response3.json().get('perfs')['antichess']['games']))+'\n'
        otherr=str(otherr)+'Rating: '+str((response3.json().get('perfs')['antichess']['rating']))+'\n\n'
        myEmbed1.add_field(name="AntiChess", value = otherr, inline=True)
      if 'atomic' in response3.json().get('perfs'):
        otherr='Games: '+str((response3.json().get('perfs')['atomic']['games']))+'\n'
        otherr=str(otherr)+'Rating: '+str((response3.json().get('perfs')['atomic']['rating']))+'\n\n'
        myEmbed1.add_field(name="Atomic", value = otherr, inline=True)
      if 'horde' in response3.json().get('perfs'):
        otherr='Games: '+str((response3.json().get('perfs')['horde']['games']))+'\n'
        otherr=str(otherr)+'Rating: '+str((response3.json().get('perfs')['horde']['rating']))+'\n\n'
        myEmbed1.add_field(name="Horde", value = otherr, inline=True)
      if 'kingOfTheHill' in response3.json().get('perfs'):
        otherr='Games: '+str((response3.json().get('perfs')['kingOfTheHill']['games']))+'\n'
        otherr=str(otherr)+'Rating: '+str((response3.json().get('perfs')['kingOfTheHill']['rating']))+'\n\n'
        myEmbed1.add_field(name="KingOfTheHill", value = otherr, inline=True)
      if 'racingKings' in response3.json().get('perfs'):
        otherr='Games: '+str((response3.json().get('perfs')['racingKings']['games']))+'\n'
        otherr=str(otherr)+'Rating: '+str((response3.json().get('perfs')['racingKings']['rating']))+'\n\n'
        myEmbed1.add_field(name="Racing Kings", value = otherr, inline=True)
      if 'threeCheck' in response3.json().get('perfs'):
        otherr='Games: '+str((response3.json().get('perfs')['threeCheck']['games']))+'\n'
        otherr=str(otherr)+'Rating: '+str((response3.json().get('perfs')['threeCheck']['rating']))+'\n\n'
        myEmbed1.add_field(name="3-Check", value = otherr, inline=True)
  else:
    myEmbed1 = discord.Embed(title="Patzer Bot", description="User not found",color=0x00ff00)
  await content.response.send_message(embed=myEmbed1)


@client.tree.command(name='gamegif' , description='GIF of a lichess game')
@commands.cooldown(1,5,commands.BucketType.user)
async def gamegif(content:discord.Interaction, gamelink:str):
 gamelink=gamelink.replace("https://lichess.org/", "")
 gamelink=gamelink.replace("/black", "")
 gamelink=gamelink.replace("/white", "")
 global updatedgamelink
 updatedgamelink=gamelink
 response=requests.get(str(f"https://lichess.org/game/export/gif/{gamelink}.gif"))
 gamelink=(f"https://lichess.org/game/export/gif/{gamelink}.gif")
 if response.status_code == 404:
    myEmbed = discord.Embed(title="Patzer Bot", description="Game not found",color=0x00ff00)
    await content.response.send_message(embed=myEmbed)
 else: 
    await content.response.send_message(gamelink) #view=Gif()
 
#  role1=await content.response.send_message(game)
#  await role1.add_reaction("🔃")
#  reaction,user = await client.wait_for("reaction_add", check=lambda reaction,user: reaction.message==role1 and user==context.author)
#  if str(reaction.emoji) == "🔃":
#    await role1.delete (delay = 0)
#    game=str(f"https://lichess.org/game/export/gif/black/{value1}.gif")
#    await content.response.send_message(game)
#add roles

@client.tree.command(name="swissrankings", description="Lichess swiss tournament: Rankings/Game downloads/FIDE trf download")
async def swissrankings(content:discord.Interaction, tournamentlink:str):
  await content.response.defer(ephemeral=False)
  tournamentlink=tournamentlink.replace("https://lichess.org/swiss/", "")
  response4=requests.get (f'https://lichess.org/api/swiss/{tournamentlink}/results')
  if response4.status_code != 404:
    myEmbed = discord.Embed(title="Patzer Bot", description="Swiss Tournament Database \n""\u200b",color=0x00ff00)
    a=(f"https://lichess.org/swiss/{tournamentlink}.trf")
    buttons=Empty()
    buttons.add_item(discord.ui.Button(label="Download TRF",style=discord.ButtonStyle.link,url=a))
    b=(f"https://lichess.org/api/swiss/{tournamentlink}/games")
    buttons.add_item(discord.ui.Button(label="Download Games",style=discord.ButtonStyle.link,url=b))
    data = response4.text.strip("\n")
    s = data.split("\n")
    count = 0
    display=''
    for i in s:
      dict = json.loads(i)
      title = ''
      if (dict.get("title") != None):
        title = dict.get("title")
      Sno=dict.get("rank")
      ranking=str(Sno)+'. '+title+' '+str(dict.get("username"))+' ('+str(dict.get("rating"))+') Performance: '+str(dict.get("performance"))+'\n'
      display=display+ranking
      count = count + 1
      if (count == 10):
        break
    myEmbed.add_field(name="Top 10:", value =display,inline=False)
    await content.followup.send(embed=myEmbed, view=buttons)
  else:
    myEmbed = discord.Embed(title="Patzer Bot", description="Swiss tournament not found",color=0x00ff00)
    await content.followup.send(embed=myEmbed)

#response4=requests.get ('https://lichess.org/api/swiss/g7aovChl/results')
#print (response4.json().get('rank'))
#defer

@client.tree.command(name="arenarankings" , description="Lichess arena tournament: Ranking/Game download")
async def arenarankings(content:discord.Interaction, tournamentlink:str):
  tournamentlink=tournamentlink.replace("https://lichess.org/tournament/", "")
  await content.response.defer(ephemeral=False)
  response4=requests.get (f'https://lichess.org/api/tournament/{tournamentlink}/results')
  if response4.status_code!=404:
    myEmbed = discord.Embed(title="Patzer Bot", description="Arena Tournament Database\n""\u200b",color=0x00ff00)
    a=(f"https://lichess.org/api/tournament/{tournamentlink}/games")
    buttons=Empty()
    buttons.add_item(discord.ui.Button(label="Download Games",style=discord.ButtonStyle.link,url=a))
    data = response4.text.strip("\n")
    s = data.split("\n")
    count = 0
    display=''
    for i in s:
      dict = json.loads(i)
      title = ''
      if (dict.get("title") != None):
        title = dict.get("title")
      ranking=str(json.loads(i).get("rank"))+'. '+str(title)+' '+str(json.loads(i).get("username"))+' ('+str(json.loads(i).get("rating"))+')\n**Points:** '+str(json.loads(i).get("score"))+'\n**Performance:** '+str(json.loads(i).get("performance"))+'\n\n'
      display=display+ranking
      count=count+1
      if (count == 10):
        break
    myEmbed.add_field(name="Top 10:", value =display,inline=False)
    await content.followup.send(embed=myEmbed, view=buttons)
  else:
    myEmbed = discord.Embed(title="Patzer Bot", description="Arena tournament not found",color=0x00ff00)
    await content.followup.send(embed=myEmbed)
#-----------------------------------------------------------
@client.tree.command(name="teamrankings", description='Lichess team tournament: Ranking/Game download')
async def teamrankings(content:discord.Interaction, tournamentlink:str):
  tournamentlink=tournamentlink.replace("https://lichess.org/tournament/", "")
  await content.response.defer(ephemeral=False)
  response4=requests.get (f"https://lichess.org/api/tournament/{tournamentlink}/teams")
  if response4.status_code!=404:
    myEmbed = discord.Embed(title="Patzer Bot", description="Team Arena Tournament Database \n""\u200b",color=0x00ff00)
    a=(f"https://lichess.org/api/tournament/{tournamentlink}/games")
    buttons=Empty()
    buttons.add_item(discord.ui.Button(label="Download Games",style=discord.ButtonStyle.link,url=a))
    lengthd = len(response4.json().get('teams'))
    display=''
    if lengthd >=10:
      for a in range (0,10):
        teamevent= str(response4.json().get('teams')[a]['rank'])+'. Team '+str(response4.json().get('teams')[a]['id'])+' (Score: '+str(response4.json().get('teams')[a]['score'])+')\n'
        display=display+teamevent
    else:
      for a in range (0,lengthd):
        teamevent= str(response4.json().get('teams')[a]['rank'])+'. Team '+str(response4.json().get('teams')[a]['id'])+' (Score: '+str(response4.json().get('teams')[a]['score'])+')'
        display=display+teamevent
    myEmbed.add_field(name="Top 10:", value =display,inline=False)
    await content.followup.send(embed=myEmbed, view=buttons)
  else:
    myEmbed = discord.Embed(title="Patzer Bot", description="Team arena tournament not found",color=0x00ff00)
    await content.followup.send(embed=myEmbed)
                                        
@client.tree.command(name="arenabyuser", description="Upcoming Lichess arenas created by a user (if any)")
async def arenabyuser(content:discord.Interaction, username:str):
  response4=requests.get(f'https://lichess.org/api/user/{username}/tournament/created')
  if response4.status_code!=404:
    data = response4.text.strip("\n")
    s = data.split("\n")
    myEmbed = discord.Embed(title="Patzer Bot", description="Tournaments made by Individuals.\n",color=0x00ff00)
    for i in s:
      if (i != ''):
        created=json.loads(i).get("status")
        if created !=30:
          name=(json.loads(i).get("fullName"))
          if json.loads(i).get('clock')['limit'] < 60:
            timecontrolduration=str(json.loads(i).get('clock')['limit'])+'sec+'+str( json.loads(i).get('clock')['limit'])
          else:
            timecontrolduration=str(int(json.loads(i).get('clock')['limit']/60))+'+'+ str(json.loads(i).get('clock')['increment'])
          duration=str(json.loads(i).get('minutes'))
          linking='https://lichess.org/tournament/'.strip()+json.loads(i).get('id')
          entire=str(name)+'\n'+str(timecontrolduration)+' Matches for '+str(duration)+' Minutes\n'+str(linking)+'\n'
          myEmbed.add_field(name="\u200b", value = entire, inline=False)
  else:
    myEmbed = discord.Embed(title="Patzer Bot", description="User not found",color=0x00ff00)
  await content.response.send_message(embed=myEmbed)


@client.tree.command(name="downloadgames", description="Download lichess games of a user")
async def downloadgames(content: discord.Interaction, username:str):
  a=f"https://lichess.org/api/games/user/{username}"
  #if a.status_code!=404:
  buttons=Empty()
  buttons.add_item(discord.ui.Button(label="Download",style=discord.ButtonStyle.link,url=a))
  myEmbed = discord.Embed(title="Patzer Bot", description=(f"Click below to download all games of **{username}** in PGN\nSpeed= 20 Games per Second"),color=0x00ff00)
  myEmbed.add_field(name="\u200b", value ="Note: If no games were played/user does not exist, the downloaded file will be empty.", inline=False)
  #await content.response.send_message(embed=myEmbed, view=buttons)
  await content.response.send_message(embed=myEmbed, view=buttons)
  #else:
  #myEmbed = discord.Embed(title="Patzer Bot", description="User not found",color=0x00ff00)
  #await content.response.send_message(embed=myEmbed)


#----------------------------------------------------------------
#CHESSCOM COMMANDS

@client.tree.command(name="chesscomclub", description="Chess.com club info")
@commands.cooldown(1,5,commands.BucketType.user)
async def chesscomclub(content:discord.Interaction, clubname:str):
 clubname= clubname.replace(" ", "-")
 response3=requests.get(f"https://api.chess.com/pub/club/{clubname}",headers=headers)
 if response3.status_code!=404:
  newchess='**Club Name: **'+str(response3.json().get('name'))+'\n**Members: **'+str(response3.json().get('members_count'))+'\n**Visibility: **'+str(response3.json().get('visibility'))+'\n**Location: **'+str(response3.json().get('location'))
  myEmbed = discord.Embed(title="Patzer Bot", description=newchess,color=15548997)
  if (response3.json().get('icon') != None):
    myEmbed.set_thumbnail(url=str(response3.json().get('icon')))
  buttons=Empty()
  buttons.add_item(discord.ui.Button(label="Join",style=discord.ButtonStyle.link,url=response3.json().get('join_request')))
  await content.response.send_message(embed=myEmbed, view=buttons)
 else:
  myEmbed = discord.Embed(title="Patzer Bot", description="Club not found",color=15548997)
  await content.response.send_message(embed=myEmbed)

@client.tree.command(name="chesscomuserinfo", description="User info of chess.com user")
async def chesscomuserinfo(content: discord.Interaction, username:str):
  response3=requests.get (f'https://api.chess.com/pub/player/{username}',headers=headers)
  if response3.status_code!=404:
    response4=requests.get (f'https://api.chess.com/pub/player/{username}/stats',headers=headers)
    response5=requests.get (f'https://api.chess.com/pub/player/{username}/is-online',headers=headers)
    chesscomprofile='Username: '+str(response3.json().get('username'))+'\n'+'Profile: '+str(response3.json().get('url'))+'\nStatus of Account: '+str(response3.json().get('status'))+'\nFollowers: '+str(response3.json().get('followers'))+'\nStreamer: '+str(response3.json().get('is_streamer'))+'\nOnline: '+str(response5.json().get('online'))
    chesscomavatar=response3.json().get("avatar")
    myEmbed = discord.Embed(title="Patzer Bot", description=chesscomprofile,color=15548997)
    myEmbed.set_thumbnail(url=chesscomavatar)
    if response4.json().get('chess_bullet') != None:
      chesscombullet='Rating: '+str((response4.json().get('chess_bullet')['last']['rating']))+'\nHighest Rating: '+str((response4.json().get('chess_bullet')['best']['rating']))+'\nBest Win: '+str((response4.json().get('chess_bullet')['best']['game']))+'\nWin: '+str((response4.json().get('chess_bullet')['record']['win']))+'\nDraw: '+str((response4.json().get('chess_bullet')['record']['draw']))+'\nLoss: '+str((response4.json().get('chess_bullet')['record']['loss']))
      myEmbed.add_field(name="Bullet", value =chesscombullet, inline=True)

    if response4.json().get('chess_blitz') != None:
      chesscomblitz='Rating: '+str((response4.json().get('chess_blitz')['last']['rating']))+'\nHighest Rating: '+str((response4.json().get('chess_blitz')['best']['rating']))+'\nBest Win: '+str((response4.json().get('chess_blitz')['best']['game']))+'\nWin: '+str((response4.json().get('chess_blitz')['record']['win']))+'\nDraw: '+str((response4.json().get('chess_blitz')['record']['draw']))+'\nLoss: '+str((response4.json().get('chess_blitz')['record']['loss']))
      myEmbed.add_field(name="Blitz", value =chesscomblitz, inline=True)

    if response4.json().get('chess_rapid') != None:
      chesscomrapid='Rating: '+str((response4.json().get('chess_rapid')['last']['rating']))+'\nHighest Rating: '+str((response4.json().get('chess_rapid')['best']['rating']))+'\nBest Win: '+str((response4.json().get('chess_rapid')['best']['game']))+'\nWin: '+str((response4.json().get('chess_rapid')['record']['win']))+'\nDraw: '+str((response4.json().get('chess_rapid')['record']['draw']))+'\nLoss: '+str((response4.json().get('chess_rapid')['record']['loss']))
      myEmbed.add_field(name="Rapid", value =chesscomrapid, inline=True)

    if response4.json().get('tactics') != None:
      chesscomtactics='Highest Rating: '+str((response4.json().get('tactics')['highest']['rating']))+'\nLowest Rating: '+str((response4.json().get('tactics')['lowest']['rating']))
      myEmbed.add_field(name="Tactics", value =chesscomtactics, inline=True)

    if response4.json().get('puzzle_rush') != None:
      puzzlerush='Matches: '+str((response4.json().get('puzzle_rush')['best']['total_attempts']))+'\nScore: '+str((response4.json().get('puzzle_rush')['best']['score']))
      myEmbed.add_field(name="Puzzle Rush", value =puzzlerush, inline=True)

    if response4.json().get('lessons') != None:
      chesscomlessons='Highest Rating: '+str((response4.json().get('lessons')['highest']['rating']))+'\nLowest Rating: '+str((response4.json().get('lessons')['lowest']['rating']))
      myEmbed.add_field(name="Puzzle Rush", value =chesscomlessons, inline=True)
  else:
    myEmbed = discord.Embed(title="Patzer Bot", description="User not found",color=15548997)
  await content.response.send_message(embed=myEmbed)

@client.tree.command(name="chesscomdownload", description="Download Chess.com games of a person")
async def chesscomdownload(content:discord.Interaction, username:str, year:str, monthnumber:str):
  response3=requests.get (f'https://api.chess.com/pub/player/{username}',headers=headers)
  if response3.status_code!=404:
    a=(f"https://api.chess.com/pub/player/{username}/games/{year}/{monthnumber}/pgn")
    buttons=Empty()
    buttons.add_item(discord.ui.Button(label="Download",style=discord.ButtonStyle.link,url=a))
    myEmbed = discord.Embed(title="Patzer Bot", description=(f"Click below to download the PGN of **{username}**'s games in **{monthnumber}/{year}**"),color=15548997)
    myEmbed.add_field(name="\u200b", value ="Note: If no games were played in the duration, the downloaded file will be empty.", inline=False)
    await content.response.send_message(embed=myEmbed, view=buttons)
  else:
    myEmbed = discord.Embed(title="Patzer Bot", description="User not found",color=15548997)
    await content.response.send_message(embed=myEmbed)

@client.tree.command(name="chesscomleaderboard", description='Chess.com leaderboard (Formats: daily, rapid, blitz, bullet, lessons, tactics)')
async def chesscomleaderboard(content:discord.Interaction, gameformat:str):
  if gameformat=="rapid" or gameformat=="blitz" or gameformat=="bullet":
    actualgameformat="live_"+gameformat
  response3=requests.get ('https://api.chess.com/pub/leaderboards',headers=headers)
  myEmbed = discord.Embed(title="Patzer Bot", description=("Leaderboard"),color=15548997)
  finalString = ''
  for a in range (0,10):
    username=str(response3.json().get(actualgameformat)[a]['username'])
    url=str(response3.json().get(actualgameformat)[a]['url'])
    Sno=a+1
    Sno=str(Sno)+'. '
    if 'title' in response3.json().get(actualgameformat)[a]:
      playertitle= str(response3.json().get(actualgameformat)[a]['title'])+' '
      finalString = finalString + str(Sno)+str(playertitle)+"["+username+"]("+url+")\n"
    else:
      finalString = finalString + str(Sno)+"["+username+"]("+url+")\n"
  myEmbed.add_field(name="\u200b", value = finalString, inline=False)
  await content.response.send_message(embed=myEmbed)

#-----------------Classes------------------------

# class PersistentViewBot(commands.Bot):
#   def __init__(self):
#     intents=discord.Intents().all()
#     super().__init__(command_prefix=commands.when_mentioned_or('p.'), intents=intents)
#   async def setup_hook(self) -> None:
#     self.add_view(Empty())
#     self.add_view(Gif())

# client=PersistentViewBot()

class Empty(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    async def Empty(self,content:discord.Interaction):
        await content.response.send_message(view=self)

class Gif(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=None)
    @discord.ui.button(label="Flip",style=discord.ButtonStyle.gray, emoji="🔄", custom_id="1")
    async def Gif(self, content:discord.Interaction,button:discord.ui.Button):
      count=2
      if count%2==0:
        game=(f"https://lichess.org/game/export/gif/black/{updatedgamelink}.gif")
        count=count+1
      else:
        game=(f"https://lichess.org/game/export/gif/{updatedgamelink}.gif")
        count=count+1
      await content.response.edit_message(content=game)

client.run(TOKEN)