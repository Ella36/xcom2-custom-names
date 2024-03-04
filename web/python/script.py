import re
import js

# Load names from textArea
namesTextArea = js.document.getElementById("namesTextArea")
# Load input bin
from js import input_bin
soldier_pool: bytes = input_bin.to_bytes()

MAX_SIZE: int = 15  # XCOM2 game limitation
BYTES_TO_MODIFY: bytes = ( # See readme to know this magic string means
    b"\x14\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x74\x6F\x6D\x61\x78\x6C\x65\x6E\x67\x74\x68\x6E\x61\x6D\x65"
)
VALUE1 = b"\x14"
VALUE2 = b"\x10"

# read in names from JS textArea
names: list[str] = []
for line in namesTextArea.value.split('\n'):
    name = line.strip()
    if name:
        names.append(name)

amount_of_names: int = len(names)
print(f"Read {amount_of_names} names from names.txt")

# Validate names are not too short or long
names_with_invalid_length = []
names_with_special_characters = []

# Special characters
regex = r"[\u00C0-\u017F]"

# Name validation
for name in names:
    # Check if name is valid length
    if not (0 < len(name) and len(name) <= MAX_SIZE):
        names_with_invalid_length.append(name)
    # Check for special characters
    if re.search(regex, name):
        names_with_special_characters.append(name)

# Print warnings for names with special characters
if names_with_special_characters:
    print(f"Warning: {len(names_with_special_characters)} potentially breaking name(s):")
    print('\n'.join(names_with_special_characters))
    print(f"Names that have special characters (letters with accents) may break")

# Print error for names with invalid length
if names_with_invalid_length:
    print(f"Warning: {len(names_with_invalid_length)} invalid name(s):")
    print('\n'.join(names_with_invalid_length))
    raise ValueError( f"All names must be between 1 and {MAX_SIZE} characters long")

# Cut out the string to modify
bytes_split: list = soldier_pool.split(BYTES_TO_MODIFY, amount_of_names)
amount_of_soldiers_to_modify_in_pool: int = len(bytes_split) - 1
amount_of_soldiers_in_pool: int = len(soldier_pool.split(BYTES_TO_MODIFY)) - 1

if amount_of_names > amount_of_soldiers_to_modify_in_pool:
    print(
        f"Not enough soldiers in the pool ({amount_of_soldiers_in_pool}) to modify ({amount_of_names} names! Pick a bigger size!"
    )
else:
    print(
        f"Modifying {amount_of_soldiers_to_modify_in_pool}/{amount_of_soldiers_in_pool} soldiers"
    )

# Substract character difference from value
def subtract_from_value(value: bytes, amount: int) -> bytes:
    value: int = int.from_bytes(value, byteorder="big")
    value: int = value - amount
    value: bytes = value.to_bytes(
        length=1,
        byteorder="big",
    )
    return value

# Construct new bytestring
print('bytestring')
new_byte_pieces: list[bytes] = []
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

# Construct our pool of soldiers
merged_string: bytes = b""

for i in range(len(bytes_split)):
    if i == len(bytes_split) - 1:
        merged_string += bytes_split[i]
    else:
        merged_string += bytes_split[i] + new_byte_pieces[i]

# Write to output .bin
soldier_pool_bin_output = '/output.bin'
with open(soldier_pool_bin_output, "wb") as f:
    soldier_pool: bytes = f.write(merged_string)