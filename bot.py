import discord
from discord.ext.commands import Bot
from discord.ext import commands 
import asyncio
import random
from bs4 import BeautifulSoup
import urllib.request
import re
import os
from boto.s3.connection import S3Connection

Client = discord.Client()
client = commands.Bot(command_prefix='$')
client.remove_command("help")

# Hangman variables
word = ""
guessesLeft = 6
playingHangman = False
blanks = []
guessedLetters=[]
lettersFound = 0

# Blackjack variables
playingBlackJack = False
dealerValue = 0
playerValue = 0
dealerCards = []
playerCards = []
dealerNumAces = 0
playerNumAces = 0
cardNames = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine',
             10: 'Ten', 11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
cardValues = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 10, 12: 10, 13: 10, 14: 11}

# Rock paper scissors variables (1 == rock, 2 == paper, 3 == scissors)
playingRPS = False
aiChoice = 0
playerChoice = 0
aiPoints = 0
playerPoints = 0

# Riddle variables
answering = False
riddle = ""
riddleAnswer = ""
riddleLine = 0
riddleGuessesLeft = 3
prevRiddleLine = 0

# Good Morning variable
gmOptionEnabled = False

@client.event
async def on_message(message):
    global gmOptionEnabled
    if gmOptionEnabled == True:
        author = message.author
        if str.lower(str(message.content)) == 'good morning' or str.lower(str(message.content)) == 'morning' or str.lower(str(message.content)) == 'mornin':
            await client.send_message(message.channel, 'Good morning, ' + str(author))
    await client.process_commands(message)

@client.command()
async def morninggreet(onOrOff):
    global gmOptionEnabled
    if str.lower(onOrOff) == "on" and gmOptionEnabled == False:
        gmOptionEnabled = True
        await client.say("PartyBot will now greet people when they say good morning")
    elif str.lower(onOrOff) == "off" and gmOptionEnabled == True:
        gmOptionEnabled = False
        await client.say("PartyBot will no longer greet people when they say good morning")

@client.command()
async def search(*, word):
    definition = ""
    linkWord = word.replace(' ', '+')
    url = 'https://www.wordnik.com/words/' + linkWord
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")
    definition = soup.select_one('.active > h3:nth-child(1)').text + "\n\n" + soup.select_one(".active > ul:nth-child(2) > li:nth-child(1)").text
    await client.say("**" + word + "\n\n" + definition + "**")

@client.command()
async def yt(*, word):
    linkWord = word.replace(' ', '+')
    url = 'https://www.youtube.com/results?sp=EgIQAQ%253D%253D&search_query=' + linkWord
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")
    vidLink = soup.find("div", {"class": "yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix"}).get("data-context-item-id")
    await client.say("https://www.youtube.com/watch?v=" + vidLink)

@client.command()
async def img(*, word):
    linkWord = word.replace(' ', '+')
    url = "https://imgur.com/search/time?q=" + linkWord + "&qs=thumbs"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")
    imgLinkList = soup.find_all("a", {"class": "image-list-link"})
    print(len(imgLinkList))
    imgLink = imgLinkList[random.randrange(0,len(imgLinkList))]
    imgLink = imgLink.get("href")
    # imgLink = imgContainerLink.find("img").get("src")
    # await client.say(imgLink.replace("//i.imgur.com/","https://i.imgur.com/"))
    await client.say("https://imgur.com/" + imgLink)

@client.command()
async def usearch(*, word):
    linkWord = word.replace(' ', '+')
    url = 'https://www.urbandictionary.com/define.php?term=' + linkWord
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")
    definition = soup.find("div", {"class": "meaning"}).text
    definition = definition.replace("&apos;", "").replace("\n","")
    example = soup.find("div", {"class": "example"}).text
    thumbsUp = soup.find("a", {"class": "up"}).find("span", {"class": "count"}).text
    thumbsDown = soup.find("a", {"class": "down"}).find("span", {"class": "count"}).text
    tags = soup.find("div", {"class": "tags"}).text
    tags = tags.replace("#"," #")
    withTags = True
    if(len(tags) < 3 ): withTags = False
    contributor = soup.find("div", {"class": "contributor"}).find("a").text
    contributeDate = soup.find("div", {"class": "contributor"}).text.replace("by","").replace(contributor,"").replace("  "," ").replace("\n","")
    example = example.replace("&apos;", "").replace("\n","")
    if(withTags): await client.say("**" + word + ": " + definition + "\n\n" + example + "\n\n" + ":thumbsup:" + thumbsUp + "  :thumbsdown:" + thumbsDown + "\n\n#" + tags[2:] + "\n\nContributed by " + contributor + " on" + contributeDate + "**")
    else: await client.say("**" + word + ": " + definition + "\n\n" + example + "\n\n" + ":thumbsup:" + thumbsUp + "  :thumbsdown:" + thumbsDown + "\n\nContributed by " + contributor + " on" + contributeDate + "**")


