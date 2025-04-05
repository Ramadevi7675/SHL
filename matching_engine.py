import pandas as pd

# List of all known/common skills SHL might assess
ALL_KNOWN_SKILLS = {
    "python", "sql", "javascript", "java", "react", "html", "css", "c++",
    "debugging", "data analysis", "machine learning", "data interpretation",
    "logical reasoning", "problem solving", "english", "vocabulary",
    "reading comprehension", "situational judgment", "behavior analysis"
}

# Extract skills from the JD text
def extract_skills_from_jd(jd_text):
    jd_text = jd_text.lower()
    matched_skills = set()

    for skill in ALL_KNOWN_SKILLS:
        if skill in jd_text:
            matched_skills.add(skill)

    return matched_skills

# Recommend assessments based on skills
def recommend_assessments(jd_text, csv_path='shl_sample_assessments.csv', top_n=5):
    # Load the CSV file
    df = pd.read_csv(csv_path)

    # Preprocess skills from the dataset
    df['Skills Measured Cleaned'] = df['Skills Measured'].fillna('').apply(
        lambda x: set(skill.strip().lower() for skill in x.split(','))
    )

    # Extract skills from JD
    jd_skills = extract_skills_from_jd(jd_text)

    # Score overlap between JD skills and assessment skills
    df['Skill_Match_Score'] = df['Skills Measured Cleaned'].apply(
        lambda x: len(jd_skills & x)
    )

    # Return top N matched assessments
    recommendations = df[df['Skill_Match_Score'] > 0] \
        .sort_values(by='Skill_Match_Score', ascending=False) \
        .head(top_n)

    return recommendations[[
        'Assessment Name', 'Test Type', 'Duration', 'Remote Testing Support',
        'Adaptive/IRT Support', 'Skills Measured', 'URL', 'Skill_Match_Score'
    ]]
