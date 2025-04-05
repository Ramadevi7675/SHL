from matching_engine import recommend_assessments

if __name__ == "__main__":
    csv_file_path = "shl_sample_assessments.csv"  # Make sure the path is correct
    recommendations = recommend_assessments(csv_file_path)
    
    print("\nTop Recommendations:\n")
    print(recommendations[['Assessment Name', 'Test Type', 'Duration', 
                           'Remote Testing Support', 'Adaptive/IRT Support', 'URL']])
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from input import get_user_query, clean_text

def recommend_assessments(csv_file_path, top_n=10):
    # Load the CSV file
    df = pd.read_csv(csv_file_path)

    # Combine relevant fields into one text column for matching
    df['Combined_Text'] = (
        df['Assessment Name'].astype(str) + ' ' +
        df['Test Type'].astype(str) + ' ' +
        df['Duration'].astype(str) + ' ' +
        df['Remote Testing Support'].astype(str) + ' ' +
        df['Adaptive/IRT Support'].astype(str)
    )

    # Clean the combined text
    df['Cleaned_Text'] = df['Combined_Text'].apply(clean_text)

    # Get and clean the user input
    user_input = get_user_query()

    # Use TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(df['Cleaned_Text'].tolist() + [user_input])

    # Compute cosine similarity
    similarity_scores = cosine_similarity(vectors[-1], vectors[:-1]).flatten()

    # Add similarity scores to DataFrame
    df['Similarity'] = similarity_scores

    # Sort and get top N matches
    top_matches = df.sort_values(by='Similarity', ascending=False).head(top_n)

    return top_matches
