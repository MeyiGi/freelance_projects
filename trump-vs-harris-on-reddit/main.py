import time
from credentials import CLIENT_ID, CLIENT_SECRET
from config import KEYWORDS_1_LIST, KEYWORDS_2_LIST, TOP_POSTS_TIME_FILTER, MAXIMUM_POSTS_PER_SUBREDDIT, SUBREDDIT_NAMES_LIST, STATES
from data_gatherer import DataGatherer
from sentiment_analyzer import SentimentAnalyzer
from datetime import datetime, timedelta

def analyze_state(state):
    backoff_time = 1  # Start with 1 second
    max_backoff = 60  # Maximum backoff time in seconds

    while True:
        try:
            # Append the state to keywords for this specific run
            KEYWORDS_1_LIST.append(state)
            KEYWORDS_2_LIST.append(state)

            # Initialize data gatherer and sentiment analyzer
            data_gatherer = DataGatherer(client_id=CLIENT_ID,
                                         client_secret=CLIENT_SECRET,
                                         subreddit_names_list=SUBREDDIT_NAMES_LIST,
                                         top_posts_time_filter=TOP_POSTS_TIME_FILTER,
                                         maximum_posts_per_subreddit=MAXIMUM_POSTS_PER_SUBREDDIT)
            comments_list_by_author = data_gatherer.get_comments_list_by_author(subreddit_name="all")
            sentiment_analyzer = SentimentAnalyzer()

            # Initialize vote counts
            keywords_1_list_total_votes = 0
            keywords_2_list_total_votes = 0

            print(f"Analyzing sentiment for {state}...")

            # Perform sentiment analysis for each comment
            for author_name in comments_list_by_author:
                keywords_1_list_sentiment_score = sentiment_analyzer.get_texts_list_sentiment_score(KEYWORDS_1_LIST, comments_list_by_author[author_name])
                keywords_2_list_sentiment_score = sentiment_analyzer.get_texts_list_sentiment_score(KEYWORDS_2_LIST, comments_list_by_author[author_name])
                
                if keywords_1_list_sentiment_score > keywords_2_list_sentiment_score:
                    keywords_1_list_total_votes += 1
                if keywords_1_list_sentiment_score < keywords_2_list_sentiment_score:
                    keywords_2_list_total_votes += 1

            print(KEYWORDS_1_LIST)
            print("Votes percent:", round(100 * keywords_1_list_total_votes / len(comments_list_by_author), 2))
            print(KEYWORDS_2_LIST)
            print("Votes percent:", round(100 * keywords_2_list_total_votes / len(comments_list_by_author), 2))
            print("Votes difference percent:", round(100 * (max(keywords_1_list_total_votes, keywords_2_list_total_votes) / min(keywords_1_list_total_votes, keywords_2_list_total_votes) - 1), 2))

            # Calculate difference percentage
            difference = round((100 * (max(keywords_1_list_total_votes, keywords_2_list_total_votes) / min(keywords_1_list_total_votes, keywords_2_list_total_votes) - 1) / 2), 2)
            if keywords_1_list_total_votes > keywords_2_list_total_votes:
                print("May", KEYWORDS_1_LIST, "win the US 2024 election?")
                donald_percentage = 50 + difference
                harris_percentage = 50 - difference
            elif keywords_1_list_total_votes < keywords_2_list_total_votes:
                print("May", KEYWORDS_2_LIST, "win the US 2024 election?")
                donald_percentage = 50 - difference
                harris_percentage = 50 + difference

            # Determine date range
            current_date = datetime.now()
            week_ago_date = current_date - timedelta(days=7)
            formatted_current_date = current_date.strftime("%b %d, %Y")
            formatted_week_ago_date = week_ago_date.strftime("%b %d")

            # Prepare result string
            overall = donald_percentage + harris_percentage
            result_string = f"{formatted_week_ago_date} - {formatted_current_date}: Donald({round(100 * (donald_percentage/overall), 2)}), Harris({round(100 * (harris_percentage/overall), 2)}) - {state}\n"

            # Append result to result.txt
            with open("result.txt", "a") as file:
                file.write(result_string)

            # Remove the state from keywords after analysis
            KEYWORDS_1_LIST.pop()
            KEYWORDS_2_LIST.pop()

            # Reset backoff time if successful
            backoff_time = 1
            break

        except Exception as e:
            # Check if error is a 429 Too Many Requests error
            if "429" in str(e):
                print(f"429 Error for {state}: Waiting {backoff_time} seconds before retrying...")
                time.sleep(backoff_time)
                backoff_time = min(backoff_time * 2, max_backoff)  # Exponential backoff, capped at max_backoff
            else:
                print(f"Error analyzing {state}: {e}. Retrying...")
                time.sleep(1)  # Short wait for other errors

# Run each state analysis in a separate thread
for state in STATES:
    analyze_state(state=state)

print("Sentiment analysis for all states completed.")
