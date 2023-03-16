import discord
import asyncio
from discord import FFmpegPCMAudio
from discord.ext import commands

keyFile = open("C:\\Users\\asian\\PycharmProjects\\akonKey.txt", 'r')
AKON_TOKEN = keyFile.readline()
keyFile.close()

AkonID = 922947088168407040
sleepTime = 15

def checkAkonPresence(memids):  # Scans for the presence of Akon's ID in a given list
    for x in memids:
        if x == AkonID:
            return True
    return False

def getMemids(memids, VC):  # Scans and resets memids
    memids.clear()
    for mem in VC.members:
        memids.append(mem.id)

    return memids

async def playLonely(vc, vocal, channelName):
    print(f"AKON has joined!!! \"{channelName}\"")
    vocal.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="Lonely.mp3"))

async def standby():
    while True:
        try:
            await asyncio.sleep(sleepTime)  # await 10 seconds before joining
            return
        except asyncio.TimeoutError:
            print(f"timeout error on standby")
            pass

async def disconnectAkon(vocal):
    await vocal.disconnect()  # Disconnect
    vocal.cleanup()
    print("Akon has left")



