import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from django.contrib.contenttypes.models import ContentType
from .models import Interaction, Recommendation, Course, Video, Article

def train_recommendation_model():
    # Extraire les interactions
    interactions = Interaction.objects.filter(rating__isnull=False).values(
        'user_id', 'content_type_id', 'content_id', 'rating'
    )
    if not interactions:
        return None, None

    # Créer une matrice utilisateur-contenu
    df = pd.DataFrame(list(interactions))
    df['content'] = df.apply(
        lambda x: f"{x['content_type_id']}_{x['content_id']}", axis=1
    )
    pivot_table = df.pivot_table(
        index='user_id', columns='content', values='rating', fill_value=0
    )

    # Appliquer SVD
    svd = TruncatedSVD(n_components=10, random_state=42)
    matrix = svd.fit_transform(pivot_table)
    corr_matrix = np.corrcoef(matrix)

    return svd, corr_matrix, pivot_table

def generate_recommendations_for_user(user_id):
    svd, corr_matrix, pivot_table = train_recommendation_model()
    if svd is None:
        return []

    try:
        user_index = pivot_table.index.get_loc(user_id)
    except KeyError:
        return []

    # Obtenir les scores de similarité pour l'utilisateur
    sim_scores = corr_matrix[user_index]
    user_ratings = pivot_table.loc[user_id]
    unrated_contents = user_ratings[user_ratings == 0].index

    # Prédire les scores pour les contenus non notés
    recommendations = []
    for content in unrated_contents:
        content_index = pivot_table.columns.get_loc(content)
        score = sim_scores.dot(pivot_table.iloc[:, content_index]) / sim_scores.sum()
        if score > 0:
            content_type_id, content_id = map(int, content.split('_'))
            recommendations.append((content_type_id, content_id, score))

    return recommendations

def save_recommendations(user_id):
    recommendations = generate_recommendations_for_user(user_id)
    if not recommendations:
        return

    # Supprimer les anciennes recommandations pour cet utilisateur
    Recommendation.objects.filter(user_id=user_id).delete()

    # Sauvegarder les nouvelles recommandations
    for content_type_id, content_id, score in recommendations:
        Recommendation.objects.create(
            user_id=user_id,
            content_type_id=content_type_id,
            content_id=content_id,
            score=score
        )