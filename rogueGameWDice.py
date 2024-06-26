import matplotlib.pyplot as plt
import tkinter
import tkinter.ttk
import numpy as np
import random
import json

#TODO:
#use health potions somehow drops random items from inv
#able to not click an option and submit next command and bypass situation?

#loads all the monster, trap, and item data from the JSON file
with open('encountersWDice.json') as json_data:
    data = json.load(json_data)


def createButtons(type):
    '''
    creates the necessary buttons that the user can choose from so that they can
    do the following commands depending on specific scenarios
    destroys previous buttons if any before constructing the new ones based on the scenario
    creates the submit command button for the user to click after they have chosen their option/button
    '''
    #if the scenario is a monster, then the user gets two options, to either attack or run
    if type == 'monster':
        choices = {
            "Attack" : "Attack",
            "Run" : "Run"
        }
    #if the scenario is an item, then the user gets two options, to either pick up the item or to not pick up the item
    elif type == 'item':
        choices = {
            "Pick Up" : "Pick up",
            "Don't Pick Up" : "Next Turn"
        }
    #if at the end of a scenario, then the uesr gets the option to move on to the next scenario
    elif type == 'next turn':
        choices = {
            "Next Turn" : "Next Turn"
        }
    #if at the start of the game, the user gets two options, to either turn left or turn right
    elif type == 'start':
        choices = {
            "Left" : "Left",
            "Right" : "Right"
        }
    #destroys any previous buttons from previous scenarios
    for widget in app.grid_slaves():
        if int(widget.grid_info()['column']) == 1 and int(widget.grid_info()['row']) > 4:
            widget.destroy()
    position = 17
    #creates the new buttons based on the parameter inputted into the function
    for (text,value) in choices.items():
        tkinter.Radiobutton(app,text=text,value=value,variable=choice).grid(row=position,column=1)
        position += 1
    #creates the submit button which the user can click so that whatever option the user has picked is computed
    nextturn = tkinter.ttk.Button(app, text='Submit Command', command=nextCommand)
    nextturn.grid(row=position+1,column=1)

def nextCommand():
    '''
    function that computes when the nextturn button is pressed 
    first checks if any of the conditions for the game to be lost is true
    based on the radio button selected by the user when the nextturn button is pressed redirects to the specific
    function
    computes the score and updates teh turn number and score labels on the GUI
    '''
    #checks if any of the conditions for losing is true
    lostGame()
    if (turnNumber.get() == 0 and (choice.get().lower() == 'left' or choice.get().lower() == 'right')):
        nextScenario()
    if choice.get().lower() == 'next turn' and turnNumber.get() != 0:
        nextScenario()
    if choice.get().lower() == 'pick up':
        pickUp()
    if choice.get().lower() == 'attack':
        battle()
    if choice.get().lower() == 'run':
        run()
    #sets the score variable with the unique score calculator which takes inputs from multiple areas of the game
    score.set((turnNumber.get()*5) + damageDone.get() + itemsUsed.get() + armorVal.get())
    #updates the turn number label in the GUI
    turnNumberLabel['text'] = 'Turn Number: '+ str(turnNumber.get()) + '\nScore: ' + str(score.get())

def pickUp():
    '''
    puts the item into the users inventory, if the inventory size is 1 under max, then
    it does not add a comma to the end of the inventory
    in addition, if the inventory reaches max inventory size and the user tries to pick
    up an item, it prints that the user has reached max inventory and allows the option of swapping
    '''
    #resets the baseline variables for user stats
    totalArmor = 0
    #checks to see if the inventory is under the maximum amount of slots
    if len(inventory) < inventorySize.get():
        #adds the item into the inventory
        inventory.append(item)
        #if the item is a backpack, increases the inventory size
        if item["name"] == 'Backpack':
            inventorySize.set(inventorySize.get() + 2)
        #equips the items from the inventory and makes the adjustments on the GUI with the new armor
        #that the user has acquired from picking up the items
        for x in inventory:
            if x['type'] == 'armor':
                totalArmor += x['defense']
        #sets the values to the GUI so that the user can see the changes of picking up the items
        armorVal.set(totalArmor)
        playerStatsLabel['text'] = 'Health: ' + str(health.get()) + '\nArmor: ' + str(armorVal.get())
        #goes to the next encounter if the user picks up an item successfully
        nextScenario()
    #if the user has reached the maximum size of their inventory, they are prompted with the following message
    else:
        eventLabel['text'] = 'You have reached maximum inventory space. If you wish to swap items, drop an item then pick up the new item.'

