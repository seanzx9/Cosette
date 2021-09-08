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
WIFI_PASSWORD_KEYWORDS = ["wifi password for", "wifi password of"]
WIFI_PASSWORD_INSTR = ["wifi password for <WIFI_NAME>", "wifi password of <WIFI_NAME>"]
WIFI_PASSWORD_CURRENT_KEYWORDS = ["this wifi password", "this network password"]


#processes input text and returns output as string
def process(query):
    #prepare text input
    query_lower = query.lower().strip()

    #empty input
    if query_lower == "":
        return ""
    #exit condition
    elif search(query_lower, EXIT_KEYWORDS):
        return "Bye bye"
    #hello condition
    elif search(query_lower, HELLO_KEYWORDS):
        return hello()
    #show commands condition
    elif search(query_lower, HELP_KEYWORDS):
        return get_commands()
    #show all wifi networks
    elif search(query_lower, WIFI_HISTORY_KEYWORDS):
        return get_all_networks()
    #show current wifi
    elif search(query_lower, CUR_WIFI_KEYWORDS):
        return get_current_network()
    #get wifi password of requested network
    elif search(query_lower, WIFI_PASSWORD_KEYWORDS):
        return get_wifi_password(query)
    elif search(query_lower, WIFI_PASSWORD_CURRENT_KEYWORDS):
        return get_current_wifi_password()
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
def get_commands():
    ret = newCommand("key words (include one in your query)",
                     "functionality (what I do)")
    ret += newCommand(" || ".join(HELP_KEYWORDS),
                      "Shows list of all functions.")
    ret += newCommand(" || ".join(EXIT_KEYWORDS),
                      "Exits Cosette.")
    ret += newCommand(" || ".join(WIFI_HISTORY_KEYWORDS),
                      "Shows all wifi networks connected to in the past and copies them to your clipboard")
    ret += newCommand(" || ".join(WIFI_HISTORY_KEYWORDS),
                      "Shows current wifi networks connected to and copies it to your clipboard")
    ret += newCommand(" || ".join(WIFI_PASSWORD_INSTR),
                      "Shows wifi password requested and copies it to your clipboard")

    return ret


#returns formatted new command definition as string
def newCommand(key_words, functionality):
    return "> \"" + key_words + "\"\n> " + functionality + "\n\n\n"


#returns all wifi networks in history
def get_all_networks():
    #get raw list of profiles
    res = subprocess.check_output(["netsh", "wlan", "show", "profiles"])
    res = res.decode('utf-8').split('\n')

    #keep lines with "All User Profile"
    profile_names = [x for x in res if "All User Profile" in x]

    #separate lines by newline
    ret = "\n".join(profile_names)

    #remove extra text
    ret = ret.replace("    All User Profile     : ", "")

    #copy comma separated list to clipboard
    clip = ret.replace("\n", ", ").strip()
    pyperclip.copy(clip)

    return "Here is your wifi history:\n\n" + ret + "\n\nI've added it to your clipboard :)"


#returns name of current connected network
def get_current_network():
    #get raw interface list
    res = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
    res = res.decode('utf-8').split('\n')

    #get all lines that contain SSID and not BSSID
    ssid_line = [x for x in res if "SSID" in x and "BSSID" not in x]

    #return name if a network can be found
    if ssid_line:
        ssid_list = ssid_line[0].split(':')
        connected_ssid = ssid_list[1].strip()

        #copy ssid to clipboard
        pyperclip.copy(connected_ssid)

        return "You're currently connected to network " + connected_ssid + " " +\
               "\n\nI've added it to your clipboard :)"
    else:
        return "Wifi not found :("


#returns wifi password of name provided
def get_wifi_password(query):
    #get last word of query (profile name)
    query = query.split(" ")
    profile = str(query[len(query) - 1])

    #check if ssid exists in history
    network_list = get_all_networks()
    if profile in network_list:
        res = subprocess.check_output(["netsh", "wlan", "show", "profiles", profile, "key=clear"])
        res = res.decode('utf-8').split('\n')

        #get line with key
        password = str([x for x in res if "Key Content" in x][0])
        password = password.replace("    Key Content            : ", "").strip()

        #copy password to clipboard
        pyperclip.copy(password)

        return "The password is " + password + " " +\
               "\n\nI've added it to your clipboard :)"
    else:
        return "I can't seem to find a network named " + profile + " :("


#returns wifi password of current wifi if connected
def get_current_wifi_password():
    current_profile = get_current_network().split(" ")[5]
    return get_wifi_password(current_profile)
