import gradio as gr
from website_summarizer import summarize

gr.Interface(
    fn=summarize,
    inputs=gr.Text(label="Website URL"),
    outputs=gr.Markdown(label="Summary"),
    title="🔎 AI website Summarizer"
).launch(share=True)