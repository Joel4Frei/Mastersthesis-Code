import tkinter as tk
import pandas as pd

def variables_input(input_list, standards_df):

    def save_input(input_dic, standards_df):
        variable_dic = {}
        for input_item, entry_var in input_dic.items():
            value = entry_var.get()
            if value == '':
                try:
                    value = standards_df[standards_df['Input'] == input_item]['Numeric Value'].iloc[0]
                except IndexError:
                    value = 0  # If no standard value exists, leave it empty
            else:
                value = int(value)  # Convert to int only if not empty
            variable_dic[input_item] = value
        
        print(variable_dic)
        return variable_dic



    root = tk.Tk()
    root.title("Stim Regimes Input")

    input_dic = {}

    # Set the initial size of the window (width x height)
    size = len(input_list) * 50
    root.geometry(f"600x{size}")  # Adjust the dimensions as needed

    input_frame = tk.Frame(root)
    input_frame.pack(side="left", padx=20)

    for input_item in input_list:
        frame = tk.Frame(input_frame)
        frame.pack(anchor="w", pady=5)

        label = tk.Label(frame, text=f"{input_item.capitalize()}:")
        label.pack(side="left")

        entry_var = tk.StringVar()  # Variable to hold the Entry value
        entry = tk.Entry(frame, textvariable=entry_var)
        entry.pack(side="left", pady=5)

        input_dic[input_item] = entry_var  # Store the Entry variable

    standards_frame = tk.Frame(root)
    standards_frame.pack(side="right", padx=20, pady=20)

    # Convert the DataFrame to a Tkinter table (using pandas' styling)
    standards_table = tk.Label(standards_frame, text=standards_df.to_string(index=False), justify="right")
    standards_table.pack(side="top")

    save_button = tk.Button(root, text="Save", command=lambda: save_input(input_dic, standards_df),width=50, height=1)
    save_button.pack(pady=20,side="bottom")


    root.mainloop()
    return save_input(input_dic, standards_df)

