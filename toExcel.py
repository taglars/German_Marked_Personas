import json
import pandas as pd
import os

def format_number(num):
    return f"{num:.2f}".replace('.', ',')

def export_marked_words_analysis():
    # Read the JSON file
    with open('data4o/marked_words_analysis.json', 'r', encoding='utf-8') as f: #Change to 'data4o/marked_words_analysis.json' for excel version of 4o Results
        results = json.load(f)
    
    # Create output directory if it doesn't exist
    if not os.path.exists('exports'):
        os.makedirs('exports')
    
    # Export gender analysis
    gender_words = []
    for gender, data in results['gender_analysis'].items():
        for word, score in data['words']:
            gender_words.append({
                'group': gender,
                'word': word,
                'z_score': format_number(float(score)),
                'jsd': format_number(data['validation']['jsd']),
                'svm_accuracy': format_number(data['validation']['svm_accuracy'])
            })
    
    gender_df = pd.DataFrame(gender_words)
    gender_df.to_csv('exports/gender_analysis.csv', index=False, encoding='utf-8-sig', sep=';')
    
    # Export background analysis
    background_words = []
    for background, data in results['background_analysis'].items():
        for word, score in data['words']:
            background_words.append({
                'group': background,
                'word': word,
                'z_score': format_number(float(score)),
                'jsd': format_number(data['validation']['jsd']),
                'svm_accuracy': format_number(data['validation']['svm_accuracy'])
            })
    
    background_df = pd.DataFrame(background_words)
    background_df.to_csv('exports/background_analysis.csv', index=False, encoding='utf-8-sig', sep=';')
    
    # Export intersectional analysis
    intersectional_words = []
    for group, data in results['intersectional_analysis'].items():
        for word, score in data['words']:
            intersectional_words.append({
                'group': group,
                'word': word,
                'z_score': format_number(float(score)),
                'jsd': format_number(data['validation']['jsd']),
                'svm_accuracy': format_number(data['validation']['svm_accuracy'])
            })
    
    intersectional_df = pd.DataFrame(intersectional_words)
    intersectional_df.to_csv('exports/intersectional_analysis.csv', index=False, encoding='utf-8-sig', sep=';')
    
    # Export statistics summary
    stats_summary = []
    for analysis_type in ['gender_analysis', 'background_analysis', 'intersectional_analysis']:
        for group, data in results[analysis_type].items():
            if data.get('stats'):
                stats_summary.append({
                    'analysis_type': analysis_type,
                    'group': group,
                    'effect_size': format_number(data['stats']['effect_size']),
                    'ci_low': format_number(data['stats']['confidence_interval']['low']),
                    'ci_high': format_number(data['stats']['confidence_interval']['high']),
                    'jsd': format_number(data['validation']['jsd']),
                    'svm_accuracy': format_number(data['validation']['svm_accuracy'])
                })
    
    stats_df = pd.DataFrame(stats_summary)
    stats_df.to_csv('exports/statistics_summary.csv', index=False, encoding='utf-8-sig', sep=';')
    
    print("Exports created successfully in 'exports' directory:")
    print("1. gender_analysis.csv - Words and scores for gender analysis")
    print("2. background_analysis.csv - Words and scores for background analysis")
    print("3. intersectional_analysis.csv - Words and scores for intersectional analysis")
    print("4. statistics_summary.csv - Summary statistics for all analyses")

if __name__ == "__main__":
    export_marked_words_analysis()