def battle():
    '''
    the player has encountered a monster and has decided to attack, computes to see how much
    damage the player does to the monster and how much the monster does to user
    then checks if the user has lost the game
    '''
    hasArmor = False
    #makes sure that the monster does not have negative health
    if 0 < monster['health']:
        #figures out the attack value from user
        dmg = 0
        for weapon in inventory:
            if weapon['type'] == 'weapon':
                for x in range(weapon['attack_mult']):
                    dmg += random.randrange(1,weapon['attack_di'])
                dmg += weapon['bonus_atk']
                print(weapon['name'] + " rolled " + str(dmg) + " as damage from " + weapon['attack_inf'] + ".")
        #subtracts the monsters health from the attack value from the user
        monster['health'] = monster['health'] - dmg
        #updates the label on the GUI with depleted health
        eventStatsLabel['text'] = 'Name: ' + monster['name'] + '\nHealth: ' + str(monster['health']) + '\nDamage: ' + str(monster['attack_inf']) + '\n'
        damageDone.set(damageDone.get() + dmg)
        #if the monsters health reaches 0 or below 0, then the user is prompted with the message of defeating the monster
        if monster['health'] <= 0:
            eventLabel['text'] = 'You have successfully defeated the ' + monster["name"] + '.'
            createButtons('next turn')
            eventStatsLabel.grid_remove()
            #adds the health back to the monster for further encounters
            monster['health'] = tempHealth.get()
    #if the monsters health is already 0 for some reason, prompts the user with the message of them defeating the monster
    else:
        eventLabel['text'] = 'You have successfully defeated the ' + monster["name"] + '.'
        createButtons('next turn')
    #if the users health is above zero and the monsters health has not reached 0, then the monster
    #attacks back
    if 0 < int(health.get()) and 0 < monster['health']:
        #calculates monster damage
        dmg = 0
        for x in range(monster['attack_mult']):
            dmg += random.randrange(1,monster['attack_di'])
        dmg += monster['bonus_atk']
        print(monster['name'] + " rolled " + str(dmg) + " as damage from " + monster['attack_inf'] + ".")
        #checks if the user has armor
        for x in inventory:
            if x['type'] == 'armor':
                hasArmor = True
                break
        #if the user has armor, the damage that they receive is reduced
        if hasArmor == True:
            if (dmg - armorVal.get()) >= 0:
                health.set(health.get() - (dmg - armorVal.get()))
            playerStatsLabel['text'] = 'Health: ' + str(health.get()) + '\nArmor: ' + str(armorVal.get())
            lostGame()
        #if the user does not have armor, the damage that they receive is not reduced
        else:
            health.set(health.get() - dmg)
            playerStatsLabel['text'] = 'Health: ' + str(health.get()) + '\nArmor: ' + str(armorVal.get())
            lostGame()
    #checks if the user has lost the game
    else:
        lostGame()

def run():
    '''
    the player has chose to try to run after encountering a monster, computes to see if the
    player successfully runs away or not
    if the user unsuccessfully runs away from the monster, the monster gets a free hit on the user
    '''
    chance = np.random.rand(1)
    #the user has a set 50% chance of running away from the monster
    if 0 <= chance <= 0.5:
        #if the user fails to run away, monster damage is computed
        dmg = 0
        for x in range(monster['attack_mult']):
            dmg += random.randrange(1,monster['attack_di'])
        dmg += monster['bonus_atk']
        print(monster['name'] + " rolled " + str(dmg) + " as damage from " + monster['attack_inf'] + ".")
        #if the armor value is greater than the dmg, then health shouldn't be gained
        if (dmg - armorVal.get()) >= 0:
            health.set(health.get() - (dmg - armorVal.get()))
            eventLabel['text'] = 'You have failed to run away from ' + monster['name'] + ', and have taken ' + str(dmg - armorVal.get()) + ' damage.\n You can either attack or attempt to run again.'
        else:
            eventLabel['text'] = 'You have failed to run away from ' + monster['name'] + ', and have taken ' + str(0) + ' damage.\n You can either attack or attempt to run again.'
        #updates GUI labels
        playerStatsLabel['text'] = 'Health: ' + str(health.get()) + '\nArmor: ' + str(armorVal.get())
        #checks if any conditions of losing game is true after the possiblity of player health reaching <=0
        lostGame()
    #if the user successfully runs away from the monster, they are prompted with the following message
    else:
        eventLabel['text'] = 'You have successfully ran away from ' + monster['name'] + '.'
        monster['health'] = tempHealth.get()
        createButtons('next turn')

