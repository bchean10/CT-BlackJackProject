import os
import random

suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10, "A":11}
playing = True

class Card():
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def __str__(self):
        return self.number + ' of ' + self.suit

class Deck():
    def __init__(self):
        self.deck = []
        for suit in suits:
            for number in numbers:
                self.deck.append(Card(suit, number))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        first_card = self.deck.pop()
        return first_card

    def __str__(self):
        deck_combination = " "
        for card in self.deck:
            deck_combination += '\n ' + card.__str__()
        return "The deck has: " + deck_combination

class Hand():
    def __init__(self):
        self.cards = [] #this is to represent all the cards in the dealer's/player's hand
        self.value = 0
        self.aces = 0 #to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.number]
        if card.number == 'A':
            self.aces += 1

    def ace_value(self):
        while self.value > 21 and self.aces:
            self.value -= 10 
            self.aces -= 1

class Chips():
    def __init__(self):
        self.total = 1000
        self.bet = 0

    def win_bet(self):
        self.total += self.bet
        print(self.total)

    def lost_bet(self):
        self.total -= self.bet
        print(self.total)

class Functions():
    def __init__(self):
        super().__init__()
        self.chip = Chips()
        self.hand = Hand()
        self.card = Card(suits, numbers)

    def take_bet(self, chips):
        while True:
            try:
                bet = int(input("How many chips would you like to bet? "))
            except ValueError:
                print("Please enter a valid number you wish to bet: ")
            else:
                if self.chip.bet > self.chip.total:
                    print("You can't bet more than what you have ")
                else:
                    break
    
    def hit(self, deck, hand):
        hand.add_card(deck.deal())
        hand.ace_value() 

    def hit_or_stand(self, deck,hand):
        global playing
        while True:
            ask = input("Would you like to hit or stand? h/s ")
            if ask.lower() == 'h':
                print(self.hit(deck, hand))
            elif ask.lower() == 's':
                print("Player will stand. Dealer will play. ")
                playing = False
            else:
                print("Please enter 'h' or 's' to continue." )
                continue
            break

    def first_show_cards(self, player, dealer):
        print("\nDealer's Hand: ")
        print(" <card hidden> ")
        print(" ", dealer.cards[1])
        print("\nPlayer's hand: ", *player.cards)
            
    def all_show_cards(self, player, dealer):
        print("\nDealer's Hand: ", *dealer.cards)
        print("\nDealer's Hand: ", dealer.value)
        print("\nPlayer's Hand: ", *player.cards)
        print("\nPlayer's hand: ", player.value)
         
    def player_bust(self, player, dealer, chips): 
        print("Player has Bust! ")
        self.chip.lost_bet()

    def player_wins(self, player, dealer, chips): 
        print("Player has Won! ")
        self.chip.win_bet()

    def dealer_bust(self, player, dealer, chips): 
        print("Dealer has Bust! ")
        self.chip.win_bet()

    def dealer_wins(self, player, dealer, chips): 
        print("Dealer has Won! ")
        self.chip.lost_bet()

    def draw(self, player, dealer, chips):
        print("It's a Tie! Neither Player or Dealer wins! ")

class UI():
    while True:
        print("Welcome to Blackjack! ")

        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        player_chips = Chips()
        bets = Functions()
        bets.take_bet(player_chips)
        bets.first_show_cards(player_hand, dealer_hand)

        while playing:
            bets.hit_or_stand(deck, player_hand)
            bets.first_show_cards(player_hand, dealer_hand)
            if player_hand.value > 21:
                bets.player_bust(player_hand, dealer_hand, player_chips)
                break
        if player_hand.value <=21:
            while dealer_hand.value < 17:
                bets.hit(deck, dealer_hand)
            bets.all_show_cards(player_hand, dealer_hand)

            if dealer_hand.value > 21:
                bets.dealer_bust(player_hand, dealer_hand, player_chips)

            elif dealer_hand.value > player_hand.value:
                bets.dealer_wins(player_hand, dealer_hand, player_chips)
            
            elif dealer_hand.value < player_hand.value:
                bets.player_wins(player_hand, dealer_hand, player_chips)
   
            elif player_hand.value > 21:
                bets.player_bust(player_hand, dealer_hand, player_chips)
            
            elif player_hand.value == dealer_hand.value:
                bets.draw(player_hand, dealer_hand, player_chips)

        print("Player's winnings are: ", player_chips.total)

        new_game = input("Would you like to play again? y/n").lower()
        if new_game.lower() == "y":
            playing = True
            continue
        else:
            print("Thanks for playing! Bye!")
            break 

blackjack = UI()
blackjack