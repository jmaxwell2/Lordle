# LORDLE
"""
Created on Tue Feb  8 17:23:31 2022

@author: JMaxwell
"""

import random
from graphics import *

# const color values
yellow = color_rgb(255, 215, 0)
purple = color_rgb(86, 54, 125)
red = color_rgb(102, 0, 0)
loseJesus = Image(Point(625,200), 'JesusSawThat.ppm')
winJesus = Image(Point(130,720), 'wellDoneJesus.ppm')



''' This function creates the Word Dictionary that holds acceptable word guesses '''
''' returns the Word Dictionary '''
def createWordDict():
    # Open word file and read in the words
    file = open('theBibleWords.txt', 'r')
    Lines = file.readlines()
    
    # Create the dictionary used to store the words
    wordDict = {}
    
    # Add each word (each line) to the dictionary
    # both the key and value is each word
    for line in Lines:
        wordDict[line.strip().upper()] = line.strip().upper()

    return wordDict


''' This function creates the basic window for the game '''
''' returns the Window object '''
def createWindow():
    # this is supposed to create the interface
    win = GraphWin("LORDLE", 750,850)
    win.setBackground('black')
    title = Text(Point(375,50), 'L O R D L E')
    title.setFace('times roman')
    title.setSize(30)
    title.setStyle('bold')
    title.setFill(yellow)
    title.draw(win)
    
    return win


''' This function generates and displays the square tiles that the player uses to guess the word '''
''' returns a list of the square objects '''
def genSquares(win):
    squareList = []
    x_start = 102.5
    y_start = 50
    square_edge = 75
    dist = 80
    
    for y in range(6):
        y_value = y_start + (dist * y) + square_edge
        for x in range(5):
            # this will create and display all of the initial squares
            x_value = x_start + (dist * x) + square_edge
            topLeft = Point(x_value, y_value)
            botRight = Point(x_value + square_edge, y_value + square_edge)
            square = Rectangle(topLeft, botRight)
            square.setFill(color_rgb(75,75,75))
            square.draw(win)
            squareList.append(square)
            
    return squareList


''' This function reads in the keyboard from the txt file '''
''' returns a list of the letters '''
def readKeyboard():
    # read in the letters
    file = open('keyboard.txt', 'r')
    Lines = file.readlines()
    alphabetList = []
    for line in Lines:
        alphabetList.append(line.strip())
    
    return alphabetList


''' This function generates the keyboard at the bottom of the screen  '''
''' returns a list of letter objects '''
def displayKeyboard(win, alphabetList):
    # create the keybord and store the letter objects into a Dictionary (letter: object)
    keyboardDict = {}
    x_start = x_value = 215
    y_start = y_value = 685
    dist = 35
    count = 0
    for l in alphabetList:
        if l == 'A' or l == 'Z':
            x_start += 20
            y_value += 40
            count = 0
        x_value = x_start + (dist * count)
        letter = Text(Point(x_value, y_value), l)
        letter.setFill(color_rgb(75,75,75))
        letter.setSize(25)
        letter.setStyle('bold')
        letter.draw(win)
        keyboardDict[l] = letter
        count += 1

    return keyboardDict


''' Resets the squares to the original colors at the start of the game '''
def resetSquares(squareList):
    for s in squareList:
        s.setFill(color_rgb(75,75,75))


''' Generates and displays the text area '''
''' returns the entry word '''
def generateTextArea(win):
    # create the Entry object where the word is entered
    entry = Entry(Point(372.5,635), 10)
    entry.setSize(25)
    entry.setFill(color_rgb(75,75,75))
    entry.setTextColor('black')
    entry.setStyle('bold')
    entry.draw(win)
    
    while win.getKey() != 'Return':
        continue
    
    return entry.getText().upper()


''' This function validates the guess '''
''' returns True if the guess is valid, otherwise False '''
def validateGuess(guess, wordDict):
    valid = True
    if len(guess) != 5:
        valid = False
    if guess not in wordDict:
        valid = False
    
    return valid


''' This function calls all the functions necessary to correctly guess a word '''
''' returns a guess that meets all criteria '''
def guessWord(win, wordDict):
    # Promts the user for the word guess until the gues is valid
    valid = False
    while valid == False:
        guess = generateTextArea(win)
        valid = validateGuess(guess, wordDict)
        
    return guess.upper()


''' Generates a random word from the list that will be the answer word '''
''' returns the secret word '''
def generateSecretWord(wordDict):
    
    return random.choice(list(wordDict.values()))


