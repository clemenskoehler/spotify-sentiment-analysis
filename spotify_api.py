import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth


class SpotifyAPI:
    def __init__(self):
        self.spotify = None

    def authenticate(self, scope, client_id=None, client_secret=None, redirect_uri=None):
        """
        Authenticate with the Spotify API using the SpotifyOAuth class from the spotipy library.

        Parameters:
            scope (str or list of str): A list of scope strings corresponding to the permissions you want to request.
            client_id (str): Your Spotify client ID.
            client_secret (str): Your Spotify client secret.
            redirect_uri (str): The redirect URI for your application, as specified in your Spotify developer dashboard.

        Returns:
            A spotipy.Spotify object authenticated with the specified user's account.
        """
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                                 client_id=client_id,
                                                                 client_secret=client_secret,
                                                                 redirect_uri=redirect_uri))

    def get_user_playlists(self):
        """
        Retrieve the playlists from a Spotify user.

        Returns:
            A list of playlists of the current user
        """
        results = self.spotify.current_user_playlists()
        playlists = results['items']
        while results['next']:
            results = self.spotify.next(results)
            playlists.extend(results['items'])
        return playlists

    def get_playlist_info(self, playlist_id):
        """
        Retrieve metadata for a single track.

        Parameters:
            playlist_id (str): The ID of the Spotify playlist.

        Returns:
            A dictionary containing metadata for the playlist.
        """
        playlist = self.spotify.playlist(playlist_id)
        return playlist

    def get_playlist_tracks(self, playlist_id):
        """
        Retrieve the tracks from a Spotify playlist.

        Parameters:
            playlist_id (str): The ID of the Spotify playlist.

        Returns:
            A list of dictionaries representing the tracks in the playlist, with each dictionary containing track metadata.
        """
        results = self.spotify.playlist_items(playlist_id, additional_types=('track',))
        tracks = results['items']
        while results['next']:
            results = self.spotify.next(results)
            tracks.extend(results['items'])
        return tracks

    def get_tracks_info(self, track_ids):
        tracks = []

        for track_id in track_ids:
            track = self.spotify.track(str(track_id['track']['id']))
            tracks.append(track)

        return tracks

    def get_track_info(self, track_id):
        """
        Retrieve metadata for a single track.

        Parameters:
            track_id (str): The ID of the Spotify track.

        Returns:
            A dictionary containing metadata for the track.
        """
        track = self.spotify.track(str(track_id))
        return track

    def get_audio_features(self, track_ids):
        """
        Retrieve audio features for one or more tracks.

        Parameters:
            track_ids (list of str): A list of Spotify track IDs.

        Returns:
            A list of dictionaries containing audio features for each track.
        """
        audio_features = self.spotify.audio_features(track_ids)
        return audio_features
