
# Create tkinter input window
def stim_regim_input(input_list, standards_df):
    import tkinter as tk

    def save_input(input_list,standards_df):
        input_values = {}
        for input_item in input_list:
            value = entry_vars[input_item].get()
            value_list = []
            
            if value == '':
                try:
                    value = standards_df[standards_df['Input'] == input_item]['Numeric Value'].iloc[0]

                    if '(' in value:
                        pairs = value.replace("(", "").replace(")", "").split(",")
                        if len(pairs) % 2 != 0:
                            print("Invalid offset entered")
                            break

                        tups = [(int(pairs[i]), int(pairs[i+1])) for i in range(0, len(pairs), 2)]
                        value_list = tups               

                    elif ',' in value:
                        value_list = [int(part.strip()) for part in value.split(',')]
                        
                    else:
                        value_list = [int(value)]        
                    
                except IndexError:
                    value = 0  # If no standard value exists, leave it empty
                    value_list = [value]
            else:
                # Split the input string by commas and convert to integers
                if '(' in value:
                    pairs = value.replace("(", "").replace(")", "").split(",")
                    if len(pairs) % 2 != 0:
                        print("Invalid offset entered")
                        break

                    tups = [(int(pairs[i]), int(pairs[i+1])) for i in range(0, len(pairs), 2)]
                    value_list = tups               

                elif ',' in value:
                    value_list = [int(part.strip()) for part in value.split(',')]
                    
                else:
                    value_list = [int(value)]               
            
            input_values[input_item] = value_list
            

        print(f'Stim values:{input_values}')
        return input_values

    root = tk.Tk()
    root.title("Stim Regimes Input")

    size = len(input_list) * 75
    root.geometry(f"300x{size}")  # Adjust the dimensions as needed

    entry_vars = {}  # Store Entry variables

    for input_item in input_list:
        label = tk.Label(root, text=f"Enter {input_item.capitalize()}:")
        label.pack(pady=5)
        
        entry_var = tk.StringVar()  # Variable to hold the Entry value
        entry = tk.Entry(root, textvariable=entry_var)
        entry.pack(pady=5)
        
        entry_vars[input_item] = entry_var  # Store the Entry variable

    save_button = tk.Button(root, text="Save", command=save_input(input_list,standards_df))
    save_button.pack(pady=10)

    
    root.mainloop()
    return save_input(input_list,standards_df)


# Iterates over input to create stim_regimes


def stim_regime_iterator(stim_inputs):
    import itertools

    stim_diameter = stim_inputs['stim_diameter']
    stim_offset = stim_inputs['stim_offset']
    duration = stim_inputs['duration']
    intensity = stim_inputs['intensity']
    input_lists = [intensity,duration,stim_offset,stim_diameter]

    stim_regimes = list(itertools.product(*input_lists))
        
    return stim_regimes

# Combines the functions


def stim_regimes_creator(input_list,standards_df):
    stim_inputs = stim_regim_input(input_list,standards_df)
    stim_regimes = stim_regime_iterator(stim_inputs)

    print("\n")
    print("Stim Regimes:")
    for n, regime in enumerate(stim_regimes):
        
        print(n,regime)
        
    print("\n")
    print("Length of stim regime:", len(stim_regimes))

    return stim_regimes


# Multiplies stim_regime list up to a ceratin number


def stim_regim_multiplier(stim_regimes, count):
    regime_count = len(stim_regimes)

    while count > regime_count:
        stim_regimes = stim_regimes + stim_regimes
        regime_count = len(stim_regimes)

    stim_regimes = stim_regimes[:count]
    return stim_regimes

# Multiplies position_list to a certain number


def position_list_multiplier(position_list, count):
    list_count = len(position_list)

    while count > list_count:
        position_list = position_list + position_list
        list_count = len(position_list)

    position_list = position_list[:count]
    return position_list

# Combines multiplier functions


def stim_pos_len_equalizer(stim_regimes, position_list, count):
    stim_regimes = stim_regim_multiplier(stim_regimes, count)
    position_list = position_list_multiplier(position_list, count)

    print('Length of the lists: ', len(stim_regimes), '&', len(position_list))
    return stim_regimes, position_list
