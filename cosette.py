import random
import subprocess
import pyperclip
import re

EXIT_KEYWORDS = ["exit", "q", "quit", "goodbye", "bye"]
HELLO_KEYWORDS = ["hello", "hi"]
HELP_KEYWORDS = ["help", "what can you do", "commands"]
WIFI_HISTORY_KEYWORDS = ["all wifi", "wifi history", "past wifi",
                         "all networks", "past networks", "network history"]
CUR_WIFI_KEYWORDS = ["current network", "current wifi", "connected to"]


#processes input text and returns output as string
def process(query):
    #prepare text input
    query = query.lower().strip()

    #empty input
    if query == "":
        return ""
    #exit condition
    elif search(query, EXIT_KEYWORDS):
        return "Bye bye"
    #hello condition
    elif search(query, HELLO_KEYWORDS):
        return hello()
    #show commands condition
    elif search(query, HELP_KEYWORDS):
        return commands()
    #show all wifi networks
    elif search(query, WIFI_HISTORY_KEYWORDS):
        return all_networks()
    #show current wifi
    elif search(query, CUR_WIFI_KEYWORDS):
        return current_network()
    #error statement
    else:
        return "Sorry I don't understand :("


#helper method for search
def search_helper(w):
    return re.compile(r'\b({0})\b'.format(w)).search


#searches for a word in a sentence in a list
def search(key, list_):
    for item in list_:
        if (search_helper(item)(key)):
            return True
    return False


#returns hello messages
def hello():
    greetings = ["Hi, how can I help?", "Hello, what can I do for you today?",
                 "Hi, what can I do for you today?", "Hello, how can I help?"]
    return random.choice(greetings)


#returns possible actions
def commands():
    ret = newCommand("key words (include one in your query)",
                     "functionality (what I do)")
    ret += newCommand(", ".join(HELP_KEYWORDS),
                      "Shows list of all functions.")
    ret += newCommand(", ".join(EXIT_KEYWORDS),
                      "Exits Cosette.")
    ret += newCommand(", ".join(WIFI_HISTORY_KEYWORDS),
                      "Shows all wifi networks connected to in the past and copies them to your clipboard")
    ret += newCommand(", ".join(WIFI_HISTORY_KEYWORDS),
                      "Shows current wifi networks connected to and copies it to your clipboard")

    return ret


#returns formatted new command definition as string
def newCommand(key_words, functionality):
    return "\"" + key_words + "\"\n\n- " + functionality + "\n\n\n"


#returns all wifi networks in history
def all_networks():
    res = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode('utf-8').split('\n')
    profile_names = [x for x in res if "All User Profile" in x]
    ret = "\n".join(profile_names)
    ret = ret.replace("    All User Profile     : ", "")
    clip = ret.replace("\n", ", ").strip()
    pyperclip.copy(clip)
    ret = "Here is your wifi history:\n\n" + ret + "\n\nI've added it to your clipboard :)"
    return ret


#returns name of current connected network
def current_network():
    res = subprocess.check_output(["netsh", "wlan", "show", "interfaces"]).decode('utf-8').split('\n')
    ssid_line = [x for x in res if "SSID" in x and "BSSID" not in x]
    if ssid_line:
        ssid_list = ssid_line[0].split(':')
        connected_ssid = ssid_list[1].strip()
        pyperclip.copy(connected_ssid)
        return "You're currently connected to network " + connected_ssid +\
               "\n\nI've added it to your clipboard :)"
    else:
        return "No wifi found :("