def nextScenario():
    '''
    computes the next scenario, there is 1/3 chance of encountering a monster, 1/3 chance of encountering a trap,
    and 1/3 chance of encountering an item

    if a monster is encountered, it chooses a random monster from the JSON file, sets the temporary health so that if
    the monster is killed, the health goes back to full so that if the monster is encountered again, the health isn't 0
    finally updates the labels displays name, health, damage info, and following options for user

    if an item is encountered, it chooses a random item from the JSON file, if the item is armor, the defense is displayed
    if the item is a utility item, then the effect is displayed, if the item is a weapon, the damage is displayed

    if a trap is encountered, it chooses a random trap from the JSON file, there is a 25% chance of evading the trap,
    if there is a failed evation, then damage is computed and the conditions of losing are checked
    '''
    chance = np.random.rand(1)
    eventStatsLabel.grid()
    #monsters
    if 0.666666 < chance < 1:
        randomInt = random.randrange(0,len(data['monsters']))
        global monster
        monster = data['monsters'][randomInt]
        tempHealth.set(monster['health'])
        eventStatsLabel['text'] = 'Name: ' + monster['name'] + '\nHealth: ' + str(monster['health']) + '\nDamage: ' + str(monster['attack_inf']) + '\n'
        eventLabel['text'] = 'You encountered a ' + monster['name'] + '. Do you wish to attack? or run?'
        createButtons('monster')
    #items
    elif 0.333333 < chance < 0.666666:
        randomInt = random.randrange(0,len(data['items']))
        global item
        item = data['items'][randomInt]
        #if the type of item is 'armor', it displays the necessary information for an armor type
        if item['type'] == 'armor':
            eventStatsLabel['text'] = 'Name: ' +  item['name'] + '\nArmor: ' + str(item['defense']) + '\n'
            eventLabel['text'] = 'You found a ' + item['name'] + '. Do you wish to pick it up?'
        #if the type of item is 'potion', it displays the necessary information for an potion type
        elif item['type'] == 'utility':
            eventStatsLabel['text'] = 'Name: ' +  item['name'] + '\nEffect: ' + str(item['effect']) + '\n'
            eventLabel['text'] = 'You found a ' + item['name'] + '. Do you wish to pick it up?\nTo use an item, go to your inventory.'
        #if the type of item is 'weapon' or anything else, it displays the necessary information for that item
        else:
            eventStatsLabel['text'] = 'Name: ' +  item['name'] + '\nDamage: ' + str(item['attack_inf']) + '\n'
            eventLabel['text'] = 'You found a ' + item['name'] + '. Do you wish to pick it up?'
        createButtons('item')
    #traps
    else:
        #chooses random trap from JSON file/data
        randomInt = random.randrange(0,len(data['traps']))
        trap = data['traps'][randomInt]
        #checks if the user evades the trap
        if random.randrange(0,101) <= 25:
            eventStatsLabel['text'] = 'Name: ' +  trap['name'] + '\nDamage: ' + trap['attack_inf'] + '\n'
            eventLabel['text'] = 'You encountered a trap, however, you have successfully evaded it.'
            createButtons('next turn')
        #failed evation of trap, then computes damage from the trap to the user
        else:
            eventStatsLabel['text'] = 'Name: ' +  trap['name'] + '\nDamage: ' + trap['attack_inf'] + '\n'
            dmg = 0
            for x in range(trap['attack_mult']):
                dmg += random.randrange(1,trap['attack_di'])
            dmg += trap['bonus_atk']
            print(trap['name'] + " rolled " + str(dmg) + " as damage from " + trap['attack_inf'] + ".")
            if (dmg - armorVal.get()) >= 0:
                health.set(health.get() - (dmg - armorVal.get()))
                eventLabel['text'] = 'You encountered a trap and failed to evade it. You took '  + str(dmg - armorVal.get()) + ' damage.'
            else:
                eventLabel['text'] = 'You encountered a trap and failed to evade it. You took '  + str(0) + ' damage.'
            playerStatsLabel['text'] = 'Health: ' + str(health.get()) + '\nArmor: ' + str(armorVal.get())
            createButtons('next turn')
            #checks lost conditions
            lostGame()
    #adds one to the turn number because the previous turn has been completed
    turnNumber.set(turnNumber.get() + 1)
    turnNumberLabel['text'] = 'Turn Number: '+ str(turnNumber.get()) + '\nScore: ' + str(score.get())

