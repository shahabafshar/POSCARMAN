import tkinter as tk
from tkinter import filedialog, messagebox
from read_write_poscar import read_poscar, write_poscar

original_filename = None
lattice_entries = []


def load_file():
    global original_filename
    original_filename = filedialog.askopenfilename(title="Open POSCAR file", filetypes=[("VASP files", "*.vasp"), ("All files", "*.*")])
    if original_filename:
        _, lattice_vectors, _ = read_poscar(original_filename)
        for i, entry in enumerate(lattice_entries):
            entry.delete(0, tk.END)
            entry.insert(0, str(lattice_vectors[i][i]))


def update_file():
    global original_filename  # to ensure the updated original_filename is used
    if original_filename is None:
        messagebox.showerror("Error", "No file loaded")
        return

    new_filename = filedialog.asksaveasfilename(title="Save As", defaultextension=".vasp", initialfile="POSCAR_new.vasp")
    if not new_filename:
        return

    scaling_factor, old_lattice_vectors, atom_positions = read_poscar(original_filename)
    
    new_lattice_vectors = [[0, 0, 0] for _ in range(3)]
    for i, entry in enumerate(lattice_entries):
        new_lattice_vectors[i][i] = float(entry.get())
    
    ratio_vectors = [old_lattice_vectors[i][i] / new_lattice_vectors[i][i] if new_lattice_vectors[i][i] != 0 else 1 for i in range(3)]
    new_atom_positions = [[pos[i] * ratio_vectors[i] for i in range(3)] for pos in atom_positions]

    write_poscar(original_filename, new_filename, new_lattice_vectors, new_atom_positions)
    
    if any(any(p > 1 for p in position) for position in new_atom_positions):
        messagebox.showwarning("Warning", "Some atom positions are greater than 1 in the updated file.")
    else:
        messagebox.showinfo("Success", "File updated successfully")


# Create the main window
window = tk.Tk()
window.title("POSCAR Manager")

# Create a frame to hold the lattice size entries and labels
frame = tk.Frame(window, pady=10, padx=10)
frame.pack()

# Create labels and entries for the lattice sizes
for i, axis in enumerate("XYZ"):
    tk.Label(frame, text=f"Lattice Size {axis}:", font=("Arial", 12)).grid(row=i, column=0, padx=5, pady=5, sticky=tk.E)
    entry = tk.Entry(frame, font=("Arial", 12), width=10)
    entry.grid(row=i, column=1, padx=5, pady=5)
    lattice_entries.append(entry)

# Create the buttons
load_button = tk.Button(window, text="Load File", command=load_file, font=("Arial", 12))
load_button.pack(pady=5)
update_button = tk.Button(window, text="Update File", command=update_file, font=("Arial", 12))
update_button.pack(pady=5)

# Run the Tkinter event loop
window.mainloop()
