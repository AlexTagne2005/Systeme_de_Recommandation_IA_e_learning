import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from .models import Interaction, Recommendation, Course, Video, Article
from django.contrib.contenttypes.models import ContentType

def train_recommendation_model():
    """
    Entraîne un modèle de recommandation basé sur SVD.
    Retourne le modèle SVD, la table pivot et ses colonnes.
    Si aucune interaction n'existe, retourne (None, None, None).
    """
    interactions = Interaction.objects.all()
    if not interactions.exists():
        return None, None, None

    # Créer une table pivot utilisateur-contenu
    data = []
    for interaction in interactions:
        content_id = f"{interaction.content_type.id}_{interaction.content_id}"
        data.append({
            'user_id': interaction.user_id,
            'content_id': content_id,
            'rating': interaction.rating
        })
    df = pd.DataFrame(data)
    pivot_table = df.pivot_table(index='user_id', columns='content_id', values='rating').fillna(0)

    # Ajuster n_components dynamiquement
    n_features = pivot_table.shape[1]
    n_components = min(10, n_features - 1) if n_features > 1 else 1
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    matrix = svd.fit_transform(pivot_table)
    
    return svd, pivot_table, pivot_table.columns

def generate_recommendations_for_user(user_id):
    """
    Génère des recommandations pour un utilisateur donné.
    Retourne une liste de tuples (content_type_id, content_id, score).
    """
    svd, pivot_table, content_ids = train_recommendation_model()
    
    # Si aucune interaction, recommander tous les contenus avec un score par défaut
    if svd is None or pivot_table is None or user_id not in pivot_table.index:
        recommendations = []
        for model in [Course, Video, Article]:
            content_type = ContentType.objects.get_for_model(model)
            for obj in model.objects.all():
                recommendations.append((content_type.id, obj.id, 0.1))  # Score minimal
        return recommendations

    # Obtenir les prédictions pour l'utilisateur
    user_index = list(pivot_table.index).index(user_id)
    user_ratings = pivot_table.iloc[user_index].values
    user_latent = svd.transform([user_ratings])[0]
    predicted_ratings = np.dot(user_latent, svd.components_)  # Utiliser toutes les composantes

    # Créer une liste de recommandations
    recommendations = []
    for idx, content_id in enumerate(content_ids):
        try:
            content_type_id, content_id = map(int, content_id.split('_'))
            score = float(predicted_ratings[idx])
            # Vérifier que le contenu n'est pas déjà noté
            if content_id in pivot_table.columns and score > 0 and pivot_table.loc[user_id, content_id] == 0:
                recommendations.append((content_type_id, content_id, score))
        except (KeyError, ValueError):
            continue

    # Ajouter des contenus non présents dans pivot_table
    existing_content_ids = {int(cid.split('_')[1]) for cid in content_ids}
    for model in [Course, Video, Article]:
        content_type = ContentType.objects.get_for_model(model)
        for obj in model.objects.all():
            if obj.id not in existing_content_ids:
                recommendations.append((content_type.id, obj.id, 0.1))  # Score minimal
    
    return recommendations

def save_recommendations(user_id):
    """
    Sauvegarde les recommandations pour un utilisateur dans la base de données.
    Supprime les recommandations existantes avant d'ajouter de nouvelles.
    """
    recommendations = generate_recommendations_for_user(user_id)
    Recommendation.objects.filter(user_id=user_id).delete()
    
    for content_type_id, content_id, score in recommendations:
        Recommendation.objects.create(
            user_id=user_id,
            content_type_id=content_type_id,
            content_id=content_id,
            score=score
        )