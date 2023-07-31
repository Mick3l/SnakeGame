import tkinter as tk
import random
import collections
from dataclasses import dataclass
from typing import *


class App(tk.Canvas):
    @dataclass()
    class Snake:
        snake: collections.deque
        direction: Tuple[int, int]
        head_pos: List[int]
        length: int

    def __init__(self, parent: tk.Tk, width: int, height: int):
        super().__init__(parent, width=width, height=height, bg='black')
        # define variables
        self.square_size = 25
        self.width = width // self.square_size
        self.height = height // self.square_size
        # self.background_id = self.create_image(0, 0, anchor=tk.NW)
        self.snake = None
        self.speed = 200
        self.apple_id = None
        self.apple_pos = None
        self.occupied = None
        self.score = tk.Label(text='0')
        self.game_over_frame = None

        # bind control
        self.focus_set()
        self.bind('<Left>', self.left)
        self.bind('<Right>', self.right)
        self.bind('<Up>', self.up)
        self.bind('<Down>', self.down)

        self.game_start()
        self.pack()

    def left(self, event):
        if self.snake.direction != (1, 0):
            self.snake.direction = (-1, 0)

    def right(self, event):
        if self.snake.direction != (-1, 0):
            self.snake.direction = (1, 0)

    def up(self, event):
        if self.snake.direction != (0, 1):
            self.snake.direction = (0, -1)

    def down(self, event):
        if self.snake.direction != (0, -1):
            self.snake.direction = (0, 1)

    def show_score(self):
        self.create_window(0, 0, window=self.score, anchor=tk.NW)

    def game_start(self):
        self.snake = App.Snake(collections.deque(), (0, 1), [self.width // 2, 1], 2)
        self.snake.snake.append(self.create_snake_rect(self.width // 2, 0))
        self.snake.snake.append(self.create_snake_rect(self.width // 2, 1))
        self.occupied = collections.defaultdict(bool)
        self.occupied[(self.width // 2, 0)] = True
        self.occupied[(self.width // 2, 1)] = True
        self.apple_pos = (random.randint(0, self.width - 1), random.randint(2, self.height - 1))
        self.apple_id = self.create_apple(self.apple_pos[0], self.apple_pos[1])
        self.score.config(text='0')
        self.show_score()
        self.after(self.speed, self.game_process)

    def game_process(self):
        self.snake.head_pos[0] += self.snake.direction[0]
        self.snake.head_pos[1] += self.snake.direction[1]
        if self.occupied[tuple(self.snake.head_pos)] or \
                self.snake.head_pos[0] == -1 or \
                self.snake.head_pos[0] == self.width or \
                self.snake.head_pos[1] == -1 or \
                self.snake.head_pos[1] == self.height:
            self.game_over()
            return

        if any(i != j for i, j in zip(self.snake.head_pos, self.apple_pos)):
            tail_id = self.snake.snake.popleft()
            self.occupied[tuple(i // self.square_size for i in self.coords(tail_id)[:2])] = False
            self.move(tail_id,
                      self.snake.head_pos[0] * self.square_size - self.coords(tail_id)[0],
                      self.snake.head_pos[1] * self.square_size - self.coords(tail_id)[1])
            self.occupied[tuple(self.snake.head_pos)] = True
            self.snake.snake.append(tail_id)
        else:
            self.occupied[tuple(self.snake.head_pos)] = True
            while self.occupied[self.apple_pos]:
                self.apple_pos = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))

            self.move(self.apple_id, self.apple_pos[0] * self.square_size - self.coords(self.apple_id)[0],
                      self.apple_pos[1] * self.square_size - self.coords(self.apple_id)[1])
            self.snake.snake.append(self.create_snake_rect(self.snake.head_pos[0], self.snake.head_pos[1]))
            self.score.config(text=str(int(self.score["text"]) + 1))
        self.after(self.speed, self.game_process)

    def game_over(self):
        self.snake.direction = (0, 0)
        game_over_frame = tk.Frame()
        tk.Label(master=game_over_frame, text='try again?').grid(row=1, columnspan=2)
        tk.Button(master=game_over_frame, text='yes', command=self.restart).grid(row=2, column=0)
        tk.Button(master=game_over_frame, text='exit', command=exit).grid(row=2, column=1)
        self.game_over_frame = self.create_window(self.winfo_width() / 2, self.winfo_height() / 2,
                                                  window=game_over_frame, anchor=tk.CENTER)

    def restart(self):
        self.delete(self.game_over_frame)
        for rect in self.snake.snake:
            self.delete(rect)
        self.delete(self.apple_id)
        self.game_start()

    def create_apple(self, x, y):
        return self.create_oval(x * self.square_size, y * self.square_size,
                                (x + 1) * self.square_size, (y + 1) * self.square_size,
                                fill='red')

    def create_snake_rect(self, x, y):
        return self.create_rectangle(x * self.square_size, y * self.square_size,
                                     (x + 1) * self.square_size, (y + 1) * self.square_size + 1,
                                     fill='green', outline='white')

    def load_background(self, image: tk.PhotoImage):
        self.itemconfigure(self.background_id, image=image)


if __name__ == '__main__':
    width, height = 720, 720
    root = tk.Tk()
    root.geometry(f'{width}x{height}')
    root.resizable(False, False)
    App(root, width, height)
    root.mainloop()