def lostGame():
    '''
    checks if the player has lost the game by checking if the health equals 0
    and if whether or not they have reached the maximum amount of turns
    if they did lose the game, then majority of the widgets are removed and a restart
    button appears giving the user the option to restart the game with the option to leave a username for
    the leaderboard
    '''
    #checks if the users health has reached 0 or below 0 and if the user has reached the maximum amount of turns
    if health.get() <= 0 or turnNumber.get() == 100:
        #removes all the widgets and provides the user with a description of them losing the game and what to do next
        if turnNumber.get() == 100:
            eventLabel['text'] = 'You have found the treasure. If you wish to restart push the reset button.'
        elif health.get() <= 0:
            eventLabel['text'] = 'You have lost the game. If you wish to restart push the reset button.'
        eventStatsLabel.grid_remove()
        invButton.grid_remove()
        for widget in app.grid_slaves():
            if int(widget.grid_info()['column']) == 1 and int(widget.grid_info()['row']) > 4:
                widget.destroy()
        #adds the username label and entry for leaderboard
        usernameLabel.grid()
        usernameEntry.grid()
        #adds the restart button for the game to restart
        restartButton = tkinter.ttk.Button(app,text='Restart', command=restart)
        restartButton.grid(row=5,column=1)
    #if the user does not lose the game it returns false
    else:
        False

def toggleInv():
    '''
    toggles the inventory in the GUI so that when the show/hide inventory
    button is pressed in the GUI, the user can see what they have inside their inventory
    if the user does not have anything in their inventory, they are prompted with a message
    describing that they have not picked up any items yet
    '''
    global toggle
    global temp
    #if the inventory is hidden, it shows the user their inventory
    if toggle == True:
        temp = eventLabel['text']
        invButton['text'] = 'Hide Inventory'
        #checks to see if the user has not picked up any item yet
        if len(inventory) == 0:
            eventLabel['text'] = 'You haven\'t picked up anything yet.'
        #if the user has items in their inventory, then it is displayed in the GUI
        else:
            position = 3
            eventLabel['text'] = 'Your iventory includes:'
            #displays all the items and necessary information
            for x in inventory:
                if x['type'] == 'weapon':
                    tkinter.Label(app,text= x["name"] + ' - Attack: ' + str(x['attack_inf'])).grid(row=position,column=1)
                elif x['type'] == 'armor':
                    tkinter.Label(app,text= x["name"] + ' - Armor: ' + str(x['defense'])).grid(row=position,column=1)
                else:
                    tkinter.Label(app,text= x["name"] + ' - ' + str(x['effect'])).grid(row=position,column=1)
                if x['name'] == 'Health Potion':
                    tkinter.ttk.Button(app,text='Use',command=lambda name=x['name']: useItem(name)).grid(row=position,column=3)
                #creates drop button for all items in the inventory if the user wishes to drop an item
                tkinter.ttk.Button(app,text='Drop ' + x['name'],command= lambda name=x['name']: drop(name)).grid(row=position,column=2)
                position += 1
        toggle = False
    #if the inventory is shown, it brings the user back to the current encounter
    elif toggle == False:
        invButton['text'] = 'Show Inventory'
        #makes the event label go back to the current encounter with the temporary variable
        eventLabel['text'] = temp
        toggle = True
        for widget in app.grid_slaves():
            if (int(widget.grid_info()['column']) >= 1 or int(widget.grid_info()['column']) <= 3) and (int(widget.grid_info()['row']) > 2 and int(widget.grid_info()['row']) < 17):
                widget.destroy()

