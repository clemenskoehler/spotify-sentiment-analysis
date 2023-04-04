from spotify_api import get_playlist_tracks
from genius_api import authenticate, get_lyrics
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()


    def get_lyrics_for_playlist(playlist_id, client_access_token):
        """
        Retrieve the lyrics for all songs in a Spotify playlist.
        
        Parameters:
            playlist_id (str): The ID of the Spotify playlist to retrieve.
            client_access_token (str): Your Spotify API client access token.
            
        Returns:
            A dictionary mapping song names to lyrics.
        """
        # Authenticate with the Genius API
        genius = authenticate(<your Genius API client access token here>)
        
        # Get the tracks in the playlist
        tracks = get_playlist_tracks(<your Spotify API client access token here>, playlist_id)
        
        # Retrieve the lyrics for each track in the playlist
        lyrics_dict = {}
        for track in tracks:
            title = track['name']
            artist = track['artists'][0]['name']
            lyrics = get_lyrics(genius, title, artist)
            lyrics_dict[title] = lyrics
        
        return lyrics_dict

    def analyze_lyrics(lyrics_dict):
        """
        Perform sentiment analysis on a dictionary of lyrics using the VADER sentiment analyzer.
        
        Parameters:
            lyrics_dict (dict): A dictionary mapping song names to lyrics.
            
        Returns:
            A dictionary mapping song names to sentiment scores.
        """
        # Initialize the sentiment analyzer
        sia = SentimentIntensityAnalyzer()
        
        # Analyze the lyrics for each song in the playlist
        scores_dict = {}
        for title, lyrics in lyrics_dict.items():
            if lyrics is not None:
                # Compute the sentiment scores for the lyrics
                scores = sia.polarity_scores(lyrics)
                # Add the scores to the dictionary
                scores_dict[title] = scores
        
        return scores_dict

    def suggest_songs(scores_dict, sentiment, num_songs):
        """
        Suggest new songs to the user based on their desired sentiment.
        
        Parameters:
            scores_dict (dict): A dictionary mapping song names to sentiment scores.
            sentiment (str): The desired sentiment of the suggested songs, either "positive" or "negative".
            num_songs (int): The number of songs to suggest.
            
        Returns:
            A list of song names with the desired sentiment, or None if no songs were found.
        """
        # Determine the sentiment threshold for the desired sentiment
        if sentiment == 'positive':
            threshold = 0.5
        elif sentiment == 'negative':
            threshold = -0.5
        else:
            return None
        
        # Sort the songs by sentiment score
        sorted_songs = sorted(scores_dict.items(), key=lambda x: x[1]['compound'], reverse=True)
        
        # Select the songs with the desired sentiment
        suggested_songs = []
        for title, scores in sorted_songs:
            if scores['compound'] >= threshold:
                suggested_songs.append(title)
                if len(suggested_songs) >= num_songs:
                    break
        
        return suggested_songs
