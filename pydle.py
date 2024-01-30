from enum import Enum
from colorama import init, Fore, Back, Style
import random, os, json, requests, string

init(autoreset=True)
max_tries = 6
curr_try = 0
won = False
state = Enum('State', 'absent correct incorrect unknown')
words = json.loads(requests.get("https://github.com/droyson/go-fetch-words/blob/main/5-letter-words.json").json()["payload"]["blob"]["rawLines"][0])
current = list(words[random.randrange(0, len(words))])
spots = [[state.unknown] * len(current) for _ in range(max_tries)]
guesses = [[None] * len(current) for _ in range(max_tries)]
alphabet = dict.fromkeys(string.ascii_lowercase, state.unknown)
width = os.get_terminal_size()[0]
err = None
os.system('cls||clear')

def centerPrint(string, end = None, adj = None):
    pos = round(((width/2) - (len(string)/2)) + adj) if adj else round((width/2) - (len(string)/2))
    print(f"{pos*' '}{string}", end) if end else print(f"{pos*' '}{string}")

def printLogo():
    centerPrint(f"{Fore.YELLOW} _____     {Fore.BLUE}  _ _     ", adj = 5)
    centerPrint(f"{Fore.YELLOW}|  _  |_ _ {Fore.BLUE}_| | |___ ", adj = 5)
    centerPrint(f"{Fore.YELLOW}|   __| | |{Fore.BLUE} . | | -_|", adj = 5)
    centerPrint(f"{Fore.YELLOW}|__|  |_  |{Fore.BLUE}___|_|___|", adj = 5)
    centerPrint(f"{Fore.YELLOW}      |___|{Fore.BLUE}          ", adj = 5)
    centerPrint("—————————————————————")

def printTable(err = None):
    os.system('cls||clear')
    printLogo()
    for i in range(max_tries):
        print(f"{round((width/2) - (18/2))*' '}", end='')
        for (state, g) in zip(spots[i], guesses[i]):
            match state:
                case state.unknown:
                    print("[_]", end=' ')
                case state.absent:
                    print(f"{Fore.BLACK}[{g}]{Fore.RESET}", end=' ')
                case state.incorrect:
                    print(f"{Fore.YELLOW}[{g}]{Fore.RESET}", end=' ')
                case state.correct:
                    print(f"{Fore.GREEN}[{g}]{Fore.RESET}", end=' ')
        print("")
    printAlphabet(err)

def printAlphabet(err = None):
    centerPrint("—————————————————————")
    for i, char in enumerate(string.ascii_lowercase):
        match alphabet[char]:
            case state.unknown:
                colored_char = char.upper()
            case state.absent:
                colored_char = f"{Fore.BLACK}{char.upper()}{Fore.RESET}"
            case state.incorrect:
                colored_char = f"{Fore.YELLOW}{char.upper()}{Fore.RESET}"
            case state.correct:
                colored_char = f"{Fore.GREEN}{char.upper()}{Fore.RESET}"
        if i == 0:
            print(f"{round((width/2) - (19/2))*' '}{colored_char}", end=' ')
        elif i == 10:
            print(colored_char, end=f"\n{round((width/2) - (16/2))*' '}")
        elif i == 19:
            print(colored_char, end=f"\n{round((width/2) - (10/2))*' '}")
        else:
            print(colored_char, end=' ')
    print("")
    centerPrint("—————————————————————")
    if err:
        centerPrint(Fore.BLACK + Back.RED + Style.DIM + err, adj = 8)
        centerPrint("—————————————————————")

while curr_try < max_tries and won == False:
    printTable(err)
    guess = list(input(f"{round(width/2 - 21/2)*' '}> ").lower())
    if guess in guesses:
        err = "Already guessed that word!"
        continue
    elif len(guess) != 5:
        err = "Please provide a word with exactly 5 letters!"
        continue
    elif ''.join(guess) not in words:
        err = "Invalid word!"
        continue
    err = None
    guesses[curr_try] = guess
    lettercount = dict.fromkeys(current, 0)
    for spot, (letter, actual_letter) in enumerate(zip(guess, current)):
        if letter == actual_letter:
            spots[curr_try][spot] = state.correct
            alphabet[letter] = state.correct
            lettercount[letter] += 1
        else:
            spots[curr_try][spot] = state.absent
            alphabet[letter] = state.absent
    for spot, (letter, actual_letter) in enumerate(zip(guess, current)):
        if letter in current and lettercount[letter] < current.count(letter) and spots[curr_try][spot] != state.correct:
            spots[curr_try][spot] = state.incorrect
            alphabet[letter] = state.incorrect if alphabet[letter] != state.correct else None
            lettercount[letter] += 1
    if spots[curr_try].count(state.correct) == len(spots[curr_try]):
        won = True
    curr_try += 1

printTable()
if won:
    centerPrint("Congratulations!!")
    centerPrint(f"{curr_try}/6", adj=0.5)
    for guess in range(curr_try):
        print(f"{round((width/2) - (10/2))*' '}", end='')
        for state in spots[guess]:
            match state:
                case state.absent:
                    print("⬛", end='')
                case state.incorrect:
                    print("🟨", end='')
                case state.correct:
                    print("🟩", end='')
        print("")
    print("")
else:
    centerPrint(f"Better luck next time! The word was: {''.join(current)}.\n")