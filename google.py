import streamlit as st
import pandas as pd
from easyscrape_googlesuggest import getsuggestions as ES

# Function to get Google suggestions
def get_suggestions(query, categories):
    results = []
    for category in categories:
        full_query = category.replace("{query}", query)
        suggestions = ES.query(full_query)
        for suggestion in suggestions:
            if query.lower() in suggestion.lower():
                results.append((category, suggestion))
    return results

# Function to categorize results
def categorize_suggestions(results, taxonomy):
    categorized_results = {key: [] for key in taxonomy.keys()}
    for category, suggestion in results:
        for key, patterns in taxonomy.items():
            if any(category.startswith(pattern) for pattern in patterns):
                if suggestion not in categorized_results[key]:
                    categorized_results[key].append(suggestion)
    return categorized_results

# Function to save results to CSV
def save_to_csv(categorized_results, filename):
    all_results = []
    for suggestions in categorized_results.values():
        all_results.extend(suggestions)
    # Remove duplicates
    all_results = list(set(all_results))
    df = pd.DataFrame(all_results, columns=["Suggestion"])
    df.to_csv(filename, index=False)
    return filename

# Taxonomy definition
taxonomy = {
    "Questions": ["Will", "Why", "Which", "When", "What", "How", "Can", "Are", "Does"],
    "Prepositions": ["To", "Without", "With", "For", "Near", "In", "At", "On", "Of"],
    "Comparison": ["Vs", "Or", "Like", "And", "Alternative"],
    "Complaints": ["Issue", "Problem", "Complaints", "Not working", "Refund policy", "Discount", "Reviews"],
    "Alphabet": [chr(i) for i in range(ord('a'), ord('z') + 1)]
}

# Streamlit app
st.title("Google Suggest Scraper")

# Introduction and Usage Instructions
st.header("Introduction")
st.write("""
This app helps businesses understand what people are searching for related to their brand on Google. By analyzing Google Suggest data, you can gain insights into common questions, competitor comparisons, complaints, and more. This information can be invaluable for improving your marketing strategy and addressing customer concerns.

### How to Use the App
1. Enter your brand or query in the input box.
2. Click the 'Scrape Google Suggestions' button.
3. View the categorized results and download them as a CSV file.
""")

# User input for the query
query = st.text_input("Enter the query", placeholder="Type your query here")

# Scraping data
if st.button("Scrape Google Suggestions"):
    # Define the categories
    questions = [
        "Will {query}", "Why {query}", "Which {query}", "When {query}",
        "What {query}", "How {query}", "Can {query}", "Are {query}", "Does {query}"
    ]

    prepositions = [
        "To {query}", "Without {query}", "With {query}", "On {query}",
        "For {query}", "In {query}", "Near {query}", "Of {query}", "At {query}"
    ]

    comparison = [
        "Vs {query}", "Or {query}", "Like {query}", "And {query}", "Alternative {query}"
    ]

    complaints = [
        "Issue {query}", "Problem {query}", "Complaints {query}",
        "Not working {query}", "Refund policy {query}", "Discount {query}", "Reviews {query}"
    ]

    alphabet = [f"{query} {chr(i)}" for i in range(ord('a'), ord('z') + 1)]
    
    results = []
    results.extend(get_suggestions(query, questions))
    results.extend(get_suggestions(query, prepositions))
    results.extend(get_suggestions(query, comparison))
    results.extend(get_suggestions(query, complaints))
    results.extend(get_suggestions(query, alphabet))
    
    categorized_results = categorize_suggestions(results, taxonomy)
    
    st.write("Scraping and categorization completed. Here are some results:")

    # Display categorized results
    st.subheader("Questions:")
    questions_suggestions = categorized_results.get("Questions", [])
    if questions_suggestions:
        st.write(questions_suggestions)
    else:
        st.write("No data found")

    st.subheader("Prepositions:")
    prepositions_suggestions = categorized_results.get("Prepositions", [])
    if prepositions_suggestions:
        st.write(prepositions_suggestions)
    else:
        st.write("No data found")

    st.subheader("Competitors:")
    competitors_suggestions = categorized_results.get("Competitors", [])
    if competitors_suggestions:
        st.write(competitors_suggestions)
    else:
        st.write("No data found")

    st.subheader("Complaints:")
    complaints_suggestions = categorized_results.get("Complaints", [])
    if complaints_suggestions:
        st.write(complaints_suggestions)
    else:
        st.write("No data found")

    st.subheader("Alphabetical order:")
    alphabet_suggestions = categorized_results.get("Alphabet", [])
    if alphabet_suggestions:
        st.write(alphabet_suggestions)
    else:
        st.write("No data found")

    # Save to CSV
    filename = save_to_csv(categorized_results, "google_suggestions_categorized.csv")
    st.success(f"Data saved to {filename}")
    
    # Provide download button
    with open(filename, "rb") as file:
        st.download_button(label="Download CSV", data=file, file_name=filename, mime="text/csv")
