# src/ai_sql.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file before using them
load_dotenv()

from openai import OpenAI
import logging

# Now the API key is available
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_sql_from_natural_language(prompt, schema_description, model="gpt-3.5-turbo"):
    try:
        full_prompt = (
            f"You are an AI assistant tasked with converting user queries into SQL statements. "
            f"The database schema is: {schema_description}. "
            f"User Query: \"{prompt}\" "
            f"Generate a SQL query along with a short explanation."
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that converts natural language into SQL queries. Provide a SQL query along with a brief explanation."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=150,
            temperature=0.3
        )
        answer = response.choices[0].message.content.strip()
        print("Generated SQL and Explanation:")
        print(answer)
    except Exception as e:
        logging.error(f"Error generating SQL with AI: {e}")
        print(f"Error: {e}")
