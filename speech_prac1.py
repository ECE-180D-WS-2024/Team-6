import time
import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True  # Enable dynamic energy threshold
time.sleep(2)
while True:
    with sr.Microphone() as source:
        print("Say something!")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Calibrate noise level

        audio = recognizer.listen(source)
        print("Got it! Now to recognize it...")

        try:
            results = recognizer.recognize_google(audio, show_all=True)
            #print("Result:")
            #print(results)

            if results and 'alternative' in results:
                speech_text = results['alternative'][0]['transcript'].lower()  # Lowercase for comparison
                print(f"You said: {speech_text}")

                if any(word in speech_text for word in {"start", "begin","play" "commence", "began", "get going"}):
                    print("Start is recognized!")

                if any(word in speech_text for word in {"stop", "stap", "finish", "end", "and", "ant", "aunt", "over", "pause", "done"}):
                    print("Stop is recognized!")

                if "exit" in speech_text or "exact" in speech_text:  # Simplified for clarity
                    print("Exiting...")
                    break

        except sr.UnknownValueError:
            print("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
