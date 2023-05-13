from spotify_api import SpotifyAPI
from genius_api import GeniusAPI
import nltk
from nltk import word_tokenize
import nltk.data
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import text2emotion as te
import re
from easynmt import EasyNMT

nltk.download('vader_lexicon')
nltk.download('punkt')


class SentimentAnalyzer:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()
        self.model = EasyNMT('opus-mt')

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

    def suggest_songs_vader(self, scores_dict, sentiment, num_songs=10):
        """
        Suggest new songs to the user based on their desired sentiment.
        
        Parameters:
            scores_dict (dict): A dictionary mapping song names to sentiment scores.
            sentiment (str): The desired sentiment of the suggested songs, either "positive" or "negative".
            num_songs (int): The number of songs to suggest.
            
        Returns:
            A list of song names with the desired sentiment, or None if no songs were found.
        """
        if sentiment == 0 or sentiment == 2:
            # Sort the songs by sentiment score
            sorted_songs = dict(sorted(scores_dict.items(), key=lambda x: x[1]['compound'], reverse=True))
        else:
            # Sort the songs by sentiment score
            sorted_songs = dict(sorted(scores_dict.items(), key=lambda x: x[1]['compound'], reverse=False))

        # Select the songs with the desired sentiment
        suggested_songs = []
        for title, scores in sorted_songs.items():
            suggested_songs.append(title)
            if len(suggested_songs) >= num_songs:
                break

        return suggested_songs

    def suggest_songs_textblob(self, scores_dict, sentiment, num_songs=10):
        """
        Suggest new songs to the user based on their desired sentiment.

        Parameters:
            scores_dict (dict): A dictionary mapping song names to sentiment scores.
            sentiment (str): The desired sentiment of the suggested songs, either "positive" or "negative".
            num_songs (int): The number of songs to suggest.

        Returns:
            A list of song names with the desired sentiment, or None if no songs were found.
        """
        if sentiment == 0 or sentiment == 2:
            # Sort the songs by sentiment score
            sorted_songs = dict(sorted(scores_dict.items(), key=lambda item: item[1], reverse=True))
        else:
            # Sort the songs by sentiment score
            sorted_songs = dict(sorted(scores_dict.items(), key=lambda item: item[1], reverse=False))

        # Select the songs with the desired sentiment
        suggested_songs = []
        for title, scores in sorted_songs.items():
            suggested_songs.append(title)
            if len(suggested_songs) >= num_songs:
                break

        return suggested_songs

    def suggest_songs_t2e(self, scores_dict, sentiment, num_songs=10):
        """
        Suggest new songs to the user based on their desired sentiment.

        Parameters:
            scores_dict (dict): A dictionary mapping song names to sentiment scores.
            sentiment (str): The desired sentiment of the suggested songs, either "positive" or "negative".
            num_songs (int): The number of songs to suggest.

        Returns:
            A list of song names with the desired sentiment, or None if no songs were found.
        """
        if sentiment == 0:
            # Sort the songs by sentiment score
            sorted_songs = dict(sorted(scores_dict.items(), key=lambda item: item[1]['Happy'], reverse=True))
        if sentiment == 1:
            # Sort the songs by sentiment score
            sorted_songs = dict(sorted(scores_dict.items(), key=lambda item: item[1]['Angry'], reverse=True))
        if sentiment == 2:
            # Sort the songs by sentiment score
            sorted_songs = dict(sorted(scores_dict.items(), key=lambda item: item[1]['Surprise'], reverse=True))
        if sentiment == 3:
            # Sort the songs by sentiment score
            sorted_songs = dict(sorted(scores_dict.items(), key=lambda item: item[1]['Sad'], reverse=True))
        else:
            # Sort the songs by sentiment score
            sorted_songs = dict(sorted(scores_dict.items(), key=lambda item: item[1]['Fear'], reverse=True))

        # Select the songs with the desired sentiment
        suggested_songs = []
        for title, scores in sorted_songs.items():
            suggested_songs.append(title)
            if len(suggested_songs) >= num_songs:
                break

        return suggested_songs

    def translate_lyrics(self, lyrics_dict):
        dict_new = {}

        for title, lyrics in lyrics_dict.items():
            lyrics_new = self.model.translate(lyrics, target_lang='en')
            print("Translation: ", lyrics_new)
            dict_new[title] = lyrics_new

        return dict_new

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
            lyrics_new = lyrics_new.replace("\n", " ").replace(r"[^\w\d'\s]+", "")
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

    def convert_emotions2polarity(self, emotions_dict):
        polarity_list = []

        for title, score in emotions_dict.items():
            polarity = score['Happy'] - score['Angry'] + score['Surprise'] - score['Sad'] - score['Fear']
            polarity_list.append(polarity)

        return polarity_list

    def get_compound_vader(self, vader_scores):
        list = []

        for title, score in vader_scores.items():
            compound = score['compound']
            list.append(compound)

        return list

    def get_polarity_textblob(self, textblob_scores):
        list = []

        for title, score in textblob_scores.items():
            list.append(score)

        return list
