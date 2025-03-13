from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from backend import *


def main():
    # colors
    color_1 = "#F5FBEF"
    color_2 = "#61707D"
    color_3 = "#D1495B"

    # initialize display
    root = Tk()
    root.title("Sprite Sorter")
    root.geometry('700x350')
    root.config(bg=color_1)

    # input and output folders
    input_folder = ""
    output_folder = ""

    # error display message
    sort_error = None

    # when select input folder button is clicked
    def select_input_folder():
        nonlocal input_folder
        folder_selected = filedialog.askdirectory()
        input_folder = folder_selected
        input_label.config(text=folder_selected)

    # when select output folder button is clicked
    def select_output_folder():
        nonlocal output_folder
        folder_selected = filedialog.askdirectory()
        output_folder = folder_selected
        output_label.config(text=folder_selected+" WARNING: will overwrite")

    # when sort button is clicked
    def run_sort():
        nonlocal sort_error

        error_display.config(text="Sorting...")
        root.update_idletasks()

        sort_error = sort(input_folder,output_folder)
        if sort_error:
            error_display.config(text=sort_error)
            root.update_idletasks()
            return

        error_display.config(text="Sorting completed!")
        root.update_idletasks()


    # create buttons and labels
    input_label = Label(root, text="No input folder selected", bg=color_1, wraplength=300, justify="left")
    input_button = Button(root, text="Select Input Folder", command=select_input_folder, bg=color_2)

    output_label = Label(root, text="No output folder selected", bg=color_1, wraplength=300, justify="left")
    output_button = Button(root, text="Select Output Folder", command=select_output_folder, bg=color_2)

    error_display = Label(root, text="", bg=color_1, width=200)

    sort_info = "SORT"
    sort_button = Button(root, text=sort_info, command=run_sort, bg=color_3,
                         padx=30, pady=10, font=('Arial', 30))

    info_str = ("Instructions:\nSelect folders and then Press SORT to copy images from the input directory "
                "into folders in the "
                "output directory. Images will be sorted by number of people. Images with one person are "
                "further classified by "
                "the pose they are in(standing, crouching, bending, kneeling, sitting, or laying)")
    info_label = Label(root, text=info_str, bg=color_1, wraplength=400, justify="left")


    # place buttons and labels on display
    input_label.place(x=100, y=25)
    input_button.place(x=100, y=75)
    output_label.place(x=100, y=125)
    output_button.place(x=100, y=175)

    error_display.place(x=425, y=50)
    sort_button.place(x=425, y=75)

    info_label.place(x=175, y=225)


    # run GUI
    root.mainloop()



if __name__ == "__main__":
    main()