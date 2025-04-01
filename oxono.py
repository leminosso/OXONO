import tkinter as tk
from tkinter import messagebox
import random

class OxonoGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("OXONO - Jogo")
        self.window.geometry("500x700")
        self.window.resizable(False, False)

        self.current_player = "Vermelho"
        self.players = {"Vermelho": "red", "Azul": "blue"}
        self.pieces = {"Vermelho": {"X": 8, "O": 8}, "Azul": {"X": 8, "O": 8}}

        self.game_state = 'SELECT_TOTEM'
        self.selected_totem_symbol = None
        self.selected_totem_start_pos = None
        self.moved_totem_pos = None

        self.board_buttons = []
        self.totem_positions = {}

        self.create_board()
        self.place_initial_totems()
        self.create_controls()
        self.update_status()
        self.window.mainloop()

    def create_board(self):
        self.board_frame = tk.Frame(self.window)
        self.board_frame.pack(pady=10)

        self.board_buttons = []
        for row in range(6):
            row_cells = []
            for col in range(6):
                cell = tk.Button(self.board_frame, text="", width=5, height=2,
                                   font=("Arial", 10, "bold"),
                                   command=lambda r=row, c=col: self.cell_clicked(r, c))
                cell.grid(row=row, column=col)
                row_cells.append(cell)
            self.board_buttons.append(row_cells)

    def get_cell_state(self, r, c):
        button_text = self.board_buttons[r][c]["text"]
        button_fg = self.board_buttons[r][c]["fg"]

        if not button_text:
            return None

        if button_text in ["X", "O"] and button_fg == "black":
            if (r,c) == self.totem_positions.get("X"): return ('Totem', 'X')
            if (r,c) == self.totem_positions.get("O"): return ('Totem', 'O')

        for player, color in self.players.items():
            if button_fg == color and button_text in ["X", "O"]:
                return (player, button_text)

        return None

    def update_cell_display(self, r, c, state):
        button = self.board_buttons[r][c]
        if state is None:
            button.config(text="", fg="black", bg="SystemButtonFace")
        elif state[0] == 'Totem':
            button.config(text=state[1], fg="black", bg="lightgrey")
            self.totem_positions[state[1]] = (r, c)
        elif state[0] in self.players:
            player, symbol = state
            color = self.players[player]
            button.config(text=symbol, fg=color, bg="SystemButtonFace")

    def place_initial_totems(self):
        positions = [(2, 3), (3, 2)]
        random.shuffle(positions)

        self.totem_positions = {"X": positions[0], "O": positions[1]}

        for r in range(6):
            for c in range(6):
                self.update_cell_display(r, c, None)

        self.update_cell_display(positions[0][0], positions[0][1], ('Totem', 'X'))
        self.update_cell_display(positions[1][0], positions[1][1], ('Totem', 'O'))

    def create_controls(self):
        self.controls_frame = tk.Frame(self.window)
        self.controls_frame.pack(pady=10, fill=tk.X)

        self.status_label = tk.Label(self.controls_frame, text="", font=("Arial", 12), justify=tk.CENTER)
        self.status_label.pack()

        self.pieces_label = tk.Label(self.controls_frame, text="", font=("Arial", 10), justify=tk.CENTER)
        self.pieces_label.pack(pady=5)

        totem_button_frame = tk.Frame(self.controls_frame)
        totem_button_frame.pack(pady=5)

        self.totem_buttons = {}
        for totem in ["X", "O"]:
            btn = tk.Button(totem_button_frame, text=f"Selecionar Totem {totem}",
                            command=lambda t=totem: self.select_totem(t))
            btn.pack(side=tk.LEFT, padx=10)
            self.totem_buttons[totem] = btn

        self.cancel_button = tk.Button(self.controls_frame, text="Cancelar Ação", command=self.cancel_action)
        self.cancel_button.pack(pady=5)
        self.cancel_button.config(state=tk.DISABLED)

        self.restart_button = tk.Button(self.controls_frame, text="Reiniciar Partida", command=self.restart_game)
        self.restart_button.pack(pady=5)

    def update_status(self):
        status_text = f"Turno: {self.current_player} ({self.players[self.current_player]})"
        if self.game_state == 'SELECT_TOTEM':
            status_text += " - Selecione um Totem (botões abaixo)"
        elif self.game_state == 'SELECT_MOVE_TARGET':
            status_text += f" - Mova o Totem {self.selected_totem_symbol} (clique no destino)"
        elif self.game_state == 'PLACE_PIECE':
            status_text += f" - Coloque sua peça '{self.selected_totem_symbol}' (clique adjacente ao Totem)"

        self.status_label.config(text=status_text)

        pieces_text = f"Vermelho: {self.pieces['Vermelho']['X']}X / {self.pieces['Vermelho']['O']}O    |    "
        pieces_text += f"Azul: {self.pieces['Azul']['X']}X / {self.pieces['Azul']['O']}O"
        self.pieces_label.config(text=pieces_text)

        for totem, btn in self.totem_buttons.items():
            if self.game_state == 'SELECT_TOTEM' and self.pieces[self.current_player][totem] > 0:
                btn.config(state=tk.NORMAL)
            else:
                btn.config(state=tk.DISABLED)

        if self.game_state != 'SELECT_TOTEM':
            self.cancel_button.config(state=tk.NORMAL)
        else:
            self.cancel_button.config(state=tk.DISABLED)

    def switch_player(self):
        self.current_player = "Azul" if self.current_player == "Vermelho" else "Vermelho"
        self.game_state = 'SELECT_TOTEM'
        self.selected_totem_symbol = None
        self.selected_totem_start_pos = None
        self.moved_totem_pos = None
        self.update_status()

    def cancel_action(self):
        if self.game_state == 'SELECT_MOVE_TARGET':
            self.game_state = 'SELECT_TOTEM'
            self.selected_totem_symbol = None
            self.selected_totem_start_pos = None
            messagebox.showinfo("Cancelado", "Seleção de totem cancelada.")
        elif self.game_state == 'PLACE_PIECE':
            self.update_cell_display(self.moved_totem_pos[0], self.moved_totem_pos[1], None)
            self.update_cell_display(self.selected_totem_start_pos[0], self.selected_totem_start_pos[1], ('Totem', self.selected_totem_symbol))
            self.totem_positions[self.selected_totem_symbol] = self.selected_totem_start_pos

            self.game_state = 'SELECT_TOTEM'
            self.selected_totem_symbol = None
            self.selected_totem_start_pos = None
            self.moved_totem_pos = None
            messagebox.showinfo("Cancelado", "Movimento do totem e colocação de peça cancelados.")

        self.update_status()

    def select_totem(self, totem):
        if self.game_state != 'SELECT_TOTEM':
            messagebox.showwarning("Ação Inválida", "Estado do jogo incorreto para selecionar totem.")
            return

        if self.pieces[self.current_player][totem] <= 0:
            messagebox.showwarning("Sem Peças", f"Você não tem mais peças '{totem}' para jogar.")
            return

        self.selected_totem_symbol = totem
        self.selected_totem_start_pos = self.totem_positions[totem]
        self.game_state = 'SELECT_MOVE_TARGET'
        self.update_status()

    def cell_clicked(self, row, col):
        if self.game_state == 'SELECT_MOVE_TARGET':
            self.handle_totem_move_target(row, col)
        elif self.game_state == 'PLACE_PIECE':
            self.handle_piece_placement(row, col)
        else:
            if self.game_state == 'SELECT_TOTEM':
                messagebox.showinfo("Aviso", "Selecione um Totem usando os botões abaixo primeiro.")

    def handle_totem_move_target(self, target_row, target_col):
        start_pos = self.selected_totem_start_pos
        target_pos = (target_row, target_col)

        valid, message = self.is_valid_totem_move(start_pos, target_pos)

        if valid:
            self.update_cell_display(start_pos[0], start_pos[1], None)
            self.update_cell_display(target_row, target_col, ('Totem', self.selected_totem_symbol))
            self.moved_totem_pos = target_pos

            self.game_state = 'PLACE_PIECE'
            self.update_status()
        else:
            messagebox.showwarning("Movimento Inválido", message)

    def is_valid_totem_move(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if start_pos == end_pos:
            return False, "Totem deve mover pelo menos uma casa."

        if start_row != end_row and start_col != end_col:
            return False, "Movimento do Totem deve ser estritamente horizontal ou vertical."

        end_cell_state = self.get_cell_state(end_row, end_col)
        if end_cell_state is not None:
            if end_cell_state[0] == 'Totem':
                return False, f"Casa de destino ({end_row},{end_col}) está ocupada por outro totem."

            if not self.is_totem_surrounded(start_row, start_col):
                return False, f"Casa de destino ({end_row},{end_col}) está ocupada."

        if start_row == end_row:
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if self.get_cell_state(start_row, col) is not None and (start_row,col)!= end_pos:
                    if not self.is_totem_surrounded(start_row, start_col):
                        return False, f"Caminho bloqueado pela peça em ({start_row},{col})."
        else:
            step = 1 if end_row > start_row else -1
            for row in range(start_pos[0] + step, end_pos[0], step):
                if self.get_cell_state(row, start_pos[1]) is not None and (row,start_pos[1]) != end_pos:
                    if not self.is_totem_surrounded(start_row, start_col):
                        return False, f"Caminho bloqueado pela peça em ({row},{start_pos[1]})."

        return True, "Movimento válido"

    def is_totem_surrounded(self, row, col):
        surrounded = True
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = row + dr, col + dc
            if 0 <= r < 6 and 0 <= c < 6:
                if self.get_cell_state(r, c) is None:
                    surrounded = False
                    break
        return surrounded

    def check_win(self, row, col):
        symbol = self.board_buttons[row][col]["text"]
        color = self.board_buttons[row][col]["fg"]

        if self.check_line(row, col, symbol=symbol) or self.check_color_line(row, col, color=color):
            return True
        return False

    def check_line(self, row, col, symbol=None):
        directions = [(0, 1), (1, 0)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 4):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < 6 and 0 <= c < 6:
                    cell_state = self.get_cell_state(r, c)
                    if cell_state and cell_state[0] in self.players and cell_state[1] == symbol:
                        count += 1
                    else:
                        break
            for i in range(1, 4):
                r, c = row - i * dr, col - i * dc
                if 0 <= r < 6 and 0 <= c < 6:
                    cell_state = self.get_cell_state(r, c)
                    if cell_state and cell_state[0] in self.players and cell_state[1] == symbol:
                        count += 1
                    else:
                        break
            if count >= 4:
                return True
        return False

    def check_color_line(self, row, col, color=None):
        directions = [(0, 1), (1, 0)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 4):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < 6 and 0 <= c < 6:
                    cell_state = self.get_cell_state(r, c)
                    if cell_state and cell_state[0] in self.players and self.players[cell_state[0]] == color:
                        count += 1
                    else:
                        break
            for i in range(1, 4):
                r, c = row - i * dr, col - i * dc
                if 0 <= r < 6 and 0 <= c < 6:
                    cell_state = self.get_cell_state(r, c)
                    if cell_state and cell_state[0] in self.players and self.players[cell_state[0]] == color:
                        count += 1
                    else:
                        break
            if count >= 4:
                return True
        return False
    
    def check_draw(self):
        total_pieces = sum(sum(p.values()) for p in self.pieces.values())
        placed_pieces = 0
        for row in range(6):
            for col in range(6):
                if self.get_cell_state(row, col) and self.get_cell_state(row, col)[0] in self.players:
                    placed_pieces += 1
        return placed_pieces == total_pieces

    def handle_piece_placement(self, place_row, place_col):
        totem_pos = self.moved_totem_pos
        symbol_to_place = self.selected_totem_symbol

        valid, message = self.is_valid_piece_placement(place_row, place_col, totem_pos)

        if valid:
            player_color = self.current_player
            self.update_cell_display(place_row, place_col, (player_color, symbol_to_place))

            self.pieces[player_color][symbol_to_place] -= 1

            if self.check_win(place_row, place_col):
                messagebox.showinfo("Fim de Jogo", f"Jogador {self.current_player} venceu!")
                self.game_over()
                return
            elif self.check_draw():
                messagebox.showinfo("Fim de Jogo", "Empate!")
                self.game_over()
                return

            self.switch_player()
        else:
            messagebox.showwarning("Posição Inválida", message)

    def is_valid_piece_placement(self, place_row, place_col, totem_pos):
        if not (0 <= place_row < 6 and 0 <= place_col < 6):
            return False, "Fora do tabuleiro."

        if self.get_cell_state(place_row, place_col) is not None:
            return False, "Esta casa já está ocupada."

        totem_r, totem_c = totem_pos
        is_adjacent = (abs(place_row - totem_r) == 1 and place_col == totem_c) or \
                     (abs(place_col - totem_c) == 1 and place_row == totem_r)

        if self.is_totem_surrounded(totem_r, totem_c) and self.is_totem_surrounded(self.selected_totem_start_pos[0],self.selected_totem_start_pos[1]):
            return True, "Posição válida"

        if not is_adjacent:
            return False, "A peça deve ser colocada adjacente ao totem."
        return True, "Posição válida"

    def game_over(self):
        self.game_state = 'GAME_OVER'
        for r in range(6):
            for c in range(6):
                self.board_buttons[r][c].config(state=tk.DISABLED)
        for btn in self.totem_buttons.values():
            btn.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)
        self.update_status()

    def restart_game(self):
        self.game_state = 'SELECT_TOTEM'
        self.current_player = 'Vermelho'
        self.pieces = {"Vermelho": {"X": 8, "O": 8}, "Azul": {"X": 8, "O": 8}}
        self.totem_positions = {}
        self.place_initial_totems()
        for row in self.board_buttons:
            for button in row:
                button.config(state=tk.NORMAL)
        self.update_status()

if __name__ == "__main__":
    OxonoGame()
