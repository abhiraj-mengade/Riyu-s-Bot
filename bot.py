from keep_alive import keep_alive
import chatterbot
from chatterbot import ChatBot
import discord
import os
import requests

import json
import random
from replit import db
import requests


client = discord.Client()

rbot = ChatBot(
    'Riyu',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch'
    ])


sad_words = ["sad", "Sad", "depressed", "unhappy", "angry", "miserable"]

starter_encouragements = [
  "Cheer up!The world hasn't ended yet! <3",
  "Hang in there.I am with you! :)",
  "You are doing great! Darling <3"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_image():
  img = "https://api.unsplash.com/photos/random?"
  return(img)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  return(quote)

def get_fact():
  response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
  json_data = json.loads(response.text)
  fact = json_data["text"]
  return(fact)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("/inspire"):
    quote = get_quote()
    await message.channel.send(quote)
    await message.channel.send('https://picsum.photos/'+ str(random.randint(500,1000)))

  


  if msg.startswith('.'):
     await message.delete()
     await message.channel.send(msg[1:])

  if msg.startswith('/hello'):
        await message.channel.send("Hello! I am Riyu's Bot. Nice to meet you 😚 ️")
  
  if msg.startswith('/help'):
        await message.channel.send("""*Hello! I am Riyu's Bot 
        Here's a list of my commands that you can try! 

          '/hello' - to get a hello msg from me!☺️ 

          '/inspire' - to get an inspiration quote from me. 

          '/fact'- to get a fun fact from me! 

          '/help' - to open this help menu  🙂

          '/c (message)' - to chat with me  😎
          

        Be patient with me, I am still small & I am learning! 

        Apart from this, I'll try to cheer you up if you feel sad or angry.   🥺👉👈*"""

)
  
  if msg.startswith('/c'):

    resp = rbot.get_response(msg[2:])

    await message.channel.send(resp)


  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
    
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")
      
keep_alive()
client.run(os.getenv("TOKEN"))
