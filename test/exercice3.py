import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open("data/content.json", "r") as f:
    contenus=json.load(f)

df=pd.DataFrame(contenus)

with open("data/interactions.json", "r") as f:
    interaction=json.load(f)

cours_id_prefere=interaction["course_id"]

cours_ref =df[df["id"]==cours_id_prefere]

if cours_ref.empty:
    print("Le cours choisi par l'utilistaeur n'existe pas dans la base.")
else:
    print(f"recommandation basée sur : {cours_ref.iloc[0]['title']}\n ")

    vectorizer=TfidfVectorizer()
    X=vectorizer.fit_transform(df["description"])

    idx_ref=df.index[df["id"]==cours_id_prefere][0]
    sim_scores=cosine_similarity(X[idx_ref],X).flatten()
    indices_similaires=cosine_similarity=sim_scores.argsort()[::-1][1:4]

    print("Cours recommandés :")
    for idx in indices_similaires:
        cours=df.iloc[idx]
        print(f"-> {cours['title']} : {cours['description']}")