from math import inf
import tkinter as tk
from tkinter import font as tkfont

def checkWinner(board, player):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    return any(board[a] == board[b] == board[c] == player for a, b, c in wins)

def miniMax(board, mimax):
    if checkWinner(board, 'X'): return 1
    if checkWinner(board, 'O'): return -1
    if ' ' not in board: return 0
    best = -inf if mimax else inf
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X' if mimax else 'O'
            score = miniMax(board, not mimax)
            board[i] = ' '
            best = max(best, score) if mimax else min(best, score)
    return best

def miniMax_move(board):
    best, move = -inf, None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            score = miniMax(board, False)
            board[i] = ' '
            if score > best:
                best, move = score, i
    return move

def greedy(board):
    # أولاً: لو أقدر أكسب دلوقتي
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            if checkWinner(board, 'X'):
                return i
            board[i] = ' '
    # ثانياً: امنع الخصم من الفوز
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            if checkWinner(board, 'O'):
                board[i] = ' '
                return i
            board[i] = ' '
    # ثالثاً: خذ المركز لو فاضي
    if board[4] == ' ':
        return 4
    # رابعاً: خذ زاوية
    for i in [0, 2, 6, 8]:
        if board[i] == ' ':
            return i
    # خامساً: خذ أي خانة فاضية
    for i in range(9):
        if board[i] == ' ':
            return i
    return None


