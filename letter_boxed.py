
import sys

ALLOWED_LETTERS='jhtawouinbge'
WORDS_FILE='30k.txt'
DEBUG=False
FIND_ALL_SOLUTIONS=False
solutions = []

def print_help():
    print("Letter-boxed solver")
    print("Usage: python letter-boxed.py [-l <letters>] [-w <words_file>] [-h]")
    print("Options:")
    print("-l <letters> - allowed letters")
    print("-w <words_file> - file with words")
    print("-a - find all solutions")
    print("-d - detailed print")
    print("-h - print this help")

def deal_with_command_line_args(args):
    global ALLOWED_LETTERS
    global WORDS_FILE
    global DEBUG
    global FIND_ALL_SOLUTIONS
    for i in range(len(args)):
        if args[i] == '-a':
            FIND_ALL_SOLUTIONS = True
        if args[i] == '-l':
            ALLOWED_LETTERS = args[i+1]
            if len(ALLOWED_LETTERS) != 12:
                print("Allowed letters must be 12")
                sys.exit(1)
        if args[i] == '-w':
            WORDS_FILE = args[i+1]
        if args[i] == '-h':
            print_help()
            sys.exit()
        if args[i] == '-d':
            DEBUG = True

    print("Allowed letters: ", ALLOWED_LETTERS)
    print("Words file: ", WORDS_FILE)
    print("Debug: ", DEBUG)
    print("Find all solutions: ", FIND_ALL_SOLUTIONS)

def import_words(words_file):
    with open(words_file, 'r', encoding='utf-8') as f:
        words = f.readlines()
        # remove \n
        words = [word.strip() for word in words]
        print("Found words: ", len(words))
        return words

def filter_by_allowed_letters(words, allowed_letters):
    print("Filtering by letters...")
    allowed_by_letters = []
    # get all words that contain only allowed letters
    for word in words:
        if all(letter in allowed_letters for letter in word):
            allowed_by_letters.append(word)
    print("Allowed by letters: ", len(allowed_by_letters))
    return allowed_by_letters

def remove_double_letters(words):
    print("Filtering by double letters...") # e.g. "hello" is not allowed because of the double l
    allowed_by_double = []
    for word in words:
        if all(word[i] != word[i+1] for i in range(len(word)-1)):
            allowed_by_double.append(word)

    print("Allowed by order: ", len(allowed_by_double))
    return allowed_by_double

def calculate_group(letters):
    groups = []
    for i in range(0, len(letters), 3):
        groups.append(letters[i:i+3])
    return groups

def filter_by_group(words, groups):
    print("Filter by group of letters...")
    # divide allowed letters into groups, like ['afi', 'ock', 'red', 'wvs']. Add first 3 letters to the first group, next 3 to the second, etc.
    allowed_by_group = []

    for word in words:
        # for each letter in the word calculate the group of letters
        groups_in_word_index = []
        for letter in word:
            for group in groups:
                if letter in group:
                    groups_in_word_index.append(groups.index(group))
                    break
        # remove words that have the same group of letters twice in a row
        if all(groups_in_word_index[i] != groups_in_word_index[i+1] for i in range(len(groups_in_word_index)-1)):
            allowed_by_group.append(word)

    print("Allowed by group: ", len(allowed_by_group))
    return allowed_by_group

def filter_by_length(words, min_length):
    return [word for word in words if len(word) > min_length]

def save_to_file(words):
    # save to  file
    with open('filtered_words.txt', 'w', encoding='utf-8') as f:
        for word in words:
            if all(letter in ALLOWED_LETTERS for letter in word):
                f.write(word + '\n')

def generate_map_words_letters_count(words):
    # for all words count number of different letters in word
    map_words_letters_count = {}
    for word in words:
        map_words_letters_count[word] = len(set(word))

    # sort by number of different letters
    map_words_letters_count = {k: v for k, v in sorted(map_words_letters_count.items(), key=lambda item: item[1], reverse=True)}
    return map_words_letters_count

def count_letters_in_solution(solution):
    return len(set(''.join(solution)))

