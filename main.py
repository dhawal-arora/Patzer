import discord
import os
from discord.ext import commands
import requests
import json
import berserk

token =os.getenv('Lichesstoken')
session = berserk.TokenSession(token)
lichess= berserk.Client(session=session)
tournaments = lichess.tournaments.get()
lengthinfo=len(tournaments['created'])
lengthstarted=len(tournaments['started'])

client = commands.Bot(command_prefix=['Ptz.','ptz.','p.','P.'], intents=discord.Intents.all())
client.remove_command("help")

@client.event
async def on_ready():
  print ('We have logged in as {0.user}' .format (client))
  await client.wait_until_ready()
  await client.change_presence(activity=discord.Game(name="Bot commands down due to implementation of new slash commands "))
#Retrieve Data From Chess.com & Lichess | Command: p.help
  await client.tree.sync()
  print(f"The totat number is {str(len(client.tree.sync()))}")


@client.tree.command(name="help", description="Basic help command")
@commands.cooldown(1,5,commands.BucketType.user)
async def help(content: discord.Interaction):
   myEmbed = discord.Embed(title="Patzer Bot", description="Write the command in the chat below. \n""\u200b",color=0x00ff00)
   myEmbed.add_field(name="Commands List:", value ="**p.help**-List of bot commands\n**p.about**-Learn more about the bot\n**p.lichessupcoming**-List of upcoming lichess tournaments\n""**p.lichessstarted**-List of started lichess tournaments\n""**p.lichessgames [Player 1] [Player 2]**-Find scoret]**-Chess.com Top 10 Leaderboard\n**p.swisstournament [Tournament ID]**er\n\nJoin our server and view #preview-chess-area for help in using a command\n\n", inline=False)
   myEmbed.add_field(name="\u200b \n""SUPPORT PATZER BOT:", value = "[Add bot to your server](https://discord.com/api/oauth2/authorize?client_id=803120439550279690&permissions=519233&scope=bot)\n""[Join our server](https://discord.gg/cdfUp5Zqs7)\n""[Vote for us](https://top.gg/bot/803120439550279690)\n ", inline=False)
   await content.response.send_message(embed=myEmbed)

@client.tree.command(name="about")
@commands.cooldown(1,5,commands.BucketType.user)
async def about(content: discord.Interaction):
   myEmbed = discord.Embed(title="About Us", description="Hi! My name is Patzer Bot. I\'m one of the FINEST Event advertisement discord bot. Get regular updates regarding various events and tournaments taking place throughout various servers. Organizers may get their events featured through me .It will then be shared to various servers, increasing the amount of people participating and improving the audience. Patzer also has dedicated chess commands to find various lichess tournaments/clubs etc! Use **p.addevent** for more details on getting your event promoted. Use **p.help** to view my simple bot commands!\n\n", color=0x00ff00)
   myEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/782500664793759744/808578357893267477/Screenshot_714.png")
   myEmbed.add_field(name="\u200b \n""SUPPORT PATZER BOT:", value = "[Add bot to your server](https://discord.com/api/oauth2/authorize?client_id=803120439550279690&permissions=519233&scope=bot)\n""[Join our server](https://discord.gg/cdfUp5Zqs7)\n""[Vote for us](https://top.gg/bot/803120439550279690)\n ", inline=False)
   await content.response.send_message(embed=myEmbed)

@client.tree.command(name="lichessgames", description="Score between two players")
@commands.cooldown(1,5,commands.BucketType.user)
async def lichessgames(content: discord.Interaction, player1:str, player2:str):
  response3=requests.get(str(f"https://lichess.org/api/crosstable/{player1}/{player2}"))
  Total='Total Games Played: '+str(response3.json().get('nbGames'))
  Player1 = list(response3.json().get('users').keys())[0]
  Player1Score = list(response3.json().get('users').values())[0]
  Player2= list(response3.json().get('users').keys())[1] 
  Player2Score= list(response3.json().get('users').values())[1] 
  whole='Current Scores:'+'\n\n'+str(Player1)+': '+str(Player1Score)+'\n\n'+str(Player2)+': '+str(Player2Score)+'\n\n'+str(Total)
  myEmbed = discord.Embed(title="Patzer Bot: Chess Area", description=whole,color=0x00ff00)
  await content.response.send_message(embed=myEmbed)

