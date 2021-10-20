import pygame
import random
from time import sleep

# imports the pygame module for a graphical output.
# imports the random module for drawing cards out the deck.
# imports the time module to allow for delay between actions.

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

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 150, 0)
blue = (10, 25, 50)

# initialises colours to be used.

pygame.init()
screen = pygame.display.set_mode((500, 350))
pygame.display.set_caption("Blackjack")

# creates a pygame window with a caption.

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

cardsOnScreen = pygame.sprite.Group()
buttons = pygame.sprite.Group()
mouseCursor = pygame.sprite.Group()

# creates sprite groups for the cards, buttons and the mouse cursor.

Run = True
mousePosition = [0] * 2
pygame.mouse.set_visible(False)

class NewCard(pygame.sprite.Sprite):

    def __init__(self, card, x, y):
        pygame.sprite.Sprite.__init__(self)
        card_image_temp = card_look_up(card)
        card_image = pygame.image.load(card_image_temp)
        self.image = pygame.Surface([69, 100])
        self.image.set_colorkey(black)
        self.image = pygame.transform.smoothscale(card_image, [69, 100])
        self.image.blit(card_image, [0, 0])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # a class to create a new card object to be shown on screen and draws from a folder with card images.

class NewButton(pygame.sprite.Sprite):

    def __init__(self, colour, text, position):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.position = position
        self.image = pygame.Surface((position[2], position[3]))
        self.image.fill(colour)
        self.image.set_colorkey(green)

        # assigns variables for the button to use.

        pygame.draw.rect(self.image, colour, pygame.Rect(0, 0, position[2], position[3]))

        # draws the button as a rectangle.

        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        # assigns rectangle specific variables.

