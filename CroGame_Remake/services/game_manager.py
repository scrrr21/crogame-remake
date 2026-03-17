import random
import time

class GameState:
    def __init__(self, chat_id, leader_id):
        self.chat_id = chat_id
        self.leader_id = leader_id
        self.word = None
        self.start_time = time.time()
        self.finished = False


class GameManager:
    def __init__(self):
        self.games = {}  # chat_id -> GameState
        self.words = self.load_words()

    def load_words(self):
        try:
            with open("data/words.txt", encoding="utf-8") as f:
                return [w.strip() for w in f if w.strip()]
        except:
            return ["Тест", "Влаг", "Умпалумпа", "Тиффани", "Ульяга"]

    def start_game(self, chat_id, user_id):
        if chat_id in self.games:
            game = self.games[chat_id]
            if not game.finished and time.time() - game.start_time < 300:
                return None  # нельзя начать

        game = GameState(chat_id, user_id)
        self.games[chat_id] = game
        return game

    def get_game(self, chat_id):
        return self.games.get(chat_id)

    def get_word(self, chat_id):
        game = self.games.get(chat_id)
        if not game:
            return None

        game.word = random.choice(self.words)
        return game.word


game_manager = GameManager()