import random
import pickle


def letter_to_number(letter):
    """
    Function to convert letter coordinates to numerical indices
    """
    return ord(letter) - ord('A')


class BattleshipGame:
    """
    Represents the Battleship game and it's mechanics.
    """

    def __init__(self):
        self.board_size = 8
        self.board = [[' ' for _ in range(self.board_size)]
                      for _ in range(self.board_size)]
        self.enemy_board = [[' ' for _ in range(self.board_size)]
                            for _ in range(self.board_size)]
        self.ships = 10
        self.create_ships()
        self.player_shots_remaining = 25
        self.computer_shots_remaining = 25

    def create_ships(self):
        """
        Randomly places ships on the player's game board.
        """
        for _ in range(self.ships):
            ship_row = random.randint(0, self.board_size - 1)
            ship_col = random.randint(0, self.board_size - 1)
            while self.board[ship_row][ship_col] == 'X':
                ship_row = random.randint(0, self.board_size - 1)
                ship_col = random.randint(0, self.board_size - 1)
            self.board[ship_row][ship_col] = 'X'

    def print_board(self, board, hide_ships=False):
        """
        Print the game board.
        """
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
        """
        Print both the player's and enemy's game boards.
        """
        print("Your Board:")
        self.print_board(self.board, hide_ships=True)
        print("\nEnemy's Board:")
        self.print_board(self.enemy_board)

    def reset_boards(self):
        """
        Reset the game boards and remaining shots for a new game.
        """
        self.board = [[' ' for _ in range(self.board_size)]
                      for _ in range(self.board_size)]
        self.enemy_board = [[' ' for _ in range(self.board_size)]
                            for _ in range(self.board_size)]
        self.create_ships()
        self.player_shots_remaining = 25
        self.computer_shots_remaining = 25

    def play(self):
        while self.player_shots_remaining > 0 or \
         self.computer_shots_remaining > 0:
            self.print_boards()
            self.player_turn()
            if self.computer_shots_remaining > 0:
                self.computer_turn()

        self.print_boards()

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
        """
        Handle the player's turn to target a location on the enemy's board.
        """
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
        """
        Handle the computer's turn to randomly target a location on the board.
        """
        if self.computer_shots_remaining == 0:
            print("The enemy is out of missiles.")
            return

        computer_row = random.randint(0, self.board_size - 1)
        computer_col = random.randint(0, self.board_size - 1)

        while self.enemy_board[computer_row][computer_col] in ['X', '-']:
            computer_row = random.randint(0, self.board_size - 1)
            computer_col = random.randint(0, self.board_size - 1)

        if self.board[computer_row][computer_col] == 'X':
            print("Computer hit your ship!")
            self.board[computer_row][computer_col] = 'C'
        else:
            print("Computer missed your ships!")
            self.board[computer_row][computer_col] = '-'

        self.computer_shots_remaining -= 1

        return True

    def get_user_target(self):
        while True:
            try:
                target_row = int(input("Enter target row (1-8): ")) - 1
                if 0 <= target_row < self.board_size:
                    break
                else:
                    print("Please enter a row number between 1 and 8.")
            except ValueError:
                print("Invalid input. Please enter a valid row number.")

        while True:
            try:
                target_col_input = input("Enter target column (A-H): ").upper()
                if 'A' <= target_col_input <= 'H' == len(target_col_input):
                    target_col = letter_to_number(target_col_input)
                    break
                elif len(target_col_input) > 1:
                    print("Please enter a single column letter.")
                else:
                    print("Please enter a column letter between A and H.")
            except ValueError:
                print("Invalid input. Please enter a valid column letter.")

        if self.enemy_board[target_row][target_col] in ['X', '-']:
            print("You have already fired on that location. Choose another.")
            return self.get_user_target()  # Prompt again for a new target
        else:
            return target_row, target_col


def main():
    """
    Main function.
    Welcome messages for new and existing users
    """
    print("Welcome to Battle at Sea!")

    while True:
        new_user = input("Are you a new user? (Y/N): \n").upper()

        if new_user == 'Y':
            print("Welcome to Battle at Sea! Let's set up your game.")
            username = input("Enter your username: \n")
            password = input("Enter your password: \n")
            stored_passwords[username] = password
            with open("passwords.pkl", "wb") as f:
                pickle.dump(stored_passwords, f)

            game = BattleshipGame()
            game.reset_boards()
            game.save_state(username + '.pkl')
            game.play()
        elif new_user == 'N':
            username = input("Enter your username: \n")
            entered_password = input("Enter your password: \n")
            game_filename = username + '.pkl'

            # Check if the entered username exists in stored passwords
            if username in stored_passwords:
                stored_password = stored_passwords[username]

                # Compare the entered password with the stored password
                if entered_password == stored_password:
                    game = BattleshipGame.load_state(game_filename)
                    print("Password verified.")
                    game.play()
                else:
                    print("Invalid password.")
            else:
                print("User not found. Please sign up as a new user.")

        else:
            print("Invalid input. Please enter Y or N.")

        play_again = input("Would you like to play it again? (Y/N):\n").upper()
        if play_again != 'Y':
            print("Goodbye!")
            break


stored_passwords = {}


def check_password(username, entered_password):
    stored_passwords = {
        "user1": "password1",
        "user2": "password2"
    }
    return stored_passwords.get(username) == entered_password


if __name__ == "__main__":
    main()
