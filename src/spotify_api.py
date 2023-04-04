import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

def authenticate(scope, username=None, client_id=None, client_secret=None, redirect_uri=None):
    """
    Authenticate with the Spotify API using the SpotifyOAuth class from the spotipy library.
    
    Parameters:
        scope (str or list of str): A list of scope strings corresponding to the permissions you want to request.
        username (str): The Spotify username of the user you want to authenticate as. If None, the current user is used.
        client_id (str): Your Spotify client ID.
        client_secret (str): Your Spotify client secret.
        redirect_uri (str): The redirect URI for your application, as specified in your Spotify developer dashboard.
        
    Returns:
        A spotipy.Spotify object authenticated with the specified user's account.
    """
    if username is None:
        username = spotipy.Spotify().me()['id']
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                    client_id=client_id,
                                                    client_secret=client_secret,
                                                    redirect_uri=redirect_uri,
                                                    username=username))
    return sp

def get_playlist_tracks(sp, playlist_id):
    """
    Retrieve the tracks from a Spotify playlist.
    
    Parameters:
        sp (spotipy.Spotify): A spotipy.Spotify object authenticated with the user's Spotify account.
        playlist_id (str): The ID of the Spotify playlist.
        
    Returns:
        A list of dictionaries representing the tracks in the playlist, with each dictionary containing track metadata.
    """
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def get_track_info(sp, track_id):
    """
    Retrieve metadata for a single track.
    
    Parameters:
        sp (spotipy.Spotify): A spotipy.Spotify object authenticated with the user's Spotify account.
        track_id (str): The ID of the Spotify track.
        
    Returns:
        A dictionary containing metadata for the track.
    """
    track = sp.track(track_id)
    return track

def get_audio_features(sp, track_ids):
    """
    Retrieve audio features for one or more tracks.
    
    Parameters:
        sp (spotipy.Spotify): A spotipy.Spotify object authenticated with the user's Spotify account.
        track_ids (list of str): A list of Spotify track IDs.
        
    Returns:
        A list of dictionaries containing audio features for each track.
    """
    audio_features = sp.audio_features(track_ids)
    return audio_features

