import sys
from database import Database
from scapper import Scrapper

if __name__ == "__main__":
    database = Database("Risibank")
    database.generate_tables()
    bot = Scrapper(database)
    bot.search(sys.argv[1::])
