from urlextract import URLExtract
from wordcloud import WordCloud
extractor = URLExtract()
import pandas as pd
from collections import Counter
import emoji
import emoji.unicode_codes
def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df= df[df['user']== selected_user]

    num_messeges =df.shape[0]
    words = []
    for messege in df['messege']:
        words.extend(messege.split( ))

    num_media_messeges = df[df['messege'] == '<Media omitted>\n'].shape[0]
   
    links= []
    for messege in df['messege']:
        links.extend(extractor.find_urls(messege))

    len(links)
    
    return num_messeges,len(words), num_media_messeges, len(links)

def most_busy_users(df):
    x= df['user'].value_counts()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = { 'user':'name', 'count':'percent'})
    return x,df 

def create_wordcloud(selected_user,df):

    if selected_user != 'Overall':
        df= df[df['user']== selected_user]

    f = open(r"C:\Users\bhavy\OneDrive\Documents\Whatsapp chat Analyser\stop_hinglish.txt",'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df= df[df['user']== selected_user]

    temp = df[df['user']!='group_notification']
    temp= temp[temp['messege'] != '<Media omitted>\n']

    def remove_stop_words(messege):
        y = []
        for word in messege.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)



    wc = WordCloud(width = 500,height = 500, min_font_size = 10, background_color= 'white')
    temp['messege'] = temp['messege'].apply(remove_stop_words)
    df_wc = wc.generate(temp['messege'].str.cat(sep=""))
    return df_wc

def most_common_words(selected_user, df):

    f = open(r"C:\Users\bhavy\OneDrive\Documents\Whatsapp chat Analyser\stop_hinglish.txt",'r')
    stop_words = f.read()


    temp = df[df['user']!='group_notification']
    temp= temp[temp['messege'] != '<Media omitted>\n']

    words = []
    for messege in temp['messege']:
        for word in messege.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(25))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df= df[df['user']== selected_user]

    emojis = []
    for messege in df['messege']:
      emojis.extend([c for c in messege if c in emoji.EMOJI_DATA])
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df= df[df['user']== selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messege'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    
    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messege'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messege', aggfunc='count').fillna(0)

    return user_heatmap

