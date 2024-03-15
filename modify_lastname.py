# %%
from pathlib import Path
import re
import argparse

# Ugly hack to argparse works inside notebook
isJupyterNotebook = hasattr(__builtins__,'__IPYTHON__')
if isJupyterNotebook:
    import sys
    sys.argv = ['']

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input", default="./data/Toms500.bin", type=str, help="Path to input .bin file"
)
parser.add_argument(
    "--output",
    default="./Toms.bin",
    type=str,
    help="Path to output .bin file. Must be Toms.bin or Dev.bin to work properly",
)
parser.add_argument(
    "--names",
    default="./names.txt",
    type=str,
    help="Path to names.txt file. Names seperated by newlines",
)
args = parser.parse_args()

PATH_IN = args.input
PATH_OUT = args.output
PATH_NAMES = args.names


MAX_SIZE: int = 15  # XCOM2 game limitation
BYTES_TO_MODIFY: bytes = ( # See readme to know this magic string means
    b"\x14\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x74\x6F\x6D\x61\x78\x6C\x65\x6E\x67\x74\x68\x6E\x61\x6D\x65"
)
VALUE1 = b"\x14"
VALUE2 = b"\x10"

# %%
# read in names from a text file
names_path = Path(PATH_NAMES)
with open(names_path, "r") as f:
    names: list[str] = []
    for line in f:
        name = line.strip()
        if name:
            names.append(name)

amount_of_names: int = len(names)
print(f"Read {amount_of_names} names from names.txt")

# Validate names are not too short or long
invalid_names = []
special_character_names = []

regex = r"[\u00C0-\u017F]"

# Warning for invalid names
for name in names:
    if not (0 < len(name) and len(name) <= MAX_SIZE):
        invalid_names.append(name)
    if re.search(regex, name):
        special_character_names.append(name)

# Warning for characters with accent
if special_character_names:
    print(f"Warning: {len(special_character_names)} potentially breaking name(s):")
    print('\n'.join(special_character_names))
    print(f"Names that have special characters may break:\n\t{regex}")

# Print invalid names
if invalid_names:
    print(f"Warning: {len(invalid_names)} invalid name(s):")
    print('\n'.join(invalid_names))
    raise ValueError( f"All names must be between 1 and {MAX_SIZE} characters long")

# %%
soldier_pool_bin = Path(PATH_IN)
with open(soldier_pool_bin, "rb") as f:
    soldier_pool: bytes = f.read()

# %%
# Cut out the string to modify
bytes_split: list = soldier_pool.split(BYTES_TO_MODIFY, amount_of_names+1)[:amount_of_names+1]
amount_of_soldiers_to_modify_in_pool = len(bytes_split) - 1
amount_of_soldiers_in_pool = len(soldier_pool.split(BYTES_TO_MODIFY)) - 1

# The last element is incorrectly ended. We should end at the BYTES_TERMINATOR
BYTES_TERMINATOR = b"\x61\x63\x6B\x67\x72\x6F\x75\x6E\x64\x54\x65\x78\x74\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x53\x74\x72\x50\x72\x6F\x70\x65\x72\x74\x79\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x4E\x6F\x6E\x65\x00\x00\x00\x00\x00"
bytes_last: bytes = bytes_split[-1]
bytes_last: bytes = bytes_last.split(BYTES_TERMINATOR)[0] + BYTES_TERMINATOR
bytes_split[-1] = bytes_last

if amount_of_names > amount_of_soldiers_to_modify_in_pool:
    print(
        f"Not enough soldiers in the pool ({amount_of_soldiers_in_pool}) to modify ({amount_of_names} names! Pick a bigger size!"
    )
else:
    print(
        f"Modifying {amount_of_soldiers_to_modify_in_pool}/{amount_of_soldiers_in_pool} soldiers"
    )

# %%
# Substract character difference from value
def subtract_from_value(value: bytes, amount: int) -> bytes:
    value: int = int.from_bytes(value, byteorder="little")
    value: int = value - amount
    value: bytes = value.to_bytes(
        length=1,
        byteorder="little",
    )
    return value

# Construct new bytestring
new_byte_pieces = []
for name in names:
    amount_of_characters: int = len(name)
    assert amount_of_characters <= MAX_SIZE
    new_name: bytes = name.encode()

    # Adjust our values
    character_difference: int = MAX_SIZE - amount_of_characters
    value1: bytes = subtract_from_value(VALUE1, character_difference)
    value2: bytes = subtract_from_value(VALUE2, character_difference)

    byte_string: bytes = (
        value1 + b"\x00\x00\x00\x00\x00\x00\x00" + value2 + b"\x00\x00\x00" + new_name
    )

    new_byte_pieces.append(byte_string)

# %%
# Construct our pool of soldiers
merged_string: bytes = b""

for i in range(len(bytes_split)):
    if i == len(bytes_split) - 1:
        merged_string += bytes_split[i]
    else:
        merged_string += bytes_split[i] + new_byte_pieces[i]


# %%
# If we return less values than the .bin holds it will copypaste the last soldier
# Patch amount of soldiers value
# For  500: ['\xF4, '\x01']
# Value located at 0x38 -> 56 LSB F4
# Value located at 0x39 -> 57 MSB 01
amount_hex: bytes = amount_of_names.to_bytes(length=2, byteorder="little")
# Value located at 0xA2 -> 162 LSB F4
# Value located at 0xA3 -> 163 MSB 01
patched_amount_of_soldiers: bytes = merged_string[:56] + amount_hex + merged_string[58:162] + amount_hex + merged_string[164:]
merged_string = patched_amount_of_soldiers

# %%
soldier_pool_bin_output = Path(PATH_OUT)
with open(soldier_pool_bin_output, "wb") as f:
    soldier_pool: bytes = f.write(merged_string)
print(f"Wrote modified .bin to {PATH_OUT}")


