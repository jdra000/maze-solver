import unittest
from canvas import Maze, Window

class Tests(unittest.TestCase):
	def test_maze_create_cells(self):
		win = Window(800, 600)
		num_cols = 12
		num_rows = 10
		m1 = Maze(win, 10, 10, num_rows, num_cols, 10, 10)

		self.assertEqual(len(m1.cells), num_rows)
		self.assertEqual(len(m1.cells[0]), num_cols)

	def test_maze_reset_visited_cells(self):
		win = Window(800, 600)
		num_cols = 12
		num_rows = 10
		m1 = Maze(win, 10, 10, num_rows, num_cols, 10, 10)
		m1.reset_cells_visited()
		
		for i in range(num_rows):
			for j in range(num_cols):
				self.assertEqual(False, self.cells[i][j].visited)

if __name__ == "__main__":
	unittest.main()
