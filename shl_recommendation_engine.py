import pandas as pd

# Load the catalog
df = pd.read_csv("shl_product_catalog.csv")

# Convert stringified lists back to real lists (if needed)
import ast
df['ApplicableRoles'] = df['ApplicableRoles'].apply(ast.literal_eval)

def recommend_assessments(job_role, top_n=5, preferred_difficulty=None, preferred_type=None):
    """
    Recommend SHL assessments for a given job role.

    Args:
    - job_role (str): The target job role.
    - top_n (int): Number of assessments to return.
    - preferred_difficulty (str, optional): Filter by difficulty level.
    - preferred_type (str, optional): Filter by assessment type.

    Returns:
    - pd.DataFrame: Top N recommended assessments.
    """
    filtered_df = df[df['ApplicableRoles'].apply(lambda roles: job_role in roles)]

    if preferred_difficulty:
        filtered_df = filtered_df[filtered_df['DifficultyLevel'] == preferred_difficulty]
    if preferred_type:
        filtered_df = filtered_df[filtered_df['AssessmentType'] == preferred_type]

    if filtered_df.empty:
        return f"No matching assessments found for '{job_role}' with given filters."

    return filtered_df.head(top_n)

# Example usage
if __name__ == "__main__":
    job_input = input("Enter a job role (e.g., 'Software Engineer'): ")
    recommendations = recommend_assessments(job_input, top_n=5)

    print("\n🔍 Top Recommendations:")
    print(recommendations[['AssessmentName', 'AssessmentType', 'DifficultyLevel']])
