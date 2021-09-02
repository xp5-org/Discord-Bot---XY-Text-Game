# bot.py
import os
import base64
import discord
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv('DISCORD_TOKEN') # this accesses the repl "secrets" where you can store a token and not show it to the whole world 
STARTINGPLAYERNAME = os.getenv('FIRST_PLAYER')  #this is a crappy workaround to init empty sql table






client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    
    if message.content.startswith('@BorksBot hello'):
        await message.channel.send('Hello!')
        return

    ## everything below here responds in DM only## 
    if message.channel.id == message.author.dm_channel.id: # dm only
        # do nothing
        print('dm message')
    elif not message.guild: # group dm only
        print('not dm message')
        return
    else:
        print('else')
        return
    
    
    if message.author == client.user:
        print('hmm')
        return


    
    if message.content.startswith('help'):
        await message.channel.send("```new - initiate new player session \n location - show player location \n use apple - use item for apple \n inventory - show current inventory \n health - show player health \n left, right, up, down - movement commands```")
        return

    if message.content.startswith('ping'):
        print(message.author)
        print(message.channel)
        await message.channel.send("```\nPong!\n This is an example of using a code-block for text in the discord bot\n its kind of neat```")
        return



    #this is the only game command a player without a matching user instance can run
    if message.content.startswith('new'):
        output = checkifexists(str(message.author))
        objs.append(Player(message.author))
        await message.channel.send('making new user connection')
        return

    # check if userid is something
    userpositionoutput = int(findusersclass(message.author))

    if userpositionoutput is not None:
        userclassname = objs[userpositionoutput].playername
    if userpositionoutput is None:
        print('user position output is none - error')






    
    if message.content.startswith('left'):
        await message.channel.send('left')
        objs[userpositionoutput].move('left')
        return
    if message.content.startswith('right'):
        await message.channel.send('right')
        objs[userpositionoutput].move('right')
        return
    if message.content.startswith('up'):
        await message.channel.send('up')
        objs[userpositionoutput].move('up')
        return
    if message.content.startswith('down'):
        await message.channel.send('down')
        objs[userpositionoutput].move('down')
        return

    if message.content.startswith('location'):
        loc = objs[userpositionoutput].currentlocation()
        messageout = ('location', str(loc))
        await message.channel.send(messageout)
        return

    if message.content.startswith('inventory'):
        inventory = objs[userpositionoutput].playerinventory()
        await message.channel.send(inventory)
        return    
    if message.content.startswith('health'):
        health = objs[userpositionoutput].playerhealth()
        await message.channel.send(health)
        return    
    if message.content.startswith('use apple'):
        appleuse = objs[userpositionoutput].use_item('apple')
        await message.channel.send(appleuse)
        return
    if message.content.startswith('use pear'):
        appleuse = objs[userpositionoutput].use_item('pear')
        await message.channel.send(appleuse)
        return
    




    print(message.author)
    await message.channel.send('I do not have any code to handle your prior entry')
    return















# copied and pasted this thing in 
# https://replit.com/@qcm/Class-Structure#main.py



import sqlite3
import json


