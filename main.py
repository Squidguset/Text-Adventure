import json
import os
if not os.path.exists("save.json"):
    
    a = open("save.json", "w")
    
    a.write("{\"inventory\": [], \"health\": 10, \"maxHealth\": 10, \"level\":1, \"position\":\"start\"}")
    a.close()


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

def Give(item):
    inventory.append(item)




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

    

    choice = options[input(">>>> ")]

    if choice == "Description":
        print("desc")
    else:
        position = choice["outcome"]
        print(choice["onpick"])
        

        # Extra Functions
        if "extra" in choice.keys() :
            print(choice["extra"])
                
            
        


        Main()

Main()