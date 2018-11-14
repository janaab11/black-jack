#dealer stands on hard 17

import time

class Counter:
	def __init__(self):
		self.count = 0
		self.hold=False
		self.clear_values()

	def clear_values(self):
		self.wins = 0
		self.losses = 0
		self.draws = 0

alice = Counter()

class Hand:
	def __init__(self, arr, limit=21):
		self.count = 0
		self.cards = []
		self.total = limit
		self.set_cards(arr)
		self.counts()

	def set_cards(self, arr):
		for card in arr:
			self.cards.append(card)

	def append(self,card):
		self.cards.append(card)
		self.counts()

	def counts(self):
		count = 0
		aces = 0
		for card in self.cards:
			if card == 'A':
				aces += 1
			else:
				count += card

		while count + 11 + aces - 1 <= 21 and aces > 0:
			aces -= 1
			count += 11
		count += aces
		self.count = count

class Deck:
	def __init__(self):
		self.number = 0
		self.deck = {}
		for i in range(2, 10):
			self.deck[i] = 4
		self.deck[10] = 4 * 4
		self.deck['A'] = 4
		self.cards_left()

	def cards_left(self):
		number = 0
		for card in self.deck.keys():
			number += self.deck[card]
		self.number = number

	def remove(self, arr):
		for card in arr:
			self.deck[card] -= 1
		self.cards_left()

	def copy(self, new_deck):
		for card in self.deck.keys():
			self.deck[card]=new_deck.deck[card]
		self.cards_left()

def chances(player, dealer, prob, counter=alice):
	if dealer.count > 21 or (dealer.count < player.count and player.count<=21):
		counter.wins += prob
	elif player.count > 21 or (dealer.count > player.count and dealer.count<=21):
		counter.losses += prob
	else:
		counter.draws += prob
	return

def deal_cards(player, dealer, deck, prob, hold=False):
	if hold:
		if dealer.count >= dealer.total or player.count >= 21:
			# print(new_dealer.cards, '\t', new_player.cards)
			chances(player, dealer, prob)
		else:
			new_deck = Deck()
			new_deck.copy(deck)
			new_player = Hand(player.cards)
			for d_card in new_deck.deck.keys():
				new_new_deck = Deck()
				new_new_deck.copy(new_deck)
				if new_new_deck.deck[d_card] > 0:
					if dealer.count < dealer.total:
						new_dealer = Hand(dealer.cards + [d_card],dealer.total)
						prob_1= prob*float(new_new_deck.deck[d_card]) / float(new_new_deck.number)
						new_new_deck.remove([d_card])
					else:
						new_dealer = Hand(dealer.cards,dealer.total)
						prob_1=prob

					if new_dealer.count >= dealer.total or new_player.count >= 21:
						# print(new_dealer.cards, '\t', new_player.cards)
						chances(new_player, new_dealer, prob_1)
					else:
						deal_cards(new_player, new_dealer, new_new_deck, prob_1, hold)
	else:
		deal_cards(player,dealer,deck,prob,True)
		for p_card in deck.deck.keys():
			new_deck = Deck()
			new_deck.copy(deck)
			if new_deck.deck[p_card] > 0:
				if player.count < 21:
					new_player = Hand(player.cards + [p_card])
					prob_2 = prob*float(new_deck.deck[p_card]) / float(new_deck.number)
					new_deck.remove([p_card])

					deal_cards(new_player, dealer, new_deck, prob_2, hold)
	return

def what_to_do(player, dealer):
	new_deck = Deck()
	new_deck.remove(player.cards + dealer.cards)

	alice.clear_values()
	deal_cards(player, dealer, new_deck, 1.0, True)
	stand = alice.wins-alice.losses
	# print(stand)
	new_new_deck = Deck()
	new_new_deck.copy(new_deck)
	hit = 0
	for card in new_deck.deck.keys():
		new_player = Hand(player.cards + [card])
		new_new_deck.remove([card])
		prob = float(new_deck.deck[card]) / float(new_deck.number)
		alice.clear_values()
		# print(card)
		deal_cards(new_player, dealer, new_new_deck, prob)
		hit += (alice.wins - alice.losses)
		# print((alice.wins - alice.losses))
		# time.sleep(5)

	# print(stand,hit)
	if hit > stand:
		decision='Hit'
	elif hit < stand:
		decision='Stand'
	else:
		decision='Do either'
	# print(decision)
	return decision

# main function
def main():
	player = Hand([4,4])
	dealer = Hand([7,7], 17)
	decision=what_to_do(player, dealer)
	print(decision)
	return
# main()
main()
