import random


"""
By Sela Roach
This program is for the card game Kalooki.
Created for python 2.7

Rules:
Kalooki is a card game with 7 rounds based on making sets.
The rounds are 33, 34, 44, 333, 334, 344, and 444.
From an original deal of 12 cards, in each round a set of 3's (a book) or a set of 4's (a run) must be created.
A run has a quantity of 4 or more cards all from the same family/suit with the value in numerical order.
For example, a run could be: 2 of clubs, 3 of clubs, 4 of clubs, 5 of clubs.
A book has a quantity of 3 or more cards that can be from the same family/suit or a different one in which the value is the same.
For example, a book could be: 2 of clubs, 2 of diamonds, 2 of spades, 2 of hearts.
Any set can have a joker as a replacement of one card not present.
There are only 4 Jokers in the deck and you cannot discard a Joker.
A Joker is worth 50 points.
An Ace of Clubs and an Ace of Spades are worth 15 points. AKA 1 of clubs, 1 of Spades
Each player is alloted 3 calls.
During each turn, the player may take a card from the pile or from the deck.
Immediately after, the player must drop any one card from their own hand or a card they just picked up from the deck.
However, you cannot discard a card you picked up from the discard pile immediately after, you have to wait until the next go around.
When a player has created all the sets, they can 'go down' by dropping the cards accordingly of the round.
A round is over once a player has no cards left, and therefore 'bends' the other players.
Overall, the goal of the game is to have the least amount of points by the final round 444.
The player with the least amount of points by 444 is the winner.
"""

#constants
suits = ["Hearts", "Spades", "Diamonds", "Clubs"]
special = ["Joker"]
rank_value = {'Special Joker':50, '1 of Clubs':15, '1 of Spades':15}


class Card:
    #This class is the blueprint for a single card

    def __init__(self, suit, value):
        """
        Class constructor.

        Args:
                suit: A string value from the suits list.
                value: An integer representing the card rank.

        Return:
                No return value
        """
        self.suit = suit
        self.value = value

    def view_card(self):
        """
        This method shows the card instance as an overall string.

		Args:
			no args.
		Returns:
			string representation of the Card. For example: 2 of Clubs, or if it is a joker: Special Joker.
		"""
        if self.suit in suits:
            print "{} of {}".format(self.value, self.suit)
        else:
            print "{} {}".format(self.suit, self.value)

    def is_joker(self):

        """Check to see if the Card is a Joker

		Args:
			no arguments
		Returns:
			Boolean
		"""
        if self.value in special:
            return True
        else:
            return False

    def is_worth15(self):

        """Check to see if the Card is a 1 of Clubs or 1 of Spades.

		Args:
			no arguments
		Returns:
			Boolean
		"""
        if self.value == '1' and (self.suit == 'Clubs' or self.suit == 'Spades'):
            return True
        else:
            return False

class Deck:
    #This class is the blueprint for the deck

    def __init__(self, packs):
        """
        Class constructor.

        Args:
                packs: An integer representing the number of packs used to create official deck.

        Return:
                No return value
        """
        self.packs = packs
        self.cards = [] #the deck
        self.table = [] #where the discards are placed and the first flip card are placed
        self.build_deck()

    def build_deck(self):
        """
        This method builds the deck based on the number of packs.

		Args:
			no args.
		Returns:
			The deck, which is a list, with all the cards including the Joker's.
		"""
        for i in range(self.packs):
            for s in suits:
                for r in range(1,13):
                    self.cards.append(Card(s,r))
            for i in range(2):
                self.cards.append(Card('Special', 'Joker'))

    def view_card(self):
        """
        This method shows all the cards in the deck.

		Args:
			no args.
		Returns:
			All the cards from the deck as a string representation.
		"""
        for c in self.cards:
            c.view_card()

    def shuffle(self):
        """ Shuffles the Deck so that the cards are ordered randomly.
		Args:
			No args
		Returns:
			A shuffled deck of cards.
		"""

        for i in range(len(self.cards)-1,0,-1):
            r = random.randint(0, i) #create a random number from (0 to range i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def is_empty(self):
        """ Checks to see if the deck is empty.
		Args:
			No args
		Returns:
			A boolean.
		"""
        return len(self.cards) == 0

    def remake_deck(self, table_deck):
        """ Remakes a new deck by flipping the table deck of discards.
		Args:
			No args
		Returns:
			No return value.
		"""
        self.cards = self.table.reverse()
        print('New deck has been set')

    def draw_card(self):
        """ Remakes a new deck by flipping the table deck of discards.
		Args:
			No args
		Returns:
			No return value.
		"""
        if self.is_empty():
            remake_deck()
        else:
            return self.cards.pop()

    def flip_card(self):
        """ Flips first card over.
		Args:
			No args
		Returns:
			No return value.
		"""
        card_flipped = self.cards.pop()
        print("The card flipped is {}").format(card_flipped)
        return self.table.append(card_flipped)


