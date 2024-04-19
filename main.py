import json
saveData = open("save.json")
saveData = json.load(saveData)
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
    lastInput = ""
    lastInput = input()
    if lastInput in globals() and (not('_' in lastInput) and (lastInput.lower() == lastInput) and (lastInput != "json")):
        callFunc = globals()[lastInput]
        callFunc()
    else:
        print("not a valid command")
    if lastInput != "end":
        Main()
# Command Definitions
def heal():
    saveData["health"] += 1
    if saveData["health"] > saveData["maxHealth"]:
        saveData["health"] = saveData["maxHealth"]
def damage():
    saveData["health"] -= 1
    if saveData["health"] < 0:
        saveData["health"] = 0
def save():
    saveConv = json.dumps(saveData)
    with open("save.json", "w") as json_file:
        json_file.write(saveConv)
    print("Game Saved!")
def end():
    print("Goodbye")
def info():
    print(f"Health:{saveData["health"]}/{saveData["maxHealth"]}")
def help():
    print("Available Commands:")
    for x in globals():
        if (not('_' in x) and (x.lower() == x) and (x != "json")):
            print(x.lower())
Main()

