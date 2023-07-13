import matplotlib.pyplot as plt
import streamlit as st

import helper
import preprocessor
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)
    user_list = df['user_name'].unique().tolist()
    user_list.remove('Group notification')
    user_list.sort()
    user_list.insert(0, "All")

    selected_user = st.sidebar.selectbox("Users", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, num_word, num_media_message, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with(col1):
            st.header("Total Messages")
            st.title(num_messages)

        with(col2):
            st.header("Total Words")
            st.title(num_word)

        with(col3):
            st.header("Media Shared")
            st.title(num_media_message)

        with(col4):
            st.header("Link Shared")
            st.title(num_links)


        # monthly_timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['user_message'], color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)


#         daily_timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['user_message'], color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)


        # week_activity_map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')

            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)



#         finding the busiest users in the group(Group level)

        if selected_user == 'All':
            st.title("Most chatty users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

         # wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        # st.image(df_wc)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])

        plt.xticks(rotation='vertical')
        for index, value in enumerate(most_common_df[1]):
            plt.text(value, index,
                     str(value))
        st.title('Most common words')

        st.pyplot(fig)


#        emoji analysis
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_analysis(selected_user, df)
        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)  
  



