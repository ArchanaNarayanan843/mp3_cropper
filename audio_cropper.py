import streamlit as st
from pydub import AudioSegment
from io import BytesIO
import traceback

def convert_to_min_sec(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def crop_audio(audio_data, start_time, end_time):
    try:
        audio = AudioSegment.from_mp3(BytesIO(audio_data))
        cropped_audio = audio[start_time * 1000:end_time * 1000]
        output = BytesIO()
        cropped_audio.export(output, format="mp3")
        return output.getvalue()
    except Exception as e:
        st.error(f"Error cropping audio: {e}")
        st.write(traceback.format_exc())

def main():
    st.title("MP3 Cropper")

    uploaded_file = st.file_uploader("Choose an MP3 file", type="mp3")

    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        st.audio(audio_bytes, format="audio/mp3")

        audio = AudioSegment.from_mp3(BytesIO(audio_bytes))
        duration = len(audio) // 1000  # duration in seconds

        st.write(f"Audio Duration: {convert_to_min_sec(duration)} (min:sec)")

        start_time, end_time = st.slider(
            "Select the time range to crop",
            0, duration, (0, duration),
            format=None
        )
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Start time: {convert_to_min_sec(start_time)}")
        with col2:
            st.write(f"End time: {convert_to_min_sec(end_time)}")

        if st.button("Crop and Save"):
            if end_time > start_time:
                cropped_audio = crop_audio(audio_bytes, start_time, end_time)
                if cropped_audio:
                    st.success("Audio cropped successfully!")
                    st.audio(cropped_audio, format="audio/mp3")

                    st.download_button(
                        label="Download cropped MP3",
                        data=cropped_audio,
                        file_name="cropped_audio.mp3",
                        mime="audio/mp3"
                    )
            else:
                st.error("End time must be greater than start time.")

if __name__ == "__main__":
    main()
