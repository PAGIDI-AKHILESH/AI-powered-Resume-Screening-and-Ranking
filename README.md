# AI-Powered Resume Screening & Ranking System

This project is an AI-powered system designed to screen and rank resumes based on a given job description. The system extracts text from PDF resumes, analyzes their content, ranks them based on similarity to the job description, performs sentiment analysis, suggests suitable job roles, and extracts candidate names.

## Features

- **Text Extraction:** Extracts text from PDF resumes.
- **Resume Ranking:** Ranks resumes based on similarity to the job description using TF-IDF and cosine similarity.
- **Sentiment Analysis:** Analyzes the sentiment of the resume text using TextBlob.
- **Job Role Suggestion:** Suggests suitable job roles based on resume content.
- **Name Extraction:** Extracts candidate names from resumes.
- **Downloadable Results:** Generates a downloadable CSV file with ranking results.

## Requirements

- Python 3.7 or higher
- Required Python packages (install using `pip install -r requirements.txt`):
  - gradio
  - pandas
  - PyPDF2
  - scikit-learn
  - textblob

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/resume_ranking.git
   cd resume_ranking
   ```

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download TextBlob corpora:**
   ```bash
   python -m textblob.download_corpora
   ```

## Usage

1. **Run the application:**
   ```bash
   python resume_ranking.py
   ```

2. **Open the provided URL in your web browser to access the Gradio interface.**

3. **Enter the job description and upload PDF resumes:**
   - Enter the job description in the provided textbox.
   - Upload one or more PDF resumes.

4. **Click the "Rank Resumes" button to rank the resumes and perform sentiment analysis and job role suggestions.**

5. **View the results:**
   - The ranked resumes will be displayed in a table along with names and match scores.
   - Sentiment analysis results and suggested job roles will be displayed in separate tables.

6. **Download the results as a CSV file:**
   - Click the "Download Results (CSV)" button to download the ranking results as a CSV file.

## Example

### Job Description

```markdown
# Job Title: Software Engineer

We are seeking a talented Software Engineer with a strong background in software development, excellent problem-solving skills, and a passion for technology.

## Responsibilities:
- Design, develop, and maintain high-quality software applications.
- Collaborate with cross-functional teams to define, design, and ship new features.
- Write clean, maintainable, and efficient code.
- Perform code reviews and provide constructive feedback to team members.
- Troubleshoot, debug, and optimize code for performance and scalability.
- Stay up-to-date with the latest industry trends and technologies.

## Requirements:
- Bachelor’s degree in Computer Science, Engineering, or a related field.
- 3+ years of experience in software development.
- Proficiency in one or more programming languages such as Python, Java, C++, or JavaScript.
- Experience with web development frameworks and technologies (e.g., React, Angular, Django).
- Strong understanding of data structures, algorithms, and software design principles.
- Experience with version control systems (e.g., Git).
- Excellent communication and teamwork skills.
- Ability to work independently and as part of a team.

## Preferred Qualifications:
- Master’s degree in Computer Science or a related field.
- Experience with cloud platforms (e.g., AWS, Azure, Google Cloud).
- Knowledge of containerization and orchestration tools (e.g., Docker, Kubernetes).
- Familiarity with continuous integration and continuous deployment (CI/CD) pipelines.
- Experience with database systems (e.g., SQL, NoSQL).
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Gradio](https://gradio.app/) for the web interface.
- [TextBlob](https://textblob.readthedocs.io/en/dev/) for sentiment analysis.
- [PyPDF2](https://pypi.org/project/PyPDF2/) for PDF text extraction.
- [scikit-learn](https://scikit-learn.org/) for similarity ranking.

---

*Created on: 2025-03-24*
