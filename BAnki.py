# Importing the libraries
import genanki
from bs4 import BeautifulSoup
import anki
import anki.importing.apkg
import requests
import sys
import re
import argparse
import os
import nltk

module_name = "BAnki: Export Brainscape Flashcards To Anki"
__version__ = "1.0"

# Function to generate cards using the given html page
def generateCards(htmlPage):
    # Set the arrays
    cardTable = []
    headersData = []
    questionsData = []
    answersData = []

    # Use genanki to define the flashcard models
    # Simple model: only question and answer
    my_model = genanki.Model(
    1407392320,
    'BAnki',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ],
    css='.card {font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white;'
    )

    # Question answer and media
    my_MediaModel = genanki.Model(
    1407392321,
    'BAnki',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Media'},
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br><img src="{{Media}}">',
        },
    ],
    css='.card {font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white;'
    )

    # Question with subject and answer
    my_SubjectModel = genanki.Model(
    1407392322,
    'BAnki',
    fields=[
        {'name': 'Subject'},
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '{{Subject}}<br>{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ],
    css='.card {font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white;'
    )

    # Question, subject, answer and media
    my_SubjectMediaModel = genanki.Model(
    1407392324,
    'BAnki',
    fields=[
        {'name': 'Subject'},
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Media'},
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '{{Subject}}<br>{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br><img src="{{Media}}">',
        },
    ],
    css='.card {font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white;'
    )
            
    # Loop the search for all of the questions, not only 30 (the Brainscape's questions limit by page)
    i = 1
    while i < 5:
        # Look for up to 5 possible pages
        url = htmlPage + '?page=' + str(i)

        # Fetch the raw HTML content
        content = requests.get(url).text

        # Parse the desired content
        soup = BeautifulSoup(content, "lxml")

        # Find the cards table
        cardTable = soup.find('div', {'class': 'market-content'})

        # Find the questions and answers
        headersData += cardTable.find_all(attrs={'class': 'card-prompt'})
        questionsData += cardTable.find_all(attrs={'class': 'card-face front'})
        answersData += cardTable.find_all(attrs={'class': 'card-face back'})
        answersData += cardTable.find_all(attrs={'class': 'card-face back blur-card'})
        i += 1

    # Find the deck's name
    deckName = soup.find('span', {'class': 'deck-name'})
    deckName = deckName.get_text()

    # Solve the bug that when a card contain a colon on its name, the Genanki module can't generate the card
    for character in deckName:
        deckName = deckName.replace(':', '')

    my_deck = genanki.Deck(
    2059400200,
    deckName)
    
    # Sort cards by simple, media, simple with subject and media with subject cards and prepare them to be exported to Anki
    for question in questionsData:
        questionNumber = questionsData.index(question)
        sentences = []
        sentences += questionsData[questionNumber].find_all('p')
        answerText = answersData[questionNumber].get_text()
        if(len(sentences) > 1):
            try:
                thumbCardImage = answersData[questionNumber].find('img')['data-src']
                if not thumbCardImage is None:
                        cardImage = thumbCardImage.replace("thumb", "original")
                        questionSubject = sentences[0].get_text()
                        questionText = sentences[1].get_text()
                        aNote = genanki.Note(
                            my_SubjectMediaModel, fields=[questionSubject, questionText, answerText, cardImage]
                        )
                        my_deck.add_note(aNote)
            except:
                answerText = answersData[questionNumber].get_text()
                questionSubject = sentences[0].get_text()
                questionText = sentences[1].get_text()
                aNote = genanki.Note(
                    my_SubjectModel, fields=[questionSubject, questionText, answerText]
                )
                my_deck.add_note(aNote)
        if(len(sentences) == 1):
            try:
                thumbCardImage = answersData[questionNumber].find('img')['data-src']
                if not thumbCardImage is None:
                    cardImage = thumbCardImage.replace("thumb", "original")
                    questionText = sentences[0].get_text()
                    aNote = genanki.Note(
                        my_MediaModel, fields=[questionText, answerText, cardImage]
                    )
                    my_deck.add_note(aNote)
            except:
                answerText = answersData[questionNumber].get_text()
                questionText = sentences[0].get_text()
                aNote = genanki.Note(
                    my_model, fields=[questionText, answerText]
                )
                my_deck.add_note(aNote)
            
    # Export to .apkg file
    genanki.Package(my_deck).write_to_file(deckName+'.apkg')
    print('Card '+"'"+deckName+"'"+' generated.')

# Main function
def main():
    # Argparse stuff
    parser = argparse.ArgumentParser(description=module_name)
    parser.add_argument("-v", "--version", action="version", version=module_name + ' ' +__version__)
    parser.add_argument('-g', '--generate', help='generate Anki card from given url', action='store_true', required=False)
    parser.add_argument('-d', '--debug', help='debug the application', action='store_true')
    parser.add_argument("-u", '--url', type=str, help="url to generate an unique card", action='store')
    parser.add_argument("-t", '--txt', help="txt file", action='store')
    args = parser.parse_args()

    # Argument to be used when there's something to be debugged
    if args.debug:
        print('Nothing is being debugged.')
    
    if args.generate:
        # Generate card by one single html link
        if args.url is not None:
            print("Your card is being generated.")
            generateCards(args.url)
            print("All done.")

        # Generate cards for each html link inside a .txt file
        if args.txt is not None:
            print("Your cards are being generated.")
            with open(args.txt) as f:
                for lineUrl in f:
                    generateCards(lineUrl)
            print("All done.")

main()