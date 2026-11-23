import pandas as pd 


df = pd.read_csv("IMDB-Movie-Data.csv")

# print(df["Revenue (Millions)"].to_string())

# print(df["Genre"].value_counts().head(20))

df["Main_Genre"] = df["Genre"].str.split(",").str[0].str.strip()

df["Revenue (Millions)"] = df["Revenue (Millions)"].fillna(
    df.groupby("Main_Genre")["Revenue (Millions)"].transform("median")
)
df["Metascore"] = df["Metascore"].fillna(
    df.groupby("Main_Genre")["Metascore"].transform("median")
)

df["Revenue (Millions)"] = df["Revenue (Millions)"].fillna(df["Revenue (Millions)"].median())
df["Metascore"] = df["Metascore"].fillna(df["Metascore"].median())


# print(df.info())

# Hypothesis 1: Runtime (110-135 m vs <95m)

def categorize_runtime(minutes):
    if minutes < 95:
        return "1. Short (<95m)"
    elif 95 <= minutes < 110:
        return "2. Medium (95-109m)"
    elif 110 <= minutes <= 135:
        return "3. Target Sweet Spot (110-135m)"
    else: 
        return "4. Long (>135m)"

df["Runtime_Category"] = df["Runtime (Minutes)"].apply(categorize_runtime)

h1_results = df.groupby("Runtime_Category").agg(
    Movie_Count=("Title", "count"),
    Avg_Rating=("Rating", "mean"),
    Avg_Votes=("Votes", "mean"),
    Avg_Revenue=("Revenue (Millions)", "mean")
).round(2)

print("\n--- RESULTS: HYPOTHESIS 1 (RUNTIME IMPACT) ---")
print(h1_results)

# Hypothesis 2: Metascore vs. Votes on Revenue 

correlations = df[["Revenue (Millions)", "Votes", "Metascore", "Rating"]].corr()

print("\n--- RESULTS: HYPOTHESIS 2 (CORRELATION WITH REVENUE) ---")
print(correlations['Revenue (Millions)'].sort_values(ascending=False).round(3))

# MAIN RESEARCH QUESTION: Genre + Runtime Combinations

df_exploded = df.copy()
df_exploded["Genre"] = df_exploded["Genre"].str.split(",")
df_exploded = df_exploded.explode("Genre", ignore_index=True)
df_exploded["Genre"] = df_exploded["Genre"].str.strip()

main_question = df_exploded.groupby(["Genre", "Runtime_Category"]).agg({
    "Title": "count",
    "Revenue (Millions)": "mean",
    "Rating": "mean",
    "Votes": "mean"
}).rename(columns={
    "Title": "Movie_Supply",
    "Revenue (Millions)": "Avg_Revenue",
    "Rating": "Avg_Rating",
    "Votes": "Avg_Votes"
}).round(2)

opportunities = main_question[
    (main_question["Movie_Supply"] >= 5) & (main_question["Movie_Supply"] <= 60)
].sort_values(by=["Avg_Revenue", "Avg_Rating", "Avg_Votes"], ascending=False)

print("\n--- RESULTS: MAIN QUESTION (TOP 10 MARKET OPPORTUNITIES) ---")
print(opportunities.head(10))