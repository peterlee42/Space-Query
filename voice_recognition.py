import speech_recognition as sr

# from this library, we are using Google Speech Recognition engine
# this requires pyaudio to be installed: pip3 install pyaudio

# variable for checking if the program did't cath the voice
correct = True
r = sr.Recognizer()

while correct:
    with sr.Microphone() as source:
        # listen for 1 second to calibrate the energy threshold for ambient noise levels
        r.adjust_for_ambient_noise(source)
        print('Ask your question:')
        # read the audio data from the default microphone, will record for 10 seconds
        # audio_data = r.record(source, duration=10)
        print("Listening...")
        audio_data = r.listen(source)
        # convert speech to text
        text = r.recognize_google(audio_data)

    try:
        print("You said: " + text)
        is_correct = input('Is this correct? (y/n): ')
        if is_correct == 'y':
            correct = False
        else:
            continue
    except sr.UnknownValueError:
        print("Sorry, I didn't get that")
        
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))