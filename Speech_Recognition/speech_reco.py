import speech_recognition as sr

# Create a recognizer instance
recognizer = sr.Recognizer()
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
            
            # Print the entire result just once
            print("result:")
            print(results)
            
            # Assuming we're taking the most likely result, which is the first one
            if results and 'alternative' in results:
                speech_text = results['alternative'][0]['transcript']
            
                print(f"You said: {speech_text}")
            
                # Check for the words 'fast', 'slow', and 'reverse' in the recognized speech
                if "start" in speech_text:
                    print("Start is recognized!")
                if "stop" in speech_text:
                    print("stop is recognized!")
                if "end" in speech_text:
                    print("end  is recognized!")
            
        except sr.UnknownValueError:
            # API was unable to understand the audio
            print("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            # API was unreachable or unresponsive
            print(f"Could not request results from Google Web Speech API; {e}")
