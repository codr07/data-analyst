# 🎬 Netflix Movie Recommendation System

This project implements two fundamental recommendation engine algorithms using Python: Content-Based Filtering and Collaborative Filtering. It reads a movie catalog and user rating records to calculate vector similarities and suggest personalized watch recommendations.

## 🎯 Objectives
- Build a text feature engineering process using TF-IDF on genres and movie plot descriptions.
- Implement **Content-Based Filtering** using pairwise cosine similarities between movie vectors.
- Implement **User-User Collaborative Filtering** using normalized, mean-centered user-item interaction matrix similarities.
- Map user taste profiles to recommend movies they have not yet rated.
- Generate comparative recommendation lists.

## 🛠️ Tech Stack
- **Recommendation & NLP Models**: Python, Scikit-learn (TfidfVectorizer, cosine_similarity)
- **Data Engineering**: Pandas, Numpy
- **Data Visualization**: Matplotlib

## ⚙️ Recommendation Algorithms
### 1. Content-Based Filtering
- Text features ($f_i$) are constructed by joining the genre string and plot summary of each movie.
- TF-IDF vectors are generated for all movies.
- The similarity between movie $A$ and movie $B$ is calculated using the Cosine Similarity of their TF-IDF representations:
  $$\text{Similarity}(A, B) = \frac{\mathbf{v}_A \cdot \mathbf{v}_B}{\|\mathbf{v}_A\| \|\mathbf{v}_B\|}$$

### 2. User-User Collaborative Filtering
- Ratings matrix ($R$) is constructed ($U \times M$).
- Mean-centered normalization is applied to each user's ratings to remove bias (e.g. generous vs critical raters):
  $$R'_{u, m} = R_{u, m} - \bar{R}_u$$
- Cosine similarity is computed between all users.
- For user $u$, unrated movie $m$'s predicted rating is calculated as the weighted average rating of $u$'s top $K$ nearest neighbors who have rated $m$:
  $$\hat{R}_{u, m} = \frac{\sum_{v \in K} \text{Sim}(u, v) \times R_{v, m}}{\sum_{v \in K} |\text{Sim}(u, v)|}$$

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate synthetic movie listings and rating databases:
   ```bash
   python generate_data.py
   ```
3. Run the content-based and collaborative recommender pipeline:
   ```bash
   python analysis.py
   ```

## 📊 Key Deliverables
- `movies.csv`: A catalog containing movie IDs, titles, genre listings, and summaries.
- `user_ratings.csv`: User-movie rating interactions (1 to 5 stars).
- `content_recommendations_demo.csv`: Output demonstration showing content recommendations for a test movie (e.g. "Inception").
- `collaborative_recommendations_demo.csv`: Output demonstration showing collaborative recommendations for a test user.
- `visualizations/genre_frequencies.png`: Distribution of film counts per genre in the catalog.
