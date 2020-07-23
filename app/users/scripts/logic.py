def sort_ingrs_by_alphabet(all_ingrs):
    ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    alphabetic_sorted_ingrs = {}

    for x in ALPHABET :
        alphabetic_sorted_ingrs[x] = []

    for x in all_ingrs :
        alphabetic_sorted_ingrs[x.name[0].lower()].append(x)
    return alphabetic_sorted_ingrs