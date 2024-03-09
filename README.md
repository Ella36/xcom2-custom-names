# XCOM 2 Custom soldier names

This script will edit the bytestrings of the lastnames of your soldiers in a given pool.

(Option 1) Use 1 origin character with a set appearance and clone it a bunch of times. Then rename all the clones with custom names. Make your own template or use premade TomsX.bin

(Option 2) Using the Dev.bin pool. They have personalities/custom appearance made by the devs. The program can rename their last names so there's some custom appearance data compared to using Tom clones

![Ingame result](img/screenshot_pool.png)

## Requirements

Python3.9+, no third party libs

bot.py (not needed) requires pyautogui
notebook.ipynb (not needed) requires jupyter

## Usage

Decide on using Tom clones with similar appearance or Dev with more appearance variety. Alternatively you can create your own template (difficult, see details below)

Input names in names.txt (one name per line). The game limits names to 15 characters. The program will show you which names are invalid and require renaming

Names that have special characters break. ó, ò, ê, ñ, ù, ç, ¿, ß

Select the appropriate bin data for your pool numbers

⚠️The output .bin needs to loaded by the game as `Toms.bin` or `Dev.bin` as that is what it is originally exported as.

Example of running the script for Toms. Result will be 400 clones, most or all with a custom name from names.txt
```
python3 modify_lastname.py --input data/Toms400.bin --names names.txt --output Toms.bin
```

example of running the script for Dev. Result will be 400 clones with <=400 amount of custom names from names.txt
```
python3 modify_lastname.py --input data/Dev143.bin --names names.txt --output Dev.bin
```

The game loads/exports pools (.bin) here:
`My Documents/My Games/XCOM2 War of the Chosen/XComGame/CharacterPool/Importable/`
```
Importable/
├── Developers.bin
├── Dev.bin
└── Toms.bin
```

## names.txt

names should be. maximum of 15 characters per name. Run program and it will tell you which names are too long. 
Empty lines and whitespace are ignored

Tip: use google sheets formula `=LEN($B2)<=15` returns FALSE is name length is invalid

names.txt

```
name1
name2
name3
```

Names with accents such as below don't display as expected
```
Gastón Rodolfo 
Darío Priego Al
Rómulo Jerez Re
...
```

## Pool creation if creating custom clone (optional)

Create a "Tom" which is your default character. I recommend to name it "tomaxlengthname" as its tied to the bytestring that gets replaced in the script

Export into a pool. Name it Toms

Export Tom again into Toms

Export Tom again in Toms

Repeat until you have 5 Toms in the pool and 1 in barracks

Now, import the 5 toms. Repeat until you have 26.

Delete 1 Tom so you have 25.

Create a new pool Tom25. Export all to Tom25

Import Tom25 so there's 50 total.

Create new pool Tom50. Export all (50) to Tom50  

Import Tom50. Now you have 100. Export to Tom100

Import Tom50. Now you have 150. Export to Tom150

repeat until you have enough Toms



![Ingame result](img/screenshot_clones.png)

## How? What bytestring do, lastname overwriting

ImHex screenshot
1, 2 numbers correlate with name length
selected is the string itself

![Im Hex screenshot](img/ImHex_screenshot.png)

modity bytestring [0x103,0x11D] of tomaxlengthname (Tom) to desired custom name and change the 2 numbers.

### Examples of names with their bytestring

tomaxlengthname (15) - Tom template
```
14 00 00 00 00 00 00 00 10 00 00 00 74 6F 6D 61 78 6C 65 6E 67 74 68 6E 61 6D 65
```

customname (10)
```
0F 00 00 00 00 00 00 00 0B 00 00 00 63 75 73 74 6F 6D 6E 61 6D 65

```

girty (5)
```
0A 00 00 00 00 00 00 00 06 00 00 00 67 69 72 74 79
```

. (1)
```
06 00 00 00 00 00 00 00 02 00 00 00 2E
```

## Pseudo-random custom named soldiers

Renaming uses the same trick as above. I must first nename the last name to "tomaxlengthname" and then loop through and replace some bytes.

There are 143 custom characters added by the Devs. I looped through every single one and renamed their first, last and nickname. A bot (included in the dir) did most of the work. It's not perfect but it does the job.

pythongui is a requirement if you want to run it

## Resources:

UE modding resources
https://github.com/Buckminsterfullerene02/UE-Modding-Tools

ImHex - Written by WerWolv

    A Hex Editor for Reverse Engineers, Programmers and people who value their retinas when working at 3 AM.

Cutter - Written by Rizin

    Free and open source RE platform
    Decompiler, graph view, debugger, linear disassmbler, emulator, python scripting engine, plugins, binary patching, etc.



