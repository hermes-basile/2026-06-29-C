from database.DB_connect import DBConnect
from model.artista import Artista


class DAO():

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                from artist a 
                
                """

        cursor.execute(query)

        for row in cursor:
            results.append(
                Artista(**row)

            )

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodi():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.ArtistId 
                    from track t , album a 
                    where t.AlbumId = a.AlbumId 
                    order by a.ArtistId asc 

                   """

        cursor.execute(query)

        for row in cursor:
            results.append(
                (row["ArtistId"])

            )

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def fillbrani(nodo):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.*
                    from track t , album a 
                    where t.AlbumId = a.AlbumId 
                    and a.ArtistId = %s
                                    """

        cursor.execute(query, (nodo.ArtistId,))

        for row in cursor:
            results.append(
                {   "TrackId" : row["TrackId"],
                    "Name": row["Name"],
                    "AlbumId": row["AlbumId"],
                    "MediaTypeId": row["MediaTypeId"],
                    "GenreId": row["GenreId"],
                    "Composer": row["Composer"],
                    "Milliseconds": row["Milliseconds"],
                    "Bytes": row["Bytes"],
                   "UnitPrice": row["UnitPrice"]
                }
            )

        cursor.close()
        conn.close()
        nodo.lista_brani = results

    @staticmethod
    def fillplaylist(nodo):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct p.PlaylistId 
                    from track t , playlisttrack p, album a  
                    where t.TrackId = p.TrackId and a.AlbumId = t.AlbumId 
                    and a.ArtistId = %s
                                        """

        cursor.execute(query, (nodo.ArtistId,))

        for row in cursor:
            results.append(
                (row["PlaylistId"])


            )

        cursor.close()
        conn.close()
        nodo.lista_playlist = results


