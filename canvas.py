from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.root = Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.close)

		self.canvas = Canvas(self.root, bg="white")
		self.canvas.pack()

		self.running = False 

	def redraw(self):
		self.root.update_idletasks()
		self.root.update()

	def wait_for_close(self):
		self.running = True 

		while self.running:
			self.redraw()

	def close(self):
		self.running = False 



	def draw_line(self, line, fill_color):
		line.draw(self.canvas, fill_color)



class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y 

class Line:
	def __init__(self, point_1, point_2):
		self.point_1 = point_1
		self.point_2 = point_2

	def draw(self, canvas, fill_color):
		canvas.create_line(
			self.point_1.x, 
			self.point_1.y, 
			self.point_2.x,
			self.point_2.y,
			fill = fill_color,
			width = 2)

class Cell:
	def __init__(self, win, x1, y1, x2, y2, left_wall, right_wall, top_wall, bottom_wall, visited = False):
		# Window
		self.win = win

		# Coordinates
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

		# Cell Walls
		self.left_wall = left_wall
		self.right_wall = right_wall
		self.top_wall = top_wall
		self.bottom_wall = bottom_wall

		# Center Coordinates of Cell
		self.xc = (self.x1+self.x2) // 2
		self.yc = (self.y1+self.y2) // 2

		self.visited = visited

	def draw(self):
		if self.left_wall:
			line = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
			self.win.draw_line(line, "red")
		else:
			line = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
			self.win.draw_line(line, "white")

		if self.right_wall:
			line = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
			self.win.draw_line(line, "red")
		else:
			line = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
			self.win.draw_line(line, "white")

		if self.top_wall:
			line = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
			self.win.draw_line(line, "red")
		else:
			line = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
			self.win.draw_line(line, "white")

		if self.bottom_wall:
			line = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
			self.win.draw_line(line, "red")
		else:
			line = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
			self.win.draw_line(line, "white")

	def draw_move(self, to_cell, undo = False):
		line = Line(Point(self.xc, self.yc), Point(to_cell.xc, to_cell.yc))

		if undo:
			self.win.draw_line(line, "black")
		else:
			self.win.draw_line(line, "red")


class Maze:
	def __init__(self, win, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, seed = None):
		self.win = win 

		self.x1 = x1
		self.y1 = y1

		self.num_rows = num_rows
		self.num_cols = num_cols

		self.cell_size_x = cell_size_x
		self.cell_size_y = cell_size_y

		self.seed = seed
		if self.seed:
			random.seed(self.seed)

		self.cells = []
		self.create_cells()

	def create_cells(self):
		for i in range(self.num_rows):
			row = []
			for j in range(self.num_cols):
				# Calculate x1, y1, x2, y2 for the Cell
				x1 = self.x1 + j * self.cell_size_x
				y1 = self.y1 + i * self.cell_size_y
				x2 = x1 + self.cell_size_x
				y2 = y1 + self.cell_size_y

				cell = Cell(self.win, x1, y1, x2, y2, left_wall=True, right_wall=True, top_wall=True, bottom_wall=True)
				row.append(cell)

			self.cells.append(row)

		for i in range(self.num_rows):
			for j in range(self.num_cols):
				self.draw_cell(i, j)

	def draw_cell(self, i, j):
		cell = self.cells[i][j]

		cell.draw()

		self.animate()

	def animate(self):
		self.win.redraw()

		time.sleep(0.05)


	def break_entrance_and_exit(self):
		entrance_cell = self.cells[0][0]
		exit_cell = self.cells[self.num_rows-1][self.num_cols-1]

		entrance_cell.top_wall = False 
		self.draw_cell(0,0)
		exit_cell.bottom_wall = False
		self.draw_cell(self.num_rows-1, self.num_cols-1)

	def break_walls_r(self, i, j):
		current_cell = self.cells[i][j]
		current_cell.visited = True

		while True:
			to_visit = []

			# Get Cell Neighbors
			if j - 1 >= 0 and not self.cells[i][j-1].visited:
				to_visit.append((i, j-1, "left"))
			if j + 1 < self.num_cols and not self.cells[i][j+1].visited:
				to_visit.append((i, j+1, "right"))
			if i - 1 >= 0 and not self.cells[i-1][j].visited:
				to_visit.append((i-1, j, "top"))
			if i + 1 < self.num_rows and not self.cells[i+1][j].visited:
				to_visit.append((i+1, j, "bottom"))

			if not to_visit:
				current_cell.draw()
				return

			new_i, new_j, direction = random.choice(to_visit)
			neighbor_chosen = self.cells[new_i][new_j]

			if direction == "left":
				current_cell.left_wall = False
				neighbor_chosen.right_wall = False 
			elif direction == "right":
				current_cell.right_wall = False
				neighbor_chosen.left_wall = False
			elif direction == "top":
				current_cell.top_wall = False
				neighbor_chosen.bottom_wall = False
			elif direction == "bottom":
				current_cell.bottom_wall = False
				neighbor_chosen.top_wall = False

			current_cell.draw()
			neighbor_chosen.draw()

			self.break_walls_r(new_i, new_j)

	def reset_cells_visited(self):
		for i in range(self.num_rows):
			for j in range(self.num_cols):
				self.cells[i][j].visited = False

	def solve(self):
		return self.solve_r(0,0)

	def solve_r(self, i, j):
		self.animate()

		current_cell = self.cells[i][j]
		current_cell.visited = True

		if i == self.num_rows-1 and j == self.num_cols-1:
			return True 

		# Get Cell Neighbors
		if j - 1 >= 0 and not self.cells[i][j-1].visited and not current_cell.left_wall:
			current_cell.draw_move(self.cells[i][j-1])
			if self.solve_r(i, j-1):
				return True
			else:
				current_cell.draw_move(self.cells[i][j-1], undo=True)

		if j + 1 < self.num_cols and not self.cells[i][j+1].visited and not current_cell.right_wall:
			current_cell.draw_move(self.cells[i][j+1])
			if self.solve_r(i, j+1):
				return True
			else:
				current_cell.draw_move(self.cells[i][j+1], undo=True)

		if i - 1 >= 0 and not self.cells[i-1][j].visited and not current_cell.top_wall:
			current_cell.draw_move(self.cells[i-1][j])
			if self.solve_r(i-1, j):
				return True
			else:
				current_cell.draw_move(self.cells[i-1][j], undo=True)

		if i + 1 < self.num_rows and not self.cells[i+1][j].visited and not current_cell.bottom_wall:
			current_cell.draw_move(self.cells[i+1][j])
			if self.solve_r(i+1, j):
				return True
			else:
				current_cell.draw_move(self.cells[i+1][j], undo=True)

		return False

def main():
	win = Window(800, 600)

	# Creating Maze
	maze = Maze(win, 10, 10, 10, 10, 20, 20, seed = 6)
	maze.break_entrance_and_exit()
	maze.break_walls_r(0,0)
	maze.reset_cells_visited()
	maze.solve()

	win.wait_for_close()

if __name__ == "__main__":
	main()

