import random
import time


ROUND_TIME = 300  # 5 минут


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
        game = self.games.get(chat_id)

        if game and not game.finished:
            if time.time() - game.start_time < ROUND_TIME:
                return None
            else:
                self.games.pop(chat_id)

        game = GameState(chat_id, user_id)
        self.games[chat_id] = game
        return game

    def get_game(self, chat_id):
        return self.games.get(chat_id)

    def get_word(self, chat_id, new=False):
        game = self.games.get(chat_id)
        if not game:
            return None

        # если новое слово — избегаем повторения
        if new and game.word:
            words = [w for w in self.words if w != game.word]
            if words:
                game.word = random.choice(words)
            else:
                game.word = random.choice(self.words)
        else:
            game.word = random.choice(self.words)

        return game.word

    def time_left(self, chat_id):
        game = self.games.get(chat_id)
        if not game:
            return 0

        elapsed = time.time() - game.start_time
        left = ROUND_TIME - elapsed
        return max(0, int(left))


game_manager = GameManager()
