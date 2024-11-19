import json
import os

if not os.path.exists("save.json"):

    with open("save.json", "w") as a:
        basesave = {
            "inventory": [], 
            "health": 10, 
            "maxHealth": 10, 
            "level":1, 
            "position":"start"
            }
        a.write(json.dumps(basesave))
        a.close

    


saveData = open("save.json")
saveData = json.load(saveData)

world = json.load(open("world.json"))



health = saveData["health"]
maxhealth = saveData["maxHealth"]
level = saveData["level"]
position = saveData["position"]
mode = "world"
inventory = saveData["inventory"]

# Gameplay Definitions

def Heal(amount):
    health =+ amount
    if health < 0:
        health = 0
    if health > maxhealth:
        health = maxhealth






def Init():
    file_path = "startMessage.txt"

    

    try:
        # Open the file in read mode
        with open(file_path, "r") as file:
            # Read the contents of the file
            file_contents = file.read()
            # Print the contents
            print(file_contents)
    except FileNotFoundError:
        print("Message file not found:", file_path)
    except IOError:
        print("Error reading message file:", file_path)


Init()

def Main():
    global position

    options = world[position]["options"]


    #formatted = [option["name"] for option in options]
    #formatted = "[" + "], [".join(formatted) + "]"
    formatted = list(options.keys())
    print("Choices:" + str(formatted))

    

    choice = input(">>>> ")
    if choice in options.keys():
        # if choice.isnumeric:
        #     choice = int(choice) - 1
        #     choice = (list(options.keys())[choice])
        
            
        choice = options[choice]

        if "conditionals" in choice.keys():
                for x in choice["conditionals"]:
                    if not conditions(x):
                        print("Conditions not met!")
                        Main()
                        break

        if choice == "Description":
            print("desc")
        else:
            position = choice["outcome"]
            print(choice["onpick"])


            # Extra Functions
            if "extra" in choice.keys() :
                for x in choice["extra"]:
                    extras(x)
            
                    
    else:
        print("Not an option!!!! (or you messed up typing it :/)")
        print(len(list(options.keys())))
            
    Main()

def extras(data):
    match data["type"]:
        case "heal":
            Heal(data["amount"])
        case "give":
            inventory.append(data["item"])
            print(inventory)
        case "take":
            inventory.remove(data["item"])
        case _:
            pass

def conditions(data):
    match data["type"]:
        case "has":
            return inventory.count(data["item"]) >= data["count"]
        case "healthatleast":
            return health >= data["amount"]
        case "healthequal":
            return health == data["amount"]
        case _:
            pass

Main()