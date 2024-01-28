import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

file_path = 'main.csv'  
df = pd.read_csv(file_path)

user_message = "Waterfall"

df['Combined Features'] = df['Category'] + ' ' + df['Description']

vectorizer = TfidfVectorizer(stop_words='english')
user_message_vector = vectorizer.fit_transform([user_message])

places_vectors = vectorizer.transform(df['Combined Features'].fillna(''))

cosine_similarities = cosine_similarity(user_message_vector, places_vectors).flatten()

best_match_index = cosine_similarities.argmax()

best_match_details = df.iloc[best_match_index]

print("Best Matching Place:")
print(f"Place Name: {best_match_details['Place Name']}")
print(f"Category: {best_match_details['Category']}")
print(f"Description: {best_match_details['Description']}")
print(f"Location: {best_match_details['Location']}")
print(f"Entry Fee (BDT): {best_match_details['Entry Fee (BDT)']}")
print(f"Opening Hours: {best_match_details['Opening Hours']}")
