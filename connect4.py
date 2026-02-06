import tkinter as tk
from tkinter import messagebox
import random

# ---------- CONSTANTS ----------
ROWS, COLS = 6, 7
CELL = 80
EMPTY, P1, P2 = 0, 1, 2
MOVE_TIME = 15

RULES_TEXT = (
    "CONNECT 4 RULES\n\n"
    "1. Two players take turns dropping discs into columns.\n"
    "2. The disc occupies the lowest empty slot.\n"
    "3. First to connect four wins.\n"
    "4. Connections may be horizontal, vertical or diagonal.\n"
    "5. A full board with no winner results in a draw.\n\n"
    "BATTLE MANIA MODE\n"
    "• Best of 3 games\n"
    "• 15 seconds per move\n"
    "• Timeout causes automatic drop"
)


class Connect4:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")
        self.root.resizable(False, False)

        self.players = ["", ""]
        self.scores = [0, 0]
        self.games_played = 0
        self.battle = False
        self.timer_id = None

        self.show_welcome()

    # ---------- UTILITY ----------
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ---------- TIMER ----------
    def stop_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    # ---------- WELCOME ----------
    def show_welcome(self):
        self.stop_timer()
        self.clear()

        frame = tk.Frame(self.root, bg="#0f172a", width=700, height=450)
        frame.pack(fill="both", expand=True)

        card = tk.Frame(frame, bg="#1e293b", bd=3, relief="ridge")
        card.place(relx=0.5, rely=0.5, anchor="center", width=560, height=360)

        tk.Label(card, text="CONNECT 4",
                 font=("Arial", 28, "bold"),
                 fg="white", bg="#1e293b").pack(pady=30)

        tk.Label(card, text="Classic Two Player Strategy Game",
                 fg="#cbd5e1", bg="#1e293b",
                 font=("Arial", 12)).pack()

        tk.Button(card, text="Start Game",
                  width=24, height=2,
                  bg="#2563eb", fg="white",
                  command=self.show_rules).pack(pady=30)

        tk.Button(card, text="Close Game",
                  width=24, height=2,
                  bg="#475569", fg="white",
                  command=self.show_exit).pack()

    # ---------- RULES ----------
    def show_rules(self):
        messagebox.showinfo("Game Rules", RULES_TEXT)
        self.show_player_setup()

    # ---------- PLAYER SETUP ----------
    def show_player_setup(self):
        self.stop_timer()
        self.clear()

        frame = tk.Frame(self.root, bg="#1e293b", width=950, height=520)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Player Setup",
                 font=("Arial", 22, "bold"),
                 fg="white", bg="#1e293b").pack(pady=20)

        form = tk.Frame(frame, bg="#1e293b")
        form.pack(pady=20)

        tk.Label(form, text="Player 1 Name:", fg="white", bg="#1e293b").grid(row=0, column=0, pady=8)
        p1_entry = tk.Entry(form, width=15)
        p1_entry.grid(row=0, column=1)

        tk.Label(form, text="Player 2 Name:", fg="white", bg="#1e293b").grid(row=1, column=0, pady=8)
        p2_entry = tk.Entry(form, width=15)
        p2_entry.grid(row=1, column=1)

        battle_var = tk.BooleanVar()
        tk.Checkbutton(frame,
                       text=" Enable Battle Mania (Best of 3, Timed)",
                       variable=battle_var,
                       bg="#1e293b", fg="white",
                       selectcolor="#334155").pack(pady=10)

        def start_game():
            p1, p2 = p1_entry.get().strip(), p2_entry.get().strip()
            if not p1 or not p2:
                messagebox.showerror("Error", "Both player names required")
                return

            self.players = [p1, p2]
            self.battle = battle_var.get()
            self.scores = [0, 0]
            self.games_played = 0
            self.start_game()

        tk.Button(frame, text="Start Game",
                  width=22, height=2,
                  bg="#2563eb", fg="white",
                  command=start_game).pack(pady=20)

        tk.Button(frame, text="Back", command=self.show_welcome).pack()

    # ---------- GAME ----------
    def start_game(self):
        self.stop_timer()
        self.clear()

        self.board = [[EMPTY] * COLS for _ in range(ROWS)]
        self.current = P1
        self.game_over = False

        top = tk.Frame(self.root)
        top.pack(pady=5)

        self.info = tk.Label(top, text=f"Turn: {self.players[0]}")
        self.info.pack(side="left", padx=10)

        tk.Button(top, text="Rules",
                  command=lambda: messagebox.showinfo("Rules", RULES_TEXT)
                  ).pack(side="right", padx=10)

        self.timer_label = tk.Label(self.root)
        self.timer_label.pack()

        drop_frame = tk.Frame(self.root)
        drop_frame.pack()

        for c in range(COLS):
            tk.Button(drop_frame, text=str(c + 1),
                      width=10, height=2,
                      command=lambda col=c: self.drop(col)
                      ).grid(row=0, column=c)

        self.canvas = tk.Canvas(self.root,
                                width=COLS * CELL,
                                height=ROWS * CELL,
                                bg="blue")
        self.canvas.pack()
        self.draw_board()

        if self.battle:
            self.start_timer()

    # ---------- TIMER ----------
    def start_timer(self):
        self.stop_timer()
        self.time_left = MOVE_TIME
        self.update_timer()

    def update_timer(self):
        if self.game_over:
            return

        self.timer_label.config(text=f"Time left: {self.time_left}s")
        if self.time_left == 0:
            self.auto_move()
            return

        self.time_left -= 1
        self.timer_id = self.root.after(1000, self.update_timer)

    # ---------- MOVES ----------
    def drop(self, col):
        if self.game_over:
            return

        self.stop_timer()

        for r in reversed(range(ROWS)):
            if self.board[r][col] == EMPTY:
                self.board[r][col] = self.current
                break
        else:
            if self.battle:
                self.start_timer()
            return

        self.draw_board()

        if self.check_win():
            self.finish_game(self.current - 1)
            return

        if self.is_draw():
            self.finish_game(None)
            return

        self.current = P2 if self.current == P1 else P1
        self.info.config(text=f"Turn: {self.players[self.current - 1]}")

        if self.battle:
            self.start_timer()

    def auto_move(self):
        choices = [c for c in range(COLS) if self.board[0][c] == EMPTY]
        if choices:
            self.drop(random.choice(choices))

    # ---------- DRAW ----------
    def draw_board(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x1, y1 = c * CELL + 5, r * CELL + 5
                x2, y2 = x1 + CELL - 10, y1 + CELL - 10
                color = "white"
                if self.board[r][c] == P1:
                    color = "red"
                elif self.board[r][c] == P2:
                    color = "yellow"
                self.canvas.create_oval(x1, y1, x2, y2, fill=color)

    # ---------- CHECKS ----------
    def check_win(self):
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] != EMPTY:
                    for dr, dc in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                        if all(
                            0 <= r + dr * i < ROWS and
                            0 <= c + dc * i < COLS and
                            self.board[r + dr * i][c + dc * i] == self.board[r][c]
                            for i in range(4)
                        ):
                            return True
        return False

    def is_draw(self):
        return all(self.board[0][c] != EMPTY for c in range(COLS))

    # ---------- FINISH ----------
    def finish_game(self, winner):
        self.stop_timer()
        self.game_over = True

        if winner is not None:
            self.scores[winner] += 1
            messagebox.showinfo("Result", f"{self.players[winner]} wins!")
        else:
            messagebox.showinfo("Result", "It's a draw!")

        self.show_welcome()

    # ---------- EXIT ----------
    def show_exit(self):
        self.root.destroy()


# ---------- RUN ----------
root = tk.Tk()
Connect4(root)
root.mainloop()
