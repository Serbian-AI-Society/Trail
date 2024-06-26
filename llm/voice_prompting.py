from streamlit_mic_recorder import mic_recorder
import streamlit as st
import io
from openai import OpenAI
import pyaudio
import os
import time



def whisper_stt(openai_api_key=None, start_prompt="Glasovni unos 🎤", stop_prompt="Završi unos 🛑", just_once=False,
               use_container_width=False, language=None, callback=None, args=(), kwargs=None, key=None):
    if not 'openai_client' in st.session_state:
        st.session_state.openai_client = OpenAI(api_key=openai_api_key or os.getenv('OPENAI_API_KEY'))
    if not '_last_speech_to_text_transcript_id' in st.session_state:
        st.session_state._last_speech_to_text_transcript_id = 0
    if not '_last_speech_to_text_transcript' in st.session_state:
        st.session_state._last_speech_to_text_transcript = None
    if key and not key + '_output' in st.session_state:
        st.session_state[key + '_output'] = None
    audio = mic_recorder(start_prompt=start_prompt, stop_prompt=stop_prompt, just_once=just_once,
                         use_container_width=use_container_width,format="webm", key=key)
    new_output = False
    if audio is None:
        output = None
    else:
        id = audio['id']
        new_output = (id > st.session_state._last_speech_to_text_transcript_id)
        if new_output:
            output = None
            st.session_state._last_speech_to_text_transcript_id = id
            audio_bio = io.BytesIO(audio['bytes'])
            audio_bio.name = 'audio.webm'
            success = False
            err = 0
            while not success and err < 3:  # Retry up to 3 times in case of OpenAI server error.
                try:
                    transcript = st.session_state.openai_client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_bio,
                        # language=language
                    )
                except Exception as e:
                    print(str(e))  # log the exception in the terminal
                    err += 1
                else:
                    success = True
                    output = transcript.text
                    st.session_state._last_speech_to_text_transcript = output
        elif not just_once:
            output = st.session_state._last_speech_to_text_transcript
        else:
            output = None

    if key:
        st.session_state[key + '_output'] = output
    if new_output and callback:
        callback(*args, **(kwargs or {}))
    return output

def stream_to_speakers(stream=int, openai_api_key=None, model="tts-1", voice="alloy") -> None:  
     if not 'openai_client' in st.session_state:
        st.session_state.openai_client = OpenAI(api_key=openai_api_key or os.getenv('OPENAI_API_KEY'))
  
     player_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=24000, output=True) 
  
     start_time = time.time() 
  
     with st.session_state.openai_client.audio.speech.with_streaming_response.create( 
         model=model, 
         voice=voice, 
         response_format="pcm",  # similar to WAV, but without a header chunk at the start. 
         input=stream, 
     ) as response: 
         print(f"Time to first byte: {int((time.time() - start_time) * 1000)}ms") 
         for chunk in response.iter_bytes(chunk_size=1024): 
             player_stream.write(chunk) 
  
     print(f"Done in {int((time.time() - start_time) * 1000)}ms.") 