@client.command(name="advertising")
@commands.cooldown(1,5,commands.BucketType.user)
async def advertsing(context):
   myEmbed = discord.Embed(title="Patzer Bot: Event Advertising", description="Write the command in the chat below. \n""\u200b",color=0x00ff00)
   myEmbed.add_field(name="Commands List:", value ="**p.upcoming**-List of upcoming events\n""**p.detailsSNo**-To find event details\n""**p.dmSNo**-Export details to DM\n""**p.addevent**-Promote your event \n""(SNo: Serial Number)\n\n", inline=False)
   myEmbed.add_field(name="\u200b \n""SUPPORT PATZER BOT:", value = "[Add bot to your server](https://discord.com/api/oauth2/authorize?client_id=803120439550279690&permissions=519233&scope=bot)\n""[Join our server](https://discord.gg/cdfUp5Zqs7)\n""[Vote for us](https://top.gg/bot/803120439550279690)\n ", inline=False)
   await context.message.channel.send(embed=myEmbed)

@client.command(name="addevent")
@commands.cooldown(1,5,commands.BucketType.user)
async def addevent(context):
   myEmbed = discord.Embed(title="Patzer Bot: Event Advertising", description="Want to get your upcoming events promoted? Want more people to join your event? Get it listed on our BOT! Here are our two advertising options:\n""\u200b",color=0x00ff00)
   myEmbed.add_field(name="BASIC (FREE): \n""\u200b", value = "Event Details:\n"
   "--Event Title/Name :white_check_mark: \n"
   "--Description (1 Line,90 words) :white_check_mark: \n"
   "--Date,Timing,Venue :white_check_mark: \n"
   "--Server Invite Link :white_check_mark:\n"
   "--Other Required Info :x:\n"
   "--Registration Form Link :x:\n"
   "--Link to Social media handle :x: \n"
   "--Brochure/Poster :x:\n"
   "--Logo of Organizing Server :x:\n"
   "--Other External Links :x:\n\n"
   "Event Addition (12-24 Hours) :white_check_mark:\n"
   "Patzer Bot Support (VC & Chat) :white_check_mark:\n"
   "Patzer Bot Premium Support (Quick Response) VC & Chat :x:\n"
   "Info Changes (x1) :white_check_mark:\n"
   "Max Listing Duration (7 Days) \n""\u200b", inline=True)

   myEmbed.add_field(name="PREMIUM (PAID): \n""\u200b", value = "Event Details:\n"
   "--Event Title/Name :white_check_mark: \n"
   "--Description :white_check_mark: \n"
   "--Date,Timing,Venue :white_check_mark: \n"
   "--Server Invite Link :white_check_mark:\n"
   "--Other Required Info :white_check_mark:\n"
   "--Registration Form Link :white_check_mark:\n"
   "--Link to Social media handle :white_check_mark: \n"
   "--Brochure/Poster :white_check_mark:\n"
   "--Logo of Organizing Server :white_check_mark:\n"
   "--Other External Links :white_check_mark:\n\n"
   "Event Addition (Within 12 Hours) :white_check_mark:\n"
   "Patzer Bot Support (VC & Chat) :white_check_mark:\n"
   "Patzer Bot Premium Support (Quick Response) VC & Chat :white_check_mark:\n"
   "Info Changes (x3) :white_check_mark:\n"
   "Max Listing Duration (1 Month) \n", inline=True)
   myEmbed.add_field(name="\u200b", value="**Send your event details to the specifically made text channel in our server.\n[Click here to join](https://discord.gg/cdfUp5Zqs7)**",inline=False)
   myEmbed.set_footer(text="Terms and Conditions Apply. Features mentioned above are be subject to availability")
   await context.message.channel.send(embed=myEmbed)

@client.command(name="upcoming")
@commands.cooldown(1,5,commands.BucketType.user)
async def upcoming(context):
   myEmbed = discord.Embed(title="Patzer Bot: Event Advertising", description="Write the command in the chat below. \n""\u200b",color=0x00ff00)
   myEmbed.add_field(name="UPCOMING EVENTS:", value = "\u200b", inline=False)
   myEmbed.add_field(name="\u200b", value="More events to be featured soon. Use **p.addevent** for details on getting your own events featured! Events are removed within 24 hours after their completion.", inline=False)
   myEmbed.add_field(name="\u200b \n""SUPPORT PATZER BOT:", value = "[Add bot to your server](https://discord.com/api/oauth2/authorize?client_id=803120439550279690&permissions=519233&scope=bot)\n""[Join our server](https://discord.gg/cdfUp5Zqs7)\n""[Vote for us](https://top.gg/bot/803120439550279690)\n ", inline=False)
   await context.message.channel.send(embed=myEmbed)

@client.command(name="details1")
@commands.cooldown(1,5,commands.BucketType.user)
async def details1(context):
   myEmbed = discord.Embed(title="The Serials Chess Tournament by Anish Naik- INR 12000 Prize Fund", description="A prestige chess tournament with various cash prizes and players of all level!", color=0x00ff00)
   myEmbed.add_field(name="Date:", value="6/3/2021\n7:30PM Ist",inline=True)
   myEmbed.add_field(name="Platform:", value="Lichess (Swiss)\n3+1sec each",inline=True)
   myEmbed.add_field(name="Entry Fee:", value="100 INR",inline=True)
   
   myEmbed.set_image(url="https://cdn.discordapp.com/attachments/782500664793759744/812574535131070494/Screenshot_801.png")
   myEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/758063966197907599/812393117415899196/THE_SERIALS.png")
   myEmbed.set_author(name="Anish Naik", url="https://www.youtube.com/c/AnishNaik", icon_url="https://th.bing.com/th/id/OIP.LLfJ7wJM2TgN2iK6aKR2XgHaHa?pid=Api&rs=1")
   myEmbed.add_field(name="Download Brochure:", value = "[CLICK HERE](https://cdn.discordapp.com/attachments/758063966197907599/812392715890720828/THE_SERIALS-finalllllllllllllllllllll.pdf)", inline=True)
   myEmbed.add_field(name="Registration Form:", value = "[CLICK HERE](https://docs.google.com/forms/d/e/1FAIpQLSdbBJGxJbSH_bDx9dO69W7f9VoQ5P21XR12YOCiGz6MaO8jpg/viewform)", inline=True)
   myEmbed.add_field(name="For More Updates:", value = "[JOIN HOST SERVER](https://discord.gg/cy4aQjh4FX)", inline=True)
   myEmbed.add_field(name="Use Referral Code H1BNDDW for 10% OFF!", value="\u200b",inline=True)
   myEmbed.set_footer(text="Export info to DM: Ptz.dm1")

   await context.message.channel.send(embed=myEmbed)