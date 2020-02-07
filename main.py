#!/usr/bin/env python3
import sys, os, json
# Check to make sure we are running the correct version of Python
assert sys.version_info >= (3,7), "This script requires at least Python 3.7"

# The game and item description files (in the same folder as this script)
game_file = 'thing.json'
item_file = 'items.json'
inventory = ["FLIER"]


# Load the contents of the files into the game and items dictionaries. You can largely ignore this
# Sorry it's messy, I'm trying to account for any potential craziness with the file location
def load_files():
    try:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, game_file)) as json_file: game = json.load(json_file)
        with open(os.path.join(__location__, item_file)) as json_file: items = json.load(json_file)
        return (game,items)
    except:
        print("There was a problem reading either the game or item file.")
        os._exit(1)

def check_inventory(item):
    for i in inventory:
        if i == item:
            return True
        return False

def render(game,items,current):
    c = game[current]
    print("\nYou are at the " + c["name"])
    print(c["desc"])

    #inventory
    for i in c["items"]:
        if not check_inventory(i["item"]):
            print(i["desc"])
    

def get_input():
    response = input("What will you do? ")
    response = response.upper().strip()
    return response

def update(game,items,current,response) :
    if response == "INVENTORY":
        print("You have")
        for i in inventory:
            print("a " + i.lower())
        return current
    c = game[current]
    if response == "LOOK UP":
        c = game[current]
        print("\n" + c["up"])


    try:
        for item in c["items"]:
            if response == "GET " + item["item"] and not check_inventory(item["item"]):
                print("")
                print(item["take"])
                inventory.append(item["item"])
    except:
        print("You can't get that item")
            
    try:
        for i in c["items"]:
            if response == "INSPECT " + i["item"]:
                print("")
                print(i["inspect"])
                return current
    except: 
        print("I don't understand what you're looking at")
        
    if response == "COMMAND":
        print("Inspect [item]- inspect allows you to gain more information about any item that allows it. This can be important as it helps solve some puzzles.")
        print("Look up- Look up let's you see what's above and may revael inportant information. Try to do it in every room.")
        print("Get [item]- entering get and an item name will allow you to pick up some items bot don't expect it to work for all of them")
        print("Use [item]- attempts to use an items in your inventory, if nothing happens that means it was unsuccessful.")
        print("Elevator- returns you from any floor to the elevator once you hve it unlocked.")
        print("Leave- allows you to quit out of the game.")




    for i in inventory:
        for action in items[i]["actions"]:
            if response == action + " " + i:
                print("")
                print(items[i]["actions"][action])
                

    for item in c["items"]:
        i = item["item"]
        for action in items[i]["actions"]:
            if response == action + " " + i:
                print("")
                print(items[i]["actions"][action])
                
    
    
    for e in c["exits"]:
        if response == e["exit"]:
            return e["target"]
 

    return current 






# The main function for the game
def main():
    current = 'START1'  # The starting location
    end_game = ['END']  # Any of the end-game locations

    (game,items) = load_files()

   
    while True:
        render(game,items,current)
        response = get_input()
        if response == "LEAVE":
            print("You decided this wasn't worth your time, and went home.")
            break
        current = update(game,items,current,response)






# run the main function
if __name__ == '__main__':
	main()