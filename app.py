SENTENCE = (
    '"One of the most basic beliefs we carry about ourselves, Dweck found in '
    "her research, has to do with how we view and inhabit what we consider to "
    "be our personality. A 'fixed mindset' assumes that our character, "
    "intelligence, and creative ability are static givens which we can't "
    "change in any meaningful way, and success is the affirmation of that "
    "inherent intelligence, an assessment of how those givens measure up "
    "against an equally fixed standard; striving for success and avoiding "
    "failure at all costs become a way of maintaining the sense of being "
    "smart or skilled. A 'growth mindset,' on the other hand, thrives on "
    "challenge and sees failure not as evidence of unintelligence but as a "
    "heartening springboard for growth and for stretching our existing "
    "abilities. Out of these two mindsets, which we manifest from a very "
    "early age, springs a great deal of our behavior, our relationship with "
    "success and failure in both professional and personal contexts, and "
    'ultimately our capacity for happiness."'
)


def search_word(term, text):
    """Search for a term in the text (case-insensitive).

    Returns a tuple of (found, count) where found is a boolean and count
    is the number of times the term appears.
    """
    term_lower = term.strip().lower()
    text_lower = text.lower()
    if not term_lower:
        return False, 0
    count = text_lower.count(term_lower)
    return count > 0, count


def highlight(term, text):
    """Return the text with all occurrences of term wrapped in ** markers."""
    term_lower = term.strip().lower()
    if not term_lower:
        return text
    result = []
    text_lower = text.lower()
    start = 0
    while True:
        idx = text_lower.find(term_lower, start)
        if idx == -1:
            result.append(text[start:])
            break
        result.append(text[start:idx])
        result.append(f"**{text[idx:idx + len(term_lower)]}**")
        start = idx + len(term_lower)
    return "".join(result)


def main():
    print("=" * 60)
    print("WORD SEARCH")
    print("=" * 60)
    print()
    print(SENTENCE)
    print()
    print("-" * 60)
    print('Type a word to search for in the passage above.')
    print('Type "quit" to exit.')
    print("-" * 60)

    while True:
        print()
        term = input("Search: ")
        if term.strip().lower() == "quit":
            print("Goodbye!")
            break
        found, count = search_word(term, SENTENCE)
        if found:
            print(f'\nA match was found! "{term.strip()}" appears {count} time(s).')
            print(f"\n{highlight(term, SENTENCE)}")
        else:
            print(f'\nNo results for "{term.strip()}". Too bad!')


if __name__ == "__main__":
    main()
