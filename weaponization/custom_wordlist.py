import itertools

#TODO: crashes with more than 8-10 words, numbers, or special characters.
#TODO: option to add or not add capitalized versions of words

def generate_wordlist(words, numbers, special_chars, filename="custom_wordlist.txt"):
    generated_words = []
    # Generate both lowercase and capitalized versions for each word
    word_variations = [word.lower() for word in words] + [word.capitalize() for word in words]
    
    # Combine all elements, including special characters and numbers
    all_elements = word_variations + numbers + special_chars

    with open(filename, "w") as file:
        # Generate all permutations for each possible length
        for perm_length in range(1, len(all_elements) + 1):
            seen = set()  # Track seen combinations to avoid duplicates
            for perm in itertools.permutations(all_elements, perm_length):
                combo = ''.join(perm)
                if combo not in seen:
                    seen.add(combo)
                    file.write(combo + '\n')
                    generated_words.append(combo)
                    
    return generated_words

