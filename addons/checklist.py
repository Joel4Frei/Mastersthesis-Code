def check_list(checkpoint_list):
    import tkinter as tk
    from tkinter import messagebox

    def check_checkboxes():
        if all(checkbox_var.get() for checkbox_var in checkbox_vars):
            root.destroy()  # Close the window and continue with the code
        else:
            messagebox.showinfo(
                "Checkboxes", "Not all checkboxes are checked. Please check all checkboxes.")

    def on_closing():
        print("Window is being closed...")
        root.destroy()

    # Create main window
    root = tk.Tk()
    # Create title on winow
    root.title("Experiment Checkpoint List")
    # Configure the window size
    size = len(checkpoint_list) * 50
    root.geometry(f"200x{size}")  # Adjust the dimensions as needed
    # Create boolean for each check box
    checkbox_vars = [tk.BooleanVar() for _ in checkpoint_list]

    for i, checkpoint in enumerate(checkpoint_list):
        checkbox = tk.Checkbutton(
            root, text=checkpoint, variable=checkbox_vars[i],  anchor='center', padx=5, pady=5)
        checkbox.config(justify="center")
        checkbox.pack(fill="both")

    continue_button = tk.Button(
        root, text="Continue", command=check_checkboxes)
    continue_button.pack(side="bottom", pady=20)

    root.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window close event

    root.mainloop()
