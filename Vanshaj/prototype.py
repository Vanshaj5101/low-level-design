import copy 

class GameCharacter:
    def __init__(self, name, health, weapons):
        self.name = name
        self.health = health
        self.weapons = weapons

    def clone(self):
        clone = copy.deepcopy(self)
        return clone
    
    def show(self):
        print(f'{self.name} has {self.health} % health left and {', '.join(self.weapons)} in the inventory')


hero = GameCharacter("Knight", 100, ["Sword", "Shield"])
clone = hero.clone()

clone.name = "Dark Knight"
clone.weapons.append("Poison Blade")

hero.show()
clone.show()