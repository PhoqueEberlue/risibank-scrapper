import sqlite3
import re


class Database:
    def __init__(self, file_name):
        self.conn = sqlite3.connect(f'{file_name}.db')
        self.file_name = file_name

    def generate_tables(self):
        """

        generate a table
        """
        self.conn.execute("CREATE TABLE IF NOT EXISTS MEDIA ( "
                          "id_media INT PRIMARY KEY NOT NULL,"
                          "date_ajout DATETIME,"
                          "auteur VARCHAR(100),"
                          "categorie VARCHAR(20),"
                          "img_full_link VARCHAR(200),"
                          "thumbnail_link VARCHAR(200),"
                          "source_link VARCHAR(200)"
                          ")")

        self.conn.execute("CREATE TABLE IF NOT EXISTS POSSEDE_TAG ("
                          "nom_tag VARCHAR(50),"
                          "id_media INT,"
                          "PRIMARY KEY (nom_tag, id_media)"
                          "FOREIGN KEY (id_media) REFERENCES MEDIA(id_media)"
                          ")")

    def add_media(self, media):
        """

        :param media:
        Add a media in the tweets table
        """

        query = "INSERT INTO MEDIA(id_media, date_ajout, auteur, categorie, img_full_link, thumbnail_link, source_link) " \
                "VALUES(?, ?, ?, ?, ?, ?, ?)"
        self.conn.execute(query, (
            media['id_media'], media['date_ajout'], media['auteur'], media['categorie'], media['img_full_link'],
            media['thumbnail_link'], media['source_link']))
        self.conn.commit()

        for tag in media["tags"]:
            query = "INSERT INTO POSSEDE_TAG(nom_tag, id_media)" \
                    "VALUES(?, ?)"
            self.conn.execute(query, (tag, media['id_media']))
            self.conn.commit()


if __name__ == "__main__":
    database = Database("Risibank")
    database.generate_tables()
