import random
import subprocess
import pyperclip

EXIT_KEYWORDS = ["exit", "q", "quit", "goodbye", "bye"]
HELLO_KEYWORDS = ["hello", "hi"]
HELP_KEYWORDS = ["help", "what can you do", "commands"]


#processes input text and returns output as string
def process(text):
    #prepare text input
    text = text.lower().strip()

    #empty input
    if text == "":
        return ""
    #exit condition
    elif search(text, EXIT_KEYWORDS):
        return "Bye bye"
    #hello condition
    elif search(text, HELLO_KEYWORDS):
        return random.choice(["Hello, what can I do for you today?",
                              "Hi, how can I help?"])
    #show commands condition
    elif search(text, HELP_KEYWORDS):
        return commands()
    #show all wifi networks
    elif search(text, ["past networks", "network history"]):
        return all_wifi_networks()
    #error statement
    else:
        return "Sorry I don't understand :("


#searches for a word in a sentence in a list
def search(key, list_):
    return any(word in key for word in list_)


#returns possible actions
def commands():
    res = "-------------------------------------------------------------------------------------\n" \
          "- key words (include one in your query)\n\n" \
          "- functionality (what I do)\n" \
          "-------------------------------------------------------------------------------------\n\n"
    res += newCommand("exit, q, quit, goodbye, bye",
                      "Exits Cosette.")
    res += newCommand("help, what can you do, commands",
                      "Shows list of all functions.")
    res += newCommand("past networks, network history",
                      "Shows all networks connected to in the past\n  and copies them to your clipboard")

    return res


#returns formatted new command definition as string
def newCommand(key_words, functionality):
    definition = "-------------------------------------------------------------------------------------\n"
    definition += "- " + key_words + "\n\n"
    definition += "- " + functionality + "\n"
    definition += "-------------------------------------------------------------------------------------\n\n"
    return definition


#returns all wifi networks in history
def all_wifi_networks():
    r = subprocess.run(["netsh", "wlan", "show", "network"], capture_output=True, text=True).stdout
    ls = r.split("\n")
    ssids = [k for k in ls if 'SSID' in k]

    res = "You have " + str(len(ssids)) + " networks saved...\n\n"
    res += "\n".join(ssids)
    res = res.replace("SSID ", "")
    res += "\n\nI've added them to your clipboard :)"

    clip = ", ".join(ssids).replace("SSID ", "")
    pyperclip.copy(clip)

    return res
