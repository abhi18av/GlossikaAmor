#!/usr/bin/env python3

import sys
import getopt

ACCENT = u'\u0301'  # Accute accent mark, denotes stress
alphabet_list = ["б", "в", "г", "д", "ж", "з", "к", "л", "м", "н", "п", "р",
                 "с", "т", "ф", "х", "ц", "ч", "ш", "щ", "й", "а", "э", "ы",
                 "у", "о", "я", "е", "ё", "ю", "и", "ь", "ъ", "Б", "В", "Г",
                 "Д", "Ж", "З", "К", "Л", "М", "Н", "П", "Р", "С", "Т", "Ф",
                 "Х", "Ц", "Ч", "Ш", "Щ", "Й", "А", "Э", "Ы", "У", "О", "Я",
                 "Е", "Ё", "Ю", "И", "Ь", "Ъ"]
vowel_list = ["а", "э", "ы", "у", "о", "я", "е", "ё", "ю", "и", "А", "Э", "Ы",
              "У", "О", "Я", "Е", "Ё", "Ю", "И"]
consonant_list = [c for c in alphabet_list[:33] if c not in vowel_list]
sonorant_list = ["й", "р", "л", "м", "н", "Й", "Р", "Л", "М", "Н"]
all_words = dict()
all_syllables = dict()


def strip_text(text, include_stress):
    """Trims a string of any unwanted characters.
        
    Removes every character from a string which is not a valid russian letter.
    
    Args:
    text (string): The text from which to remove characters.
    
    Returns:
    string: Lowercase string with all non-letters or stress marks having been removed.
    """
    to_join = []
    sanitized = []
    for word in text.split():
        for character in word:
            if ((character in alphabet_list) or (include_stress and character == ACCENT)):
                to_join.append(character.lower())
        if to_join != []:
            sanitized.append("".join(to_join))
            del to_join[:]
    return " ".join(sanitized)


# Though the loop appears to be zero-indexed, it actually returns the position
# of the accent mark — which is always 1 more than the character which is
# stressed (as unicode stressed characters are actually represented "и´" as
# opposed to "и́".) This gives the correct 1-indexed position of the rendered
# ("и́") plaintext.
def find_stress_char(word):
    u"""Identifies the stressed character in a russian word.
        
    Iterates through a string until a stressed character is found. A
    stressed character is one with an accute accent mark over it (и́).
    
    Args:
    word (string): The single word string in which to find the stress.
    
    Returns:
    string: Single character string of the stressed letter. None if no
    stress mark.
    int: 1-indexed position of the stressed character. None if no stress mark.
    """
    i = 0
    for character in word:
        if character == ACCENT:
            return (previous_char + character), i  # b/c "и́">>"и´"
        previous_char = character
        i += 1
    return None, None


def find_stress_syllable(word_list, substr):
    u"""Identifies the syllable containing a stressed russian letter.
    
    Iterates through a list consisting of the syllables of a single russian 
    word to find one containing a specified stressed letter. A stressed letter 
    is one with an accute accent mark over it (и́).
    
    Args:
    word_list (list): The list of syllables constituting a single russain word.
    substr (string): A string of the syllable containing the stress mark.
    
    Returns:
    string: String containing the stressed syllable. None if no stress mark.
    int: 1-indexed position of the stressed syllables. None if no stress mark.
    
    Restrictions: 
    Can only be called on a list of syllables not on an entire word (even if 
    the word is only one syllable), i.e. after split_syllables or equivalent
    has been called.
    """
    for word in word_list:
        if substr in word:
            return word, word_list.index(word)+1
    return None, None


def count_symbols(input_string, symbol_list, stop_string=None,
                  inclusive=True, bad_stop=False):
    """Counts the occurances of any in specified set of characters in a string.
    
    Counts the number of characters from a specified list are present in a 
    particular string. Can count the number of these characters in the entire
    string or up-to or including the first occurnce of a specified substring.
    
    Args:
    input_string (string): The string to search for characters in.
    symbol_list (list): List of 1-character stings to count in input_string.
    stop_string (string): (Default=None) Substring of which find the position
    in input_string.
    inclusive (boolean): (Default=True) If true, then characters of stop_string
    will be included in search.
    
    Returns:
    int: number of characters in the examined range of input_string which are 
    listed in symbol_list
    
    Restrictions:
    While stop_sting may be a multi-character string, Symbol_list only supports
    single characters. In other words, this cannot count multi-character
    strings proceeding stop_char, only single character strings. (Number of
    vowels, not number of groups of vowels.)
    """
    the_count = 0
    to_return = ""
    if stop_string:
        if inclusive:
            for character in input_string[:input_string.find(stop_string)
                                          +len(stop_string)]:
                if character in symbol_list:
                    to_return += character
                    the_count += 1
                elif bad_stop:
                    return to_return, the_count
        else:
            for character in input_string[:input_string.find(stop_string)]:
                if character in symbol_list:
                    to_return += character
                    the_count += 1
                elif bad_stop:
                    return to_return, the_count
    else:
        for character in input_string:
            if character in symbol_list:
                to_return += character
                the_count += 1
            elif bad_stop:
                return to_return, the_count
    return to_return, the_count




