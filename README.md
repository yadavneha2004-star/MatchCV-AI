# MatchCV-AI: Resume Ranking & Job Match Scoring

A web application built with Python and Flask that compares candidate resumes against a job description and ranks them using Natural Language Processing (TF-IDF and Cosine Similarity).

This project was developed as my final-year B.Tech capstone project.

**Live Demo:** [https://ai-job-app-ij1y.onrender.com](https://ai-job-app-ij1y.onrender.com)
*(The app is hosted on a free tier, so the first load may take a short while.)*

<!-- Add 1-2 screenshots here, for example:
![Home page](screenshots/home.png)
![Results page](screenshots/results.png)
-->

---

## Features

- **Match scoring:** Converts the resume and job description into TF-IDF vectors and computes their Cosine Similarity to produce a match score.
- **Skill detection:** Extracts technical skills and keywords from resume text using regular expressions.
- **Multiple file formats:** Reads resumes in PDF (`.pdf`), Word (`.docx`) and plain text (`.txt`) formats.
- **Batch processing:** Upload several resumes at once and view them ranked against the same job description.
- **Web interface:** Simple HTML/CSS/JavaScript front end that communicates with the Flask backend.

---

## How It Works

1. The user pastes a job description and uploads one or more resumes.
2. Text is extracted from each file (`pdfplumber` for PDF, `python-docx` for DOCX).
3. The text is cleaned and converted into TF-IDF vectors using scikit-learn.
4. Cosine Similarity between each resume and the job description gives the match score.
5. Skills found in the resume are shown alongside the score, and resumes are ranked from highest to lowest.

---

## Tech Stack

| Area | Tools |
|------|-------|
| Backend | Python, Flask |
| NLP / ML | scikit-learn (TF-IDF, Cosine Similarity), Regex |
| Document parsing | pdfplumber, python-docx |
| Frontend | HTML5, CSS3, JavaScript (Fetch API) |
| Deployment | Render (live demo), Procfile / `vercel.json` included |

---

## Project Structure

```
MatchCV-AI/
├── templates/          # HTML templates (front end)
├── app.py              # Flask application and scoring logic
├── requirements.txt    # Python dependencies
├── Procfile            # Process definition for deployment
├── vercel.json         # Vercel configuration
├── LICENSE             # Apache-2.0 License
└── README.md
```

---

## Setup and Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/yadavneha2004-star/MatchCV-AI.git
cd MatchCV-AI
```

**2. Create a virtual environment (recommended)**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
python app.py
```

Then open the address shown in the terminal (usually `http://127.0.0.1:5000`) in your browser.

---

## Limitations

This project uses a classical, keyword-based approach, so it has known limits:

- **TF-IDF matches words, not meaning.** Two resumes describing the same skill with different wording (for example "ML engineer" and "machine learning developer") may score differently.
- **Regex-based skill detection** only finds skills that appear in its predefined patterns, so uncommon skills can be missed.
- **Scanned or image-based PDFs** cannot be read, since the app extracts text only (no OCR).
- **The score is a similarity measure, not a hiring decision.** It should support, not replace, human review.

---

## Evaluation

<!-- Fill this in after you test, or delete this whole section until then.
Example format:
I tested the system on N resumes and M job descriptions and compared the app's ranking with a manual ranking.
Result: ...
Do NOT add numbers that you have not actually measured. -->

*Evaluation results will be added after testing on a labelled set of resumes.*

---

## Future Work

- Replace or combine TF-IDF with sentence embeddings (for example `sentence-transformers`) to capture meaning, and compare the two approaches.
- Expand the skills dictionary and add skill-gap suggestions.
- Add OCR support for scanned resumes.
- Add automated tests.

---

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

---

## Author

**Neha Salla**
- GitHub: [@yadavneha2004-star](https://github.com/yadavneha2004-star)
- Email: yadav.neha2004@gmail.com
