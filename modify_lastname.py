# %%
from pathlib import Path
import re
import argparse
from typing import NamedTuple

# Ugly hack to argparse works inside notebook
isJupyterNotebook = hasattr(__builtins__,'__IPYTHON__')
if isJupyterNotebook:
    import sys
    sys.argv = ['']

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input", default="./data/Toms.bin", type=str, help="Path to input .bin file"
)
parser.add_argument(
    "--output",
    default="./Toms.bin",
    type=str,
    help="Path to output .bin file. Must be Toms.bin or Devs.bin to work properly",
)
parser.add_argument(
    "--names",
    default="./names.txt",
    type=str,
    help="Path to names.txt file. Names separated by newlines",
)

parser.add_argument(
    "--delimiter",
    default="@:@",
    type=str,
    help="Separates firstname and lastname like John@:@Smith; no delimiter defaults to {firstname: '.', lastname: lastname} e.g. '. John'",
)

args = parser.parse_args()

PATH_IN = args.input
PATH_OUT = args.output
PATH_NAMES = args.names

NAME_DELIM = args.delimiter # separates firstname and lastname

MAGIC_STRING: bytes = ( # See readme.md to see what this magic string does
b"\x0C\x00\x00\x00\x53\x74\x72\x50\x72\x6F\x70\x65\x72\x74\x79\x00\x00\x00\x00\x00"
+ b"\x06\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x2E" # Magic string for first name
+ b"\x00\x0C\x00\x00\x00\x73\x74\x72\x4C\x61\x73\x74\x4E\x61\x6D\x65\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x53\x74\x72\x50\x72\x6F\x70\x65\x72\x74\x79\x00\x00\x00\x00\x00"
+ b"\x14\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x74\x6F\x6D\x61\x78\x6C\x65\x6E\x67\x74\x68\x6E\x61\x6D\x65" # Magic string for last name
)

LAST_NAME_MAX_LENGTH: int = 15  # XCOM2 game limitation
LAST_NAME_MAGIC_VALUE1 = b"\x14"
LAST_NAME_MAGIC_VALUE2 = b"\x10"

FIRST_NAME_MAX_LENGTH: int = 11 # XCOM2 game limitation
FIRST_NAME_MAGIC_VALUE1 = b"\x06"
FIRST_NAME_MAGIC_VALUE2 = b"\x02"

NAME_DELIM: str = "@:@" # seperates firstname and lastname

# %%
soldier_pool_bin = Path(PATH_IN)
with open(soldier_pool_bin, "rb") as f:
    soldier_pool: bytes = f.read()

# %%
# read in names from a text file
names_path = Path(PATH_NAMES)

class Name(NamedTuple):
    first_name: str
    last_name: str
    def __repr__(self):
        return f"Name(first_name={self.first_name}, last_name={self.last_name}"

names: list[Name] = []

with open(names_path, "r") as f:
    for line in f:
        name_stripped = line.strip()
        if name_stripped:
            # Check if first name, last name
            if name_stripped.find(NAME_DELIM) == -1: # last name only
                first_name = '.'
                last_name = name_stripped
            else: # Name: firstname@lastname
                first_name, last_name = name_stripped.split(NAME_DELIM, maxsplit=1)
                if len(first_name) < 1: first_name = '.'
                if len(last_name) < 1: last_name = '.'
            name: Name = Name(first_name, last_name)
            names.append(name)

amount_of_names: int = len(names)
print(f"Read {amount_of_names} names from names.txt")

# Validate names
names_with_invalid_length = []
names_with_special_characters = []

regex_special_characters = r"[\u00C0-\u017F]"
has_special_characters = lambda name: re.search(regex_special_characters, name)

for name in names:
    isValidFirstName: bool = 0 < len(name.first_name) and len(name.first_name) <= FIRST_NAME_MAX_LENGTH
    isValidLastName: bool = 0 < len(name.last_name) and len(name.last_name) <= LAST_NAME_MAX_LENGTH
    if not isValidFirstName or not isValidLastName:
        names_with_invalid_length.append(name)
    if has_special_characters(first_name) or has_special_characters(last_name):
        names_with_special_characters.append(name)

# Warning for characters with accent
if names_with_special_characters:
    print(f"Warning: {len(names_with_special_characters)} potentially breaking name(s):")
    for n in names_with_special_characters:
        print(str(n))
    print(f"Names that have special characters may show incorrectly in game:\n\t{regex_special_characters}")

# Error names with invalid length
if names_with_invalid_length:
    print(f"Warning: {len(names_with_invalid_length)} invalid name(s):")
    for n in names_with_invalid_length:
        print(str(n))
    raise ValueError( f"First names max 11;Last names max 15 characters!")

