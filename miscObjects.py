class Weapon(object):
	def __init__(self, attackDamage, price, name):
		self.attackDamage = attackDamage
		self.price = price
		self.name = name

class Potion(object):
	def __init__(self, potionType, recoverAmount, price, name):
		self.potionType = potionType
		self.recoverAmount = recoverAmount
		self.price = price
		self.name = name

	def usePotion(self, player):
		if self.potionType == "Health":
			player.currentHealth += self.recoverAmount
			if player.currentHealth > player.maxHealth:
				player.currentHealth = player.maxHealth
		elif self.potionType == "Mana":
			player.currentMana += self.recoverAmount
			if player.currentMana > player.maxMana:
				player.currentMana = player.maxMana


class Ability(object):

	def __init__(self,name, damage, manaCost):
		self.name = name
		self.damage = damage
		self.manaCost = manaCost
		self.description = self.makeDescription()

	def makeDescription(self):
		if self.name == "Double Throw":
			return "1.5x weapon damage, costs %d mana" % self.manaCost
		elif self.name == "Triple Throw":
			return "2.5x weapon damage, cost %d mana" % self.manaCost
		return "Deals %d damage, costs %d mana" %(self.damage, self.manaCost)

	def useAbility(self,enemy,player):
		if self.name == "Double Throw":
			enemy.currentHealth -= 1.5*player.weapon.attackDamage
		elif self.name == "Triple Throw":
			enemy.currentHealth -= 2.5*player.weapon.attackDamage
		else:
			enemy.currentHealth -= self.damage
		player.currentMana -= self.manaCost


class PlatformType(object):

	def __init__(self,width,height,x,y):
		self.dimensions = [width,height,x,y]
		self.isShop = False
		self.isHealing = False
