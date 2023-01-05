import re
import sys

# Phantasy Star Online uses unicode values to determine which of the 10 section IDs your character will receive.
# By converting the individual characters in a name to unicode and summing their value, the last digit [0-9]
# will determine the section ID.
section_ids = {
    'Viridia': 0,
    'Greenill': 1,
    'Skyly': 2,
    'Bluefull': 3,
    'Purplenum': 4,
    'Pinkal': 5,
    'Redria': 6,
    'Oran': 7,
    'Yellowboze': 8,
    'Whitill': 9
}

# In Blue Burst we must also consider the character class in the calculation. This prevents characters with the
# same name but different class from having the same section ID.
blue_burst_classes = {
    'HUmar': 5,
    'HUnewearl': 6,
    'Hucast': 7,
    'HUcaseal': 4,
    'RAmar': 8,
    'RAmarl': 6,
    'RAcast': 9,
    'RAcaseal': 0,
    'FOmar': 5,
    'FOmarl': 1,
    'FOnewm': 2,
    'FOnewearl': 3,
}

print('Welcome to the Section ID Calculator for Phantasy Star Online Episode I & II (including Plus & Blue Burst)')
blue_burst_names = input('Do you want to check names for Blue Burst? [y/n]: ')
blue_burst_names = blue_burst_names.upper()
if blue_burst_names == 'Y' or blue_burst_names == 'YES':
    blue_burst_names = True
    print('What class will you play as in Blue Burst?')
    for key in blue_burst_classes.keys():
        print(key)
    while True:
        character_class = input()
        if character_class not in blue_burst_classes.keys():
            print('Sorry, that class does not exist. Try again. (Input is case sensitive!)')
        else:
            break
else:
    pass

name = input('Name: ')
end_program = ''
confirm_exit = False


def name_converter():
    global name
    global end_program
    global confirm_exit

    character_name = name
    if len(character_name) > 10 and blue_burst_names == True:
        print('Character name is too long. The limit is 10 characters in Blue Burst (you have ' + str(len(
            character_name)) + ').')
        name = input()
        name_converter()
    elif len(character_name) > 12:
        print('Character name is too long. The limit is 12 characters in Episode I & II (you have ' + str(len(
            character_name)) + ').')
        name = input()
        name_converter()
    else:
        pass

    pattern = re.compile(r'[\w\W\s\S]')

    unicode_characters = []

    # According to https://phantasystar.fandom.com/wiki/Section_ID
    # Some characters have different values in Blue Burst which are not accounted for here
    # ' = 9, unicode 39
    # ` = 6, unicode 96
    # } = 5, unicode 125
    list_name = list(filter(pattern.match, character_name))
    for character in list_name:
        unicode_conversion = ord(character)
        unicode_characters.append(int(unicode_conversion))
    if blue_burst_names == True:
        calculated_id = str(sum(unicode_characters) + blue_burst_classes.get(character_class))[-1]
    else:
        calculated_id = str(sum(unicode_characters))[-1]

    # Output calculated section ID
    print(character_name + ' is a ' + list(section_ids.keys())[int(calculated_id)])
    if confirm_exit == False:
        end_program = input('Type \'--exit\' to stop, or continue by typing a new name.\n')
        confirm_exit = True
    else:
        end_program = input()

    # We cannot output the name '--exit' unless it was the first name used
    if end_program == '--exit':
        sys.exit(0)
    else:
        name = end_program
        name_converter()


name_converter()
