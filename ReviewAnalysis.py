from afinn import Afinn

sia = Afinn()

# Analyse the text
def sentiment_score(sentence):
    # Creates and appends reviews to text file
    def create_review(status):
        with open(f"./{status}.txt", "a+") as text_file:
            text_file.writelines(sentence)

    # Creates a sentiment object
    sia = Afinn()
    score = sia.score(sentence)

    # Store Sentences
    if score > 0:
        create_review("positive")
    elif score < 0:
        create_review("negative")
    else:
        create_review("neutral")

