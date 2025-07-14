def preprocess(data):
    import re
    import pandas as pd

    pattern = r'\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s*(?:am|pm)\s-\s'
    messeges = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_messege': messeges, 'date': dates})
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M %p - ')
    
    users = []
    messeges = []
    for messege in df['user_messege']:
        entry = re.split(r'([\w\W]+?):\s', messege)
        if entry[1:]:
            users.append(entry[1])
            messeges.append(entry[2])
        else:
            users.append('group notification')
            messeges.append(entry[0])

    # ✅ Add 'user' and 'messege' columns
    df['user'] = users
    df['messege'] = messeges

    # ✅ Drop old column
    df.drop(columns=['user_messege'], inplace=True)

    # Time-based features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Period (e.g., "14-15")
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour+1}")

    df['period'] = period

    return df
