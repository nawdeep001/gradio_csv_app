import gradio as gr
import pandas as pd
import ollama
import matplotlib.pyplot as plt
from PIL import Image
import io

def load_llm_model():
    def generate_response(prompt):
        response = ollama.generate(model="llama3:latest", prompt=prompt)
        return response.get("response", "Error")
    return generate_response

llm = load_llm_model()
data = None  

def upload_csv(file_path):
    global data
    try:
        data = pd.read_csv(file_path) 
        return f"File uploaded successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

def process_query(question):
    global data
    if data is None:
        return "Please upload a CSV file."
    
    csv_context = data.head(5).to_string()  
    prompt = f"Here is the dataset:\n{csv_context}\n\nAnswer the question based on this data: {question}"
    
    response = llm(prompt)
    return response

def plot_graph(x_column, y_column):
    global data
    if data is None:
        return "Please upload a CSV file.", None
    
    if x_column not in data.columns or y_column not in data.columns:
        return "Invalid column.", None
    
    plt.figure(figsize=(8,5))
    plt.scatter(data[x_column], data[y_column], color='blue', alpha=0.5)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{y_column} vs {x_column}")
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()  

    
    image = Image.open(img)

    return None, image  
with gr.Blocks() as demo:
    gr.Markdown("# CSV Question Answering & Visualization App")
    
    file_upload = gr.File(label="Upload CSV", type="filepath")  
    upload_button = gr.Button("Upload")
    upload_output = gr.Textbox()
    
    question_input = gr.Textbox(label="Ask a question about the data")
    query_button = gr.Button("Get Answer")
    answer_output = gr.Textbox()
    
    x_column = gr.Textbox(label="X-axis Column")
    y_column = gr.Textbox(label="Y-axis Column")
    graph_button = gr.Button("Plot Graph")
    graph_output = gr.Image(type="pil")  
    
    upload_button.click(upload_csv, inputs=file_upload, outputs=upload_output)
    query_button.click(process_query, inputs=question_input, outputs=answer_output)
    graph_button.click(plot_graph, inputs=[x_column, y_column], outputs=[upload_output, graph_output]) 


demo.launch()