def all_letters_in_solution(solution, allowed_letters):
    return count_letters_in_solution(solution) == len(allowed_letters)

def find_solution(solution, map_words_letters_count, find_all_solutions, detailed_print=False):
    global solutions
    if detailed_print:
        print(solution)
    old_count = count_letters_in_solution(solution)
    # find all words that start with the last letter of last word
    word = solution[-1]
    possible_next_words = [w for w in map_words_letters_count.keys() if w[0] == word[-1]]
    # remove all words that are already in the solution
    possible_next_words = [w for w in possible_next_words if w not in solution]

    # preferred letters: the ones that are not in the solution
    preferred_letters = [l for l in ALLOWED_LETTERS if l not in ''.join(solution)]
    # print("Letters still missing in solution: ")
    # print(preferred_letters)

    # count the number of preferred letters in the possible next words
    map_next_words_preferred_count = {w: sum([1 for l in preferred_letters if l in w]) for w in possible_next_words}

    # sort
    map_next_words_preferred_count = {k: v for k, v in sorted(map_next_words_preferred_count.items(), key=lambda item: item[1], reverse=True)}
    none_helped = True
    for next_word in enumerate(map_next_words_preferred_count):
        solution.append(next_word[1])
        # print("Trying word: " + word)
        if count_letters_in_solution(solution) <= old_count:
            # print(next_word[1] + " doesnt help. Backtracking")
            solution.pop()
            continue
        none_helped = False
        # if all letters are in the solution, print and exit
        if all_letters_in_solution(solution, ALLOWED_LETTERS):
            solutions.append(solution)
            if detailed_print or (not find_all_solutions):
                print("Solution found: ")
                print(solution)
                if not find_all_solutions:
                    sys.exit()
            return True
        if find_solution(solution, map_words_letters_count, find_all_solutions, detailed_print):
            return True
        else:
            none_helped = True
    
    if none_helped:
        solution.pop()
        return [False]

def check_params(words_file, allowed_letters, find_all_solutions, debug):
    if words_file == None or allowed_letters == None or find_all_solutions == None or debug == None:
        return ["Missing parameters"]
    if len(allowed_letters) != 12:
        print("Allowed letters must be 12")
        return ["Wrong length"]
    return []

def letter_boxed_solver(words_file, allowed_letters, find_all_solutions, debug, limit=-1):
    if check_params(words_file, allowed_letters, find_all_solutions, debug) != []:
        return {"Errors": check_params(words_file, allowed_letters, find_all_solutions, debug)}
    global solutions
    words = import_words(words_file)
    allowed_by_letters = filter_by_allowed_letters(words, allowed_letters)
    allowed_by_double = remove_double_letters(allowed_by_letters)

    letter_groups = calculate_group(allowed_letters)
    allowed_by_group = filter_by_group(allowed_by_double, letter_groups)
    allowed_by_group = filter_by_length(allowed_by_group, 2) # optimization - there's certainly something better cmon
    allowed_by_group.sort(key=len, reverse=True) # order by length descending, let's try the longest words first to get rid of more letters at once

    save_to_file(allowed_by_group)

    map_words_letters_count = generate_map_words_letters_count(allowed_by_group)

    for word in allowed_by_group:
        find_solution([word], map_words_letters_count, find_all_solutions, debug)
    
    # filter solution by length (max 5 words) and sort by length to show the shortest solutions first
    # solutions = [solution for solution in solutions if len(solution) < 6]
    solutions.sort(key=len)
    
    if limit != -1:
        solutions = solutions[:int(limit)]
    return solutions

def main():
    # read arguments in command line
    deal_with_command_line_args(sys.argv[1:])

    solutions = letter_boxed_solver(WORDS_FILE, ALLOWED_LETTERS, FIND_ALL_SOLUTIONS, DEBUG)

    print("\nSolutions:")
    for solution in solutions:
        print(solution)

    print("Found solutions: ", len(solutions))
    if len(solutions) > 0:
        print("Shortest solution: " + str(solutions[0]) + " (" + str(len(solutions[0])) + " words)")

if __name__ == '__main__':
    main()
