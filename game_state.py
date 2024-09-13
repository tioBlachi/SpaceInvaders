class GameState:
    def __init__(self):
        self.difficulty = 3

    def increase_difficulty(self):
        self.difficulty += 1

game_state = GameState()