@client.tree.command(name="chesscomclub", description="Chess.com club Info")
@commands.cooldown(1,5,commands.BucketType.user)
async def chesscomclub(content:discord.Interaction, clubname:str):
 value= value.replace(" ", "-")
 response3=requests.get (str(f"https://api.chess.com/pub/club/{clubname}"))
 newchess='**Club Name: **'+str(response3.json().get('name'))+'\n**Members: **'+str(response3.json().get('members_count'))+'\n**Visibility: **'+str(response3.json().get('visibility'))+'\n**Location: **'+str(response3.json().get('location'))+'**\nJoining Link: **'+str(response3.json().get('join_request'))
 myEmbed = discord.Embed(title="Patzer Bot: Chess Area", description=newchess,color=0x00ff00)
 if (response3.json().get('icon') != None):
   myEmbed.set_thumbnail(url=str(response3.json().get('icon')))
 await content.response.send_message(embed=myEmbed)


# @client.tree.command(name="lichessupcoming", description="Upcoming lichess tournament")
# @commands.cooldown(1,60,commands.BucketType.user)
# async def lichessupcoming(content:discord.Interaction):
#   myEmbed = discord.Embed(title="Patzer Bot: Chess Area", description="All tournaments shown below will have a minimum of 15 players.\n Only the top 4 events according to the number of players are shown.\n If nothing is shown it indicates that no tournaments meet the requirements.\n\nList of upcoming arena tournaments hosted by lichess:",color=0x00ff00)
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
#   myEmbed = discord.Embed(title="Patzer Bot: Chess Area", description="All tournaments shown below will have a minimum of 20 players.\n Only the top 4 events according to the number of players are shown.\n If nothing is shown it indicates that no tournaments meet the requirements.\n\nList of started arena tournaments hosted by lichess:",color=0x00ff00)
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

@client.tree.command(name="lichessuserinfo", description="Lichess user info (follow following info issue)")
async def lichessuserinfo(content:discord.Interaction, username:str):
  response3=requests.get (str(f'https://lichess.org/api/user/{username}'))
  allinfo=str('Username: '+str(response3.json().get('username'))+'\n'+
  'Title: '+str(response3.json().get('title'))+'\n'+
  'Lichess Patron: '+str(response3.json().get('patron'))+'\n'+
  'Profile Link: '+str(response3.json().get('url'))+'\n'+
  'Online Status: '+str(response3.json().get('online'))+'\n\n'+
  'All Games Played: '+str(response3.json().get('count')['all'])+'\n'+
  'Rated Games: '+str(response3.json().get('count')['rated'])+'\n'+
  'Wins: '+str(response3.json().get('count')['win'])+'\n'+
  'Draws: '+str(response3.json().get('count')['draw'])+'\n'+
  'Losses: '+str(response3.json().get('count')['loss'])+'\n'+
  'Completion Rate: '+str(response3.json().get('completionRate'))+'%\n'+
  'Games Playing Now: '+str(response3.json().get('count')['playing'])+'\n\n'+
  'Followers: '+str(response3.json().get('nbFollowers'))+'\n'+
  'Following: '+str(response3.json().get('nbFollowing'))+'\n\u200b')
  myEmbed1 = discord.Embed(title="Patzer Bot: Chess Area", description=allinfo,color=0x00ff00)
  ratings=''
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
  myEmbed1.set_footer(text="For variant ratings use p.lichessvariantratings [username]")
  await content.response.send_message(embed=myEmbed1)
#----------------------------------------------
@client.tree.command(name="lichessvariantratings", description="Lichess variant ratings (less games highest rating)")
async def lichessvariantratings(content:discord.Interaction , username:str):
  myEmbed1 = discord.Embed(title="Patzer Bot: Chess Area", description="More Ratings Info:",color=0x00ff00)
  response3=requests.get (str(f'https://lichess.org/api/user/{username}'))
  otherr=''
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

  await content.response.send_message(embed=myEmbed1)