@client.command()
async def et(*, word):
    word = str.lower(word)
    word = word.replace('eggplant',':eggplant:').replace('bored', ':sleeping:').replace('hungry',':eggplant:')\
        .replace('happy', ':smiley_cat:').replace('angry',':anger:').replace('dont', ':no_entry_sign: ')\
        .replace('think', ':thinking:').replace('tired', ':sleeping:').replace('sleepy', ':sleeping:')\
        .replace('people', ':man_dancing:').replace('hate', ':angry:').replace('.', ':end:').replace('?', ':question:')\
        .replace('dislike', ':angry:').replace('barbecue', ':hamburger:').replace('bbq', '').replace('alone', ':broken_heart:')\
        .replace('mine', ':pick:').replace('mining', ':pick:').replace('dollars', ':euro:').replace('cash', ':euro:')\
        .replace('bucks', ':euro:').replace('money', ':euro:').replace('furry', ':smiley_cat:')\
        .replace('lovely', ':heart_decoration:').replace('wonderful', ':heart_decoration:') \
        .replace('lmaoo', ':rofl: :rofl:').replace('rofl', ':rofl: :rofl:').replace('!', ':grey_exclamation:') \
        .replace('guitar', ':guitar:').replace('musical', ':notes:').replace('alcohol', ':beers:').replace('wine', ':wine_glass:')\
        .replace('sports', ':soccer:').replace('sport', ':soccer: ').replace('olympics', ':medal:').replace('musician', ':guitar:')\
        .replace('stars', ':stars:').replace('shooting star', ':stars:').replace('loves', ':heart_eyes:')

    word = re.sub(r"\bu\b", ":point_up_2:", word)
    word = re.sub(r"\bperson\b", ":man_dancing:", word)
    word = re.sub(r"\bman\b", ":man_dancing:", word)
    word = re.sub(r"\bwoman\b", ":man_dancing:", word)
    word = re.sub(r"\bgirl\b", ":man_dancing:", word)
    word = re.sub(r"\bguy\b", ":man_dancing:", word)
    word = re.sub(r"\blady\b", ":man_dancing:", word)
    word = re.sub(r"\bo\b", "  :regional_indicator_o:  ", word)
    word = re.sub(r"\ba\b", "  :a:  ", word)
    word = re.sub(r"\bcat\b", ":smiley_cat:", word)
    word = re.sub(r"\bsad\b", ":sweat_drops:", word)
    word = re.sub(r"\bi\b", ":eye:", word)
    word = re.sub(r"\bim\b", ":eye:", word)
    word = re.sub(r"\bnot\b", ":no_good:", word)
    word = re.sub(r"\bk\b", ":ok_hand:", word)
    word = re.sub(r"\bok\b", ":ok_hand:", word)
    word = re.sub(r"\bokay\b", ":ok_hand:", word)
    word = re.sub(r"\bye\b", ":ok_hand:", word)
    word = re.sub(r"\bya\b", ":ok_hand:", word)
    word = re.sub(r"\byes\b", ":ok_hand:", word)
    word = re.sub(r"\byou\b", ":point_up_2:", word)
    word = re.sub(r"\byeh\b", ":ok_hand:", word)
    word = re.sub(r"\bno\b", ":no_entry_sign:", word)
    word = re.sub(r"\bye\b", ":ok_hand:", word)
    word = re.sub(r"\bare\b", "  :regional_indicator_r:  ", word)
    word = re.sub(r"\bam\b", "  :regional_indicator_i: :regional_indicator_s:  ", word)
    word = re.sub(r"\bis\b", "  :regional_indicator_i::regional_indicator_s:  ", word)
    word = re.sub(r"\bcan\b", ":canoe:", word)
    word = re.sub(r"\bcant\b", ":no_entry:", word)
    word = re.sub(r"\band\b", ":open_hands:", word)
    word = re.sub(r"\b&\b", ":open_hands:", word)
    word = re.sub(r"\bmusic\b", ":notes:", word)
    word = re.sub(r"\bart\b", ":art:", word)
    word = re.sub(r"\bolympic\b", ":medal:", word)
    word = re.sub(r"\blove\b", ":heart_eyes:", word)
    word = re.sub(r"\blike\b", ":heart:", word)
    word = re.sub(r"\bstar\b", ":stars:", word)
    word = re.sub(r"\blmao\b", ":rofl: :rofl:", word)
    word = re.sub(r"\bbeer\b", ":beers:", word)
    word = re.sub(r"\bbeers\b", ":beers:", word)
    word = re.sub(r"\bsay\b", ":speech_left:", word)
    word = re.sub(r"\bcode\b", ":desktop:", word)
    word = re.sub(r"\bprogram\b", ":desktop:", word)
    word = re.sub(r"\bprogramming\b", ":desktop:", word)
    word = re.sub(r"\bthis\b", ":point_down:", word)
    word = re.sub(r"\bits\b", ":point_down:", word)
    word = re.sub(r"\bwrite\b", ":pen_ballpoint:", word)
    word = re.sub(r"\writing\b", ":pen_ballpoint:", word)
    word = re.sub(r"\bpen\b", ":pen_ballpoint:", word)
    word = re.sub(r"\bpencil\b", ":pencil2:", word)
    word = re.sub(r"\bbut\b", ":shrug:", word)
    word = re.sub(r"\bgood\b", ":thumbsup:", word)
    word = re.sub(r"\bgreat\b", ":thumbsup: :thumbsup:", word)
    word = re.sub(r"\blol\b", ":laughing:", word)
    word = re.sub(r"\bbread\b", ":french_bread:", word)
    word = re.sub(r"\btoast\b", ":bread:", word)
    word = re.sub(r"\bcake\b", ":cake:", word)
    word = re.sub(r"\bcookie\b", ":cookie:", word)
    word = re.sub(r"\bpretty\b", ":white_flower:", word)
    word = re.sub(r"\bbeautiful\b", ":white_flower:", word)
    word = re.sub(r"\bdelightful\b", ":white_flower:", word)
    word = re.sub(r"\buwu\b", ":sunflower::white_flower::sunflower:", word)
    await client.say(word)


