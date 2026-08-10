import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import gradio as gr
from clients import *

geminiClient = getGeminiClient()
groqClient = getGroqClient()

def ask(client, model, prompt):
    r = client.chat.completions.create(model=model, messages=[{"role":"user", "content": prompt}])
    return r.choices[0].message.content

def battle(prompt):
    a = ask(geminiClient, getGeminiModel(), prompt)
    b = ask(groqClient, getGroqModel(), prompt)
    return a, b

def vote(label):
    return f"🗳️ Thanks! You voted: **{label}**" 

with gr.Blocks(title="LLM Arena") as demo:
    gr.Markdown("# 🥊 LLM Arena — one prompt, two models")
    prompt = gr.Textbox(label="Ask both models the same thing")
    go = gr.Button("⚔️ Battle!", variant="primary")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🤖 Model A")
            out_a = gr.Markdown()
            with gr.Row():
                up_a   = gr.Button("👍");  down_a = gr.Button("👎")
        with gr.Column():
            gr.Markdown("### 🤖 Model B")
            out_b = gr.Markdown()
            with gr.Row():
                up_b   = gr.Button("👍");  down_b = gr.Button("👎")

    verdict = gr.Markdown()

    go.click(battle, inputs=prompt, outputs=[out_a, out_b])
    up_a.click(lambda: vote("👍 Model A"), outputs=verdict)
    down_a.click(lambda: vote("👎 Model A"), outputs=verdict)
    up_b.click(lambda: vote("👍 Model B"), outputs=verdict)
    down_b.click(lambda: vote("👎 Model B"), outputs=verdict)

demo.launch()