@client.tree.command(name="chesscomuserinfo", description="User Info of chess.com user (no profile photo)")
async def chesscomuserinfo(content: discord.Interaction, username:str):
  response3=requests.get (str(f'https://api.chess.com/pub/player/{username}'))
  response4=requests.get (str(f'https://api.chess.com/pub/player/{username}/stats'))
  response5=requests.get (str(f'https://api.chess.com/pub/player/{username}/is-online'))
  chesscomprofile='Username: '+str(response3.json().get('username'))+'\n'+'Profile: '+str(response3.json().get('url'))+'\nStatus of Account: '+str(response3.json().get('status'))+'\nFollowers: '+str(response3.json().get('followers'))+'\nStreamer: '+str(response3.json().get('is_streamer'))+'\nOnline: '+str(response5.json().get('online'))

  myEmbed = discord.Embed(title="Patzer Bot: Chess Area", description=chesscomprofile,color=0x00ff00)

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
  await content.response.send_message(embed=myEmbed)

@client.tree.command(name="chesscomdownload", description="Download chesscom games of a person (now with time stamps)")
async def chesscomdownload(content:discord.Interaction, username:str, year:str, monthnumber:str):
  a=(f"https://api.chess.com/pub/player/{username}/games/{year}/{monthnumber}/pgn")
  click='Click Here'
  b='['+click+']'+'('+a+')'
  myEmbed = discord.Embed(title="Patzer Bot: Chess Area\nClick here to download the games in PGN", description=b,color=0x00ff00)
  await content.response.send_message(embed=myEmbed)

@client.tree.command(name='lichessgif' , description='Send a GIF of a lichess game (no customization yet but roles coming)')
@commands.cooldown(1,5,commands.BucketType.user)
async def lichessgif(content:discord.Interaction, gameid:str):
 game=str(f"https://lichess.org/game/export/gif/{gameid}.gif")
 await content.response.send_message(game)
#  role1=await content.response.send_message(game)
#  await role1.add_reaction("🔃")
#  reaction,user = await client.wait_for("reaction_add", check=lambda reaction,user: reaction.message==role1 and user==context.author)
#  if str(reaction.emoji) == "🔃":
#    await role1.delete (delay = 0)
#    game=str(f"https://lichess.org/game/export/gif/black/{value1}.gif")
#    await content.response.send_message(game)

@client.tree.command(name="lichessswisstournament", description="Lichess Swiss Tournament Ranking/game downloads/trf download")
async def lichessswisstournament(content:discord.Interaction, tournamentid:str):
  myEmbed = discord.Embed(title="Patzer Bot: Chess Area", description="Swiss Tournament Database \n""\u200b",color=0x00ff00)
  a=(f"https://lichess.org/swiss/{tournamentid}.trf")
  click='Click Here'
  b='['+click+']'+'('+a+')'
  myEmbed.add_field(name="Tournament Report File:", value = b, inline=False)
  a=(f"https://lichess.org/api/swiss/{tournamentid}/games")
  click='Click Here'
  b='['+click+']'+'('+a+')'
  myEmbed.add_field(name="Download Games:", value = b, inline=False)
  response4=requests.get (f'https://lichess.org/api/swiss/{tournamentid}/results')
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
  await content.response.send_message(embed=myEmbed)

#response4=requests.get ('https://lichess.org/api/swiss/g7aovChl/results')
#print (response4.json().get('rank'))

@client.tree.command(name="lichessarenatournament" , description='Lichess Arena Tournament Ranking Download (Recently Completed tourney might have issue)')
async def lichessarenatournament(content:discord.Interaction, tournamentid:str):
  myEmbed = discord.Embed(title="Patzer Bot: Chess Area", description="Arena Tournament Database\n""\u200b",color=0x00ff00)
  a=(f"https://lichess.org/api/tournament/{tournamentid}/games")
  click='Click Here'
  b='['+click+']'+'('+a+')'
  myEmbed.add_field(name="Download Games:", value = b, inline=False)
  response4=requests.get (f'https://lichess.org/api/tournament/{tournamentid}/results')
  data = response4.text.strip("\n")
  s = data.split("\n")
  count = 0
  display=''
  for i in s:
    dict = json.loads(i)
    title = ''
    if (dict.get("title") != None):
      title = dict.get("title")
    ranking=str(json.loads(i).get("rank"))+'. '+str(title)+' '+str(json.loads(i).get("username"))+' ('+str(json.loads(i).get("rating"))+')'' Points: '+str(json.loads(i).get("score"))+' Performance: '+str(json.loads(i).get("performance"))+'\n'
    display=display+ranking
    count=count+1
    if (count == 10):
      break
  myEmbed.add_field(name="Top 10:", value =display,inline=False)
  await content.response.send_message(embed=myEmbed)
