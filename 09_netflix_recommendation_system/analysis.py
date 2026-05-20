import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Content-Based Recommender System
class ContentBasedRecommender:
    def __init__(self, df_movies):
        self.df = df_movies.copy()
        # Combine Genre and Description for a rich text feature
        self.df['combined_features'] = self.df['Genres'].str.replace('|', ' ') + " " + self.df['Description']
        
        # TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_features'])
        
        # Cosine Similarity matrix
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        
    def recommend(self, movie_title, top_n=5):
        # Find index of movie
        matching_movies = self.df[self.df['Title'].str.lower() == movie_title.lower()]
        if matching_movies.empty:
            return pd.DataFrame(columns=['Title', 'Genres', 'Similarity_Score'])
            
        idx = matching_movies.index[0]
        
        # Get pairwise similarity scores
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        # Sort based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # Exclude the movie itself (index 0 is the movie itself)
        sim_scores = sim_scores[1:top_n+1]
        
        movie_indices = [i[0] for i in sim_scores]
        scores = [i[1] for i in sim_scores]
        
        result = self.df.iloc[movie_indices][['Title', 'Genres']].copy()
        result['Similarity_Score'] = scores
        return result

# 2. User-User Collaborative Filtering Recommender
class CollaborativeRecommender:
    def __init__(self, df_ratings, df_movies):
        self.ratings = df_ratings.copy()
        self.movies = df_movies.copy()
        
        # Create User-Item Matrix
        self.user_item = self.ratings.pivot(index='User_ID', columns='Movie_ID', values='Rating')
        
        # Normalize ratings (mean-centering per user to account for positive/negative rating bias)
        self.user_means = self.user_item.mean(axis=1)
        self.user_item_norm = self.user_item.sub(self.user_means, axis=0).fillna(0)
        
        # Compute User Cosine Similarity Matrix
        self.user_sim = cosine_similarity(self.user_item_norm)
        self.user_sim_df = pd.DataFrame(self.user_sim, index=self.user_item.index, columns=self.user_item.index)
        
    def recommend(self, user_id, top_n=5):
        if user_id not in self.user_item.index:
            # Fallback: Return top popular movies for cold-start
            popular_movies = self.ratings.groupby('Movie_ID')['Rating'].agg(['count', 'mean'])
            popular_movies = popular_movies[popular_movies['count'] > 5].sort_values(by='mean', ascending=False)
            movie_ids = popular_movies.head(top_n).index.tolist()
            result = self.movies[self.movies['Movie_ID'].isin(movie_ids)][['Title', 'Genres']].copy()
            result['Pred_Rating'] = popular_movies.head(top_n)['mean'].values
            return result
            
        # Get rated movies for the user
        user_ratings = self.user_item.loc[user_id]
        unrated_movies = user_ratings[user_ratings.isna()].index.tolist()
        
        # Find 5 most similar users
        sim_users = self.user_sim_df.loc[user_id].sort_values(ascending=False)
        # Remove self
        sim_users = sim_users.drop(user_id).head(5)
        
        preds = []
        for movie_id in unrated_movies:
            # Get ratings of similar users for this movie
            sim_users_ratings = self.user_item.loc[sim_users.index, movie_id]
            # Filter non-NaN ratings
            valid_ratings = sim_users_ratings.dropna()
            
            if len(valid_ratings) == 0:
                # Fallback to movie's average rating in the dataset
                pred_val = self.ratings[self.ratings['Movie_ID'] == movie_id]['Rating'].mean()
                if np.isnan(pred_val):
                    pred_val = 3.0
            else:
                # Weighted average of similar users' ratings
                weights = self.user_sim_df.loc[user_id, valid_ratings.index]
                if weights.sum() == 0:
                    pred_val = valid_ratings.mean()
                else:
                    pred_val = np.dot(valid_ratings.values, weights.values) / weights.sum()
                    
            preds.append((movie_id, pred_val))
            
        preds = sorted(preds, key=lambda x: x[1], reverse=True)[:top_n]
        
        movie_ids = [p[0] for p in preds]
        ratings_val = [p[1] for p in preds]
        
        result = self.movies[self.movies['Movie_ID'].isin(movie_ids)][['Title', 'Genres']].copy()
        # Ensure order matches recommended ids
        result = result.set_index('Movie_ID').loc[movie_ids].reset_index()
        result['Predicted_Rating'] = ratings_val
        return result

def main():
    print("[*] Starting Netflix Movie Recommendation Analysis...")
    movies_file = "movies.csv"
    ratings_file = "user_ratings.csv"
    
    if not os.path.exists(movies_file) or not os.path.exists(ratings_file):
        print("[-] Data files not found! Run generate_data.py first.")
        return
        
    df_movies = pd.read_csv(movies_file)
    df_ratings = pd.read_csv(ratings_file)
    print(f"[+] Loaded {len(df_movies)} movies and {len(df_ratings)} user ratings.")
    
    # 1. Content-Based Recommendation Demo
    content_recommender = ContentBasedRecommender(df_movies)
    test_movie = "Inception"
    print(f"\n[*] Generating Content-Based Recommendations for '{test_movie}':")
    recs_content = content_recommender.recommend(test_movie, top_n=5)
    print(recs_content.to_string(index=False))
    
    # 2. Collaborative Recommendation Demo
    collab_recommender = CollaborativeRecommender(df_ratings, df_movies)
    test_user = 5
    print(f"\n[*] Generating Collaborative Recommendations for User {test_user}:")
    recs_collab = collab_recommender.recommend(test_user, top_n=5)
    print(recs_collab.to_string(index=False))
    
    # Save demo outputs
    recs_content.to_csv("content_recommendations_demo.csv", index=False)
    recs_collab.to_csv("collaborative_recommendations_demo.csv", index=False)
    print("\n[+] Saved recommendations outputs to CSV files.")
    
    # Create visualizations
    os.makedirs("visualizations", exist_ok=True)
    import matplotlib.pyplot as plt
    
    # Plot 1: Genre Frequency Chart
    genres_list = []
    for g in df_movies['Genres']:
        genres_list.extend(g.split('|'))
    genres_df = pd.Series(genres_list).value_counts().reset_index()
    genres_df.columns = ['Genre', 'Count']
    
    plt.figure(figsize=(10, 5))
    plt.bar(genres_df['Genre'], genres_df['Count'], color='#e50914', edgecolor='none', width=0.6) # Netflix red
    plt.title('Movie Catalog Genre Frequencies', fontsize=12, fontweight='bold', color='#2c3e50')
    plt.xlabel('Genre')
    plt.ylabel('Count')
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("visualizations/genre_frequencies.png", dpi=150)
    plt.close()
    
    print("[+] Saved genre distribution plot to visualizations/genre_frequencies.png")
    print("[+] Netflix recommendation pipeline finished successfully!")

if __name__ == "__main__":
    main()
