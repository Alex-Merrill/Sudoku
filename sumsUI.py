import sys
import itertools
import argparse
import tkinter as tk

# gets combos


def get_all_combos(s, d, f_type='none', f_nums=None):
    # initialize f_nums if default
    if f_nums is None:
        f_nums = []
    poss_nums = []

    # add possible numbers to array
    # handles excluding filter condition upfront
    for i in range(1, 10):
        if f_type == 'exc' and i not in f_nums:
            poss_nums.append(i)
        elif f_type != 'exc':
            poss_nums.append(i)

    # creates all combinations
    # if d == -1 (any combination allowed), run through all iterations
    # if d != -1 (only d length combinations allowed), only run when i == d
    mostly_final = set()
    for i in range(1, 10):
        if d != -1 and i != d:
            continue

        c = list(itertools.combinations(poss_nums, i))
        all_combos = set(c)

        for combo in all_combos:
            if sum(combo) == s:
                mostly_final.add(combo)

    # if inclusive filter active, make sure each combo has at least one of the included filter numbers
    num_set = set(f_nums)
    final = set()
    if f_type == 'inc':
        for fin in mostly_final:
            fin_set = set(fin)
            if len(fin_set) != len(fin_set-num_set):
                final.add(fin)
    else:
        final = mostly_final

    return final


# UI

# destroys widgets in given frame
def clearFrame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# sets up ui
window = tk.Tk()
window.title("Sudoku Sum-Digit Calculator")

# frames
top_bar = tk.Frame(window)
main_container = tk.Frame(window)
bottom_bar = tk.Frame(window)


# filter checkbox vars
f_inc = tk.BooleanVar()
f_exc = tk.BooleanVar()
buttons = []

def changeColor(i):
    if(buttons[i].cget("bg") == "red"):
        buttons[i].config(bg="SystemButtonFace")
    else:
        buttons[i].config(bg="red")

def reset_buttons(combos):
    for b in buttons:
        b.destroy()
    for i in range(len(buttons)):
        buttons.pop()
    for i, combo in enumerate(combos):
        newButton = tk.Button(main_container, text=str(combo), command=lambda i=i: changeColor(i))
        newButton.pack()
        buttons.append(newButton)


# run on submit
def main():
    # clear top bar of errors
    clearFrame(top_bar)

    # throw error if both checkboxes are selected
    if f_inc.get() and f_exc.get():
        tk.Label(
            top_bar, text="Can only have one checkbox checked at a time.", fg="red").pack()
        return

    # parse input
    filter_nums_input = filter_nums.get("1.0", "end-1c")
    filter_type = 'inc' if f_inc.get() else 'exc' if f_exc.get() else 'none'
    num_digits_input = int('-1' if num_digits.get("1.0", "end-1c") == '' else num_digits.get("1.0", "end-1c"))
    sum_input = int(sum_tk.get("1.0", "end-1c"))
    fnums = filter_nums_input.replace(" ", "").split(",")
    if fnums == ['']:
        fnums = []
    for i in range(len(fnums)):
        fnums[i] = int(fnums[i])

    # get combos
    combos = get_all_combos(sum_input, num_digits_input, filter_type, fnums)

    reset_buttons(combos)

    # print results
    


# finishes ui setup
filter_type_label = tk.Label(
    main_container, text="Filter Type (Optional):").pack()
filter_inc = tk.Checkbutton(
    main_container, text="Include Filter", variable=f_inc).pack()
filter_exc = tk.Checkbutton(
    main_container, text="Exclude Filter", variable=f_exc).pack()
filer_nums_label = tk.Label(
    main_container, text="Filter Numbers: (Comma seperated)").pack()
filter_nums = tk.Text(main_container, height=1, width=10)
filter_nums.pack()
num_digits_label = tk.Label(main_container, text="Number of digits").pack()
num_digits = tk.Text(main_container, height=1, width=3)
num_digits.pack()
sum_label = tk.Label(main_container, text="Sum:").pack()
sum_tk = tk.Text(main_container, height=1, width=3)
sum_tk.pack()
submit_btn = tk.Button(main_container, text="submit", bg="grey",
                       command=main).pack()
result_label = tk.Label(main_container, text="Results:")
result_label.pack()

top_bar.pack(side="top")
main_container.pack()
bottom_bar.pack(side="bottom")


window.mainloop()
