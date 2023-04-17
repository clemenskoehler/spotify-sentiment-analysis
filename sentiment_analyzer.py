from spotify_api import SpotifyAPI
from genius_api import GeniusAPI
import nltk
from nltk import word_tokenize
import nltk.data
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import text2emotion as te
import re

nltk.download('vader_lexicon')
nltk.download('punkt')


class SentimentAnalyzer:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()

    """
    def get_lyrics_for_playlist(self, playlist_id, client_access_token):
        """"""
        Retrieve the lyrics for all songs in a Spotify playlist.
        
        Parameters:
            playlist_id (str): The ID of the Spotify playlist to retrieve.
            client_access_token (str): Your Spotify API client access token.
            
        Returns:
            A dictionary mapping song names to lyrics.
        """"""
        genius = GeniusAPI()

        # Authenticate with the Genius API
        genius.authenticate("-YBRRHhrBgG0JIqi29wYKqNhvlilQ6heuJaN0VOR0z2eNiL4MadFf4PV_juK4cbD")

        # Get the tracks in the playlist
        tracks = SpotifyAPI.get_playlist_tracks(playlist_id)

        # Retrieve the lyrics for each track in the playlist
        lyrics_dict = {}
        for track in tracks:
            title = track['name']
            artist = track['artists'][0]['name']
            lyrics = genius.get_lyrics(title, artist)
            lyrics_dict[title] = lyrics

        return lyrics_dict
    """

    def analyze_lyrics_vader(self, lyrics_dict):
        """
        Perform sentiment analysis on a dictionary of lyrics using the VADER sentiment analyzer.
        
        Parameters:
            lyrics_dict (dict): A dictionary mapping song names to lyrics.
            
        Returns:
            A dictionary mapping song names to sentiment scores.
        """

        # lyrics_dict = self.clean_lyrics(lyrics_dict)

        # Analyze the lyrics for each song in the playlist
        scores_dict = {}
        for title, lyrics in lyrics_dict.items():
            if lyrics is not None:
                # Compute the sentiment scores for the lyrics
                scores = self.sid.polarity_scores(lyrics)
                # Add the scores to the dictionary
                scores_dict[title] = scores

        return scores_dict

    def analyze_lyrics_textblob(self, lyrics_dict):
        """
        Perform sentiment analysis on a dictionary of lyrics using the TextBlob sentiment analyzer.

        Parameters:
            lyrics_dict (dict): A dictionary mapping song names to lyrics.

        Returns:
            A dictionary mapping song names to sentiment scores.
        """
        # lyrics_dict = self.clean_lyrics(lyrics_dict)

        # Analyze the lyrics for each song in the playlist
        scores_dict = {}
        for title, lyrics in lyrics_dict.items():
            if lyrics is not None:
                # Compute the sentiment scores for the lyrics
                scores = TextBlob(lyrics)
                # Add the scores to the dictionary
                scores_dict[title] = scores.sentiment.polarity

        return scores_dict

    def suggest_songs(self, scores_dict, sentiment, num_songs):
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

    def clean_lyrics(self, lyrics_dict):
        """
        Function to clean lyrics from unuseful words, such as stopwords or "chorus" etc.

        Parameters:
            lyrics_dict (dict): dictionary with the lyrics of all the songs in the playlist
        Returns:
            A dictionary of cleaned lyrics
        """
        dict_new = {}
        stopwords = nltk.corpus.stopwords.words('english')

        for title, lyrics in lyrics_dict.items():
            lyrics_new = lyrics.lower()
            lyrics_new = re.sub(r"[\[].*?[\]]", "", lyrics_new)
            # lyrics_new = lyrics_new.replace(r"verse |[1|2|3]|chorus|bridge|outro", "").replace("[",
            #                                                                                            "").replace(
            #     "]", "")
            # lyrics_new = lyrics_new.lower().replace(r"instrumental|intro|guitar|solo", "")
            lyrics_new = lyrics_new.replace("\n", " ").replace(r"[^\w\d'\s]+", "")
            # lyrics_new = lyrics_new.strip()
            words = word_tokenize(lyrics_new)
            contentwords = [w for w in words if w.lower() not in stopwords]
            dict_new[title] = ' '.join(contentwords)

        return dict_new

    def get_lyrics_emotions(self, lyrics_dict):
        # Analyze the lyrics for each song in the playlist
        scores_dict = {}
        for title, lyrics in lyrics_dict.items():
            if lyrics is not None:
                # Compute the emotion scores for the lyrics
                scores = te.get_emotion(lyrics)
                # Add the scores to the dictionary
                scores_dict[title] = scores

        return scores_dict