''' This function calculates the frequency of each letter in the answer word '''
''' returns a list of frequencies '''
def freqList(word):
    freq = {}
    
    for i in range(len(word)):
        freq[word[i]] = frequency(word[i], word)

    return freq


''' returns the frequency of a letter in a word '''
def frequency(l, word):
    freq = 0
    for i in range(len(word)):
        if l == word[i]:
            freq += 1
            
    return freq


''' This function draws a square and displays the answer that the player did not get '''
def drawLoseSquare(answer, win):
    # draw the rectangle
    loseSquare = Rectangle(Point(315,80), Point(435,115))
    loseSquare.setFill('grey')
    loseSquare.setOutline(purple)
    loseSquare.draw(win)
    
    # display the target answer
    answerText = Text(Point(375,97.5), answer.upper())
    answerText.setFill('black')
    answerText.setSize(18)
    answerText.setStyle('bold')
    answerText.draw(win)
    
    # displays the losing Jesus image
    loseJesus.draw(win)
    
    return loseSquare, answerText


''' This function undraws the keyboard at the bottom of the screen '''
def deleteKeyboard(keyboardDict, win):
    # delete each letter through the loop
    for key in keyboardDict:
        keyboardDict[key].undraw()
    

''' This function is runs the complete gameplay of the game '''
def game(wordDict, alphabetList, win):
    # Displays the initial squares, and then stores the list of the square objects in a list
    squareList = genSquares(win)
     
    # Reads the keyboard txt file and then displays the alphabet at the bottom of the screen 
    keyboardDict = displayKeyboard(win, alphabetList)
    
    # Generate's the random word
    answer = generateSecretWord(wordDict)
    print(answer)
    
    # Guessing the word gameplay
    for row in range(6):
        correctLetters = 0
        
        # Promts the user to guess until the guess meets criteria
        guess = guessWord(win, wordDict)
        freqL = freqList(answer)
        
        # got through the word searching for CORRECT letters -> green
        column = 0
        for l in range(len(answer)):
            index = (row * 5) + column
            square = squareList[index]
            center = square.getCenter()
            if guess[l] == answer[l]:
                square.setFill(purple)
                letter = keyboardDict.__getitem__(guess[l].upper())
                letter.setFill(purple)
                correctLetters += 1
                freqL[guess[l]] -= 1
            # display guess[l] in the square's center point
            text = Text(center, guess[l])
            text.setStyle('bold')
            text.setSize(20)
            text.draw(win)
            # increment the column index
            column += 1
    
        # go through the word searching for letters in the answer, but not in the correct spot
        column = 0
        for l in range(len(answer)):
            index = (row * 5) + column
            square = squareList[index]
            center = square.getCenter()
            if guess[l] != answer[l] and guess[l] in answer:
                # if this letter's freqL is zero, then make it grey, otherwise make it yellow
                if freqL[guess[l]] == 0:
                    square.setFill('grey')
                    letter = keyboardDict.__getitem__(guess[l].upper())
                    letter.setFill('grey')
                else:
                    square.setFill(yellow)
                    letter = keyboardDict.__getitem__(guess[l].upper())
                    letter.setFill(yellow)
                    freqL[guess[l]] -= 1
            # display guess[l] in the square's center point
            text = Text(center, guess[l])
            text.setStyle('bold')
            text.setSize(20)
            text.draw(win)
            # increment the column index
            column += 1
            
        # then search for letters not in the word -> these will be grey
        column = 0
        for l in range(len(answer)):
            index = (row * 5) + column
            square = squareList[index]
            center = square.getCenter()
            if guess[l] not in answer:
                square.setFill('grey')
                letter = keyboardDict.__getitem__(guess[l].upper())
                letter.setFill('black')
            # display guess[l] in the square's center point
            text = Text(center, guess[l])
            text.setStyle('bold')
            text.setSize(20)
            text.draw(win)
            # increment the column index
            column += 1
        

        if correctLetters == 5:
            winJesus.draw(win)
            while win.getKey() != 'Return':
                continue
            winJesus.undraw()
            break
        
    # if it makes it here then the player lost
    if correctLetters != 5:
        loseSquare, answerText = drawLoseSquare(answer, win)
        while win.getKey() != 'Return':
            continue
        loseSquare.undraw()
        answerText.undraw()
        loseJesus.undraw()
    
    deleteKeyboard(keyboardDict, win)
    
    
    

def main():
    
    # Create the dictionary that holds the word list
    wordDict = createWordDict()
    
    # read in the keyboard letters file
    alphabetList = readKeyboard()
           
    # Create the Graphics Interface
    win = createWindow()
        
    # Gameplay!
    while True:
        game(wordDict, alphabetList, win)
        


# function calls
main()

