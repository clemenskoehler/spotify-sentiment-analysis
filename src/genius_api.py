import lyricsgenius

def authenticate(client_access_token):
    """
    Authenticate with the Genius API using the client access token.
    
    Parameters:
        client_access_token (str): Your Genius API client access token.
        
    Returns:
        A lyricsgenius.Genius object authenticated with the client access token.
    """
    genius = lyricsgenius.Genius(client_access_token)
    return genius

def search_song(genius, title, artist):
    """
    Search for a song on Genius and return the song object.
    
    Parameters:
        genius (lyricsgenius.Genius): A lyricsgenius.Genius object authenticated with the client access token.
        title (str): The title of the song to search for.
        artist (str): The name of the artist who performed the song.
        
    Returns:
        A lyricsgenius.songs.Song object representing the song, or None if the song was not found.
    """
    search_term = f"{title} {artist}"
    song = genius.search_song(search_term, get_full_info=True)
    return song

def get_lyrics(genius, title, artist):
    """
    Retrieve the lyrics for a song.
    
    Parameters:
        genius (lyricsgenius.Genius): A lyricsgenius.Genius object authenticated with the client access token.
        title (str): The title of the song.
        artist (str): The name of the artist who performed the song.
        
    Returns:
        A string containing the lyrics of the song, or None if the song was not found.
    """
    song = search_song(genius, title, artist)
    if song is not None:
        return song.lyrics
    else:
        return None

