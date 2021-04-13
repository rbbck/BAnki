# BAnki

BAnki: Export Brainscape Flashcards To Anki 

*This software and its author are not affiliated/associated with the main Anki project or Brainscape in any way.*

__DISCLAIMER: This software is for educational purposes only. It should not be used for illegal activity. The author is not responsible for its use. All Brainscape content belong to their respective owners.__

## Getting Started

In order to run the software, you need to have these Python modules installed:

- [genanki](https://github.com/kerrickstaley/genanki)
    - `pip install genanki` 
- [Anki](https://apps.ankiweb.net/index.html)
	- `pip install anki`
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
    - `pip install beautifulsoup4`
- [argparse](https://github.com/ThomasWaldmann/argparse/)
    - `pip install argparse`
- [nltk](http://www.nltk.org/)
    - `pip install nltk`

## Command line options

The following command line arguments are available:

| Option | Description |
| ------ | ----------- |
| `-h`, `--help` | Displays the help message |
| `-v`, `--version` | Displays the software version. |
| `-g`, `--generate` | Generate Anki card from given url. |
| `-d`, `--debug` | Debug the application. |
| `-u`, `--url` | Url to generate an unique card. |
| `-t`, `--txt` | TXT file to multiple parsing. |

## Usage

Some examples of the application usage

From an unique url:
- Linux / Mac
    - `python BAnki.py -g -u https://www.brainscape.com/flashcards/biochem-cellular-5862182/packs/9139025`
- Windows
    - `py BAnki.py -g -u https://www.brainscape.com/flashcards/federal-judicial-system-7745547/packs/13169405`

From a txt file (put a link on each line of the .txt file):
- Linux / Mac
    - `python BAnki.py -g -t links.txt`
- Windows
    - `py BAnki.py -g -u links.txt`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) for details

    