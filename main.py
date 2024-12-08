import json
import os
import math

def loadGame():
    global world
    world = input("Game file: ")
    if not os.path.exists(world):
        print("Path Doesn't Exist!!!")
        loadGame()
    elif not os.path.splitext(world)[1] == ".tagame":
        print("not a .tagame!!!!")
        loadGame()
    else:
        world = json.loads(open(world).read())
        world = world["world"]

loadGame()


save = input("Save Name: ")

if not ".tasave" in save:
    save = save + ".tasave"

if not os.path.exists(save):

    with open(save, "w") as a:
        basesave = {
            "version":1,
            "inventory": [], 
            "Health": 10, 
            "maxHealth": 10, 
            "level":1, 
            "position":"start",
            "SavedExtras":{
                
            }
            }
        a.write(json.dumps(basesave))
        a.close

    


saveData = open(save)
saveData = json.load(saveData)

#world = json.load(open("world.json"))


inventory = saveData["inventory"]
Values = saveData
Values.pop("version",None)
#Values.pop("inventory",None)

mode = "world"

SavedExtras = saveData["SavedExtras"]
#SavedExtras = {}
#health = saveData["health"]
#maxhealth = saveData["maxHealth"]
#level = saveData["level"]
#position = saveData["position"]


#specials = {}


# Gameplay Definitions

def Heal(amount):
    global Values
    
    Values["Health"] = Values["Health"] + amount
    if Values["Health"] < 0:
        Values["Health"] = 0
    if Values["Health"] > Values["maxHealth"]:
        Values["Health"] = Values["maxHealth"]






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
    global Values

    formatted = []

    options = world[Values["position"]]["options"]

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


        Values["position"] = choice["outcome"]
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
                print(Values["inventory"])
            case "status":
                print(f"Health:{Values["Health"]}/{Values["maxHealth"]},Level:{Values["level"]}")
            case _:
                print("Not an option!!!! (or you messed up typing it)")

        
            
    Main()

def extras(data):
    global Values
    match data["type"]:
        case "heal":
            global Heal
            Heal(data["amount"])
        case "give":
            Values["inventory"].append(data["item"])
        case "take":
            Values["inventory"].remove(data["item"])


        case "set variable":
            
            Values[data["key"]] = data["value"]
            



        case "set saved variable":
            global SavedExtras
            SavedExtras[data["key"]] = data["value"]



        case _:
            pass

def conditions(data):
    match data["type"]:
        case "has":
            out = Values["inventory"].count(data["item"]) >= data["count"]
        case "greater":
            out = Values[data["key"]] > data["value"]
        case "less":
            out = Values[data["key"]] < data["value"]
        case "greaterequal":
            out = Values[data["key"]] >= data["value"]
        case "lessequal":
            out = Values[data["key"]] <= data["value"]
        case "equal":
            out = Values[data["key"]] == data["value"]
        case _:
            pass
    if "not" in data:
        if data["not"]:
            return not out
        else:
            return out
    else:
        return out

Main()