import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s(?:AM|PM)'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert dates datatype
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    user_names = []
    user_messages = []

    # Function to extract user name and user message
    def extract_username_usermessage(message):
        colon_index = message.find(":")
        if colon_index != -1:
            user_name = message[2:colon_index].strip()
            user_message = message[colon_index + 1:].strip()
        else:
            user_name = "Group notification"
            user_message = message.strip()
        return user_name, user_message

    # Apply the function to each row in the DataFrame
    for message in df['user_message']:
        user_name, user_message = extract_username_usermessage(message)
        user_names.append(user_name)
        user_messages.append(user_message)

    # Assign the extracted user names and user messages to the DataFrame
    df['user_name'] = user_names
    df['user_message'] = user_messages

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    # new_order = ['date', 'user_name', 'user_message', 'day', 'month', 'year', 'hour', 'minute']
    # df = df[new_order]

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