@client.command()
@commands.has_permissions(administrator=True)
async def delete(channel: discord.Channel, numberOfMessages):
    async for message in client.logs_from(channel, limit=int(numberOfMessages)+1):
        await client.delete_message(message)


@client.command()
async def riddle():
    global riddle, riddleLine, prevRiddleLine, riddleAnswer, riddleGuessesLeft, answering
    answering = True
    riddle = ""
    riddleAnswer = ""
    riddleGuessesLeft = 3

    with open("riddles.txt", "r") as f:
        lines = f.readlines()
    while riddle == "" or "=" in riddle or riddleLine == prevRiddleLine:
        riddleLine = random.randrange(0, len(lines))
        riddle = lines[riddleLine]
        riddleAnswer = lines[riddleLine+1]
    prevRiddleLine = riddleLine
    f.close()

    riddleAnswer = riddleAnswer.replace("=", "")
    riddleAnswer = riddleAnswer.replace(" ", "")

    await client.say("Use $answer <word> to solve the riddle.  All answers to these riddles will be one word or number.  You have three guesses per riddle.\n\n" + "`"+riddle+"`")

@client.command()
async def answer(userAnswer):
    global riddleAnswer, riddleGuessesLeft, answering

    if answering is False:
        await client.say("Use $riddle to receive another riddle")
        return

    userAnswer = userAnswer.strip()
    riddleAnswer = riddleAnswer.strip()

    if str.lower(userAnswer) == str.lower(riddleAnswer):
        await client.say("Correct!")
        answering = False
    else:
        riddleGuessesLeft -= 1
        await client.say("Incorrect!  Guesses left:" + str(riddleGuessesLeft))
    if riddleGuessesLeft == 0:
        await client.say("Out of guesses!  The answer was: " + riddleAnswer)

@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))

@client.command()
async def help():
    await client.say("`GAMES\n$hangman -> Start a new game of hangman"
                     "\n$blackjack -> Start a new game of blackjack"
                     "\n$riddle -> Get a riddle to answer"
                     "\n$rps -> Start a new game of rock, paper, scissors "
                     "\nUTILITY\n$search <word> -> search for a word's definition"
                     "\n$usearch <word> -> search for an urban dictionary word's definition"
                     "\n$yt <video name> -> search for the most relevant YouTube video given the name"
                     "\n$et <phrase> -> translate the phrase into emoji"
                     "\n$img <name> -> show a randomly chosen, recent and related image from imgur"
                     "\n$delete <channel name> <number> -> delete the last <number> messages from a specific channel (I.E. $delete general 100 to delete the last 100 messages in the general channel"
                     "\n$morninggreet <on/off> -> turn on bot greeting in response to user greetings (IE 'good morning')`")