# The first large for-loop splits the string into a list after every vowel,
# except for the last vowel.
#
# The second for-loop iterates through the items in the list inital_split and
# modifies them... A syllable in inital_split is added to final_split;
# characters will be appended to the end of this syllable. Sonorant consonants,
# and any non-sonorant chacters preceding them are appeneded to the previous
# syllable, as long as that sonorant character does not directly precede a
# vowel. (In other words, as long as that sonorant is not the last character in
# a group of 1 or more consonants preceeding a vowel).
def split_syllables(word):
    """Separates a russian word into distinct syllables.
    
    Splits a string, consisting of a single russian word, into a list of 
    syllables as defined by Avanesov's Syllabification Rule, aka the 
    "Acsendent Sonority" Rule, which details the criteria for the proper 
    syllibification of Russian words.
    
    Args:
    word (string): The string to split into syllables.
    
    Returns:
    list: Broken up list of syllables of word.
    int: Number of syllables in word.
    """
    to_join = []
    initial_split = []
    possible_join = []
    final_split = []
    for x in range(len(word)):
        try:  # IndexError b/c x+1 lookup
            if word[x] == ACCENT:
                continue  # Handled in another case
            elif word[x] not in vowel_list:
                to_join.append(word[x])
            elif word[x+1] == ACCENT:
                to_join.append(word[x])
                to_join.append(word[x+1])
                initial_split.append("".join(to_join))
                del to_join[:]
            else:
                to_join.append(word[x])
                initial_split.append("".join(to_join))
                del to_join[:]
        except IndexError:
            to_join.append(word[x])  # Add last character on exception
            initial_split.append("".join(to_join))
            del to_join[:]
    if to_join != []:
        initial_split[-1] += "".join(to_join)  # Consonants after final vowel
    x = 1
    for item in initial_split:
        del to_join[:]
        if x == 1:
            x = 3
            final_split.append(item)  # Adds first syllable to final list
            continue
        elif x == 2:  # Skip: when two characters added in previous iteration
            x = 3
            continue
        else:
            for y in range(len(item)):
                if (item[y] in vowel_list):
                    break
                elif (item[y] not in sonorant_list):
                    possible_join.append(item[y])  # Add depending on sonorant
                elif (item[y+1] not in vowel_list):
                    possible_join.append(item[y])
                    if ((item[y] != "й") and   # 2 character sonorants
                        ((item[y+1] == "ь") or (item[y+1] == item[y]))):
                        if item[y+2] not in vowel_list:
                            possible_join.append(item[y+1])
                            to_join = to_join + possible_join
                            x = 2
                    else:
                        to_join = to_join + possible_join
                    del possible_join[:]
        final_split[-1] = final_split[-1] + "".join(to_join)
        final_split.append(item[len("".join(to_join)):])  # Don't append twice
    return final_split, len(final_split)


def main(argv):
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["infile=", "outfile="])
    except getopt.GetoptError:
        print('RUSHin.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('RUSHin.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--infile"):
            input_file = arg
        elif opt in ("-o", "--outfile"):
            output_file = arg

    with open(input_file, encoding='utf-8') as input_file:
        input_text = input_file.read()
    for word in strip_text(input_text, True).split():
        the_word = RussianWord(word)
        if (word not in all_words and the_word.stress_char):
            all_words[word] = the_word
            for syllable in the_word.syllable_list:
                the_syll = RussianSyllable(syllable)
                if the_syll.syllable_text in all_syllables:
                    all_syllables[the_syll.syllable_text].add_occurance(syllable)
                else:
                    all_syllables[the_syll.syllable_text] = the_syll
    #for key, value in all_syllables.items():
        #print(key, value.quantity)



            # consonant groups before and after stress vowel
            # consonant groups before and after unstressed vowel
            # letter directly before and behind stressed vowel
            # letter directly before and behind unstressed vowel
            # syllable directly before and after stressed syllable
            # all syllables before and after stressed syllable

class RussianWord:
    'Russian word class'
    
    def __init__(self, word_input):
        self.word_text = word_input
        self.stress_char, self.stress_char_pos = find_stress_char(word_input)
        self.number_letters = count_symbols(word_input, alphabet_list)[1]
        self.number_vowels = count_symbols(word_input, vowel_list)[1]
        self.syllable_list, self.number_syllables = split_syllables(word_input)
        if self.stress_char:
            print("Word: ", self.word_text)
            self.stress_on_vowel_num = count_symbols(word_input, vowel_list,
                                            self.stress_char)[1]
            self.stress_syll, self.stress_on_syll_num = find_stress_syllable(self.syllable_list,
                                                                   self.stress_char)
            self.con_bef_stress, self.con_aft_stress = self.word_text.split(self.stress_char)
            self.con_bef_stress = (count_symbols(self.con_bef_stress[::-1], consonant_list,
                                                 None, bad_stop=True)[0])[::-1]
            self.con_aft_stress =count_symbols(self.con_aft_stress, consonant_list,
                                               None, bad_stop=True)[0]
            print(self.con_bef_stress, self.con_aft_stress)


class RussianSyllable:
    'Russian syllable class'

    def __init__(self, syll_input):
        self.syllable_text = strip_text(syll_input, False)
        #print(" syll:", self.syllable_text)
        self.quantity = 1
        self.quantity_stressed = 0
        self.number_letters = count_symbols(syll_input, alphabet_list)[1]
        self.stress_char, self.stress_char_pos = find_stress_char(syll_input)
        if self.stress_char:
            self.quantity_stressed = 1

    def add_occurance(self, syll_input):
        self.quantity += 1
        if not self.stress_char:
            self.stress_char, self.stress_char_pos = find_stress_char(syll_input)
        if self.stress_char:
            self.quantity_stressed += 1

class RussianTextUnit:
    'Text units smaller than a syllable'



if __name__ == "__main__":
    main(sys.argv[1:])



