#Unifox Discord bot
#adminComands.py

#---imports---#
#again all likely ARE used, but mainly just when running
import discord
import discord.ext
import time
import datetime
import pickle
from main import Main
from cogs.botSettings import BotSettings
from discord.ext import commands

#---admin commands class---#
#this houses all the commands that only server admin can use
class AdminCommands(commands.Cog, name="Admin Commands", description='Commands for only admin to use'):

	#these two functions probably will be deleted eventually lol
	#they just spam a channel forever, they get started a bit lower
	async def spam1(ctx):
		await ctx.send("spamming")
		await AdminCommands.spam2(ctx)

	async def spam2(ctx):
		await ctx.send("spamming")
		await AdminCommands.spam1(ctx)

	#basic ping command to see if the bot is up
	@commands.command(name='ping', help='used to check if bot is up ig')
	@commands.has_any_role('admin', 'owner')
	async def ping(self, ctx):
		await ctx.send("pong!")  #simple command so that when you type "!ping" the bot will respond with "pong!"
	
	#this command dont work the way I want, not sure if there even is a way to do what I wanted with this
	@commands.command(name='errorlist', help='used to see a list of possible errors ig')
	@commands.has_any_role('admin', 'owner')
	async def errorlist(self, ctx):
		for x in discord.errors:
			await ctx.send(x)
			
	#a command to kick people out of a server
	@commands.command(name='kick', help='used to kick a user with a reason')
	@commands.has_any_role('admin', 'owner')
	async def kick(self, ctx, member: discord.Member, *, reason):
		try:
			await member.kick(reason=reason)
			await ctx.send(f"kicked {member.mention} for {reason}")  #simple kick command to demonstrate how to get and use member mentions
		except:
			await ctx.send("bot does not have the kick members permission!")
	
	#a command to BAN people from a server (i should add an unban ig)
	@commands.command(name='ban', help='used to ban a user with a reason')
	@commands.has_any_role('admin', 'owner')
	async def ban(self, ctx, member: discord.Member, *, reason):
		try:
			await member.ban(reason=reason)
			await ctx.send(f"Hit {member.mention} With the ban hammer for {reason}")  #simple kick command to demonstrate how to get and use member mentions
		except:
			await ctx.send("bot does not have the ban members permission!")
	
	#this is the spam command that starts the 2 functions from before
	#if used requires a bot restart to stop
	@commands.command(name='spam', help="Starts spamming, don't use. Bot will need to be shut down to stop")
	@commands.has_any_role('admin', 'owner')
	async def spam(self, ctx):
		await ctx.send('spamming...')
		await AdminCommands.spam1(ctx)
	
	#a command to mute and unmute someone, this makes them unable to speak in a voice channel
	@commands.command(name='mute', help='mutes a user')
	@commands.has_any_role('admin', 'owner')
	async def mute(self, ctx, member: discord.Member):
		await ctx.send(f"muted {member}")
		await member.mute()
	
	@commands.command(name='unmute', help='unmutes a user')
	@commands.has_any_role('admin', 'owner')
	async def unmute(self, ctx, member: discord.Member):
		await ctx.send(f"unmuted {member}")
		await member.unmute()	
	
	#used to get the server name and ID
	@commands.command(name='guildID', help='gets current guild id')
	@commands.has_any_role('admin', 'owner')
	async def guildID(self, ctx):
		await ctx.send(f"guild: {ctx.guild}")
		await ctx.send(f"has id: {ctx.guild.id}")
	
	#used to get the channel name and ID
	@commands.command(name='channelID', help='gets current channel id')
	@commands.has_any_role('admin', 'owner')
	async def channelID(self, ctx):
		await ctx.send(f"channel: {ctx.channel}")
		await ctx.send(f"has id: {ctx.channel.id}")

	#used to announce something important to every server the bot is in, but only their announcement channels
	@commands.command(name='announceAll', help='sends an @ everyone announcement to every server the bot is in.')
	@commands.has_any_role('admin', 'owner')
	async def announceAll(self, ctx, *, message):
		for guild in Main.bot.guilds:
			for channel in guild.text_channels:
				if str(channel) in BotSettings.announceChannels:
					await channel.send(f'@everyone {message}')

	#used to send a message to every channel of every server the bot is in lol
	@commands.command(name='allChan', help='Sends a message to EVERY channel, in EVERY server, the bot is in. ~~why did i make this~~')
	@commands.has_any_role('admin', 'owner')
	async def allChan(self, ctx, *, message):
		for guild in Main.bot.guilds:
			for channel in guild.text_channels:
				await channel.send(message)

	#to change the bot prefix, or what the bot looks for to see if it should do something
	@commands.command(name='prefix', help='changes the bot prefix, *will need to be set upon bot reset*')
	@commands.has_any_role('admin', 'owner')
	async def prefix(self, ctx, newpre):
		Main.bot.command_prefix = newpre
		BotSettings.setPrefix(newpre)
		await ctx.send(f'prefix now: {newpre}')
		BotSettings.quietSave()

	#used to clear a number of messages from a channel, good for clearing spam
	@commands.command(name='purge', help='deletes the given number of messages from the channel. cannot purge more than 100')
	@commands.has_any_role('admin', 'owner')
	async def purge(self, ctx, messagenum: int):
		if messagenum > 100:
			return await ctx.send('cannot purge more than 100')
		async with ctx.typing():
			async for message in ctx.channel.history(limit=messagenum + 1):
				await message.delete()

	#used to ignore a channel, the bot wont check messages, or for commands
	@commands.command(name='ignore', help='add a channel to ignore bad words in (send this in the channel)')
	@commands.has_any_role('admin', 'owner')
	async def ignore(self, ctx):
		BotSettings.ignoreChannels.append(str(ctx.channel))
		await ctx.send(f'now ignoring this channel')
		BotSettings.quietSave()

	#used to clear a channel from being ignored. must be sent in a non ignored channel (I may change this later idk)
	@commands.command(name='delIgnore', help='remove a channel from the ignore list, use listIgnored to identify the index of the channel. (starts at 0, not 1)', breif='remove a channel from the ignore list')
	@commands.has_any_role('admin', 'owner')
	async def delIgnore(self, ctx, *, channelindex: int):
		await ctx.send(f'now monitoring {BotSettings.ignoreChannels[channelindex]}')
		BotSettings.ignoreChannels.pop(int(channelindex))
		BotSettings.BotSetings.quietSave()

	#gets the list of channels the bot is ignoring
	@commands.command(name='listIgnored', help='lists the ignored channels')
	@commands.has_any_role('admin', 'owner')
	async def listIgnore(self, ctx):
		await ctx.send(BotSettings.ignoreChannels)

	#set the number of warns required for specific actions to happen
	@commands.command(name='setwarns', help='sets the warn limit')
	@commands.has_any_role('admin', 'owner')
	async def setwarns(self, ctx, limit: int):
		BotSettings.setWarnlimit(limit)
		await ctx.send(f'warn limit set to {limit}')
		BotSettings.quietSave()

	#used to warn someone, and keep track of how many warns people have
	#if a user gets to the warn limit, it notifies the person
	#if they then exceed by 1, they are kicked. they can rejoin, but warns are only manually cleared
	#if they exceed by 2, by being kicked and rejoining, they are banned
	@commands.command(name='warn', help='warns given user, and add 1 to the warn counts. WARNING: will kick a user if warn count for them goes above a limit!', brief='warns a user, use help warn to see more')
	@commands.has_any_role('admin', 'owner')
	async def warn(self, ctx, *, member: discord.Member):
		await ctx.send(f'@{member}... you have been warned')
		try:
			BotSettings.warnlist[member] += 1
			if BotSettings.warnlist[member] == BotSettings.warnlimit:
				ctx.send(f'@{member}! you are at the warn limit, once more and you are kicked!')
			if BotSettings.warnlist[member] == BotSettings.warnlimit + 1:
				AdminCommands.kick(ctx, member, 'You have exceeded your warn limit.')
			if BotSettings.warnlist[member] == BotSettings.warnlimit + 2:
				AdminCommands.ban(ctx, member, 'Your warnings were not reset, and you had been kicked but returned. You have now been banned.')
		except:
			BotSettings.warnlist[member] = 1
		BotSettings.quietSave()

	#used to clear a users warnings
	@commands.command(name='delWarn', help='removes given users warnings')
	@commands.has_any_role('admin', 'owner')
	async def delWarn(self, ctx, *, member: discord.Member):
		await ctx.send(f'@{member}, warnings removed!')
		try:
			BotSettings.warnlist[member] -= BotSettings.warnlist[member]
		except:
			await ctx.send(f'{member} has no warnings on record')
		BotSettings.quietSave()

	#used to add a word to the blacklist of words that shall not be spoken
	@commands.command(name='addbadword', aliases = ['abw'], help='used to add a word to a blacklist of words')
	@commands.has_any_role('admin', 'owner')
	async def addbadword(self, ctx, *, word):
		for x in word.split():
			BotSettings.badwords.append(x)
		BotSettings.quietSave()

	#used to manually save the bot settings, shouldnt need to be used, as commands auto save
	@commands.command(name='savesett', help='used to save the bots current settings in case of crash or shutdown', breif='saves bot settings')
	@commands.has_any_role('admin', 'owner')
	async def savesett(self, ctx):
		await ctx.send('saving settings')
		settfile = open('bot.sett', 'wb')
		pickle.dump(BotSettings.botSettingsToSave, settfile)
		settfile.close()
		await ctx.send('settings saved')

	#used to completely wipe a channel of all messages, if purge would take too long
	@commands.command(name='totalwipe', help='completely wipes a channel')
	@commands.has_any_role('admin', 'owner')
	async def totalwipe(self, ctx):
		await ctx.send('wiping channel...')
		time.sleep(5)
		newchan = await ctx.channel.clone(reason='complete channel wipe')
		await ctx.channel.delete(reason='complete channel wipe')
		await newchan.send('channel wiped', delete_after=10)

	#used to completely clear a server, only for if every channel possible has been spammed too much to clear with purge
	#also requires me to come here to replit to allow a clear
	@commands.command(name='SERVERWIPE', help='WARNING: this command competely clears the server! ONLY use if a server reset is needed, such as a large raid.', breif='WARNING: this command competely clears the server!')
	@commands.has_any_role('admin', 'owner')
	async def serverwipe(self, ctx):
		await ctx.send('are you sure? go to replit console to confirm')
		confirm = input('CONFIRM SERVER WIPE? (Y/N)')
		if confirm.lower() == 'y':
			await ctx.send('CLEARING SERVER')
			for channel in ctx.guild.text_channels:
				if not channel.name in BotSettings.clearIgnore:
					await channel.clone(reason='SERVER WIPE')
					await channel.delete(reason='SERVER WIPE')
				else:
					print(f"channel ignored: {channel}")
		elif confirm.lower() == 'n':
			print('wipe cancelled')
			await ctx.send('wipe cancelled from replit console')

	#add a channel to the channels pinged upon an announcement command
	@commands.command(name='addannounce', help='used to add a channel to the announcement list')
	@commands.has_any_role('admin', 'owner')
	async def addannounce(self, ctx, *, channel):
		BotSettings.announceChannels.append(channel)
		BotSettings.quietSave()
		await ctx.send(f'now announcing in {channel} as well')

	#remove a channel from that list
	@commands.command(name='delannounce', help='used to remove a channel from the announcement list, use listannounce to identify the index of the channel. (starts at 0, not 1)', breif='remove a channel from the announcement list')
	@commands.has_any_role('admin', 'owner')
	async def delannounce(self, ctx, *, chanindex: int):
		await ctx.send(f'no longer announcing in {BotSettings.announceChannels[chanindex]}')
		BotSettings.announceChannels.pop(chanindex)
		BotSettings.quietSave()

	#and show the channels in the list
	@commands.command(name='listannounce', help='lists the announcement channels')
	@commands.has_any_role('admin', 'owner')
	async def listannounce(self, ctx):
		await ctx.send(BotSettings.announceChannels)

	#add channel to no be cleared on server clear
	@commands.command(name='addClearIgnore', help='adds a channel to be ignored upon serverwipe', aliases=['aci'])
	@commands.has_any_role('admin', 'owner')
	async def addClearIgnore(self, ctx, *, channel):
		BotSettings.clearIgnore.append(channel)
		BotSettings.quietSave()
		await ctx.send(f"{channel} won't be cleared")

	#remove server from list that won't be cleared
	@commands.command(name='delClearIgnore', help='removes a channel from being ignored upon serverwipe', aliases=['dci'])
	@commands.has_any_role('admin', 'owner')
	async def delClearIgnore(self, ctx, *, channelid: int):
		await ctx.send(f"{BotSettings.clearIgnore[channelid]} will now be cleared")
		BotSettings.clearIgnore.pop(channelid)
		BotSettings.quietSave()

#and list the channels that won't be cleared
	@commands.command(name='listClearIgnore', help='lists the clear ignored channels', aliases=['lci'])
	@commands.has_any_role('admin', 'owner')
	async def listClearIgnore(self, ctx):
		await ctx.send(BotSettings.clearIgnore)

#a setup function required in all files that have commands, used by discord to load the commands into the bot
def setup(bot):
	bot.add_cog(AdminCommands(bot))