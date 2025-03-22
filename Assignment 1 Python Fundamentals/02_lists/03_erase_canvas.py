'''
Problem Statement
Implement an 'eraser' on a canvas.

The canvas consists of a grid of blue 'cells' which are drawn as rectangles on the screen. We then create an eraser rectangle which, when dragged around the canvas, sets all of the rectangles it is in contact with to white.
'''

from tkinter import Tk, Canvas

CANVAS_WIDTH: int = 400
CANVAS_HEIGHT: int = 400

CELL_SIZE: int = 40
ERASER_SIZE: int = 20

def erase_object(canvas, eraser):
    """Erase objects under the eraser."""
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()

    left_x = mouse_x
    top_y = mouse_y
    right_x = left_x + ERASER_SIZE
    bottom_y = top_y + ERASER_SIZE

    overlapping_objects = canvas.find_overlapping(left_x, top_y, right_x, bottom_y)

    for overlapping_object in overlapping_objects:
        if overlapping_object != eraser:
            canvas.itemconfig(overlapping_object, fill='white')

def main():
    root = Tk()
    root.title("Eraser Tool")
    canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
    canvas.pack()

    num_rows = CANVAS_HEIGHT // CELL_SIZE
    num_cols = CANVAS_WIDTH // CELL_SIZE

    # Create a grid of blue squares
    for row in range(num_rows):
        for col in range(num_cols):
            left_x = col * CELL_SIZE
            top_y = row * CELL_SIZE
            right_x = left_x + CELL_SIZE
            bottom_y = top_y + CELL_SIZE

            canvas.create_rectangle(left_x, top_y, right_x, bottom_y, fill='blue', outline="black")

    # Create a single eraser (initially invisible)
    eraser = canvas.create_rectangle(0, 0, ERASER_SIZE, ERASER_SIZE, fill='white', outline="")

    def move_eraser():
        """Move the eraser and erase objects under it."""
        mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
        mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
        
        canvas.coords(eraser, mouse_x, mouse_y, mouse_x + ERASER_SIZE, mouse_y + ERASER_SIZE)
        erase_object(canvas, eraser)
        
        # Keep the eraser on top
        canvas.tag_raise(eraser)

        root.after(30, move_eraser)

    def on_click(event):
        """Start moving the eraser when the mouse is clicked."""
        canvas.itemconfig(eraser, fill='white')  # Make eraser visible
        move_eraser()

    canvas.bind('<Button-1>', on_click)

    root.mainloop()

if __name__ == '__main__':
    main()
