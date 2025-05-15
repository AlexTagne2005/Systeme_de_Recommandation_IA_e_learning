import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Charger les données depuis un fichier JSON
contents = pd.read_json("data/content.json")

# Vectorisation des descriptions de cours
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(contents["description"])

def get_recommendations(user_id=None, top_n=3):
    """
    Fonction de recommandation simple.
    Pour le moment, elle recommande les cours les plus proches du premier (index 0).
    """
    sim = cosine_similarity(X)
    indices = sim[0].argsort()[-top_n:][::-1]
    recs = contents.iloc[indices].to_dict(orient='records')
    return recs