BG          = "#0F0F1A"
PANEL       = "#1A1A2E"
BORDER      = "#16213E"
ACCENT_X    = "#E94560"
ACCENT_O    = "#0F9B8E"
ACCENT_MID  = "#533483"
TEXT_BRIGHT = "#EAEAEA"
TEXT_DIM    = "#7A7A9A"
BTN_IDLE    = "#1F1F35"
BTN_HOVER   = "#2A2A45"


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("XO — Tic Tac Toe")
        self.root.resizable(True, True)
        w = self.root.winfo_screenwidth() // 2
        h = self.root.winfo_screenheight() // 2
        x = self.root.winfo_screenwidth() // 4
        y = self.root.winfo_screenheight() // 4
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.configure(bg=BG)

        self.mode      = tk.StringVar(value='minimax')
        self.board     = [' '] * 9
        self.buttons   = []
        self.scores    = {'AI': 0, 'You': 0, 'Draw': 0}
        self.game_over = False

        self._build_fonts()
        self._buildUI()
        self.startGame()

    def _build_fonts(self):
        self.f_title   = tkfont.Font(family="Courier New", size=14, weight="bold")
        self.f_cell    = tkfont.Font(family="Courier New", size=20, weight="bold")
        self.f_status  = tkfont.Font(family="Courier New", size=10, weight="bold")
        self.f_score_n = tkfont.Font(family="Courier New", size=16, weight="bold")
        self.f_score_l = tkfont.Font(family="Courier New", size=8)
        self.f_btn     = tkfont.Font(family="Courier New", size=10, weight="bold")
        self.f_radio   = tkfont.Font(family="Courier New", size=9)

    def _buildUI(self):
        outer = tk.Frame(self.root, bg=BG)
        outer.place(relx=0.5, rely=0.5, anchor='center')

        # title
        title_frame = tk.Frame(outer, bg=BG)
        title_frame.pack(fill='x', pady=(0, 10))
        tk.Label(title_frame, text="X", font=self.f_title,
                 fg=ACCENT_X, bg=BG).pack(side='left')
        tk.Label(title_frame, text="  TIC TAC TOE  ",
                 font=self.f_title, fg=TEXT_BRIGHT, bg=BG).pack(side='left')
        tk.Label(title_frame, text="O", font=self.f_title,
                 fg=ACCENT_O, bg=BG).pack(side='left')

        # scoreboard
        score_card = tk.Frame(outer, bg=PANEL, padx=20, pady=8,
                              highlightbackground=BORDER,
                              highlightcolor=ACCENT_MID,
                              highlightthickness=1)
        score_card.pack(fill='x', pady=(0, 10))

        self.score_vars = {}
        for label, key, color in [("AI", "AI", ACCENT_X),
                                   ("DRAW", "Draw", TEXT_DIM),
                                   ("YOU", "You", ACCENT_O)]:
            col = tk.Frame(score_card, bg=PANEL)
            col.pack(side='left', expand=True)
            sv = tk.StringVar(value="0")
            self.score_vars[key] = sv
            tk.Label(col, textvariable=sv, font=self.f_score_n,
                     fg=color, bg=PANEL).pack()
            tk.Label(col, text=label, font=self.f_score_l,
                     fg=TEXT_DIM, bg=PANEL).pack()

        # mode selector
        mode_frame = tk.Frame(outer, bg=BG)
        mode_frame.pack(fill='x', pady=(0, 8))
        tk.Label(mode_frame, text="AI MODE", font=self.f_score_l,
                 fg=TEXT_DIM, bg=BG).pack(side='left', padx=(0, 8))

        self.radio_btns = []
        for text, val in [("MINIMAX", "minimax"), ("GREEDY", "greedy")]:
            rb = tk.Radiobutton(mode_frame, text=text, variable=self.mode,
                                value=val, font=self.f_radio,
                                fg=TEXT_DIM, bg=BG, selectcolor=BG,
                                activebackground=BG, activeforeground=TEXT_BRIGHT,
                                indicatoron=0, padx=10, pady=4,
                                relief='flat', bd=0, cursor='hand2',
                                command=self._update_radio_style)
            rb.pack(side='left', padx=4)
            self.radio_btns.append((rb, val))
        self._update_radio_style()

        # status bar
        self.status_var = tk.StringVar(value="")
        status_frame = tk.Frame(outer, bg=PANEL, pady=6,
                                highlightbackground=BORDER,
                                highlightcolor=ACCENT_MID,
                                highlightthickness=1)
        status_frame.pack(fill='x', pady=(0, 10))
        self.status_dot = tk.Label(status_frame, text="●", font=self.f_status,
                                   fg=ACCENT_O, bg=PANEL)
        self.status_dot.pack(side='left', padx=(10, 6))
        tk.Label(status_frame, textvariable=self.status_var,
                 font=self.f_status, fg=TEXT_BRIGHT, bg=PANEL).pack(side='left')

        # board
        board_outer = tk.Frame(outer, bg=ACCENT_MID, padx=2, pady=2)
        board_outer.pack(pady=(0, 10))
        board_card = tk.Frame(board_outer, bg=PANEL, padx=4, pady=4)
        board_card.pack()

        for i in range(9):
            r, c = divmod(i, 3)
            btn = tk.Label(board_card, text=" ", font=self.f_cell,
                           width=4, height=2,
                           bg=BTN_IDLE, fg=TEXT_BRIGHT,
                           cursor='hand2', relief='flat')
            btn.grid(row=r, column=c, padx=3, pady=3)
            btn.bind("<Button-1>", lambda e, idx=i: self.humanMove(idx))
            btn.bind("<Enter>",    lambda e, b=btn: self._hover(b, True))
            btn.bind("<Leave>",    lambda e, b=btn: self._hover(b, False))
            self.buttons.append(btn)

        # new game button
        tk.Button(outer, text="NEW GAME",
                  font=self.f_btn,
                  fg=TEXT_BRIGHT, bg=ACCENT_MID,
                  activeforeground=TEXT_BRIGHT,
                  activebackground=ACCENT_X,
                  padx=20, pady=8,
                  cursor='hand2', relief='flat',
                  bd=0, command=self.reset).pack(fill='x')

    def _hover(self, btn, entering):
        if btn.cget('text').strip() == '':
            btn.config(bg=BTN_HOVER if entering else BTN_IDLE)

    def _update_radio_style(self):
        chosen = self.mode.get()
        for rb, val in self.radio_btns:
            if val == chosen:
                rb.config(fg=BG, bg=ACCENT_MID,
                          activebackground=ACCENT_MID, activeforeground=BG)
            else:
                rb.config(fg=TEXT_DIM, bg=PANEL,
                          activebackground=PANEL, activeforeground=TEXT_BRIGHT)

    def changeStatus(self, msg, color=TEXT_BRIGHT):
        self.status_var.set(msg)
        self.status_dot.config(fg=color)

    def startGame(self):
        self.game_over = False
        self.changeStatus("AI is thinking...", ACCENT_X)
        self.root.after(400, self.aiTurn)

    def humanMove(self, i):
        if self.game_over or self.board[i] != ' ':
            return
        self.board[i] = 'O'
        self.buttons[i].config(text="O", fg=ACCENT_O, cursor='arrow')
        if self.endCheck(): return
        self.changeStatus("AI is thinking...", ACCENT_X)
        self.root.after(350, self.aiTurn)

    def aiTurn(self):
        move = (miniMax_move(self.board)
                if self.mode.get() == 'minimax'
                else greedy(self.board))
        if move is None: return
        self.board[move] = 'X'
        self.buttons[move].config(text="X", fg=ACCENT_X, cursor='arrow')
        if self.endCheck(): return
        self.changeStatus("Your turn  O", ACCENT_O)

    def endCheck(self):
        def highlight_winner(player, color):
            wins = [(0,1,2),(3,4,5),(6,7,8),
                    (0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
            for a, b, c in wins:
                if self.board[a] == self.board[b] == self.board[c] == player:
                    for idx in (a, b, c):
                        self.buttons[idx].config(bg=color, fg=BG)

        if checkWinner(self.board, 'X'):
            self.game_over = True
            highlight_winner('X', ACCENT_X)
            self.disableAll()
            self.scores['AI'] += 1
            self.score_vars['AI'].set(str(self.scores['AI']))
            self.changeStatus("AI wins!  X", ACCENT_X)
            self._show_result("AI WINS", ACCENT_X)
            return True

        if checkWinner(self.board, 'O'):
            self.game_over = True
            highlight_winner('O', ACCENT_O)
            self.disableAll()
            self.scores['You'] += 1
            self.score_vars['You'].set(str(self.scores['You']))
            self.changeStatus("You win!  O", ACCENT_O)
            self._show_result("YOU WIN!", ACCENT_O)
            return True

        if ' ' not in self.board:
            self.game_over = True
            self.disableAll()
            self.scores['Draw'] += 1
            self.score_vars['Draw'].set(str(self.scores['Draw']))
            self.changeStatus("It's a draw", TEXT_DIM)
            self._show_result("DRAW", TEXT_DIM)
            return True

        return False

    def _show_result(self, msg, color):
        popup = tk.Toplevel(self.root)
        popup.title("")
        popup.resizable(False, False)
        popup.configure(bg=PANEL)
        popup.grab_set()
        self.root.update_idletasks()
        x = self.root.winfo_x() + self.root.winfo_width()  // 2 - 130
        y = self.root.winfo_y() + self.root.winfo_height() // 2 - 70
        popup.geometry(f"260x140+{x}+{y}")
        tk.Label(popup, text=msg,
                 font=tkfont.Font(family="Courier New", size=18, weight="bold"),
                 fg=color, bg=PANEL).pack(pady=(22, 12))
        tk.Button(popup, text="CLOSE",
                  font=tkfont.Font(family="Courier New", size=10, weight="bold"),
                  fg=BG, bg=color, padx=20, pady=6,
                  cursor='hand2', relief='flat', bd=0,
                  command=popup.destroy).pack()

    def disableAll(self):
        for btn in self.buttons:
            btn.config(cursor='arrow')
            btn.unbind("<Enter>")
            btn.unbind("<Leave>")

    def reset(self):
        self.board     = [' '] * 9
        self.game_over = False
        for btn in self.buttons:
            btn.config(text=" ", fg=TEXT_BRIGHT, bg=BTN_IDLE, cursor='hand2')
            btn.bind("<Enter>",  lambda e, b=btn: self._hover(b, True))
            btn.bind("<Leave>",  lambda e, b=btn: self._hover(b, False))
        self.startGame()


root = tk.Tk()
TicTacToe(root)
root.mainloop()