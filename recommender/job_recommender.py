# recommender/job_recommender.py
import math
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from difflib import SequenceMatcher

@dataclass
class JobRecommenderConfig:
    text_fields = ("title", "skills", "description")
    ngram_range = (1, 2)
    max_features = 10000
    stop_words = "english"

class JobRecommender:
    def __init__(self, config=None):
        self.cfg = config or JobRecommenderConfig()
        self.vectorizer = None
        self.job_matrix = None
        self.jobs = None

    def fit(self, jobs_df):
        self.jobs = jobs_df.copy()
        combined = self.jobs.apply(lambda x: " ".join([str(x[c]) for c in self.cfg.text_fields]), axis=1)
        self.vectorizer = TfidfVectorizer(ngram_range=self.cfg.ngram_range, max_features=self.cfg.max_features, stop_words=self.cfg.stop_words)
        self.job_matrix = self.vectorizer.fit_transform(combined)
        return self

    def build_user_profile(self, *, resume_text=None, skills=None, target_title=None):
        text_parts = []
        if target_title: text_parts.append(target_title)
        if skills: text_parts.append(" ".join(skills))
        if resume_text: text_parts.append(resume_text)
        user_text = " ".join(text_parts)
        return self.vectorizer.transform([user_text])

    def recommend(self, *, user_vector, k=10, user_location=None, desired_salary_min=None, desired_salary_max=None):
        sims = cosine_similarity(user_vector, self.job_matrix).flatten()
        self.jobs["similarity"] = sims
        self.jobs["score"] = sims
        recs = self.jobs.sort_values("score", ascending=False).head(k)
        return recs
