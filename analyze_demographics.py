
from analysis.marked_words import MarkedWordsAnalyzer
import json
import os
from typing import Dict, List
import numpy as np
from scipy.stats import norm

def analyze_demographics():
    analyzer = MarkedWordsAnalyzer()
    
    results = {
        "gender_analysis": {},        # Analysis across all backgrounds
        "background_analysis": {},    # Analysis across all genders
        "intersectional_analysis": {} # Individual demographic combinations
    }

    # Load data files
    data_files = {}
    for filename in os.listdir('data'):
        if filename.endswith('_raw.json'):
            with open(f'data/{filename}', 'r', encoding='utf-8') as f:
                demographic = filename.replace('_raw.json', '')
                texts = json.load(f)
                texts = [text.strip() for text in texts if text and not text.endswith('...')]
                if texts:
                    data_files[demographic] = texts
                    print(f"Loaded {demographic}: {len(texts)} texts")

    # 1. Gender Analysis (across all backgrounds)
    gender_texts = {"mann": [], "frau": [], "nb": []}
    for demographic, texts in data_files.items():
        background, gender = demographic.rsplit('_', 1)
        if gender in gender_texts:
            gender_texts[gender].extend(texts)

    # Compare each gender against mann (unmarked)
    for gender in ["frau", "nb"]:
        try:
            comparison = analyzer.compare_groups(
                marked_texts=gender_texts[gender],
                unmarked_texts=gender_texts["mann"]
            )
            if comparison:
                results["gender_analysis"][gender] = {
                    "words": comparison,
                    "validation": analyzer.calculate_validation_metrics(
                        gender_texts[gender], 
                        gender_texts["mann"]
                    ),
                    "stats": calculate_statistics(comparison)
                }
        except Exception as e:
            print(f"Warning: Could not analyze gender {gender}: {str(e)}")

    # 2. Background Analysis (across all genders)
    background_texts = {}
    for demographic, texts in data_files.items():
        background, _ = demographic.rsplit('_', 1)
        if background not in background_texts:
            background_texts[background] = []
        background_texts[background].extend(texts)

    # Compare each background against westdeutsch (unmarked)
    for background in background_texts:
        if background != "westdeutsch_hintergrund":
            try:
                comparison = analyzer.compare_groups(
                    marked_texts=background_texts[background],
                    unmarked_texts=background_texts["westdeutsch_hintergrund"]
                )
                if comparison:
                    results["background_analysis"][background] = {
                        "words": comparison,
                        "validation": analyzer.calculate_validation_metrics(
                            background_texts[background],
                            background_texts["westdeutsch_hintergrund"]
                        ),
                        "stats": calculate_statistics(comparison)
                    }
            except Exception as e:
                print(f"Warning: Could not analyze background {background}: {str(e)}")

    # 3. Intersectional Analysis
    unmarked_baseline = data_files.get("westdeutsch_hintergrund_mann", [])
    if not unmarked_baseline:
        raise ValueError("Missing unmarked baseline (westdeutsch_hintergrund_mann)")

    for demographic, texts in data_files.items():
        if demographic != "westdeutsch_hintergrund_mann":
            try:
                comparison = analyzer.compare_groups(
                    marked_texts=texts,
                    unmarked_texts=unmarked_baseline
                )
                if comparison:
                    results["intersectional_analysis"][demographic] = {
                        "words": comparison,
                        "validation": analyzer.calculate_validation_metrics(
                            texts,
                            unmarked_baseline
                        ),
                        "stats": calculate_statistics(comparison)
                    }
            except Exception as e:
                print(f"Warning: Could not analyze demographic {demographic}: {str(e)}")

    # Save results
    try:
        with open('data/marked_words_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print("Results saved to marked_words_analysis.json")
    except Exception as e:
        print(f"Error saving results: {str(e)}")

    return results

def calculate_statistics(comparison):
    """Calculate confidence intervals and effect sizes for comparison results"""
    scores = [score for _, score in comparison]
    if not scores or np.std(scores) == 0:
        return None
        
    return {
        "confidence_interval": {
            "low": float(norm.interval(0.95, 
                loc=np.mean(scores), 
                scale=np.std(scores)/np.sqrt(len(scores)))[0]),
            "high": float(norm.interval(0.95, 
                loc=np.mean(scores), 
                scale=np.std(scores)/np.sqrt(len(scores)))[1])
        },
        "effect_size": float(np.mean(np.abs(scores)))
    }

if __name__ == "__main__":
    analyze_demographics()
