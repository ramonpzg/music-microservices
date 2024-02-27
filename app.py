import gradio as gr
from pedalboard.io import AudioFile
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from faker import Faker
import requests

from glob import glob
import os


def get_latest_file():
    files = glob("./music/*.mp3")
    latest_file = max(files, key=os.path.getctime)
    with AudioFile(latest_file, "r") as f:
        waveform = f.read(f.frames)
        sample_rate = f.samplerate
    return waveform, sample_rate


def make_waveform():
    waveform, sample_rate = get_latest_file()

    num_channels, num_frames = waveform.shape
    time_axis = np.arange(0, num_frames) / sample_rate
    with plt.xkcd():
        figure = Figure()
        axes = figure.subplots(num_channels, 1)
        if num_channels == 1:
            axes = [axes]
        for c in range(num_channels):
            axes[c].plot(time_axis, waveform[c], linewidth=1)
            axes[c].grid(True)
            if num_channels > 1:
                axes[c].set_ylabel(f"Channel {c+1}")
        figure.suptitle("Waveform")
    return figure


def make_spectogram():
    waveform, sample_rate = get_latest_file()

    num_channels, num_frames = waveform.shape
    with plt.xkcd():
        figure = Figure()
        axes = figure.subplots(num_channels, 1)
        if num_channels == 1:
            axes = [axes]
        for c in range(num_channels):
            axes[c].specgram(waveform[c], Fs=sample_rate)
            if num_channels > 1:
                axes[c].set_ylabel(f"Channel {c+1}")
        figure.suptitle("Spectrogram")
    return figure


def make_sound(text, guidance_scale, max_new_tokens, sample_rate):
    faker = Faker()
    # endpoint = "http://localhost:8080/v2/models/musicgen_model/infer"
    # input_request = {
    #     'inputs': [
    #         StringCodec.encode_input(name='text', payload=[text], use_bytes=False).dict(),
    #         NumpyCodec.encode_input(name='guidance_scale', payload=np.array([guidance_scale])).dict(),
    #         NumpyCodec.encode_input(name='max_new_tokens', payload=np.array([max_new_tokens])).dict()
    #     ]
    # }
    # result = requests.post(endpoint, json=input_request).json()
    # audio_array = np.array(result['outputs'][0]['data'])

    # file_name = os.path.join('./music', f"{faker.user_name()}.mp3")
    # with AudioFile(file_name, "w", samplerate=sample_rate, num_channels=1) as f:
    #     f.write(audio_array)
    # return sample_rate, audio_array
    pass


def audio_effect():
    # endpoint = "http://localhost:7050/v2/models/novice_dj/infer"
    # files =  glob("./music/*.mp3")
    # latest_file = max(files, key=os.path.getctime)
    # with AudioFile(latest_file, "r") as f:
    #     waveform = f.read(f.frames)
    #     sample_rate = f.samplerate
    # input_request = {
    #     'inputs': [
    #         NumpyCodec.encode_input(name='song', payload=waveform).dict(),
    #         NumpyCodec.encode_input(name='sample_rate', payload=np.array([sample_rate])).dict()
    #     ]
    # }
    # result = requests.post(endpoint, json=input_request).json()
    # audio_array = np.array(result['outputs'][0]['data'])
    # return gr.make_waveform((sample_rate, audio_array), bg_image="bg.png")
    pass


with gr.Blocks(theme="gstaff/xkcd") as demo:
    gr.Markdown("# Music Generation and Editing App")
    gr.Markdown("Second Demo of the Day!")

    with gr.Column():
        gr.Markdown("# Step 1 - Describe the music you want 😎 🎸 🎹 🎵")
        with gr.Row(equal_height=True):
            with gr.Column(min_width=900):
                text = gr.Textbox(
                    label="Name",
                    lines=3,
                    interactive=True,
                    info="Audio Prompt for the kind of song you want your model to produce.",
                    value="a fast bachata with violin sounds and few notes from a saxophone",
                    placeholder="Type your song description in here.",
                )
                make_music = gr.Button("Create Music")
            with gr.Column():
                tokens = gr.Slider(
                    label="Max Number of New Tokens",
                    value=200,
                    minimum=5,
                    maximum=1000,
                    step=1,
                )
                guidance = gr.Slider(
                    label="Guidance Scale", value=3, minimum=1, maximum=50, step=1
                )
                sample_rate = gr.Radio(
                    [16000, 32000, 44100], label="Sample Rate", value=32000
                )

        audio_output = gr.Audio()
        make_music.click(
            fn=make_sound,
            inputs=[text, guidance, tokens, sample_rate],
            outputs=audio_output,
            api_name="create_music",
        )

        gr.Markdown()
        gr.Markdown("# Step 2 - Visualize your creation 📈 👀 👌")
        with gr.Row():
            with gr.Column():
                create_plots = gr.Button("Visualize Waveform")
                plot1 = gr.Plot()
                create_plots.click(fn=make_waveform, outputs=plot1)
            with gr.Column():
                create_plots = gr.Button("Visualize Spectogram")
                plot2 = gr.Plot()
                create_plots.click(fn=make_spectogram, outputs=plot2)

        gr.Markdown()
        gr.Markdown("# Step 3 - Add Some Effects to it 📼 🎧 🎷 🎼")
        with gr.Column():
            update_music = gr.Button("Update your Music")
            output_video = gr.Video(label="Output", elem_id="output-video")
            update_music.click(audio_effect, outputs=[output_video])

        gr.Markdown()
        gr.Markdown("# Step 4 - Create a MIDI Representation! 🎛️ 🎶 🎼")
        gr.HTML(
            value="""<iframe src="https://basicpitch.spotify.com/" height="1000" width="100%"></iframe>"""
        )

demo.launch(server_port=os.getenv("PORT", 3000), server_name="0.0.0.0")
