🎓 Udemy Course Recommender

A content-based recommendation system that suggests Udemy courses based on a learner's interests, career goals, preferred difficulty level, and available time — built with TF-IDF vectorization, cosine similarity, and deployed as an interactive Streamlit app.

Built as part of a Data Science training project under the guidance of Harshit Gaur.

🔍 Overview

Instead of relying on collaborative filtering (which needs user history), this project uses content-based filtering — it recommends courses purely by comparing the text content of each course (name, category, level, skills, instructor) against what a learner says they're interested in.

⚙️ How It Works
Feature combination — Course name, category, level, skills, and instructor are merged into a single text field per course.
TF-IDF vectorization — TfidfVectorizer (unigrams + bigrams) converts course text into numerical vectors. TF-IDF was chosen over simple Count Vectorization because it down-weights words that appear across most courses (like "python") and up-weights terms that actually distinguish one course from another — giving more meaningful similarity scores.
Cosine similarity — The learner's stated interests are vectorized using the same fitted vectorizer, then compared against every course using cosine similarity to produce a match score.
Filtering & ranking — Courses are filtered by maximum duration, given a bonus if their difficulty level matches the learner's preference, and a small rating-based bonus for tie-breaking.
Interactive app — Built with Streamlit: users enter their interests, pick a level and max duration, and get ranked recommendations with match %, ratings, and direct links to the course, plus a bar chart of match scores.
🛠️ Tech Stack
Python
Pandas — data handling
Scikit-learn — TfidfVectorizer, cosine_similarity
Streamlit — interactive web app

