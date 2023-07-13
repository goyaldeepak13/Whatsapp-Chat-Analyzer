from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):
    if selected_user != 'All':
        df = df[df['user_name'] == selected_user]

    # fetch total no of message
    num_message = df.shape[0]

    #fetch total no of words
    num_word = []
    for message in df['user_message']:
        num_word.extend(message.split())

    #fetch total no of media
    num_media_messages = df[df['user_message'] ==  '<Media omitted>'].shape[0]

    # fetch total no of links

    links = []
    for message in df['user_message']:
      links.extend(extractor.find_urls(message))

    return num_message, len(num_word), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user_name'].value_counts().head()
    df = round((df['user_name'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns = {'count':'percent'})
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'All':
        df = df[df['user_name'] == selected_user]

    temp = df[df['user_name'] != 'Group notification']
    temp = temp[temp['user_message'] != '<Media omitted>']

    f = open('stop_hinglish(stop_words).txt', 'r')
    stop_words = f.read()

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['user_message'] = temp['user_message'].apply(remove_stop_words)
    text = temp['user_message'].str.cat(sep=" ")
    wc.generate(text)

    # Convert the WordCloud object to an image
    image = wc.to_image()

    return image


def most_common_words(selected_user, df):
    if selected_user != 'All':
        df = df[df['user_name'] == selected_user]

    temp = df[df['user_name'] != 'Group notification']
    temp = temp[temp['user_message'] != '<Media omitted>']

    f = open('stop_hinglish(stop_words).txt', 'r')
    stop_words = f.read()

    words = []
    for message in temp['user_message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_analysis(selected_user, df):
    if selected_user != 'All':
        df = df[df['user_name'] == selected_user]

    emojis = []
    for message in df['user_message']:
        #     emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'All':
        df = df[df['user_name'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['user_message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "- " + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'All':
        df = df[df['user_name'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['user_message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'All':
        df = df[df['user_name'] == selected_user]

    return df['day_name'].value_counts()



def monthly_activity_map(selected_user, df):
    if selected_user != 'All':
        df = df[df['user_name'] == selected_user]

    return df['month'].value_counts()




def activity_heatmap(selected_user, df):
    if selected_user != 'All':
        df = df[df['user_name'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='user_message', aggfunc='count').fillna(0)

    return user_heatmap

