import re
import openai
import asyncio
import openpyxl
import numpy as np
import pandas as pd
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.utils import clean_text, remove_links

class DecisionEngine:
    def __init__(self, xlsx_filepath):
        self.df = pd.read_excel(xlsx_filepath)
        self.processed_titles = []  # Store processed titles for similarity comparison

    def apply_condition(self, statement, condition):
        tokens = re.findall(r'"[^"]+"|\'[^\']+\'|\w+|\(|\)|and|or|not', condition)
        statement = statement.lower()
        evaluated_expression = ""

        for token in tokens:
            if token.lower() in ["and", "or", "not", "(", ")"]:
                evaluated_expression += f" {token.lower()} "
            else:
                phrase = token.strip('"\'').lower()
                evaluated_expression += str(phrase in statement)

        try:
            return eval(evaluated_expression)
        except Exception as e:
            print(f"Error evaluating condition: {e}")
            return False

    def check_similarity(self, new_title, threshold=0.55):
        """Check if the new title is too similar to already processed titles."""
        new_title = remove_links(new_title)
        if not self.processed_titles:
            return False  # No previous titles to compare

        # Combine the new title with processed titles for vectorization
        vectorizer = TfidfVectorizer().fit_transform([new_title] + self.processed_titles)
        similarity_matrix = cosine_similarity(vectorizer[0:1], vectorizer[1:])
        max_similarity = np.max(similarity_matrix)
        return max_similarity >= threshold

    def process(self, titles, similarity_threshold=0.55):
        items = []

        for newest_title in titles:
            # Skip if the title is too similar to already processed ones
            if self.check_similarity(newest_title, threshold=similarity_threshold):
                print(f"Skipping similar title: {remove_links(newest_title)}")
                continue
            
            # Apply Boolean conditions
            for _, row in self.df.iterrows():
                condition, tag = row["Condition"], row["Tag"]
                if newest_title and self.apply_condition(newest_title, condition):
                    items.append((clean_text(newest_title), condition, tag))
                    break  # Exit the loop once a match is found
            
            # Add the title to processed list after handling it
            self.processed_titles.append(newest_title)

        return items
    



class SmartFilter:
    def __init__(self, OPEANAI_API_KEY, CONDITIONS_FILE):
        self.CONDITIONS_FILE = CONDITIONS_FILE
        openai.api_key = OPEANAI_API_KEY  # Set API key globally

    def load_conditions(self) -> Dict:
        conditions = {}
        workbook = openpyxl.load_workbook(self.CONDITIONS_FILE)
        sheet = workbook.active
        for row in sheet.iter_rows(min_row=2, values_only=True):
            category, description, examples, tag = row
            conditions[category] = {"description": description, "examples": examples, "tag": tag}
        return conditions

    async def check_conditions_openai(self, text: str, conditions: Dict) -> str:
        for _, condition in conditions.items():
            description_and_example = f"{condition['description']}\n{condition['examples']}"
            prompt = (
                f"The following news title: '{text}'\n\n"
                f"Does it match this description and example: '{description_and_example}'?\n\n"
                "Respond with 'Yes' or 'No'."
            )

            try:
                response = await openai.ChatCompletion.acreate(  # ✅ Use async method `acreate()`
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an assistant helping to classify news."},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=20
                )

                if "yes" in response["choices"][0]["message"]["content"].lower():
                    return condition["tag"]
            except openai.OpenAIError as e:
                print(f"OpenAI API error: {e}")
                return None

        return None

    async def process(self, titles: List[str]) -> List[str]:
        conditions = self.load_conditions()
        tasks = [self.check_conditions_openai(title, conditions) for title in titles]
        results = await asyncio.gather(*tasks)

        return [f"title: {title}\ntag: {tag}" for title, tag in zip(titles, results) if tag]

# Usage example:
# smart_filter = SmartFilter("your-api-key", "conditions.xlsx")
# asyncio.run(smart_filter.process(["Breaking news headline", "Another headline"]))
