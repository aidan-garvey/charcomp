
'''
charcomp.py - Sega Genesis graphics compression tool
Copyright (C) 2022  Aidan Garvey

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

def charcomp(
        in_name: str,   # input file name
        out_name: str,  # output file name
        in_chars: str,  # label for characters in input file
        out_rows: str,  # label for rows in output
        out_comp: str,  # label for compressed chars in output
        num_chars: int
        ):
    infile = open(in_name, mode="rt")
    outfile = open(out_name, mode="wt")

    # advance to start of target chars
    currline = infile.readline().strip()
    while currline.find(in_chars) < 0:
        currline = infile.readline().strip()

    # store array with each unique row
    saved_rows = ["$00000000"]
    # compress characters as row IDs
    comp_chars = []

    # read 8 rows per character
    char_index = 0
    while char_index < num_chars * 8:
        currline = infile.readline().strip()
        hex_index = currline.find("$")
        # if hex character found, it is a valid line
        if hex_index >= 0:
            char_index += 1
            curr_row = currline[hex_index:]
            # add row to dict if not present 
            if curr_row not in saved_rows:
                saved_rows.append(curr_row)
            comp_chars.append(saved_rows.index(curr_row))
    
    infile.close()

    # write output file
    outfile.write('\n' + out_rows + ':\n')
    for row in saved_rows:
        outfile.write(f"\tDC.L\t{row}\n")
    outfile.write('\n' + out_comp + ':\n')
    for char in comp_chars:
        outfile.write(f"\tDC.B\t{char}\n")
    outfile.write('\n')
    outfile.close()

    print("Compression successful")
    print(f"Size of uncompressed characters: {num_chars * 32} bytes")
    print(f"Size of compressed characters: {len(saved_rows) * 4 + len(comp_chars)} bytes")

    return



if __name__ == "__main__":
    print("Source file name", end=" > ")
    infile = input()
    print("\nOutput file name", end=" > ")
    outfile = input()
    print("\nLabel of characters in source file", end=" > ")
    in_chars = input()
    print("\nLabel for character rows in output", end=" > ")
    out_lines = input()
    print("\nLabel for compressed characters in output", end=" > ")
    out_comp = input()
    print("\nNumber of characters from source file to compress", end=" > ")
    num_chars = int(input())
    print()
    
    charcomp(infile, outfile, in_chars, out_lines, out_comp, num_chars)
