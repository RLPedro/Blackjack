#!/usr/bin/env python
# coding: utf-8

# BLACK JACK game
# 
# Player vs Computer
# 
# 
# - Dealer hits until she reaches 17
# - Aces count as 1 or 11
# - Player starts with 100 chips

# In[1]:


#creating the data structures for suits, ranks and values.
#setting a global boolean variable of playing equal to true

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True


# In[2]:


#creating a card class

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __str__(self):
        return self.rank + " of " + self.suit


# In[3]:


#creating a deck class

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.deck.append(created_card)
    
    def __str__(self):
        deck_content = ''
        for card in self.deck:
            deck_content += '\n '+card.__str__()
        return 'The deck has:\n' + deck_content

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        new_card = self.deck.pop()
        return new_card


# In[4]:


#creating a hand class

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0   
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# In[5]:


#creating a chips class

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


# In[6]:


#function to take a bet

def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, must insert a number!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
            else:
                break


# In[7]:


#hit function

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


# In[8]:


#function to prompt the player to hit or stand

def hit_or_stand(deck,hand):
    global playing
    
    while True:
    
        hit_or_stand = input('Want to hit or stand? Enter H or S. ')

        if hit_or_stand[0].lower() == 'h':
            hit(deck,hand)
            
        elif hit_or_stand[0].lower() == 's':
            print('Player stands. ')
            playing = False
            
        else:
            print('Sorry, invalid reply. Try again. ')
            continue
        break


# In[9]:


#functions to show cards

def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)


# In[10]:


#functions to handle the different scenarios

def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print("Dealer and Player tie! It's a push.")


# In[ ]:


#game flow

while True:
    
    print('Welcome to my Black Jack game!\n    Get as close to 21 as you can without going over! Dealer hits until she reaches 17.\n    Aces count as 1 or 11.\n    Player starts with 100 chips.')
    
    # Shuffling the deck, dealing two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    
        
    # Seting up the player's chips and prompting the bet
    player_chips = Chips()
    take_bet(player_chips)
    
    
    # Showing cards (keeping one of the dealer's cards hidden)
    show_some(player_hand,dealer_hand)
    
    
    while playing:  # variable from our hit_or_stand function
        
        # Prompt the player to hit or stand, showing cards (one dealer card hidden)
        hit_or_stand(deck,player_hand)
        show_some(player_hand,dealer_hand)
 
        
        # if player bursts
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break        


    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)    
    
        # Showing all cards
        show_all(player_hand,dealer_hand)
    
        # Running the winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand)  
            
            
        # Printing total of chips
        print('Your total of chips is ', player_chips.total)
    
    # Asking to play again

    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    
    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break

