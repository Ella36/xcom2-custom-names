# XCOM 2 Custom soldier names

This project aims to simplify the process of creating custom soldier pools by generating them programmatically instead of manually renaming each one.

While you can still create soldier pools by hand, it can be time-consuming and tedious, especially when making changes. To address this issue, I developed a tool that quickly generates hundreds of soldier names of your choosing

Since the soldier pools are stored in binary (.bin) formats, there's no real easy way to edit en masse. This script will do a bytestring replacement of firstname + lastname fields of a premade* soldier pool.

Currently I have made 2 pools:

* (Option 1) Use 1 origin character with a set appearance and clone it a bunch of times. Then rename all the clones with custom names. Make your own template or use premade Toms.bin

* (Option 2) Using the Devs.bin pool. They have personalities/custom appearance made by the devs. The program can rename their last names so there's some custom appearance data compared to using Tom clones

Ofcourse you can also make your own pool (see details below), but this requires some effort

Result when importing some names from names.txt:
![Ingame result](img/screenshot_pool.png)

## Requirements

Python3.9+, no third party libs

bot.py (not needed) requires pyautogui used to rename the ~140 dev soldiers to create a pool
notebook.ipynb (not needed) requires jupyter

## Usage

Decide on using Tom clones with similar appearance or Dev with more appearance variety. Alternatively you can create your own template, this requires some work (see below)

Input names in names.txt (one name per line). The game limits first names to 11 characters and last names to 15 characters. The program will Error and show you which names are invalid and require renaming.

Tip: use google sheets formula `=LEN($B2)<=15` returns FALSE is name length is invalid

Names that have special characters(ó, ò, ê, ñ, ù, ç, ¿, ß, ...) may show up incorrectly.

First and lastnames are seperated by default with `@:@`. Omitting a delimiter will default to Lastname with firstname as a `.`. You can specify your delimiter with the `--delimiter` option
```
name in names.txt -> ingame
Alice -> '. Alice'
Firstname@:@Lastname  -> 'Firstname Lastname'
Some@Thing -> '. Some@Thing'
John@:@ -> 'John .'
```

Example of running the script for Toms
```
python3 modify_lastname.py --input data/Toms.bin --names names.txt --output Toms.bin
```

The game loads/exports pools (.bin) here:
`My Documents/My Games/XCOM2 War of the Chosen/XComGame/CharacterPool/Importable/`
Opening/closing the menu is sufficient for the .bin to show
```
Importable/
├── Developers.bin
├── Devs.bin
└── Toms.bin
```

## TODO
There's minimal customization options. I won't add more as it requires setting up a pool of soldiers with a specific name (see Pool creation below). The devs provide a pool which is available but the script will go sequentially and the appearance is never truly random. Extra .bin could be useful to make this process more random

## (optional) Pool creation if creating custom clone 

Create a character in the game. I require it to be named as follows:

firstname lastname `. tomaxlengthname`

as the name is tied to the bytestring replacement


️Name your custom pool exactly 4 characters long. Or it will change byte offsets.

If your pool like this ingame, the script can replace the names
![Ingame result](img/screenshot_clones.png)

## How? What bytestring do, shown for lastname overwriting 

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



