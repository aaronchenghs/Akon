from AkonKey import *

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

global b_status, vocal, voice
b_status = False


#   event on_ready():
#   prints to the terminal when AKON is ready for use
@client.event
async def on_ready():
    print("AKON ready!")


#   command check_b_stat():
#   Sends a message to discord channel to confirm b status
#   @param: ctx - context, reference to get channel
@client.command()
async def check_b_stat(ctx):
    global b_status
    await ctx.send(f"{b_status}")


#   command join():
#   Forces a join to the commander's voice channel !!THIS METHOD IS BROKEN!!
#   @param: ctx - context, reference to get channel
@client.command(pass_context=True)
async def join(ctx):
    global vocal, voice, b_status

    if ctx.author.voice:

        if len(client.voice_clients) > 0:  # If Akon is already connected somewhere
            await ctx.guild.voice_client.disconnect()
            await disconnectAkon(vocal)
            b_status = False

        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You're not in a voice channel")


#   command leave():
#   Forces Akon to leave it's channel
#   @param: ctx - context, reference to get channel
@client.command(pass_context=True)
async def leave(ctx):
    global b_status
    if len(client.voice_clients) > 0:  # If Akon is already connected somewhere
        b_status = False
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("Akon is not in a channel ya beach")


#   command beautiful(ctx):
#   Joins commander's voice channel and plays the best Akon song
#   @param: ctx - context
@client.command(pass_context=True)
async def beautiful(ctx):
    global b_status, vocal, voice

    if ctx.author.voice:
        if len(client.voice_clients) > 0:  # If Akon is already connected somewhere
            await ctx.guild.voice_client.disconnect()
            await disconnectAkon(vocal)

        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="Beautiful.mp3"))

        b_status = True
    else:
        await ctx.send("You're not in a voice channel :slight_frown: (Or you're just not beautiful)")


#@client.event
#async def on_message(self, message):
    #if(message == "who told han that?"):
        #await message.channel.send("I, Akon, hit senegalese singer and songwriter, did.");

#   event on_voice_state_update():
#   Responds to a change in voice state, joins after 10 seconds if user is alone, plays Lonely
#   @param: member - user whose voice state triggers the event
#           before - channel that user leaves
#           after - channel that user enters
@client.event
async def on_voice_state_update(member, before, after):
    global b_status, vocal, voice

    member_ids = []

    if member == client.user:  # CATCH
        print("catch")
        return

    if after.channel is None:  # User has left a voice channel
        print("User left a voice channel")

        vc = before.channel  # set voice channel to before
        member_ids = getMemids(member_ids, vc)

        if checkAkonPresence(member_ids) is False:  # Doesn't have to do with Akon
            if len(member_ids) == 1:
                await standby()
                member_ids = getMemids(member_ids, vc)

                if len(member_ids) == 1:
                    print("User has been left alone")
                    vocal = await vc.connect()
                    await playLonely(vc, vocal, before.channel.name)
                    return
                else:
                    print("No longer alone")
                    return
            else:
                print("Not Alone")
                return

        ###############################

        if len(member_ids) == 1:  # if user is now alone after somebody leaves, join

            member_ids = getMemids(member_ids, vc)

            #check akon presence
            if checkAkonPresence(member_ids):  # check if akon is already in a voice channel, disconnect
                print("akon is present in a voice channel")
                if b_status:
                    print("beautiful is playing")
                    return
                await disconnectAkon(vocal)

            await standby()

            member_ids = getMemids(member_ids, vc)
            if len(member_ids) == 1:
                vocal = await vc.connect()
                await playLonely(vc, vocal, before.channel.name)
                return

            else:
                print("No longer alone...")

            return

        else:
            if len(member_ids) > 1:  # user is not alone
                print("User Joined, Not alone")
                return

            else:
                await disconnectAkon(vocal)
                b_status = False

    #################################

    else:
        if before.channel is not after.channel:  # User joins a new channel
            print(f"User joined \"{after.channel.name}\"")

            if before.channel is not None:
                #check if akon is alone
                vc = before.channel
                member_ids = getMemids(member_ids, vc)

                if checkAkonPresence(member_ids) and len(member_ids) == 1 and b_status is False:
                    await disconnectAkon(vocal)
                #

            vc = member.voice.channel
            member_ids = getMemids(member_ids, vc)

            if len(member_ids) == 1:  # if there is 1 person in the channel

                await standby()

                member_ids = getMemids(member_ids, vc)
                if len(member_ids) == 1:    # recheck for loneliness

                    if len(client.voice_clients) > 0:  # If Akon is already connected somewhere
                        await disconnectAkon(vocal)
                        b_status = False

                    vocal = await vc.connect()
                    await playLonely(vc, vocal, after.channel.name)
                    return

                else:
                    print("Not Alone Anymore...")
                    return

            else:   # if somebody new joins, leave (+person)
                if len(client.voice_clients) == 0:
                    return
                if checkAkonPresence(member_ids) and b_status:
                    return
                await disconnectAkon(vocal)
    return

client.run(AKON_TOKEN)
