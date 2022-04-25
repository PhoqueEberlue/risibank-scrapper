import sys
from database import Database
from scapper import Scrapper

if __name__ == "__main__":
    print(sys.argv)
    database = Database("Risibank")
    bot = Scrapper(database)
    bot.search(sys.argv[1::])
