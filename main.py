import streamlit as st
import pandas as pd
import random

def load_data():
    df = pd.read_csv('fetched.csv')
    return df

def main():
    st.markdown("Welcome to News Explorer")

    st.subheader("Explore News Clusters")

    data = load_data()

    clusters = data['Cluster'].unique()
    random.shuffle(clusters)  # Shuffle the clusters

    chosen_cluster = st.sidebar.radio("Choose a Cluster", clusters)

    st.success(f"Selected Cluster: {chosen_cluster}")

    cluster_articles = data[data['Cluster'] == chosen_cluster]

    for idx, row in cluster_articles.iterrows():
        st.markdown(f"**Title:** {row['Title']}")
        st.markdown(f"**Category:** {row['Category']}")
        st.markdown(f"**Source:** {row['Source']}")
        st.markdown(f"**URL:** {row['Link']}")
        st.write(" ")

# Running the app
if __name__ == "__main__":
    main()