# %%
## Modify last name
# Cut out the string to modify
bytes_split: list = soldier_pool.split(MAGIC_STRING, amount_of_names+1)[:amount_of_names+1]
amount_of_soldiers_to_modify_in_pool: int = len(bytes_split) - 1
amount_of_soldiers_in_pool: int = len(soldier_pool.split(MAGIC_STRING)) - 1

# The last element is incorrectly ended. We should end at the BYTES_TERMINATOR
BYTES_TERMINATOR = b"\x61\x63\x6B\x67\x72\x6F\x75\x6E\x64\x54\x65\x78\x74\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x53\x74\x72\x50\x72\x6F\x70\x65\x72\x74\x79\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x4E\x6F\x6E\x65\x00\x00\x00\x00\x00"
bytes_last: bytes = bytes_split[-1]
bytes_last: bytes = bytes_last.split(BYTES_TERMINATOR)[0] + BYTES_TERMINATOR
bytes_split[-1] = bytes_last

if amount_of_names > amount_of_soldiers_to_modify_in_pool:
    print(
        f"Not enough soldiers in the pool ({amount_of_soldiers_in_pool}) to modify ({amount_of_names} names! "
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

def add_to_value(value: bytes, amount: int) -> bytes:
    value: int = int.from_bytes(value, byteorder="little")
    value: int = value + amount
    value: bytes = value.to_bytes(
        length=1,
        byteorder="little",
    )
    return value

# Construct new bytestring
new_byte_pieces: list[bytes] = []
for name in names:
    ## Last name
    last_name = name.last_name
    amount_of_characters: int = len(last_name)
    assert amount_of_characters <= LAST_NAME_MAX_LENGTH
    new_last_name: bytes = last_name.encode()
    # Adjust our values
    character_difference: int = LAST_NAME_MAX_LENGTH - amount_of_characters
    last_name_value1: bytes = subtract_from_value(LAST_NAME_MAGIC_VALUE1, character_difference)
    last_name_value2: bytes = subtract_from_value(LAST_NAME_MAGIC_VALUE2, character_difference)
    #
    last_name_byte_string: bytes = (
        last_name_value1 + b"\x00\x00\x00\x00\x00\x00\x00" + last_name_value2 + b"\x00\x00\x00" + new_last_name
    )
    ## First name
    first_name = name.first_name
    amount_of_characters: int = len(first_name)
    assert amount_of_characters <= FIRST_NAME_MAX_LENGTH
    new_first_name: bytes = first_name.encode()
    # Adjust our values
    character_difference: int = amount_of_characters - 1
    first_name_value1: bytes = add_to_value(FIRST_NAME_MAGIC_VALUE1, character_difference)
    first_name_value2: bytes = add_to_value(FIRST_NAME_MAGIC_VALUE2, character_difference)
    #
    first_name_byte_string: bytes = (
        first_name_value1 + b"\x00\x00\x00\x00\x00\x00\x00" + first_name_value2 + b"\x00\x00\x00" + new_first_name
    )
    ## Format bytestring
    byte_string: bytes = (
        b"\x0C\x00\x00\x00\x53\x74\x72\x50\x72\x6F\x70\x65\x72\x74\x79\x00\x00\x00\x00\x00"
        + first_name_byte_string # Magic string for first name
        +b"\x00\x0C\x00\x00\x00\x73\x74\x72\x4C\x61\x73\x74\x4E\x61\x6D\x65\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x53\x74\x72\x50\x72\x6F\x70\x65\x72\x74\x79\x00\x00\x00\x00\x00"
        + last_name_byte_string  # Magic string for last name
    )
    #
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
# This number occurs twice:
# Once before name.bin
# Value located at 0x38 -> 56 LSB F4
# Value located at 0x39 -> 57 MSB 01
amount_hex: bytes = amount_of_names.to_bytes(length=2, byteorder="little")
# Once after name.bin. This is why Devs.bin and Toms.bin are 4 characters long
# Value located at 0xA2 -> 162 LSB F4
# Value located at 0xA3 -> 163 MSB 01
patched_amount_of_soldiers: bytes = merged_string[:56] + amount_hex + merged_string[58:160] + amount_hex + merged_string[162:]

merged_string = patched_amount_of_soldiers

# %%
soldier_pool_bin_output = Path(PATH_OUT)
with open(soldier_pool_bin_output, "wb") as f:
    soldier_pool: bytes = f.write(merged_string)
print(f"Wrote modified .bin to {PATH_OUT}")


