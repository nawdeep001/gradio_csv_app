import gradio as gr
import pandas as pd
import json
import ollama
from pydantic import BaseModel

class AIModel(BaseModel):
    def generate_response(self, query, data):
        system_prompt = f"""You are an expert advisor. Take a look at the input CSV file which is converted into a text file.
        After processing the dataset as stated above, the dataset is:
        {data.to_string()}
        Answer the following question based on that data: {query}
        Response must be an answer to the question and must be to the point."""
        
        response = ollama.chat(model="llama3:latest", messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ])
        return response['message']['content']

# Load dataset
data = pd.read_csv('Housing.csv')
ai_model = AIModel()

def query_model(query):
    return ai_model.generate_response(query, data)

# Gradio Interface
demo = gr.Interface(
    fn=query_model,
    inputs=gr.Textbox(placeholder="Enter your search query"),
    outputs=gr.Textbox(),
    title="AI Document Search",
    description="Ask questions about the dataset and get precise answers."
)

demo.launch()