def useItem(itemName):
    '''
    this function computes if the user wants to use an item in their inventory
    first it checks if the user has the item in their inventory that was inputted in the commmand box
    then it gets rid of the item from their inventory and applies the necessary effect of the item
    '''
    hasItem = False
    count = 0
    #checks if the user has the item in their inventory that was inputted in the command box
    for x in inventory:
        count += 1
        if x['name'] == itemName:
            hasItem = True
            break
    #conditional goes through if the user has the item in their inventory
    if hasItem == True:
        #gets rid of the item in their inventory
        inventory.pop(count-1)
        #checks if the item that the user wants to use is a health potion
        if itemName == 'Health Potion':
            #adds to the items used for the stats section of the app
            itemsUsed.set(itemsUsed.get() + 1)
            if health.get() <= 90:
                #applies the necssary effect of the item and makes the change on the GUI for the user to see
                health.set(health.get() + 10)
                playerStatsLabel['text'] = 'Health: ' + str(health.get()) + '\nArmor: ' + str(armorVal.get())
            else:
                #if the user has between 91-100 health, they don't go over 100 because 100 is the maximum health
                #applies the necssary effect of the item and makes the change on the GUI for the user to see
                health.set(100)
                playerStatsLabel['text'] = 'Health: ' + str(health.get()) + '\nArmor: ' + str(armorVal.get())
            hasItem = False
            
        print(itemName + ' has been used')
        toggleInv()
        toggleInv()

def drop(item):
    '''
    this function computes if the user wants to drop an item in their inventory
    first it checks if the user has the item in their inventory that was inputted from the function parameters
    then it gets rid of the item from their inventory
    '''
    for x in inventory:
        #if there is an item in the inventory that matches the item the user wants to drop
        if item == x['name']:
            print(x['name'] + ' has beed dropped')
            #if the item is a backpack that the user wants to drop, then the inventory size is decreased
            if x['name'] == 'Backpack':
                inventorySize.set(inventorySize.get() - 2)
            #if the item is an armor type that the user wants to drop, then the armor value is decreased accordingly
            elif x['type'] == 'armor':
                armorVal.set(armorVal.get() - x["defense"])
                playerStatsLabel['text'] = 'Health: ' + str(health.get()) + '\nArmor: ' + str(armorVal.get())
            inventory.remove(x)
            #refreshes inventory to depict dropeed item
            toggleInv()
            toggleInv()
            break

def restart():
    '''
    if the user clicks the restart button at the very end of the game, this function computes
    adds all the data from the previous session into the necssary variables for graphing
    resets the event label back to the very start
    resets all the necessary variables back to their starting values
    brings back all the widgets and clears the inventory from the previous session
    '''
    global inventory
    #adds all the data form the previous session into the necessary variables for graphing
    scoreData.append(score.get())
    #adds name to leaderboard list
    if usernameEntry.get() != "":
        leaderboard_dict[usernameEntry.get()] = score.get()
    #resets the event label back to the very start
    eventLabel['text'] = 'You have entered the cave and have found a forked pathway, do you wish to go left or right?'
    #resets all the necessary variables back to their starting values
    turnNumber.set(0)
    score.set(0)
    #resets the turn number label in the GUI back to 0 and score back to 0
    turnNumberLabel['text'] = 'Turn Number: '+ str(turnNumber.get()) + '\nScore: ' + str(score.get())
    #continues to reset all the necessary variables back to their starting values
    health.set(100)
    armorVal.set(0)
    damageDone.set(0)
    itemsUsed.set(0)
    inventorySize.set(3)
    #resets all the stats given to the user in the GUI
    playerStatsLabel['text'] = 'Health: ' + str(health.get()) + '\nArmor: ' + str(armorVal.get())
    eventStatsLabel['text'] = ''
    #clears the inventory
    inventory = []
    #removes the restart button and adds back all the original widgets
    restartButton.grid_remove()
    createButtons('start')
    eventStatsLabel.grid()
    invButton.grid()
    #removes the username entry and label info
    usernameEntry.grid_remove()
    usernameLabel.grid_remove()
    #removes any previous text in username entry
    usernameEntry.delete(0,tkinter.END)

