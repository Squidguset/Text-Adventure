import json
import os
import math

if not os.path.exists("save.json"):

    with open("save.json", "w") as a:
        basesave = {
            "inventory": [], 
            "health": 10, 
            "maxHealth": 10, 
            "level":1, 
            "position":"start",
            "SavedExtras":{
                
            }
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
Values = {}
specials = {}
#SavedExtras = saveData["SavedExtras"]
SavedExtras = {}


# Gameplay Definitions

def Heal(amount):
    global health
    global maxhealth
    health = health + amount
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

    formatted = []

    options = world[position]["options"]

    for x in options.keys():
        if "visibility" in options[x].keys():
            match options[x]["visibility"]:
                case "visible":
                    formatted.append(x)
                case "whenmet":
                    for y in options[x]["conditionals"]:
                        if not conditions(y):
                            break
                        formatted.append(x)
                case "never":
                    break
                case _:
                    break
        else:    
            formatted.append(x)

    formatted = ("Choices:" + str(formatted))

    da = (len(formatted)-7)/2

    print(f"<{"-"*math.floor(da)}< ♦ >{"-"*math.ceil(da)}>")         
   
    

    print(formatted)

    

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


        position = choice["outcome"]
        print(choice["onpick"])


        # Extra Functions
        if "extra" in choice.keys() :
            for x in choice["extra"]:
                extras(x)
            
                    
    else:
        
        match choice.lower():
            case "help":
                aa = open("help.txt","r")
                print(aa.read())
                aa.close 
            case "inventory":
                print(inventory)
            case "status":
                print(f"Health:{health}/{maxhealth},Level:{level}")
            case _:
                print("Not an option!!!! (or you messed up typing it)")

        
            
    Main()

def extras(data):
    match data["type"]:
        case "heal":
            global Heal
            Heal(data["amount"])
        case "give":
            inventory.append(data["item"])
        case "take":
            inventory.remove(data["item"])


        case "set variable":
            global specials
            specials[data["key"]] = data["value"]



        case "set saved variable":
            global SavedExtras
            SavedExtras[data["key"]] = data["value"]



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
        case "variable matches":
            return specials[data["key"]] == data["value"]
        case "variable mismatches":
            return not specials[data["key"]] == data["value"]
        case _:
            pass

Main()