
import pandas as pd
import streamlit as st

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(
    page_title="Udemy Course Recommender",
    page_icon="🎓",
    layout="wide"
)


@st.cache_data
def load_data():
    df = pd.read_csv("courses.csv")

    text_columns = [
        "course_name",
        "category",
        "level",
        "skills",
        "instructor"
    ]

    for column in text_columns:
        df[column] = df[column].fillna("")

    return df


@st.cache_resource
def build_model(df):
    model_df = df.copy()

    model_df["combined_features"] = (
        model_df["course_name"] + " " +
        model_df["category"] + " " +
        model_df["level"] + " " +
        model_df["skills"] + " " +
        model_df["instructor"]
    ).str.lower()

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    course_matrix = vectorizer.fit_transform(
        model_df["combined_features"]
    )

    return model_df, vectorizer, course_matrix


def recommend_courses(
    query,
    preferred_level,
    max_duration,
    df,
    vectorizer,
    course_matrix,
    top_n=5
):
    profile_text = f"{query} {preferred_level}".lower()

    profile_vector = vectorizer.transform(
        [profile_text]
    )

    similarity_scores = cosine_similarity(
        profile_vector,
        course_matrix
    ).flatten()

    results = df.copy()

    results["match_score"] = similarity_scores

    results = results[
        results["duration_hours"] <= max_duration
    ].copy()

    results["level_bonus"] = (
        results["level"]
        .eq(preferred_level)
        .astype(float)
        * 0.08
    )

    results["rating_bonus"] = (
        results["rating"] / 5
    ) * 0.02

    results["final_score"] = (
        results["match_score"] +
        results["level_bonus"] +
        results["rating_bonus"]
    )

    results["match_percentage"] = (
        results["match_score"] * 100
    ).round(1)

    return (
        results
        .sort_values(
            ["final_score", "rating"],
            ascending=False
        )
        .head(top_n)
        .reset_index(drop=True)
    )


df = load_data()
df, vectorizer, course_matrix = build_model(df)


st.title("🎓 Engineering Course Recommendation System")

st.write(
    """
    Discover relevant Udemy courses based on your career goal,
    technical interests, preferred difficulty and available learning time.
    """
)


with st.sidebar:
    st.header("Student Profile")

    interests = st.text_area(
        "Skills, interests or career goal",
        (
            "I want to become a machine learning engineer "
            "and learn Python, statistics and artificial intelligence."
        ),
        height=130
    )

    preferred_level = st.selectbox(
        "Preferred course level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    max_duration = st.slider(
        "Maximum course duration",
        min_value=5,
        max_value=80,
        value=40,
        step=1
    )

    top_n = st.slider(
        "Number of recommendations",
        min_value=3,
        max_value=10,
        value=5
    )

    recommend_button = st.button(
        "Recommend Courses",
        type="primary",
        use_container_width=True
    )


if recommend_button:

    if not interests.strip():
        st.warning(
            "Please enter at least one skill, interest or career goal."
        )

    else:
        recommendations = recommend_courses(
            query=interests,
            preferred_level=preferred_level,
            max_duration=max_duration,
            df=df,
            vectorizer=vectorizer,
            course_matrix=course_matrix,
            top_n=top_n
        )

        st.subheader("Recommended Udemy Courses")

        if recommendations.empty:
            st.info(
                "No courses match the selected duration. "
                "Increase the maximum duration."
            )

        else:
            for rank, (_, row) in enumerate(
                recommendations.iterrows(),
                start=1
            ):
                with st.container(border=True):

                    content_column, metric_column = st.columns(
                        [4, 1]
                    )

                    with content_column:
                        st.markdown(
                            f"### {rank}. {row['course_name']}"
                        )

                        st.write(
                            f"**Instructor:** {row['instructor']}"
                        )

                        st.write(
                            f"**Category:** {row['category']}  |  "
                            f"**Level:** {row['level']}  |  "
                            f"**Duration:** {row['duration_hours']} hours"
                        )

                        st.write(
                            f"**Skills covered:** {row['skills']}"
                        )

                        st.link_button(
                            "Open Udemy Course ↗",
                            row["course_url"],
                            use_container_width=False
                        )

                    with metric_column:
                        st.metric(
                            "Match",
                            f"{row['match_percentage']:.1f}%"
                        )

                        st.metric(
                            "Rating",
                            f"{row['rating']}/5"
                        )

                        st.caption(
                            f"Platform: {row['platform']}"
                        )

            st.subheader("Recommendation Scores")

            chart_data = (
                recommendations[
                    ["course_name", "match_percentage"]
                ]
                .set_index("course_name")
                .sort_values("match_percentage")
            )

            st.bar_chart(
                chart_data,
                horizontal=True,
                x_label="Match percentage",
                y_label="Course"
            )


with st.expander("How does the recommendation algorithm work?"):
    st.markdown(
        """
        1. Course name, category, level, skills and instructor are combined.
        2. TF-IDF converts the course descriptions into numerical vectors.
        3. The student's interests are converted using the same vectorizer.
        4. Cosine similarity measures the similarity between the student
           profile and every course.
        5. Courses exceeding the selected duration are removed.
        6. A small bonus is added when the course level matches the
           student's preferred level.
        7. Courses are ranked using relevance and rating.
        """
    )


with st.expander("Machine-learning concepts used"):
    st.markdown(
        """
        - Content-based recommendation
        - Natural-language processing
        - Feature engineering
        - TF-IDF vectorization
        - Unigrams and bigrams
        - Cosine similarity
        - Filtering and ranking
        - Recommendation score
        """
    )


st.caption(
    "Portfolio project: Python • Pandas • Scikit-learn • "
    "TF-IDF • Cosine Similarity • Streamlit"
)
