import gradio as gr
import pandas as pd
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import re
import tempfile

# 📌 **Extract text from PDFs**
def extract_text_from_pdf(file):
    """Extracts text from a PDF file."""
    pdf = PdfReader(file)
    text = "\n".join([page.extract_text() or "" for page in pdf.pages]).strip()
    return text if text else "No readable text found."

# 📌 **Extract name from resume text**
def extract_name(resume_text):
    """Extracts the name of the candidate from the resume text using regex."""
    name_pattern = re.compile(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)")
    match = name_pattern.search(resume_text)
    return match.group(0) if match else "Unknown"

# 📌 **Rank Resumes based on Job Description**
def rank_resumes(job_description, resume_files):
    """Ranks resumes based on similarity to the job description using TF-IDF."""
    resumes = [extract_text_from_pdf(file) for file in resume_files]
    if not resumes:
        return pd.DataFrame(columns=["Name", "Resume", "Match Score (%)"])  # Return empty if no resumes
    
    all_docs = [job_description] + resumes

    vectorizer = TfidfVectorizer().fit_transform(all_docs)
    vectors = vectorizer.toarray()

    job_vector = vectors[0]
    resume_vectors = vectors[1:]

    scores = cosine_similarity([job_vector], resume_vectors).flatten()

    results_df = pd.DataFrame({
        "Name": [extract_name(resume) for resume in resumes],
        "Resume": [file.name for file in resume_files],
        "Match Score (%)": (scores * 100).round(2)
    }).sort_values(by="Match Score (%)", ascending=False)

    return results_df

# 📌 **Sentiment Analysis on Resume**
def analyze_sentiment(resume_text):
    """Analyzes the sentiment of the resume text."""
    blob = TextBlob(resume_text)
    sentiment_score = blob.sentiment.polarity
    sentiment = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
    return sentiment, sentiment_score

# 📌 **Suggest Suitable Job Role**
def suggest_job_role(resume_text):
    """Suggests a suitable job role based on the resume content."""
    keywords = {
        "Software Engineer": ["programming", "development", "software", "coding", "engineering"],
        "Data Scientist": ["data", "machine learning", "statistics", "analysis", "modeling"],
        "Project Manager": ["management", "leadership", "project", "planning", "coordination"],
        "UX/UI Designer": ["design", "user experience", "interface", "prototyping", "creativity"]
    }

    resume_keywords = resume_text.lower().split()
    scores = {role: sum(1 for word in resume_keywords if word in kw_list) for role, kw_list in keywords.items()}
    suggested_role = max(scores, key=scores.get)
    return suggested_role

# 📌 **Generate Downloadable CSV**
def download_results(job_description, resume_files):
    """Creates a temporary CSV file with ranking results, sentiment analysis, and suggested job roles."""
    ranking_results = rank_resumes(job_description, resume_files)
    sentiment_results = []
    job_role_results = []
    
    for file in resume_files:
        resume_text = extract_text_from_pdf(file)
        name = extract_name(resume_text)
        sentiment, sentiment_score = analyze_sentiment(resume_text)
        suggested_role = suggest_job_role(resume_text)
        
        sentiment_results.append({
            "Name": name,
            "Resume": file.name,
            "Sentiment": sentiment,
            "Sentiment Score": sentiment_score
        })
        
        job_role_results.append({
            "Name": name,
            "Resume": file.name,
            "Suggested Job Role": suggested_role
        })
    
    sentiment_df = pd.DataFrame(sentiment_results)
    job_role_df = pd.DataFrame(job_role_results)
    
    combined_df = pd.merge(ranking_results, sentiment_df, on=["Name", "Resume"], how="left")
    combined_df = pd.merge(combined_df, job_role_df, on=["Name", "Resume"], how="left")
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    combined_df.to_csv(temp_file.name, index=False)
    return temp_file.name

# 📌 **Gradio UI**
with gr.Blocks() as app:
    gr.Markdown("# 🚀 AI-Powered Resume Screening & Ranking System")

    with gr.Row():
        job_desc_input = gr.Textbox(
            lines=5, 
            placeholder="Enter job description here...", 
            label="📝 Job Description"
        )

        resume_upload = gr.Files(
            file_types=[".pdf"], 
            label="📤 Upload PDF Resumes"
        )

    rank_button = gr.Button("🔍 Rank Resumes")
    download_button = gr.Button("⬇️ Download Results (CSV)")

    results_output = gr.Dataframe(label="📊 Resume Rankings")

    sentiment_output = gr.Dataframe(label="📈 Sentiment Analysis")
    job_role_output = gr.Dataframe(label="💼 Suggested Job Role")

    def process_resumes(job_description, resume_files):
        ranking_results = rank_resumes(job_description, resume_files)
        sentiment_results = []
        job_role_results = []
        for file in resume_files:
            resume_text = extract_text_from_pdf(file)
            name = extract_name(resume_text)
            sentiment, sentiment_score = analyze_sentiment(resume_text)
            suggested_role = suggest_job_role(resume_text)
            sentiment_results.append({
                "Name": name,
                "Sentiment": sentiment,
                "Sentiment Score": sentiment_score,
                "Resume": file.name
            })
            job_role_results.append({
                "Name": name,
                "Suggested Job Role": suggested_role,
                "Resume": file.name
            })
        return ranking_results, pd.DataFrame(sentiment_results), pd.DataFrame(job_role_results)

    rank_button.click(
        process_resumes, 
        inputs=[job_desc_input, resume_upload], 
        outputs=[results_output, sentiment_output, job_role_output]
    )

    download_button.click(
        download_results, 
        inputs=[job_desc_input, resume_upload], 
        outputs=gr.File()
    )

# 📌 **Launch App**
app.launch(server_name="0.0.0.0", server_port=7860, share=True)
