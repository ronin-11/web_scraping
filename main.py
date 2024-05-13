import streamlit as st
import pandas as pd

def load_data():
    df = pd.read_csv('fetched.csv')
    return df

def main():
    st.markdown("<h3 style='background-color: #0074D9; padding: 10px; border-radius: 5px; color: white;'>Welcome to News Explorer by R204434C</h3>", unsafe_allow_html=True)

    st.sidebar.subheader("Explore News Clusters")

    data = load_data()

    clusters = sorted(data['Cluster'].unique())  # Sort the clusters from 0 to 3

    chosen_cluster = st.sidebar.radio("Choose a Cluster", [f"Cluster {cluster}" for cluster in clusters])

    cluster_number = int(chosen_cluster.split()[1])  # Extract cluster number from the chosen_cluster string

    st.sidebar.success(f"**Chosen Cluster:** {chosen_cluster}")

    cluster_articles = data[data['Cluster'] == cluster_number]

    st.subheader(f"**News Articles in {chosen_cluster}**")

    for idx, row in cluster_articles.iterrows():
        st.markdown(f"**Title:** {row['Title']} - **Category:** {row['Category']} - **Source:** {row['Source']}")
        st.markdown(f"**URL:** {row['Link']}")
        st.write(" ")

# Running the app
if __name__ == "__main__":
    main()
