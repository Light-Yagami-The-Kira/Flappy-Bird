import os
import sys
def startGame():
    os.system('start game.py')

def endGame():
    sys.exit()

def showScore():
    with open('score.txt', 'r') as f:
        content = f.read()
        if content == "":
            print("No History Found...")
            return
        print(content)

def showHighScore():
    with open('score.txt', 'r') as f:
        content = f.read()
        if content == "":
            print("No History Found...")
            return
        content = content.split('\n')
        content = [data.split('|') for data in content[:-1]]
        scores = [item[1] for item in content]
        maxm_score = max(scores)

        def max_finder_filter_func(nested_list):
            if nested_list[1] == maxm_score:
                return nested_list

        highScores_ = list(filter(max_finder_filter_func, content))

        highScores_Dates = list(map(lambda x: x[0], highScores_))

        print("HighScore Obtained is: ", maxm_score, "on: ")

        print("\n".join(highScores_Dates))


def clearScore():
    with open("score.txt", "w") as f:
        f.write("")

def invalidSyntax():
    print("Not a valid command... Please Try again...")

def clearScreen():
    os.system('cls')

def showMenu():
    print('''
1. Start the Flappy Bird Game
2. Show history of Scores Achieved
3. Show the Highest Score
4. Clear All the Scores
5. Exit the Game Launcher
6. Clear The Game Launcher Terminal Screen
''')

if __name__ == '__main__':

    switch = {

        '1' : startGame,
        '2' : showScore,
        '3' : showHighScore,
        '4' : clearScore,
        '5' : endGame,
        '6' : clearScreen

    }

    print("WELCOME TO FLAPPY BIRD GAME LAUNCHER")
    while True:
        showMenu()
        UI = input(">>> Enter your input: ")

        if UI not in switch.keys():
            invalidSyntax()
        else:
            switch[UI]()
        
