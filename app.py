import ui

# Import demo for Gradio's reload mechanism to find it
demo = ui.demo

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)