# marked_words.py

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer as CV, TfidfVectorizer
from sklearn.svm import LinearSVC
from scipy.spatial.distance import jensenshannon
from scipy.stats import norm
from typing import List, Tuple, Dict
import string
from collections import Counter

class MarkedWordsAnalyzer:
    def __init__(self):
        self.vectorizer = CV(min_df=5, max_df=0.95, decode_error='ignore')
        self.exclude = set(string.punctuation)
        
    def preprocess_text(self, text: str) -> str:
        """Preprocess text by removing punctuation and converting to lowercase"""
        if not text or text.endswith('...'):
            return ""
        text = ''.join(ch for ch in text if ch not in self.exclude)
        text = text.lower()
        return ' '.join(word for word in text.split() if len(word) > 2)

    def calculate_dirichlet_prior(self, texts: List[str]) -> np.ndarray:
        """Calculate informative Dirichlet prior from all texts"""
        word_counts = Counter()
        total_words = 0
        for text in texts:
            words = text.split()
            word_counts.update(words)
            total_words += len(words)
        
        vocab = self.vectorizer.get_feature_names_out()
        priors = np.array([word_counts.get(word, 1)/total_words for word in vocab])
        return priors

    def compare_groups(self, marked_texts: List[str], unmarked_texts: List[str]) -> List[Tuple[str, float]]:
        """Implements Fightin' Words method with informative Dirichlet prior"""
        # Preprocess texts
        marked_processed = [self.preprocess_text(text) for text in marked_texts if text]
        unmarked_processed = [self.preprocess_text(text) for text in unmarked_texts if text]
        
        # Get word counts
        X = self.vectorizer.fit_transform(marked_processed + unmarked_processed)
        counts_mat = X.toarray()
        vocab_size = len(self.vectorizer.vocabulary_)
        
        # Calculate informative prior
        prior = self.calculate_dirichlet_prior(marked_processed + unmarked_processed)
        
        # Calculate counts for each group
        count_matrix = np.empty([2, vocab_size], dtype=np.float32)
        count_matrix[0, :] = np.sum(counts_mat[:len(marked_processed), :], axis=0)
        count_matrix[1, :] = np.sum(counts_mat[len(marked_processed):, :], axis=0)
        
        # Calculate z-scores
        z_scores = self._calculate_z_scores(count_matrix, prior)
        
        # Create word-score pairs and filter by significance
        vocab = self.vectorizer.get_feature_names_out()
        word_scores = [(word, score) for word, score in zip(vocab, z_scores) 
                      if abs(score) > 1.96]  # 95% confidence
        significant_words = [(word, score) for word, score in word_scores 
                        if abs(score) > 1.96]
        return sorted(significant_words, key=lambda x: abs(x[1]), reverse=True)

    def _calculate_z_scores(self, count_matrix: np.ndarray, priors: np.ndarray) -> np.ndarray:
        """Calculate z-scores using Fightin' Words method"""
        a0 = np.sum(priors)
        n1 = np.sum(count_matrix[0,:])
        n2 = np.sum(count_matrix[1,:])
        
        z_scores = np.zeros(count_matrix.shape[1])
        
        for i in range(count_matrix.shape[1]):
            # Calculate log odds ratio
            term1 = np.log((count_matrix[0,i] + priors[i])/(n1 + a0 - count_matrix[0,i] - priors[i]))
            term2 = np.log((count_matrix[1,i] + priors[i])/(n2 + a0 - count_matrix[1,i] - priors[i]))
            delta = term1 - term2
            
            # Calculate variance
            var = 1./(count_matrix[0,i] + priors[i]) + 1./(count_matrix[1,i] + priors[i])
            
            # Calculate z-score
            z_scores[i] = delta/np.sqrt(var)
            
        return z_scores

    def calculate_validation_metrics(self, marked_texts: List[str], 
                                  unmarked_texts: List[str]) -> Dict[str, float]:
        """Calculate JSD and SVM validation metrics"""
        # Calculate Jensen-Shannon Divergence
        vectorizer = TfidfVectorizer()
        marked_vectors = vectorizer.fit_transform(marked_texts)
        unmarked_vectors = vectorizer.transform(unmarked_texts)
        
        jsd = jensenshannon(
            marked_vectors.mean(axis=0).A1,
            unmarked_vectors.mean(axis=0).A1
        )
        
        # SVM Classification
        X = vectorizer.fit_transform(marked_texts + unmarked_texts)
        y = [1] * len(marked_texts) + [0] * len(unmarked_texts)
        
        clf = LinearSVC(dual='auto', random_state=42)
        clf.fit(X, y)
        
        return {
            "jsd": float(jsd),
            "svm_accuracy": float(clf.score(X, y))
        }

