import random
import pickle


def letter_to_number(letter):
    return ord(letter) - ord('A')


class BattleshipGame:

    def __init__(self):
        self.board_size = 8
        self.board = [[' ' for _ in range(self.board_size)]
                      for _ in range(self.board_size)]
        self.enemy_board = [[' ' for _ in range(self.board_size)]
                            for _ in range(self.board_size)]
        self.ships = 30
        self.create_ships()
        self.player_shots_remaining = 5
        self.computer_shots_remaining = 5

    def create_ships(self):
        for _ in range(self.ships):
            ship_row = random.randint(0, self.board_size - 1)
            ship_col = random.randint(0, self.board_size - 1)
            while self.board[ship_row][ship_col] == 'X':
                ship_row = random.randint(0, self.board_size - 1)
                ship_col = random.randint(0, self.board_size - 1)
            self.board[ship_row][ship_col] = 'X'

    def print_board(self, board, hide_ships=False):
        print('  A B C D E F G H')
        print('  ***************')
        row_num = 1
        for row in board:
            cells = [' 'if hide_ships and cell == 'X'else cell for cell in row]
            formatted_row = f"{row_num}|{'|'.join(cells)}|"
            print(formatted_row)
            row_num += 1

    def save_state(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_state(cls, filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)

    def print_boards(self):
        print("Your Board:")
        self.print_board(self.board, hide_ships=True)
        print("\nEnemy's Board:")
        self.print_board(self.enemy_board)

    def reset_boards(self):
        self.board = [[' ' for _ in range(self.board_size)]
                      for _ in range(self.board_size)]
        self.enemy_board = [[' ' for _ in range(self.board_size)]
                            for _ in range(self.board_size)]
        self.create_ships()
        self.player_shots_remaining = 5
        self.computer_shots_remaining = 5

    def play(self):
        while self.player_shots_remaining > 0 or \
         self.computer_shots_remaining > 0:
            self.print_boards()
            self.player_turn()
            if self.computer_shots_remaining > 0:
                self.computer_turn()

        self.print_boards()  # Print the final boards

        player_hits = sum(row.count('X') for row in self.enemy_board)
        computer_hits = sum(row.count('C') for row in self.board)

        print("Game over.")
        if player_hits > computer_hits:
            print("Congratulations! You win with more hits!")
        elif computer_hits > player_hits:
            print("Computer wins with more hits!")
        else:
            print("It's a draw! Both sides have the same number of hits.")

    def player_turn(self):
        if self.player_shots_remaining == 0:
            print("You are out of missiles.")
            return

        target_row, target_col = self.get_user_target()

        if self.enemy_board[target_row][target_col] == 'X':
            print("You've already hit that location.")
            return
        elif self.enemy_board[target_row][target_col] == '-':
            print("You've already missed that location.")
            return
        elif self.board[target_row][target_col] == 'X':
            print("Hit! You sunk an enemy ship!")
            self.enemy_board[target_row][target_col] = 'X'
            self.player_shots_remaining -= 1
            print(f"You have {self.player_shots_remaining} missiles left.")
        else:
            print("Miss. No enemy ship at that location.")
            self.enemy_board[target_row][target_col] = '-'
            self.player_shots_remaining -= 1
            print(f"You have {self.player_shots_remaining} missiles left.")

    def computer_turn(self):
        if self.computer_shots_remaining == 0:
            print("The enemy is out of missiles.")
            return

def main():
    print("Welcome to Battle at Sea!")

    while True:
        new_user = input("Are you a new user? (Y/N): ").upper()

        if new_user == 'Y':
            print("Welcome to Battleship! Let's set up your game.")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            game = BattleshipGame()
            game.reset_boards()  # Resetting the boards here
            game.save_state(username + '.pkl')
            game.play()
        elif new_user == 'N':
            print("Welcome back! Let's continue your existing game.")
            username = input("Enter your username: ")
            entered_password = input("Enter your password: ")
            game_filename = username + '.pkl'
            if check_password(username, entered_password):
                game = BattleshipGame.load_state(game_filename)
                game.print_boards()
                game.play()
            else:
                print("Invalid password.You can't continue the existing game.")
        else:
            print("Invalid input. Please enter Y or N.")

        play_again = input("Would you like to play it again? (Y/N): ").upper()
        if play_again != 'Y':
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
