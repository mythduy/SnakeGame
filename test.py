import tkinter as tk
from tkinter import messagebox
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title('Snake Game')
        self.master.resizable(False, False)

        # Khởi tạo các biến
        self.width = 600
        self.height = 400
        self.block_size = 20
        self.speed = 150
        
        # Tạo canvas để vẽ game
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, bg='black')
        self.canvas.pack()

        # Khởi tạo rắn
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.snake_direction = 'Right'
        
        # Điểm số
        self.score = 0
        self.score_display = self.canvas.create_text(
            50, 20, text=f"Score: {self.score}", fill="white", font=('Arial', 14)
        )

        # Khởi tạo mồi
        self.food = self.create_food()
        self.food_object = self.canvas.create_oval(
            self.food[0], self.food[1],
            self.food[0] + self.block_size,
            self.food[1] + self.block_size,
            fill='red'
        )

        # Bắt sự kiện bàn phím
        self.master.bind('<Left>', lambda e: self.change_direction('Left'))
        self.master.bind('<Right>', lambda e: self.change_direction('Right'))
        self.master.bind('<Up>', lambda e: self.change_direction('Up'))
        self.master.bind('<Down>', lambda e: self.change_direction('Down'))

        # Bắt đầu game
        self.game_running = True
        self.update()

    def create_food(self):
        while True:
            x = random.randint(0, (self.width - self.block_size) // self.block_size) * self.block_size
            y = random.randint(0, (self.height - self.block_size) // self.block_size) * self.block_size
            food_pos = (x, y)
            if food_pos not in self.snake:
                return food_pos

    def change_direction(self, new_direction):
        opposites = {'Left': 'Right', 'Right': 'Left', 'Up': 'Down', 'Down': 'Up'}
        if new_direction != opposites.get(self.snake_direction):
            self.snake_direction = new_direction

    def move_snake(self):
        head = self.snake[0]
        if self.snake_direction == 'Left':
            new_head = (head[0] - self.block_size, head[1])
        elif self.snake_direction == 'Right':
            new_head = (head[0] + self.block_size, head[1])
        elif self.snake_direction == 'Up':
            new_head = (head[0], head[1] - self.block_size)
        else:  # Down
            new_head = (head[0], head[1] + self.block_size)

        # Kiểm tra va chạm với tường
        if (new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over()
            return

        # Kiểm tra va chạm với thân
        if new_head in self.snake[1:]:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # Kiểm tra ăn mồi
        if new_head == self.food:
            # Tăng điểm
            self.score += 1
            self.canvas.itemconfig(self.score_display, text=f"Score: {self.score}")
            
            # Tạo mồi mới
            self.food = self.create_food()
            self.canvas.coords(self.food_object,
                             self.food[0], self.food[1],
                             self.food[0] + self.block_size,
                             self.food[1] + self.block_size)
        else:
            # Xóa đuôi nếu không ăn mồi
            self.snake.pop()

    def draw_snake(self):
        # Xóa rắn cũ
        self.canvas.delete('snake')
        
        # Vẽ rắn mới
        for segment in self.snake:
            self.canvas.create_rectangle(
                segment[0], segment[1],
                segment[0] + self.block_size,
                segment[1] + self.block_size,
                fill='green', tags='snake'
            )

    def game_over(self):
        self.game_running = False
        answer = messagebox.askquestion('Game Over', 
                                      f'Your score: {self.score}\nPlay Again?')
        if answer == 'yes':
            self.restart_game()
        else:
            self.master.quit()

    def restart_game(self):
        # Reset các giá trị
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.snake_direction = 'Right'
        self.score = 0
        self.canvas.itemconfig(self.score_display, text=f"Score: {self.score}")
        self.food = self.create_food()
        self.canvas.coords(self.food_object,
                         self.food[0], self.food[1],
                         self.food[0] + self.block_size,
                         self.food[1] + self.block_size)
        self.game_running = True
        self.update()

    def update(self):
        if self.game_running:
            self.move_snake()
            self.draw_snake()
            self.master.after(self.speed, self.update)

def main():
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()