@client.command()
async def rps():
    await client.say("""`
------           -     ------                        -----      -                        
| ___ \         | |    | --- \                      /  ___|    (_)                       
| |_/ /---   ---| | __ | |_/ /--- - --   ---  ----| \  --.  --- - --- ---  --- |----|--- 
|    // _ \ /---| |/ / |  --/ _  |  _ \ / - \|  __|  ---. \/ __| / __/ __|/ _ \|  --| __|
| |\ \ (_) | (__|   <  | | | (_| | |_) |  --/| |    /\__/ / (__| \__ \__ \ (_) | |  \__ 
\_| \_\---/ \---|_|\_\ \_|  \__ _|  __/ \--- |_|    \____/ \___|_|___/___/\___/|_|  |___/
                                 | |                                                    
                                 |_|                                                                                                                                              
    `""")

    await client.say("Type $choose rock/paper/scissors to make your choice for the round.  First to 3 points wins! ")
    global playingRPS
    playingRPS = True

@client.command()
async def choose(rockPaperOrScissors):
    global playingRPS, aiChoice, playerChoice, aiPoints, playerPoints

    if playingRPS is False:
        await client.say("Type $rps to play a game of rock paper scissors!")
        return

    #AI choice
    aiChoice = random.randrange(1,4)
    choiceList = {1:"rock", 2:"paper", 3:"scissors"}

    #Player choice
    if str.lower(rockPaperOrScissors) == "rock": playerChoice = 1
    if str.lower(rockPaperOrScissors) == "paper": playerChoice = 2
    if str.lower(rockPaperOrScissors) == "scissors": playerChoice = 3

    #See who won
    await client.say("You picked: " + rockPaperOrScissors + " and AI picked: " + choiceList[aiChoice] + ".")
    if playerChoice is 1 and aiChoice is 3 or playerChoice is 2 and aiChoice is 1 or playerChoice is 3 and aiChoice is 2:
        playerPoints += 1
        await client.say("You win the round!")
    elif playerChoice == aiChoice:
        await client.say("Tie!")
    else:
        aiPoints += 1
        await client.say("AI wins the round!")

    #End game if someone hit 3 points
    if playerPoints == 3:
        await client.say("You hit 3 points.  You win!")
        await endRPS()
        return
    if aiPoints == 3:
        await client.say("AI hit 3 points.  You lose!")
        await endRPS()
        return
    await client.say("Type $choose <rock/paper/scissors> to continue. ")
    await client.say("SCORE -> Player: " + str(playerPoints) + " AI: " + str(aiPoints))

async def endRPS():
    global playingRPS, aiChoice, playerChoice, aiPoints, playerPoints
    playingRPS = False
    aiChoice = 0
    playerChoice = 0
    aiPoints = 0
    playerPoints = 0

async def printCards(playerOrComputer):
    if playerOrComputer is 1:
        await client.say("Your value: " + str(playerValue))
        await client.say("Your cards: " + str.join(" ", playerCards))
    elif playerOrComputer is 2:
        await client.say("Dealer value: " + str(dealerValue))
        await client.say("Dealer cards: " + str.join(" ", dealerCards))
    elif playerOrComputer is 3:
        await client.say("Your value: " + str(playerValue))
        await client.say("Your cards: " + str.join(" ", playerCards))
        await client.say("Dealer value: " + str(dealerValue))
        await client.say("Dealer cards: " + str.join(" ", dealerCards))

async def resetBlackJack(finishedOrReset):
    global playingBlackJack, dealerValue, playerValue, dealerCards, playerCards, dealerNumAces, playerNumAces, cardNames, cardValues
    if finishedOrReset is 0:
        await printCards(3) #Print both player and AI's values and cards
        if(playerValue > 21 or playerValue <= 21 and dealerValue <= 21 and playerValue < dealerValue):
            await client.say("You lose!")
        elif(dealerValue > 21 or playerValue <= 21 and dealerValue <= 21 and playerValue > dealerValue):
            await client.say("You win!")
        playingBlackJack = False
    dealerValue = 0
    playerValue = 0
    dealerCards = []
    playerCards = []
    dealerNumAces = 0
    playerNumAces = 0

