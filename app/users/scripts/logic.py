def sort_ingrs_by_alphabet(all_ingrs):
    ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    alphabetic_sorted_ingrs = {}

    for x in ALPHABET:
        alphabetic_sorted_ingrs[x] = []

    for x in all_ingrs:
        alphabetic_sorted_ingrs[x.name[0].lower()].append(x)
    return alphabetic_sorted_ingrs


def calculate_user_status(total_points):
    level1 = 400
    level2 = 1000
    level3 = 2000
    if level1 < total_points < level2 :
        return 'Advance user'
    elif level2 < total_points < level3 :
        return 'Premium user'
    elif level3 < total_points:
        return 'Top user'
    return 'Basic user'