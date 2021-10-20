import random

# imports the random module for drawing card out the deck

deck = [
    "Ace",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King"
]
suits = [
    " Of Spades",
    " Of Hearts",
    " Of Clubs",
    " Of Diamonds"
]

# assigns two parallel arrays to be used as the card suit and the card value. This is used to tell the player which
# card the have.

deckValues = {
    "Ace": "1 or 11",
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10
}

# assigns a dictionary to be used to find out what value each card has.

playerCards = []
compCards = []

# creates two lists to store the cards the player and computer has.

Bust = False
Run = True

# two variables which wil cause the game to end if either is True.


def create_card():
    suit = random.randint(0, 3)
    suit = suits[suit]

    # assigns the variable suit with a random number and then uses the array suits to assign a suit to the card.

    card_val = random.randint(0, 12)
    card_val = deck[card_val]

    # assigns the variable card_val with a random number and to be used to assign a value to the card.
    # using the deck array it assigns the value of the card based on the random number.

    for COUNTER in range(len(playerCards) - 1):

        # loops though the whole array of playerCards.

        while playerCards[COUNTER] == card_val and playerCards[COUNTER] == suit:

            # the card is checked to make sure one does not already exist but checking the currents card's value and
            # suit with all cards in the playerCard array. If it already exists ir repeats the process until it
            # creates a card that is not held by the player

            card_val = random.randint(0, 12)
            card_val = deck[card_val]

    card = [card_val, suit]

    # once a card has been created and has been verified to not already be held by the player, that card is returned.

    return card


def card_print(card_example):

    # a small print statement just to print the cards without having the formatting of an array.
    # i.e. "Ace of Diamonds" rather than "['Ace', ' Of Diamonds']"

    print(*card_example, sep='')


def ace_exception(total):
    if total + 11 > 21:
        total += 1
    else:
        total += 11

    # to be used when adding the value of cards up. As an ace can either be one or ten this is automatically decided
    # by seeing if the player would go bust by adding eleven, if so then only one is added.

    return total


def card_add(player_card):
    total = 0

    # total variable is assigned to count the total value of the cards.

    for x in range(len(player_card)):

        # loops for all the cards the player has.

        if player_card[x][0] == "Ace":
            total = ace_exception(total)

            # if the card is an ace the ace_exception() procedure is called.

        else:
            total += deckValues[player_card[x][0]]

            # other wise the value of the card is added using the dictionary, this value is then returned.

    return total


def check_bust(total):
    if total >= 21:
        bust = True
    else:
        bust = False

    # checks to see if the player has got over ot equal to 21 if so the player is considered bust and the bust
    # variable is changed to False. This is done even at 21 to stop the game is the player get 21 at any time.

    return bust


def draw():
    card = create_card()
    card_print(card)
    playerCards.append(card)

    # creates a card using the create_card() procedure and then shows that card using the card_print() function. Then
    # adds that card onto the playerCards list


def win(bust, comp_result, play_result):
    if play_result == 21:
        print("Got 21")

        # checks if the player has gotten 21 and if they have the player is shown a victory message. This is done
        # first as the bust variable is written as True if the player gets 21.

    elif bust:
        print("Went bust")

    else:
        if comp_result == 21:
            print("Computer Wins")

        elif comp_result == "Bust":
            print("You win")

        # if the computer gets or goes over 21 the appropriate message is shown.

        elif play_result > comp_result:
            print("Player wins")

        else:
            print("Computer Wins")

        # if neither of these happen whoever got the highest score wins.


def play_input():
    choice = input("Would you like to stick or draw? (S, D) ")

    if choice == "S" or choice == "s":
        run = False

    elif choice == "D" or choice == "d":
        draw()
        run = True

    else:
        print("Please enter S or D")
        run = play_input()

    # ask the player if they would like to stick or draw, either capital or lowercase letters "d" and "s" are
    # accepted. then either draws another card or sets the game to end depending on the response and if no response
    # if given that acceptable the function will repeat until is has either an "d" or "s".

    return run


def comp_output():
    card = create_card()
    compCards.append(card)
    result = comp_Bust()

    # does the same thing as the draw() function but does not show the cards to the player.
    # then the value of the computer's cards are calculated using the comp_Bust() procedure and then returned.

    return result


def comp_Bust():
    result = card_add(compCards)

    while result < 16:
        card = create_card()
        compCards.append(card)
        result = card_add(compCards)

    # forced the computer to draw another card f the value of their cards is under 16.

    if result > 21:
        result = "Bust"

    # sets the value of the computer's cards to bust if teh go over 21.

    return result


for counter in range(2):
    draw()

# draws two cards for the player.

totalVal = card_add(playerCards)
Bust = check_bust(totalVal)

# the cards are counted just in case the players gets 21 in the first deal, if this is the game the game ends and the
# player doesn't continue the main loop.

while Run and not Bust:

    # loops until the player goes bust or chooses to not draw a card.

    Run = play_input()

    # determines if the player wants to draw a card or not.

    totalVal = card_add(playerCards)
    Bust = check_bust(totalVal)

    # determines if the player has gone bust or gotten 21.

CompResult = comp_output()

# plays the computer's turn using the comp_output() procedure.

win(Bust, CompResult, totalVal)

# determines who has one using the win() function.