#-----------------------------------------------------------
@client.tree.command(name="lichessteamtournament", description='Lichess Team Tournament Ranking+download (spacing issue)')
async def lichessteamtournament(content:discord.Interaction, tournamentid:str):
  myEmbed = discord.Embed(title="Patzer Bot: Chess Area", description="Team Arena Tournament Database \n""\u200b",color=0x00ff00)
  a=(f"https://lichess.org/api/tournament/{tournamentid}/games")
  click='Click Here'
  b='['+click+']'+'('+a+')'
  myEmbed.add_field(name="Download Games:", value = b, inline=False)
  response4=requests.get (f"https://lichess.org/api/tournament/{tournamentid}/teams")
  lengthd = len(response4.json().get('teams'))
  if lengthd >=10:
    for a in range (0,10):
      teamevent= str(response4.json().get('teams')[a]['rank'])+'. Team '+str(response4.json().get('teams')[a]['id'])+' (Score: '+str(response4.json().get('teams')[a]['score'])+')'
      myEmbed.add_field(name="\u200b", value = teamevent, inline=False)
  else:
    for a in range (0,lengthd):
      teamevent= str(response4.json().get('teams')[a]['rank'])+'. Team '+str(response4.json().get('teams')[a]['id'])+' (Score: '+str(response4.json().get('teams')[a]['score'])+')'
      myEmbed.add_field(name="\u200b", value = teamevent, inline=False)
  await content.response.send_message(embed=myEmbed)
#----------------------------------------------------------------
@client.tree.command(name="chesscomleaderboard", description='chesscom Leaderboard (Formats:daily,live_rapid,live_blitz,live_bullet,lessons,tactics')
async def chesscomleaderboard(content:discord.Interaction, gameformat:str):
  response3=requests.get ('https://api.chess.com/pub/leaderboards')
  myEmbed = discord.Embed(title="Patzer Bot: Chess Area", description="Leaderboard\n",color=0x00ff00)
  finalString = ''
  for a in range (0,10):
    username=str(response3.json().get(gameformat)[a]['username'])
    url=str(response3.json().get(gameformat)[a]['url'])
    Sno=a+1
    Sno=str(Sno)+'. '
    if 'title' in response3.json().get(gameformat)[a]:
      playertitle= str(response3.json().get(gameformat)[a]['title'])+' '
      finalString = finalString + str(Sno)+str(playertitle)+"["+username+"]("+url+")\n"
    else:
      finalString = finalString + str(Sno)+"["+username+"]("+url+")\n"
  myEmbed.add_field(name="\u200b", value = finalString, inline=False)
  await content.response.send_message(embed=myEmbed)

@client.tree.command(name="lichessuserarena", description="Lichess Arenas created by a user")
async def lichessuserarena(content:discord.Interaction, username:str):
  response4=requests.get(f'https://lichess.org/api/user/{username}/tournament/created')
  data = response4.text.strip("\n")
  s = data.split("\n")
  myEmbed = discord.Embed(title="Patzer Bot: Chess Area", description="Tournaments made by Individuals.\n",color=0x00ff00)
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
        linking='https://lichess.org/swiss/'.strip()+json.loads(i).get('id')
        entire=str(name)+'\n'+str(timecontrolduration)+' Matches for '+str(duration)+' Minutes\n'+str(linking)+'\n'
        myEmbed.add_field(name="\u200b", value = entire, inline=False)
  await content.response.send_message(embed=myEmbed)


@client.tree.command(name="lichessdownload", description="Download lichess games of a user")
async def lichessdownload(content: discord.Interaction, username:str):
  a=(f"https://lichess.org/api/games/user/{username}")
  click='Click Here'
  b='['+click+']'+'('+a+')'
  myEmbed = discord.Embed(title="Patzer Bot: Chess Area\nClick here to download the games in PGN\n(Speed= 20 Games per Second)", description=b,color=0x00ff00)
  await content.response.send_message(embed=myEmbed)


client.run(os.getenv('TOKEN'))
