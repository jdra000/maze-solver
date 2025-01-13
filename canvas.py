from tkinter import Tk, BOTH, Canvas
import time

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
	def __init__(self, win, x1, y1, x2, y2, left_wall, right_wall, top_wall, bottom_wall):
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

	def draw(self):
		if self.left_wall:
			line = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
			self.win.draw_line(line, "red")

		if self.right_wall:
			line = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
			self.win.draw_line(line, "red")

		if self.top_wall:
			line = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
			self.win.draw_line(line, "red")

		if self.bottom_wall:
			line = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
			self.win.draw_line(line, "red")

	def draw_move(self, to_cell, undo = False):
		line = Line(Point(self.xc, self.yc), Point(to_cell.xc, to_cell.yc))

		if undo:
			self.win.draw_line(line, "gray")
		else:
			self.win.draw_line(line, "red")


class Maze:
	def __init__(self, win, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y):
		self.win = win 

		self.x1 = x1
		self.y1 = y1

		self.num_rows = num_rows
		self.num_cols = num_cols

		self.cell_size_x = cell_size_x
		self.cell_size_y = cell_size_y

		self.cells = []
		self.create_cells()

	def create_cells(self):
		for i in range(self.num_rows):
			row = []
			for j in range(self.num_cols):
				# Calculate x1, y1, x2, y2 for the Cell
				x1 = self.x1 + i * self.cell_size_x
				y1 = self.y1 + j * self.cell_size_y
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







def main():
	win = Window(800, 600)

	#Creating Cells
	cell_1 = Cell(win, 10, 10, 40, 40, left_wall=True, right_wall=True, top_wall=True, bottom_wall=True)
	cell_1.draw()

	cell_2 = Cell(win, 40, 10, 70, 40, left_wall=True, right_wall=True, top_wall=True, bottom_wall=True)
	cell_2.draw()

	cell_1.draw_move(cell_2)

	# Creating Maze
	maze = Maze(win, 10, 10, 10, 10, 10, 10)



	win.wait_for_close()

if __name__ == "__main__":
	main()

