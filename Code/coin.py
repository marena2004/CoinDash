class Coin:
    def __init__(self, position, value=10):
        self.position = list(position)
        self.value = value
        self.radius = 10

    def collect(self, player):
        if player.rect().collidepoint(self.position):
            player.collect_coin(self)
            return True
        return False