class MouseCursor(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        mouseImage = pygame.image.load("Playing Cards/PNG-cards-1.3/Ace Of SpadesMouse.png")
        self.image = pygame.Surface([34, 50])
        self.image.set_colorkey(black)
        self.image = pygame.transform.scale(mouseImage, [34, 50])
        self.image.blit(mouseImage, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        # does a similar function to the previous two but creates a card image at the mouse cursor.

    def move_mouse(self, MousePosition):
        self.rect.x = MousePosition[0]
        self.rect.y = MousePosition[1]

        # sets the x and y positions of the MouseCursor object to be the same as the mouse cursor of the player.

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
    UseAceException = 0

    # total variable is assigned to count the total value of the cards.

    for x in range(len(player_card)):

        # loops for all the cards the player has.

        if player_card[x][0] == "Ace":
            UseAceException += 1

            # if the card is an ace the UseAceException variable had one added to it.

        else:
            total += deckValues[player_card[x][0]]

        # other wise the value of the card is added using the dictionary, this value is then returned.

    if UseAceException > 0:
        for x in range(UseAceException):
            total = ace_exception(total)

        # loops for the amount of aces in the player#s hand.

    return total

def card_look_up(card):
    data = "".join(j for i in card for j in i)
    return "Playing Cards/PNG-cards-1.3/"+"".join(data) + ".png"

    # this is used to convert the card variable into the format the images use.

def check_bust(total):
    if total >= 21:
        bust = True
    else:
        bust = False

    # checks to see if the player has got over ot equal to 21 if so the player is considered bust and the bust
    # variable is changed to False. This is done even at 21 to stop the game is the player get 21 at any time.

    return bust

def comp_bust():
    result = card_add(compCards)

    while result < 16:
        sleep(0.5)
        draw(35, compCards)
        result = card_add(compCards)

    # forces the computer to draw another card if the value of their cards is under 16.

    if result > 21:
        result = "Bust"

    # sets the value of the computer's cards to bust if teh go over 21.

    return result

def comp_output():
    for x in range(2):
        draw(35, compCards)
    result = comp_bust()

    # does the same thing as the draw() function and shows the cards to the player.
    # then the value of the computer's cards are calculated using the comp_Bust() procedure and then returned.

    return result

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

def draw(y, HeldCards):
    card = create_card()
    HeldCards.append(card)
    draw_cards(card, HeldCards, y)

def draw_cards(card, CardsHeld, y):
    x = 0

    for Counter in range(len(CardsHeld)):
        x += 35

        # loops through the card hand and sets the x variable to be 35 more than the previous to stop the cards from
        # overlapping.

    Card = NewCard(card, x, y)

    # takes the text version of the card and creates a NewCard object with it.

    cardsOnScreen.add(Card)
    cardsOnScreen.draw(screen)
    pygame.display.flip()

    # this is then appended to the sprite group and drawn to the screen.
    # the screen is then updated.

def draw_to_screen():
    screen.fill(green)
    cardsOnScreen.draw(screen)
    buttons.draw(screen)
    mouseCursor.draw(screen)
    for button in buttons:
        text_button_to_screen(button)

    # draws all objects to the screen.

def main(run):

    bust, mouse, totalVal = startup()

    while run and not bust:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEMOTION:
                mousePosition[:] = list(event.pos)
                mouse.move_mouse(mousePosition)

                # gets the position of the mouse and then move the mouse object to said position.

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                collision = pygame.sprite.groupcollide(buttons, mouseCursor, False, False)

                # find if hte player has pressed a button.

                for button in collision:
                    run = play_input(button.text)

                # calls the play input procedure with the text from the button the player pressed.

                totalVal = card_add(playerCards)
                bust = check_bust(totalVal)

                # determines the current value of the players hand.

        draw_to_screen()
        pygame.display.flip()
        clock.tick(60)

    CompResult = comp_output()

    # plays the computer's turn using the comp_output() procedure.

    win(bust, CompResult, totalVal)

    # determines who has one using the win() function.

    sleep(2)

    # waits for two seconds before exiting th game.

    pygame.quit()

def play_input(choice):

    if choice == "Stick":
        run = False

    elif choice == "Hit":
        draw(200, playerCards)
        run = True

    # uses the text form the button the user pressed to find their choice,
    # then either draws another card or sets the game to end depending on the response

    return run

def startup():
    Mouse = MouseCursor()
    mouseCursor.add(Mouse)

    # creates a MouseCursor object and appends it to the sprite group mouseCursor.

    hitButton = NewButton(blue, 'Hit', [350, 180, 100, 50])
    StickButton = NewButton(blue, 'Stick', [350, 255, 100, 50])
    buttons.add(StickButton)
    buttons.add(hitButton)
    buttons.draw(screen)

    # creates two buttons using the NewButton class, appends them to the sprite group buttons and then draws them to the
    # screen.

    for counter in range(2):
        draw(200, playerCards)

    # draws two cards at the start of the game.

    TotalVal = card_add(playerCards)
    Bust = check_bust(TotalVal)

    return Bust, Mouse, TotalVal

def text_button_to_screen(button):
    style = pygame.font.Font(None, 18)
    text_formatting(button.text, button.position, style, white)

    # draws text to the screen

def text_formatting(text, position, style, colour):
    textWidth, textHeight = style.size(text)
    message = style.render(text, 1, colour)
    x = position[0] + position[2] // 2 - textWidth // 2
    y = position[1] + position[3] // 2 - textHeight // 2
    screen.blit(message, (x, y))

    # uses style.size to find the size of the text and then draws the text in the middle of the object using that
    # information.

def win(bust, comp_result, play_result):
    if play_result == 21:
        texting = "Got 21"

        # checks if the player has gotten 21 and if they have the player is shown a victory message. This is done
        # first as the bust variable is written as True if the player gets 21.

    elif bust:
        texting = "Went Bust"

    else:
        if comp_result == 21:
            texting = "Computer Wins"

        elif comp_result == "Bust":
            texting = "You Win"

        # if the computer gets or goes over 21 the appropriate message is shown.

        elif play_result == comp_result:
            texting = "Draw"

        elif play_result > comp_result:
            texting = "You Win"

        else:
            texting = "Computer Wins"

        # if neither of these happen whoever got the highest score wins.

    text_formatting(texting, (0, 0, 500, 350), font, black)
    pygame.display.flip()

if __name__ == '__main__':
    main(Run)
