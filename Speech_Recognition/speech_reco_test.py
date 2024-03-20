import time
import speech_recognition as sr
# Create a recognizer instance
recognizer = sr.Recognizer()
time.sleep(2)
while True:
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Say something!")
        
        # Adjusts the recognizer sensitivity to ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Listen for the first phrase and extract audio data
        audio = recognizer.listen(source)
        
        print("Got it! Now to recognize it...")
        
        try:
            # Recognize speech using Google Web Speech API
            results = recognizer.recognize_google(audio, show_all=True)
            
            #print("Result:")
            #print(results)
            
            # Check if any results were returned
            if results and 'alternative' in results:
                # Assuming the first result is the most likely
                speech_text = results['alternative'][0]['transcript']
                print(f"You said: {speech_text}")

                # Define the words to check for
                start_words = {"start", "begin", "commence", "began", "get going"}
                stop_words = {"stop", "stap", "finish", "end", "and", "ant", "aunt", "over", "pause", "done"}
                exit_word = {"exit", "exact", "break", "exeed"}
                # Check for 'start' related words
                if any(word in speech_text for word in start_words):
                    print("Start is recognized!")
                
                # Check for 'stop' related words
                if any(word in speech_text for word in stop_words):
                    print("Stop is recognized!")
    
                if any(word in speech_text for word in exit_word):
                    break


        except sr.UnknownValueError:
            # API was unable to understand the audio
            print("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            # API was unreachable or unresponsive
            print(f"Could not request results from Google Web Speech API; {e}")