@client.command()
async def blackjack():
    await client.say("""`
 _     _            _     _            _    
| |__ | | __ _  ___| | __(_) __ _  ___| | __
|  _ \| |/ _  |/ __| |/ /| |/ _  |/ __| |/ /
| |_) | | (_| | (__|   < | | (_| | (__|   < 
|_ __/|_|\__,_|\___|_|\_\/ |\__ _|\___|_|\_
                       |__/                                                                           
    `""")
    await resetBlackJack(1)
    global playingBlackJack, dealerValue, playerValue, dealerCards, playerCards, dealerNumAces, playerNumAces, cardNames, cardValues
    playingBlackJack = True

    #Simulate dealer's turn
    while dealerValue < 17:
        nextCard = random.randrange(1,15)
        if nextCard is 14: dealerNumAces += 1
        dealerCards.append(cardNames[nextCard])
        dealerValue += cardValues[nextCard]
        while dealerValue > 21:
            if(dealerNumAces > 0):
                dealerValue -= 10
                dealerNumAces -= 1
            else: break

    #Give player 2 cards
    for i in range(0,2):
        nextCard = random.randrange(1, 15)
        playerValue += cardValues[nextCard]
        playerCards.append(cardNames[nextCard])

    #print("Dealer value: " + str(dealerValue))
    #print("Dealer cards: " + str.join(" ", dealerCards))
    await client.say("Say $hit to be dealt another card, and $stay to stick with your current total value.")
    await client.say("Dealer's first card is: " + dealerCards[0])
    await printCards(1) #Print player cards/value

@client.command()
async def hit():
    if playingBlackJack is False:
        await client.say("Type $blackjack to begin a game of blackjack")
        return
    global playerValue, playerCards, playerNumAces
    nextCard = random.randrange(1, 15)
    if nextCard is 14: playerNumAces += 1
    playerCards.append(cardNames[nextCard])
    playerValue += cardValues[nextCard]
    while playerValue > 21:
        if (playerNumAces > 0):
            playerValue -= 10
            playerNumAces -= 1
        else:
            await resetBlackJack(0)
            break
    await printCards(1) #Print player cards/value

@client.command()
async def stay():
    if playingBlackJack is False:
        await client.say("Type $blackjack to begin a game of blackjack")
        return
    await resetBlackJack(0) #End the game

@client.command()
async def hangman():
    global playingHangman, word, guessesLeft, blanks, lettersFound, guessedLetters
    lines = []
    with open("hangmanwords.txt", "r") as f:
        lines = f.readlines()
    random_line_num = random.randrange(0, len(lines))
    word = lines[random_line_num]
    f.close()
    blanks = []
    guessedLetters = []
    lettersFound = 0
    guessesLeft = 6
    playingHangman = True
    for i in range(1, len(word)):
        blanks .append("-")
    await client.say("""`                                                                      
  _                                   
 | |_  ____ _ _  __ _ _ __  __ _ _ _  
 | - \/ -  | - \/ -  |  - \/ -  | - \ 
 |_||_\__,_|_||_\__, |_|_|_\__,_|_||_|
                |___/                                                                                                   
`""")

    await client.say("Welcome to hangman.")
    await client.say("You have " + str(guessesLeft) + " "
                                                      "guesses to get all of the letters in the word.  "
                                                      "To guess a letter, type $guess letter \n" + " ".join(blanks))

@client.command()
async def guess(guess):
    global playingHangman
    global word
    global guessesLeft
    global blanks
    global lettersFound
    global guessedLetters
    if playingHangman is True:
        if str.isalpha(guess) and len(guess) is 1 and str.lower(guess) not in guessedLetters:
            if str.lower(guess) in word:
                await client.say(guess + " is in the word.  Good job!")
                for i in range(0, len(word)):
                    if word[i] == str.lower(guess):
                        blanks[i] = str.lower(guess)
                        lettersFound += 1

            else:
                await client.say(guess + " is NOT in the word.")
                guessesLeft -= 1

            guessedLetters.append(str.lower(guess))
            await client.say(" ".join(blanks))
            await client.say("Guessed letters: " + " ".join(guessedLetters))
            await client.say("Guesses left: " + str(guessesLeft))
            #print(lettersFound)
            #print(len(word))

            if guessesLeft == 0:
                await client.say("No guesses left.  You lose!")
                playingHangman = False
            if lettersFound == len(word)-1:
                await client.say("You guessed all the letters!  You've won!  The word was: " + word)
                playingHangman = False

        else:
            await client.say("ERROR: You can only guess with single letters that haven't already been entered.")
            await client.say("Guessed letters: " + " ".join(guessedLetters))

    else: await client.say("Start a game of Hangman with $hangman before trying to guess a letter!")

s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])
client.run(os.environ['DISCORD'])