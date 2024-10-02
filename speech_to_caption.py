import streamlit as st
import speech_recognition as sr


def transcribe_speech(api, language):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak now...")
        audio_text = r.listen(source)
        st.info("Transcribing...")

        try:
            if api == "Google":
                text = r.recognize_google(audio_text, language=language)
            elif api == "Sphinx":
                text = r.recognize_sphinx(audio_text, language=language)
            else:
                return "Selected API is not supported yet."
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Could not request results; check your network connection."
        except Exception as e:
            return f"An error occurred: {str(e)}"


def main():
    st.title("Speech Recognition App")
    st.write("Click on the microphone to start speaking:")

    # Select the speech recognition API
    api = st.selectbox("Select Speech Recognition API", ["Google", "Sphinx"])

    # Select the language
    language = st.selectbox("Select Language", ["en-US", "es-ES", "fr-FR", "de-DE", "zh-CN"])

    # Initialize session state for transcription and control
    if 'transcription' not in st.session_state:
        st.session_state.transcription = ""
    if 'is_paused' not in st.session_state:
        st.session_state.is_paused = False
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False

    # Start Recording button
    if st.button("Start Recording"):
        st.session_state.is_recording = True
        st.session_state.is_paused = False
        text = transcribe_speech(api, language)
        st.session_state.transcription += text + " "
        st.write("Transcription: ", st.session_state.transcription)

    # Pause Recording button
    if st.session_state.is_recording and not st.session_state.is_paused:
        if st.button("Pause Recording"):
            st.session_state.is_paused = True
            st.warning("Recording paused. Click resume to continue.")

    # Resume Recording button
    if st.session_state.is_recording and st.session_state.is_paused:
        if st.button("Resume Recording"):
            st.session_state.is_paused = False
            text = transcribe_speech(api, language)
            st.session_state.transcription += text + " "
            st.write("Transcription: ", st.session_state.transcription)

    # Input field for file name
    file_name = st.text_input("Enter the file name to save the transcription")

    # Save Transcription button
    if st.button("Save Transcription"):
        if st.session_state.transcription:
            with open(file_name, "w") as f:
                f.write(st.session_state.transcription)
            st.success(f"Transcription saved to {file_name}")
        else:
            st.warning("No transcription available to save.")


if __name__ == "__main__":
    main()
