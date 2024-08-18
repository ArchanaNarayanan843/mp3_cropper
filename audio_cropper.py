import streamlit as st
from pydub import AudioSegment
from io import BytesIO

def convert_to_seconds(minutes, seconds):
    return minutes * 60 + seconds

def crop_audio(audio_data, start_time, end_time):
    # Convert the uploaded file into an AudioSegment
    audio = AudioSegment.from_mp3(BytesIO(audio_data))
    
    # Crop the audio
    cropped_audio = audio[start_time * 1000:end_time * 1000]
    
    # Save the cropped audio to a BytesIO object
    output = BytesIO()
    cropped_audio.export(output, format="mp3")
    return output.getvalue()

def main():
    st.title("MP3 Cropper")

    uploaded_file = st.file_uploader("Choose an MP3 file", type="mp3")

    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/mp3")

        st.write("Enter start time:")
        col1, col2 = st.columns(2)
        with col1:
            start_minutes = st.number_input("Minutes", min_value=0, value=0, key="start_minutes")
        with col2:
            start_seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0, key="start_seconds")

        # End time input
        st.write("Enter end time:")
        col3, col4 = st.columns(2)
        with col3:
            end_minutes = st.number_input("Minutes", min_value=0, value=0, key="end_minutes")
        with col4:
            end_seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0, key="end_seconds")


        if st.button("Crop and Save"):
            start_time = convert_to_seconds(start_minutes, start_seconds)
            end_time = convert_to_seconds(end_minutes, end_seconds)

            if end_time > start_time:
                cropped_audio = crop_audio(uploaded_file.read(), start_time, end_time)
                
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