def showLeaderboard():
    '''
    shows leaderboard with usernames and the connected scores in order
    '''
    global toggle_leaderboard
    global temp_leaderboard
    if toggle_leaderboard == True:
        temp_leaderboard = eventLabel['text']
        leaderboard['text'] = 'Hide Leaderboard'
        #if there is no one in the leaderboards yet, depicts following message
        if len(leaderboard_dict) == 0:
                eventLabel['text'] = 'There is no user saved in the leaderboards yet.'
        #if there are leaderboards saved, it is displayed in the GUI
        else:
            #sorts leaderboard
            sorted_leaderboard = {}
            for key in sorted(leaderboard_dict,key = leaderboard_dict.get,reverse=True):
                sorted_leaderboard[key] = leaderboard_dict[key]
            #prints leaderboard
            position = 3
            eventLabel['text'] = 'Leaderboard:'
            for x, y in sorted_leaderboard.items():
                tkinter.Label(app,text= x + ' -  ' + str(y)).grid(row=position,column=1)
                position += 1
        toggle_leaderboard = False
    elif toggle_leaderboard == False:
        leaderboard['text'] = "Leaderboard"
        #sets the event label back to the temporary one that was saved when the leaderboards were first shown
        eventLabel['text'] = temp_leaderboard
        toggle_leaderboard = True
        #destroys all the widgets that include the usernames and the corresponding scores
        for widget in app.grid_slaves():
            if (int(widget.grid_info()['column']) >= 1 or int(widget.grid_info()['column']) <= 3) and (int(widget.grid_info()['row']) > 2 and int(widget.grid_info()['row']) < 17):
                widget.destroy()

#starts the app in tkinter
app = tkinter.Tk()
#adds the title for the app
app.title('Cave Exploration')

#is the text label which describes the event stats that the player has encountered at
#the start of eachturn
eventStatsLabel = tkinter.ttk.Label(app,text='')
eventStatsLabel.grid(row=1,column=1)

#is the text label which describes the event that the player has encountered at the
#start of each turn
eventLabel = tkinter.ttk.Label(app,text='You have entered the cave and have found a forked pathway, do you wish to go left or right?')
eventLabel.grid(row=2,column=1)

#create list that will store the score data over many sessions for leaderboard
scoreData = []

#creates the inventory variables
inventory = []

choice = tkinter.StringVar(app,"")
nextturn = tkinter.ttk.Button(app, text='Submit Command', command=nextCommand)

#sets a tempHealth variable for when monster attack
tempHealth = tkinter.IntVar(app,value=0)

#creates the leaderboard button, when pushed, computes the showLeaderboard function
leaderboard = tkinter.ttk.Button(app,text='Leaderboard',command=showLeaderboard)
leaderboard.grid(row = 0, column=20)
leaderboard_dict = {}

#creates leaderboard label and entry widgets
username = tkinter.StringVar(app)
usernameLabel = tkinter.ttk.Label(app,text="Enter username: ")
usernameEntry = tkinter.ttk.Entry(app,textvariable=username)
usernameLabel.grid(row=3,column=1)
usernameEntry.grid(row=4,column=1)
usernameLabel.grid_remove()
usernameEntry.grid_remove()

#sets toggle for show inventory usage
toggle = True
#sets totggle for show leaderboard usage
toggle_leaderboard  = True

#creates the heatlh, and armorVal integer variables in tkinter so they can be manipulated as the game goes on
health = tkinter.IntVar(app,value=100)
armorVal = tkinter.IntVar(app,value=0)
#creates the player stats label which shows the player their health,armor, and attack in the GUI
playerStatsLabel = tkinter.ttk.Label(app,text = 'Health: ' + str(health.get()) + '\nArmor: ' + str(armorVal.get()))
playerStatsLabel.grid(row=20,column=20)

inventorySize = tkinter.IntVar(app,value=3)

#creates the turn number and score integer variables in tkinter so they can be manipulated as the game goes on
turnNumber = tkinter.IntVar(app,value=0)
score = tkinter.IntVar(app,value=0)
itemsUsed = tkinter.IntVar(app,value=0)
damageDone = tkinter.IntVar(app,value=0)
#creates the turn number label which shows the player the turn number and score in the GUI
turnNumberLabel = tkinter.ttk.Label(app,text = 'Turn Number: '+ str(turnNumber.get()) + '\nScore: ' + str(score.get()))
turnNumberLabel.grid(row=20,column=0)

#creates the restart button for the player to use when the game is over, computes the restart function
restartButton = tkinter.ttk.Button(app,text='Restart', command=restart)
restartButton.grid(row=5,column=1)
#hides the restart button at the very beginning so that it can be shown when the game is over
restartButton.grid_remove()

#creates the inventory button for the user to use when they want to see their inventory, computes the toggleInv function
invButton = tkinter.ttk.Button(app,text='Show Inventory',command=toggleInv)
invButton.grid(row=0,column=0)

#creates the buttons for the start of the game
createButtons('start')

app.mainloop()