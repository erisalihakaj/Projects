#!/usr/bin/env python3

from sys import argv
import sys
import random

players = {}

print("Who's Playing? write (No one else) move one after players names are writen.")

player = sys.stdin.readline().strip()

while player != "No one else":
    players[player] = []
    player = sys.stdin.readline().strip()




# randomly give out cards
# MAKE OUT CARD DICTIONARY

def shuffle():
    suits = ["clubs", "spades", "hearts", "diamonds"]
    values = [str(x) for x in range(2, 11)] + ["J", "Q", "K", "A"]

    global deck
    deck = []

    for suit in suits:
        for value in values:
            deck.append(f'{value}_{suit}')
    
    #return deck

    for i in range(0, 5):
        for player in players:
            card_passed_out = random.choice(deck)
            players[player].append(card_passed_out)
            deck.remove(card_passed_out)

shuffle()

# function
def verifier(cards, the_card_placed):
    Card_list = []

    for Card in cards:
        Card = Card.split("_")
        Card_list.append(Card[0])
    
    if the_card_placed in Card_list:
        return True
    return False

def quantity_verifier(cards, the_card_placed, quantity):
    Card_list = []

    for Card in cards:
        Card = Card.split("_")
        Card_list.append(Card[0])
    
    quantity = int(quantity)

    if Card_list.count(the_card_placed) >= quantity and (quantity + tot) <= total_place:
        return True
    return False

def remove_el_and_add(cards, the_card_placed, quantity):
    aw = []
    counter = 0
# bug fixed :) problem: quantity was declered as a string and not a varible
    for x in cards:
        if counter == int(quantity):
            break
        if the_card_placed in x:
            counter += 1
            aw.append(x)
    return aw



# Now we start the game 

fields = []
type_of_cards = [str(x) for x in range(2, 11)] + ["J", "Q", "K", "A"]

terminate = False
tok = False

card_called = "Nothing"
last_placed_quantiy = 0

while terminate != True:

    # Declering cards
    for player, cards in players.items():
        
        record = []
        print(f'\nIts {player} turn. How many cards you going to place?')
        print(f'Your deck: {cards}\n')
    
        total_place = int(sys.stdin.readline().strip())

        
        
        if total_place == 0:
            if len(deck) == 0:
                while total_place == 0:
                    print("No Cards are in the deck. Place Something!")
                    total_place = int(sys.stdin.readline().strip())
            else:
                draw = random.choice(deck)
                deck.remove(draw)
                players[player].append(draw)
                tok = True


        else:
            tok = False
            while total_place >= 4:
                print("Ivalid number. Try again")
                total_place = int(sys.stdin.readline().strip())

        
        
        
        tot = 0
        while tot != total_place:
            
            print(f'\nWhich card(s) will you place? No need to list the suit only type the number of the card (e.g 10, 2 or Q).')
            print(f'Your deck: {cards}\n')
        
            the_card_placed = sys.stdin.readline().strip()
            while verifier(cards, the_card_placed) == False:
                print(f'{the_card_placed} is Invalid. Input something else shown')
                the_card_placed = sys.stdin.readline().strip()


            print(f'Quantity:')
        
            quantity = sys.stdin.readline().strip()
            while quantity_verifier(cards, the_card_placed, quantity) == False:
                print(f'{quantity} is Invalid. Input something else shown')
                quantity = sys.stdin.readline().strip()

            tot += int(quantity)

            for x in range(0, int(quantity)):
                record.append(the_card_placed)

            aw = remove_el_and_add(cards, the_card_placed, quantity)
            #print(aw)

            for x in aw:
                fields.append(x)
                players[player].remove(x)

            if tot != total_place:
                print("You still need to reach the total cards you specified")
            
            #if len(cards) == 0:
            #    print(f'{player} IS THE WINNER!!!')
            #    terminate = True
    
        
        
        if terminate == True:
            break

        

        if tok == False:
            print(f'\nOk thats done. What will you say you placed? Last placed card: {card_called} x {last_placed_quantiy}.')      # using method find what is before and after the card called. find the index in the list of the card called and then to find the rest index + 1 and -1 but if it is the last number it goes back too 1
            if card_called != "Nothing" and card_called != "A":
                print(f'Note: Place a card higher or lower then the last card placed! --> Cards you can place: {type_of_cards[(type_of_cards.index(card_called) - 1)]}, {type_of_cards[type_of_cards.index(card_called)]}, {type_of_cards[(type_of_cards.index(card_called) + 1)]}\n')
            elif card_called == "A":
                print(f'Note: Place a card higher or lower then the last card placed! --> Cards you can place: {type_of_cards[(type_of_cards.index(card_called) - 1)]}, {type_of_cards[type_of_cards.index(card_called)]}, {type_of_cards[0]}\n')
            elif card_called == "2":
                print(f'Note: Place a card higher or lower then the last card placed! --> Cards you can place: {type_of_cards[len(type_of_cards)]}, {type_of_cards[0]}, {type_of_cards[1]}\n')
            card_called = sys.stdin.readline().strip()

            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

        # Does anyone call BS?
            print(f'{player} has placed the card {card_called} x {total_place}. Anyone calling BS? (Y or N). Last placed card: {card_called} x {last_placed_quantiy}.')
            response = sys.stdin.readline().strip()
            last_placed_quantiy = total_place


        # response
            if response == "Y" or response == "y":          # using response varible to waste less memory
                print(f'Who calls BS?')

                response = sys.stdin.readline().strip()
                while response not in players.keys():
                    print(f'Invalid player. Try again')
                    response = sys.stdin.readline().strip()

                if total_place != record.count(card_called):
                    players[player].extend(fields)
                    print(f'{response} was correct!!')
            
                elif total_place == record.count(card_called):
                    players[response].extend(fields)
                    print(f'Womp Womp! {response} was not correct.')

                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\nOk next round\n")

            elif response == "N" or response == "n":
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\nOk next round\n")

        
        
        
        # case 2: places nothing

        elif tok == True:
            print(f'{player} has placed nothing so he drawed a card.')
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\nOk next round\n")

        if len(cards) == 0:
                print(f'{player} IS THE WINNER!!!')
                terminate = True
    
        if terminate == True:
            break




# bug it removes 2 jacks when i specify 1



#To Do list

# fix the programand use a key word to execute it
# use the rest of the deck too darw cards from it
# make a functiong ui soon 
