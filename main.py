import os, json
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
from agents.supervisor.supervisor import MasterAgent

load_dotenv()
supervisor = MasterAgent()
groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API"))
        
def transcribe_with_whisper(audio_path):
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = groq_client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        return f"[Voice message - transcription failed: {str(e)}]"

def process_message(message, audio, history):
    if not message and audio is None:
        return history
    
    if audio is not None:
        user_message = transcribe_with_whisper(audio)
    else:
        user_message = message
    
    history = history + [{"role": "user", "content": user_message}]
    bot_response = supervisor.invoke(user_message)
    commands = bot_response.split('&&')
    final_response = "**Executed the following tasks**\n---\n\n"
    for i, command in enumerate(commands):
        final_response += f"{i+1}. " + f" {command}\n\n"
        
    os.system(bot_response)
        
    
    history = history + [{"role": "assistant", "content": final_response}]
    print(bot_response)
    return history

# Create the Gradio interface
with gr.Blocks(css="""
    .container {max-width: 1000px; margin: auto;}
    .input-row {gap: 10px;}
    .message-box {border-radius: 20px !important; padding: 8px 15px !important;}
    .send-btn {background-color: #FF7F50 !important;}
""") as demo:
    with gr.Column(elem_classes=["container"]):
        # Chat history display
        chatbot = gr.Chatbot(
            value=[], 
            height=500, 
            type="messages",
            show_label=False
        )
        
        # Input row with text field and buttons
        with gr.Row(elem_classes=["input-row"]):
            # Text input
            text_input = gr.Textbox(
                placeholder="Type your message here...",
                show_label=False,
                container=True,
                elem_classes=["message-box"],
                lines=2,
                scale=8
            )
            
            # Audio input
            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="",
                scale=1
            )
            
            # Send button
            send_button = gr.Button(
                value="➤",
                elem_classes=["send-btn"],
                scale=1
            )
    
    # Handle sending messages
    send_button.click(
        process_message,
        inputs=[text_input, audio_input, chatbot],
        outputs=[chatbot]
    ).then(
        lambda: (None, None),
        None,
        [text_input, audio_input]
    )
    
    # Also handle pressing Enter to send
    text_input.submit(
        process_message,
        inputs=[text_input, audio_input, chatbot],
        outputs=chatbot
    ).then(
        lambda: (None, None),  # Clear inputs after sending
        None,
        [text_input, audio_input]
    )
demo.launch()