class Player:
    #This class is the blueprint for each player
    def __init__(self, name, deck, game):
        """
        Class constructor.

        Args:
                name: A string which is the name of the player.
                deck: Reference to the current Deck Object of the Game.
                game: Reference to the current game Object.

        Return:
                No return value
        """
        self.name = name
        self.deck = deck
        self.game = game

        #----- Kalooki Technicalities -----
        #Kalooki Hand
        self.hand = [] #The players hand
        self.made_hand = [] # The player's go down hand
        self.run_count = 0
        self.book_count = 0

        #Kalooki Score
        self.score = 0 #Each player starts with a score of zero
        self.hand_count = 0 #Player's score for the curent round

        #Kalooki Calls
        self.calls = 3 # The number of calls each player has
        self.call_round = False # The decision to call
        self.check_calls = False


    def get_score_incremented(self, card_selected):
        """ Updates score to be increased.
		Args:
			card_selected: A card instance
		Returns:
			No return value.
		"""
        if card_selected.is_joker():
            self.hand_count += 50
        elif card_selected.is_worth15():
            self.hand_count += 15
        else:
            self.hand_count += card_selected.value

    def get_score_decremented(self, card_selected):
        """ Updates score to be decreased.
		Args:
			card_selected: A card instance
		Returns:
			No return value.
		"""
        if card_selected.is_joker():
            self.hand_count -= 50
        elif card_selected.is_worth15():
            self.hand_count -= 15
        else:
            self.hand_count -= card_selected.value


    def deal_card(self):
        """ Deals an individual card to player's hand with updated hand count.
		Args:
			No args.
		Returns:
			No return value.
		"""
        deckcard = self.deck.draw_card()
        self.get_score_incremented(deckcard)
        self.hand.append(deckcard)

    def deal_hand(self):
        """ Deals the player's hand.
		Args:
			No args.
		Returns:
			No return value.
		"""
        for i in range(12):
            self.deal_card()

    def pickup_card(self):
        """ Adds pick up card from table to player's hand.
		Args:
			No args.
		Returns:
			No return value.
		"""
        pickupcard = self.deck.table.pop()
        self.get_score_incremented(pickupcard)
        return self.hand.append(pickupcard)

    def throw_out(self, card_index):
        """ Removes card from player's hand to table.
		Args:
			card_index: An integer representing the location of card in hand from 1 - 13.
		Returns:
			No return value.
		"""
        if card_index < 1 or card_index > 13:
            print('That is not a valid card index. Remeber the cards are ordered 1 - 13, the top representing 1 and the bottom 13.')
        throwout = self.hand.pop(card_index)
        self.get_score_decremented(throwout)
        self.deck.table.append(throwout)

    def tack(self, card_index, group):
        """ Removes card from player's hand to table.
        Args:
            card_index: An integer representing the location of card in hand from 1 - 13.
            group: A list representing the sets the player wants to tack to.
        Returns:
            No return value.
        """
        thecard = self.hand.pop(card_index)
        self.get_score_decremented(thecard)
        group.append(thecard)

    def call_action(self, player_who_called):
        """ Adds the card the player called to hand as well as penalty card from deck.
        Args:
            player_who_called: The player who wants the card on table.
        Returns:
            No return value.
        """
        if player_who_called.calls > 0:
            player_who_called.calls -= 1
            player_who_called.pickup_card()
            player_who_called.deal_card()
            print('Player {} calls! They have {} call(s) left and have picked up from the table and deck! Back to the current player!'.format(player_who_called.name, player_who_called.calls))
            print('********************************************')
        else:
            print('********* Sorry, Player {} is out of calls.'.format(player_who_called.name))

    def hand_empty(self):
        """ Checks to see if the player has an empty hand which would signify a successful bend.
        Args:
            No args.
        Returns:
            Boolean.
        """
        return len(self.hand) == 0

    def any_calling(self, current_player_index):
        """ Checks to see if any of the players want to call.
        Args:
            current_player_index: Integer representing the current player
        Returns:
            No return value.
        """
        the_current_player = self.game.players[current_player_index]
        other_player_index = current_player_index

        #goes through all the other players and see if they want to call
        while the_current_player.call_round == False:
            print(chr(27)+"[2J") #clears screen
            other_player_index += 1 #go to the next player
            if other_player_index == len(self.game.players): #resets the cycle to make sure index doesn't go out of range
                other_player_index = 0

            if self.game.players[other_player_index] == the_current_player: #This means that no one wanted to call as the index is back to the current player
                the_current_player.call_round = True
                print(chr(27)+"[2J")
                print("*** No one called! ***")
                break

            #check if the other player wants to call
            next_player = self.game.players[other_player_index]
            if len(next_player.hand) < 12:
                print('You cannot call! You already went down.')
            else:
                print("*********  Hello {}! The top card is: ").format(next_player.name)
                show_lastcard(self.deck.table)
                print("********* Below is your hand: ********* ")
                show_hand(next_player.hand)
                decision = raw_input('*********  Would You like to call the top card on the pile? Enter (Y) for yes and (N) for no:  ')
                if decision == 'Y':
                    self.call_action(next_player)
                    print(chr(27)+"[2J")
                    print("*** {} called! .......").format(next_player.name)
                    the_current_player.call_round = True
                    break

    def show_sets(self):
        """ Displays the hands of players that went down.
		Args:
			No args
		Returns:
			No return value.
		"""
        print('***** Below is the sets that have gone down! *****')
        for sets in self.made_hand:
            show_table(sets)

    def show_all_sets(self):
        """ Displays the hands of players that went down.
		Args:
			No args
		Returns:
			No return value.
		"""
        print('***** Updated! Below are the sets that have gone down! *****')
        for sets in self.game.all_players_hand:
            for c in sets:
                show_table(c)


    def go_down(self):
        """ Allows player to go down by making their sets and adding those sets to the overall go down pile.
        Args:
            No args:
        Returns:
            No return value.
        """
        final_set = [] #Overall set for round to be added to game all_players_hand
        set1 = [] #The individual set for each book or run

        #Checks
        hand_is_made = False
        is_3_made = False
        is_4_made = False

        while hand_is_made != True:
            print("******** Always add the 3 first to avoid going down with the wrong hand for the round! ******** ")
            self.game.report_round(self.game.round) #reports the current round


            decision1 = raw_input("********* Would you like to add a 3? If so, enter (Y) for yes! else press return.     ")
            if decision1 == 'Y':
                while is_3_made == False:
                    show_hand(self.hand)
                    card1_index = int(raw_input("********* Enter the card number from 1 - 13, the top card is 1 and the bottom is 13 that you would like to add to your 3. ")) - 1
                    self.tack(card1_index, set1)
                    print('********* {}, below is your modified hand! *********').format(self.name)
                    show_hand(self.hand)

                    do_continue = raw_input("********* Do you have another card to add, if so enter (Y) for yes! Else press return:   ")
                    if do_continue != "Y":
                        print(show_hand(set1))
                        print(check_book(set1))
                        if check_book(set1) and len(set1) > 2:
                            final_set.append(set1)
                            set1 = []
                            is_3_made == True
                            self.book_count += 1
                            break
                        else:
                            print("Incorrect 3, all cards will be added back into you hand!")
                            for c in set1:
                                self.hand.append(c)
                                self.get_score_incremented(c)
                                return


            decision2 = raw_input("********* Would you like to add a 4? If so, enter (Y) for yes! else press return.   ")
            if decision2 == 'Y':
                    while is_4_made == False:
                        show_hand(self.hand)
                        card1_index = int(raw_input("********* Enter the card number from 1 - 13, the top card is 1 and the bottom is 13 that you would like to add to your 4. ")) - 1
                        self.tack(card1_index, set1)
                        print('***** {}, below is your modified hand! *****').format(self.name)
                        show_hand(self.hand)

                        do_continue = raw_input("********* Do you have another card to add, enter (Y) for yes! Else press return.   ")
                        if do_continue != "Y":
                            print(show_hand(set1))
                            print(check_run(set1))
                            if check_run(set1) and len(set1) > 3:
                                is_4_made == True
                                self.run_count += 1
                                final_set.append(set1)
                                set1 = []
                                break
                            else:
                                print("Incorrect 4, all cards will be added back into you hand!")
                                for c in set1:
                                    self.hand.append(c)
                                    self.get_score_incremented(c)
                                    return



            decision3 = raw_input("********* Is your hand, ready to go down! Enter (Y) for yes! Else press return.   ")
            if decision3 == 'Y':
                self.made_hand = final_set
                print("DEBUG:current round:", self.game.round)
                print("DEBUG:book count:", self.book_count)
                print("DEBUG:runcount:", self.run_count)
                print("DEBUG:boolean:", check_hand(self.game.round, self.book_count, self.run_count))
                if check_hand(self.game.round, self.book_count, self.run_count):
                    self.game.all_players_hand.append(self.made_hand)
                    hand_is_made = True
                    print('***** {}, below is the hand you went down with! *****').format(self.name)
                    self.show_sets()
                    print('***** {}, below is your modified hand! *****').format(self.name)
                    show_hand(self.hand)
                    self.made_hand = []
                    self.book_count = 0
                    self.run_count = 0
                else:
                    print("Try again, all cards will be added back to your hand!")
                    for sets in self.made_hand:
                        for c in sets:
                            self.hand.append(c)
                            self.get_score_incremented(c)
                    self.made_hand = []
                    self.run_count = 0
                    self.book_count = 0



    def play(self):
        """ Play a single turn by the Player
		Args:
			No args
		Returns:
			Boolean
		"""
		# Loop ends when Player discards.
        while True:
            print(chr(27)+"[2J")
            print('***** {}, below is your hand! *****').format(self.name)
            show_hand(self.hand)
            print('***** {}, below is the top card on the table! *****')
            show_table(self.deck.table)
            prev_action = None

            while prev_action != 'D' or prev_action != 'd':
                action = raw_input("*** " + self.name + ", What would you like to do? ***, \n(S)wap Cards in your hand, (P)ick up from table,(T)ake from deck, (D)iscard, (G)o Down, (K)Tack, (O)Sort, (R)ules: ")
                if action == 'S' or action == 's':
                    swap_index1 = raw_input("Enter the first card you want to do the swap with. \nEnter card number from 1 - 12, the top card is 1 and the bottom is 12. ")
                    swap_index1 = int(swap_index1.strip().upper())
                    if swap_index1 < 1 or (swap_index1 > 13 and self.calls == 3):
                        print('That card is not in your hand. Please enter a card that is in your hand.')
                        continue

                    # #Get the postition where the card needs to be moved.
                    swap_index2 =  raw_input("Enter which card you would like to complete the swap with.\nEnter card number from 1 - 12, the top card is 1 and the bottom is 12." )
                    swap_index2 = int(swap_index2.strip().upper())
                    if swap_index2 < 1 or (swap_index2 > 13 and self.calls == 3):
                        raw_input('That card is not in your hand. Please enter a card that is in your hand.')
                        continue
                    self.hand[swap_index1 - 1], self.hand[swap_index2 - 1] = self.hand[swap_index2 - 1], self.hand[swap_index1 - 1]
                    print('***** {}, below is your modified hand! *****').format(self.name)
                    show_hand(self.hand)


                # Pick card from table Pile
                elif action == 'P' or action == 'p':
                    no_actions = ['T', 't', 'P', 'p']
                    show_table(self.deck.table)
                    if prev_action in no_actions:
                        print('Sorry, you either already picked up or took a card from deck!')
                        print('You can discard!')
                    elif len(self.hand) < 12:
                        print('Sorry, you went down, so you cannot pick up from table pile! Pick up from deck.')
                    else:
                        print(chr(27)+"[2J")
                        print('{} picked up.').format(self.name)
                        self.pickup_card()
                        print('***** {}, below is your modified hand! *****').format(self.name)
                        show_hand(self.hand)
                        prev_action = 'P'
                        print('Now you can discard a card, enter (D) to discard or maybe go down!')

                # Take card from Deck
                elif action == 'T' or action == 't':
                    no_actions = ['T', 't', 'P', 'p']
                    if prev_action in no_actions:
                        print('Sorry, you cannot not take card from deck, you already picked up from table!')
                        print('You can discard, enter (D) to discard!')
                    else:
                        self.any_calling(self.game.current_player)
                        self.deal_card()
                        print('You drew a card!')
                        prev_action = 'T'
                        print('***** {}, below is your modified hand! *****').format(self.name)
                        show_hand(self.hand)
                        print('Now you can discard a card, enter (D) to discard.')


                # Discard card, placing card on table pile
                elif action == 'D' or action == 'd':
                    no_actions = ['D', 'd']
                    must_actions = ['T', 't', 'p', 'P', 'g', 'G']
                    if prev_action in no_actions:
                        print('Sorry, you already discarded!')
                    elif prev_action not in must_actions:
                        print('Sorry, you did not pickup! Enter (P) to pick up from pile or (T) to take from deck.')
                    else:
                        discard_index = raw_input("Which card would you like to discard? \nEnter card number from 1 - 13, the top card is 1 and the bottom is 13. ")
                        discard_index = int(discard_index.strip().upper()) - 1
                        self.throw_out(discard_index)
                        prev_action = 'D'
                        print('***** {}, below is your modified hand! *****').format(self.name)
                        show_hand(self.hand)
                        return False


                # Show rules to player
                elif action == 'R' or action == 'r':
                    print("------------------ Kalooki Rules ------------------- \nKalooki is a card game based on making sets.\n - From an original deal of 12 cards,depending on each round, sets must be created of 3's and 4's. \n- A set of 4 has a quantity of 4 or more cards all from the same family/suit with the value in numerical order.\n- For example, a set could be [2 of clubs, 3 of clubs, 4 of clubs, 5 of clubs].\n- A set of 3 has a quantity of 3 or more cards that can be from the same family/suit or a different one in which the value is the same.\n- A set can be run with a joker as a replacement of one card not present.\n- A run is a sequence of numbers in a row, all with the same suit. \n \tFor example: 4 of Hearts, 5 of Hearts, and 6 of Hearts\n- A book of cards must have the same rank but may have different suits.\n \tFor example: 3 of Diamonds, 3 of Spades, 3 of Clubs.\n- There are only 4 Jokers in the deck\n- You cannot discard a Joker\n- A Joker is worth 50 points\n- Each player is alloted 3 calls, if a player has more than 18 cards after discarding, they cannot go down, only discard.\n- During each turn, the player may take a card from the pile or from the deck.Immediately after, the player must drop any one card from their own hand or a card they just picked up from the deck.\n- However, you cannot discard a card you picked up from the discard pile immediately after, you have to wait until the next go around.\n- When a player has created all the sets, select Go Down option and drop the cards accordingly of the round.\n- Ace/(1) of Clubs and Ace/(1) of Spades are worth 15 points\n- The goal of the game is to have the least amount of points by the final round 444. \n -------------------------------------------- ")

                    raw_input("Enter to continue ....")

                elif action == 'O' or action == 'o':
                    print(chr(27)+"[2J")
                    print('***** {}, below is the top card on the table! *****').format(self.name)
                    show_lastcard(self.deck.table)
                    self.hand = sort_group(self.hand)
                    print('***** {}, below is your modified hand! *****').format(self.name)
                    show_hand(self.hand)

                elif action == 'G' or action == 'g':
                    no_actions = ['G', 'g']
                    must_actions = ['T', 't', 'p', 'P']
                    if prev_action in no_actions:
                        print('Sorry, you already went down. Maybe you want to tack or discard!')
                    elif prev_action not in must_actions:
                        print('Sorry, you did not pickup! Enter (P) to pick up from pile or (T) to take from deck.')

                    else:
                        main_decision = raw_input("You have decided to go down! If you are are actually not ready to do so, press (N) for no! else press whatever to continue")
                        if main_decision != 'N':
                            self.go_down()
                            print('You can now discard a card, enter (D) to do so!')
                            print('Or you can now tack, enter (K) to do so!')

                elif action == 'K' or action == 'k':
                    self.show_all_sets()
                    tack_decision = raw_input("Do you want to tack?")
                    if tack_decision == 'Y':
                        if len(self.game.all_players_hand) == 0:
                            print("No players have gone down. Not even yourself. You can't tack.")
                        else:
                            set_selection = int(raw_input("If so enter card set number, the first set represents 1, else press return. ")) - 1
                            thecards = self.game.all_players_hand[set_selection]
                            for c in thecards:
                                show_hand(c)
                            decision = raw_input('If this the the set you want to tack on? Enter (Y) for yes, else press return.')
                            if decision == 'Y':
                                set_decision = int(raw_input('Enter the set number within that you want to tack on. Top set is 1.')) - 1
                                card_selection = int(raw_input("Select the card in your hand you want to tack. \nEnter card number you would like to tack. The top card is 1. ")) - 1
                                self.tack(card_selection, thecards[set_decision])
                                print("You have tacked successfully!")
                                self.show_all_sets()
                                print('***** {}, below is your modified hand! *****').format(self.name)
                                show_hand(self.hand)





