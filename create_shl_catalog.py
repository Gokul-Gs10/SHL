import pandas as pd
import random

assessment_types = ["Cognitive", "Personality", "Behavioral", "Situational", "Technical"]
difficulty_levels = ["Easy", "Medium", "Hard"]

# Rich set of job roles
job_roles = [
    "Software Engineer", "Data Scientist", "Product Manager", "Finance Analyst", "HR Manager",
    "Marketing Executive", "Business Analyst", "Sales Executive", "Retail Manager", "Team Lead",
    "Consultant", "Legal Associate", "Customer Service Rep", "Project Manager", "UX Designer",
    "QA Engineer", "Support Engineer", "Operations Manager", "DevOps Engineer", "IT Administrator",
    "Graphic Designer", "AI Engineer", "Blockchain Developer", "Cybersecurity Analyst", "System Architect",
    "Content Strategist", "Digital Marketer", "Logistics Coordinator", "Medical Officer", "Nurse Manager"
]

# Generate 500 synthetic SHL assessments
catalog = []
for i in range(500):
    assessment_id = 1000 + i
    assessment_type = random.choice(assessment_types)
    difficulty = random.choice(difficulty_levels)
    applicable_roles = random.sample(job_roles, k=random.randint(2, 6))
    assessment_name = f"{assessment_type} Assessment {i+1}"

    catalog.append([
        assessment_id,
        assessment_name,
        assessment_type,
        applicable_roles,
        difficulty
    ])

# Create DataFrame
df_large = pd.DataFrame(catalog, columns=["AssessmentID", "AssessmentName", "AssessmentType", "ApplicableRoles", "DifficultyLevel"])

# Save to CSV
df_large.to_csv("shl_product_catalog.csv", index=False)

print("✅ Large SHL product catalog (500 assessments) saved to 'shl_product_catalog.csv'")
df_large.head()
