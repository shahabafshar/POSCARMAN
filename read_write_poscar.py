def read_poscar(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    scaling_factor = float(lines[1].strip())
    lattice_vectors = [list(map(float, line.split()[:3])) for line in lines[2:5]]
    atom_positions = [list(map(float, line.split()[:3])) for line in lines[9:]]

    return scaling_factor, lattice_vectors, atom_positions


def write_poscar(original_filename, filename, new_lattice_vectors, new_atom_positions):
    with open(original_filename, 'r') as old_file:
        old_lines = old_file.readlines()
    with open(filename, 'w') as file:
        file.writelines(old_lines[:2])  # keep original header
        for i, vector in enumerate(new_lattice_vectors):
            vector_str = [f'{v:20.16f}' for v in vector]  # format to preserve leading zeros
            file.write(" ".join(vector_str) + "\n")
        file.writelines(old_lines[5:9])
        for position, old_line in zip(new_atom_positions, old_lines[9:]):
            position_str = [f'{p:20.16f}' for p in position]  # format to preserve leading zeros
            file.write(f"{' '.join(position_str)} {' '.join(old_line.split()[3:])}\n")


# Ensure the original_filename is accessible in this module too
original_filename = None