class Game:
    #This class is the blueprint for each player

    def __init__(self, num_of_players, deck):
        """
        Class constructor.

        Args:
                num_of_players: An integer representing the number of players.
                deck: Reference to the current Deck Object of the Game.

        Return:
                No return value
        """
        #all the players
        self.players = []
        #starting round
        self.round = 1
        self.current_player = 0
        self.all_players_hand = []
        #Getting players names
        for i in range(num_of_players):
            name1 = raw_input("Enter name of Player " + str(i) + ": ")
            player_obj = Player(name1, deck, self)
            self.players.append(player_obj)

    def display_scores(self):
        """ Displays score of each player.
        Args:
            No args:
        Returns:
            No return value.
        """
        for i in range(num_of_players):
            print('{}\'s score: {}'.format(self.players[i].name, self.players[i].score))



    def report_round(self, current_round):
        """ Displays the current round.
        Args:
            current_round: An integer representing which round it is.
        Returns:
            No return value.
        """
        if current_round == 1:
            print('The round is 33')
        elif current_round == 2:
            print('The round is 34')
        elif current_round == 3:
            print('The round is 333')
        elif current_round == 4:
            print('The round is 334')
        elif current_round == 5:
            print('The round is 344')
        elif current_round == 6:
            print('The round is 444')
        else:
            print('GAME OVER')

    def game_over(self):
        """ Returns the winner - the player who has the least amount of points.
        Args:
            No args:
        Returns:
            The winner of the game.
        """
        if self.players[0].score < self.players[1].score and self.players[0].score < self.players[2].score:
            winner = self.players[0].name
            winner_score = self.players[0].score
        elif self.players[1].score < self.players[0].score and self.players[1].score < self.players[2].score:
            winner = self.players[1].name
            winner_score = self.players[1].score
        else:
            winner = self.players[2].name
            winner_score = self.players[2].score
        return ('The winner is {} with a score of {}!'.format(winner, winner_score))

    def round_over(self):
        """ Checks to see if round is over.
        Args:
            No args:
        Returns:
            No return value.
        """
        for player_hand in self.players:
            if len(player_hand.hand) == 0:
                print("Round {} Over!").format(self.round)
                self.round += 1
                print("***** This round scores are ... ")
                self.display_scores()
                if self.round == 7:
                    print('GAME OVER')
                    self.game_over()

    def play(self):
        """ Play the game.
		Args:
			No args
		Returns:
			No return value.
		"""
        i = 0
        while self.players[i].play() == False:
            self.round_over()
            print(chr(27)+"[2J")
            i += 1
            self.current_player += 1
            if i == len(self.players):
                i = 0
            if self.current_player == len(self.players):
                self.current_player = 0
            print("***", self.players[i].name, "to play now.")
            raw_input(self.players[i].name + " hit return to continue...")



