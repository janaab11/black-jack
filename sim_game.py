import basic_strategy as bs
import random

class Counter:
	def __init__(self):
		self.wins=0
		self.losses=0
		self.draws=0
		self.total=0

	def totals(self):
		self.total=self.wins+self.losses+self.draws

	def update(self,chump,house):
		if house.hand.count>21 or (chump.hand.count>house.hand.count and chump.hand.count<=21):
			self.wins+=1
			print('win')
		elif chump.hand.count>21 or (chump.hand.count<house.hand.count and house.hand.count<=21):
			self.losses+=1
			print('loss')
		else:
			self.draws+=1
			print('draw')
		print('\n')
		self.totals()

class Player:
	def __init__(self,limit=21,arr=[]):
		self.hand=bs.Hand(arr,limit)
		self.state='Hit'

	def draw_card(self,deck):
		cards=[]
		for card in deck.deck.keys():
			if deck.deck[card]>0:
				cards.append(card)
		random_card=random.choice(cards)
		self.hand.append(random_card)
		deck.remove([random_card])

def end_game(chump,house,decision):
	end=False
	if (house.hand.count >= house.hand.total and decision=='Stand') or chump.hand.count > 21:
		end=True
	return end

def game(chump,house,deck,decision=None):
	print(chump.hand.cards,house.hand.cards)
	if decision!='Stand':
		decision=bs.what_to_do(chump.hand,house.hand)
		if decision=='Do either':
			decision=random.choice(['Hit','Stand'])
		if decision=='Hit':
			chump.draw_card(deck)
	house.draw_card(deck)
	if not end_game(chump,house,decision):
		chump,house,deck, decision=game(chump,house,deck,decision)
	return chump,house,deck,decision

def main(number=1):
	alice=Counter()
	deck=bs.Deck()
	for i in range(0,number):
		chump=Player()
		chump.draw_card(deck)
		chump.draw_card(deck)
		house=Player(17)
		house.draw_card(deck)
		chump,house,deck,decision=game(chump,house,deck)
		print(chump.hand.cards, house.hand.cards)
		alice.update(chump,house)
		if deck.number<15:
			deck=bs.Deck()

	print('win percentage:',100*float(alice.wins)/float(alice.total))
	return

main(20)

print("i put on my robe and wizard hat")