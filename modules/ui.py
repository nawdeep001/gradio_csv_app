import gradio as gr
from modules.csv_handler import load_csv, csv_data
from modules.ai_agent import process_query
from modules.plot_generator import generate_plot

def create_ui():
    """Builds the Gradio UI layout."""
    with gr.Blocks() as app:
        gr.Markdown("# CSV Question Answering & Visualization")

        with gr.Row():
            csv_upload = gr.File(label="Upload CSV File", type="filepath")
            upload_btn = gr.Button("Upload")
            upload_output = gr.Textbox(label="Upload Status")

        with gr.Row():
            user_input = gr.Textbox(label="Ask a Question")
            query_btn = gr.Button("Get Answer")
            query_output = gr.Textbox(label="AI Answer")

        with gr.Row():
            x_column = gr.Textbox(label="X-Axis Column")
            y_column = gr.Textbox(label="Y-Axis Column")
            plot_btn = gr.Button("Plot Graph")
            plot_output = gr.Image(label="Graph")

        upload_btn.click(load_csv, inputs=[csv_upload], outputs=[upload_output])
        query_btn.click(lambda q: process_query(q, csv_data), inputs=[user_input], outputs=[query_output])
        plot_btn.click(lambda x, y: generate_plot(csv_data, x, y), inputs=[x_column, y_column], outputs=[plot_output])

    return app