#global functions

def sort_group(group):
    """ Orders card values numerically.
    Args:
        group: A list of cards.
    Returns:
        The group with cards values ordered.
    """
    is_sort_complete = False
    while is_sort_complete == False:
        is_sort_complete = True
        length = len(group) - 1
        for i in range(0, length):
            if group[i].value > group[i + 1].value:
                group[i], group[i + 1] = group[i + 1], group[i]
                is_sort_complete = False
    return group


def check_book(group):
    """ Check to see if card group is a valid book.
    Args:
        group: A list of cards.
    Returns:
        Boolean.
    """
    for card in group:
        if card.suit == 'Special':
            continue
        elif card.value != group[0].value:
            return False
    return True

def check_run(group):
    """ Check to see if card group is a valid run.
    Args:
        group: A list of cards.
    Returns:
        Boolean.
    """
    group = sort_group(group)
    for card in group:
        if card.suit == 'Special':
            continue
        elif card.suit != group[0].suit:
            return False
        else:
            for i in range(1,len(group)):
                if group[i].suit == 'Special':
                    continue
                if group[i].value != group[i-1].value +1:
                    return False
    return True

def check_hand(round, book_tally, run_tally):
    """ Check to see if card sets fit the round requirements.
    Args:
        book_tally: An integer representing the number of book sets added to go down hand.
        run_tally: An integer representing the number of run sets added to go down hand.
    Returns:
        Boolean.
    """
    if round == 1 and book_tally == 2:
        return True
    elif round == 2 and book_tally == 1 and run_tally == 1:
        return True
    elif round == 3 and run_tally == 2 and book_tally == 0:
        return True
    elif round == 4 and book_tally == 3 and run_tally == 0:
        return True
    elif round == 5 and book_tally == 2 and run_tally == 1:
        return True
    elif round == 6 and book_tally == 1 and run_tally == 2:
        return True
    elif round == 7 and run_tally == 3 and book_tally == 0:
        return True
    else:
        return False


#showing cards/hands
def show_hand(sequence):
    """ Displays cards that are within a list.
    Args:
        sequence: A list of cards within a list.
    Returns:
        No return value.
    """
    for c in sequence:
        c.view_card()


def show_table(sequence):
    """ Displays cards that are on the table pile.
    Args:
        sequence: A list of cards that are on table.
    Returns:
        No return value.
    """
    if len(sequence) == 0:  #***add this elsewhere outside function
        print('At the moment, there are no cards in the table pile')
    for card in sequence:
        card.view_card()


def show_lastcard(sequence):
    """ Displays last card.
    Args:
        sequence: A list of cards that are on table.
    Returns:
        No return value.
    """
    lastone = sequence[-1]
    lastone.view_card()


def main():
    """ Main Program """
    deck = Deck(2) #create a deck with two packs
    deck.shuffle() #shuffles deck
    g = Game(3, deck)
    #create a new game with  3 players
    for thehand in g.players:
        thehand.deal_hand()
    deck.flip_card()
    g.play()

if __name__ == "__main__":
    main()
