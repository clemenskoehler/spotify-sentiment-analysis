import lyricsgenius

class GeniusAPI:
    def __init__(self):
        self.genius = None

    def authenticate(self, client_access_token):
        """
        Authenticate with the Genius API using the client access token.

        Parameters:
            client_access_token (str): Your Genius API client access token.

        Returns:
            A lyricsgenius.Genius object authenticated with the client access token.
        """
        self.genius = lyricsgenius.Genius(client_access_token)

    def search_song(self, title, artist):
        """
        Search for a song on Genius and return the song object.

        Parameters:
            title (str): The title of the song to search for.
            artist (str): The name of the artist who performed the song.

        Returns:
            A lyricsgenius.songs.Song object representing the song, or None if the song was not found.
        """
        search_term = f"{title} {artist}"
        song = self.genius.search_song(search_term, get_full_info=True)
        return song

    def get_lyrics(self, tracks):
        """
        Retrieve the lyrics for a song.

        Parameters:
            tracks: a list of tracks whose lyrics we want to retrieve

        Returns:
            A string containing the lyrics of the song, or None if the song was not found.
        """
        tracks_lyrics = {}

        for track in tracks:
            try:
                song = self.genius.search_song(track['name'], track['artists'][0]['name'])
                if song is not None:
                    tracks_lyrics[track['name']] = song.lyrics
                else:
                    tracks_lyrics[track['name']] = ""
            except AttributeError:
                tracks_lyrics[track['name']] = ""

        return tracks_lyrics

