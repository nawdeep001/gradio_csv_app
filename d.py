import gradio as gr
import pandas as pd
import json
import ollama
import matplotlib.pyplot as plt
from io import BytesIO
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

def upload_file(file):
    global data
    data = pd.read_csv(file.name)
    return "File uploaded successfully! Now you can ask questions about the data."

def query_model(query):
    return ai_model.generate_response(query, data)

def plot_graph(x_column, y_column):
    """Generates a scatter plot for the selected columns."""
    global csv_data
    if csv_data is None:
        return "Please upload a CSV file first."

    if x_column not in csv_data.columns or y_column not in csv_data.columns:
        return f"Invalid column selection: {x_column}, {y_column}"

    plt.figure(figsize=(6, 4))
    plt.scatter(csv_data[x_column], csv_data[y_column], alpha=0.5)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{x_column} vs {y_column}")

    # Save and return the plot
    plt.savefig("plot.png")
    return "plot.png"

ai_model = AIModel()

demo = gr.Blocks()

with demo:
    gr.Markdown("## AI Document Search with CSV Upload and Graph Plotting")
    file_upload = gr.File(label="Upload CSV File", type="filepath")
    upload_button = gr.Button("Upload")
    upload_output = gr.Textbox()
    
    query_input = gr.Textbox(placeholder="Enter your search query")
    query_button = gr.Button("Ask")
    query_output = gr.Textbox()
    
    column_x = gr.Textbox(placeholder="Enter X-axis column name")
    column_y = gr.Textbox(placeholder="Enter Y-axis column name")
    plot_button = gr.Button("Generate Plot")
    plot_output_text = gr.Textbox()
    plot_output_image = gr.Image()
    
    upload_button.click(upload_file, inputs=[file_upload], outputs=[upload_output])
    query_button.click(query_model, inputs=[query_input], outputs=[query_output])
    plot_button.click(plot_graph, inputs=[column_x, column_y], outputs=[plot_output_text, plot_output_image])

demo.launch()