class Player:
  def __init__(self, name):
    self.playername = name
    self.playerid = str(sql_findid(con, self.playername))
    self.position_x = 0
    self.position_y = 0
    self.inventory = {}
    self.health = 0
    self.score = 0
    self.movecount = 0 #(counts up and then triggers event like food use do not store)
    print('self dot playerid val is', self.playerid)
    self.sql_read()

  def currentlocation(self):
    pos = [self.position_x, self.position_y]
    print(self.playername, pos)
    return pos

  def playerhealth(self):
    return self.health

  def playerinventory(self):
    return self.inventory    

  def sql_read(self):
    con = sqlite3.connect("PlayerDB.db")
    cursorObj = con.cursor()
    cursorObj.execute('''SELECT * FROM playerinfo WHERE id = ?''', (self.playerid))
    rows = cursorObj.fetchall()
    print('output of rows', rows)
    print('player id from object', self.playerid)
    print('PlayerID', rows[0][0])
    print('Player Name', rows[0][1])
    print('Player X-Pos', rows[0][2])
    print('Player Y-Pos', rows[0][3])
    self.position_x = int(rows[0][2])
    self.position_y = int(rows[0][3])
    self.inventory = json.loads(rows[0][4])
    # print('name:', self.name, ' , ', 'inventory: ', self.inventory)
    self.health = int(rows[0][5])
    self.score = int(rows[0][6])



  def sql_update(self):
    con = sqlite3.connect("PlayerDB.db")
    cursorObj = con.cursor()
    inventorystring = json.dumps(self.inventory)
    print('DEBUG: Num of rows updated: ', cursorObj.execute('''UPDATE playerinfo SET position_x = ? , position_y = ? , inventory = ? , health = ?, score = ? WHERE id = ?''', (self.position_x, self.position_y, inventorystring, self.health, self.score, str(self.playerid))).rowcount)
    con.commit()
    print('update statement ran for : ', self.position_x, self.position_y, self.playerid)
    sql_fetch(con)

  def use_item(self, item):
      if item in self.inventory:
          print('found', item, 'in dict list')
          output = int(self.inventory[item])
          self.inventory[item] = (output - 1)
          self.health += 10
          print(self.inventory)
          self.sql_update()
      return self.inventory



  def move(self, inputaction):
    command = inputaction.lower()
    if command == 'up':
        self.position_y += 1
        print('up')
    if command == 'down':
        self.position_y -= 1
        print('down')
    if command == 'left':
        self.position_x -= 1
        print('left')
    if command == 'right':
        self.position_x += 1
        print('right')
    print('movement command executed inside class')
    self.sql_update()
    self.movecount += 1


  def action(self, command):
    if command == 'open':
        print('open action performed at ', [self.position_x, self.position_y], 'block-id-command-here')
    if command == 'close':
        print('close action performed at ', [self.position_x, self.position_y])











# SQL for store load player info

def sql_connection(tablename):
    try:
        con = sqlite3.connect(tablename)
        return con
    except Error:
        print(Error)


def sql_create_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE playerinfo(id, name, position_x, position_y, inventory, health, score)")
    con.commit()

def sql_newplayer(con, name):
    cursorObj = con.cursor()
    tablename = "playerinfo"
    playerid = str(sql_getnumrows(con))
    playername = str(name)
    position_x = '0'
    position_y = '0'
    inventory = {"apple": "5", "pear": "2"}
    dict_string = json.dumps(inventory)
    health = int('90')
    score = int('0')
    sectorcolumns = (playerid, playername, position_x, position_y, dict_string, health, score)
    cursorObj.execute('INSERT INTO ' + tablename + '(id, name, position_x, position_y, inventory, health, score) VALUES(?, ?, ?, ?, ?, ?, ?)', sectorcolumns)
    con.commit()

def sql_fetch(con):
    # this is outside the class, so that the class is reusing 
    # existing single sql connection to prevent DB lock conflict
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM playerinfo')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)

def sql_getnumrows(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM playerinfo')
    rows = cursorObj.fetchall()
    print(len(rows))
    return len(rows)


def sql_findid(con, name):
    playername = str(name)
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM playerinfo')
    rows = cursorObj.fetchall()
    iter = 0
    max = len(rows)
    while iter < max:
        if playername in (rows[iter][1]):
            print('found match', rows[iter][1], 'id is:', rows[iter][0])
            return str(rows[iter][0])
        iter += 1
    return None 



con = sql_connection("PlayerDB.db")
#sql_create_table(con) #create table
# sql_newplayer(con, 'discordusernamek#1234') # insert starting values for Player-0
# sql_newplayer(con, STARTINGPLAYERNAME) # insert starting values for Player-0 using name from secrets file

sql_fetch(con)

#p1 = Player('discordusernamek#1234')
#p1 = Player(STARTINGPLAYERNAME)





def checkifexists(name):
    playername = str(name)
    out = sql_findid(con, playername)
    if out is not None:
        print('found user: ', out)
    else:
        sql_newplayer(con, playername)

        print('creating new user: ', playername)



objs = list()
objs.append(Player(STARTINGPLAYERNAME))


def findusersclass(username):
    # returns the first instance-id of an existing 
    # Player class object for user
    objs_iter = 0
    objs_depth = len(objs)
    print(objs_depth)
    while objs_iter < objs_depth:
        print('objs: ', objs[objs_iter].playername)
        print('username: ', username)
        if str(objs[objs_iter].playername) == str(username):
            print('found user ', objs[objs_iter].playername)
            return objs_iter
        objs_iter += 1
    else:
        print('didnt find the user')
        return None






print('here')
#sql_findid(con, STARTINGPLAYERNAME)


def initplayer(name):
    sql_getnumrows(con)



client.run(TOKEN)
