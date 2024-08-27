import speech_recognition as sr
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, QObject
from collections import deque
import threading
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from prompt import PromptWidget
import re

#first code - hanging and speech not captured
"""
class AudioMonitorThread(QThread):
    prompt_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.active = False
        self.last_speech_time = None
        self.pause_timer = None

    def run(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.active:
                audio = self.recognizer.listen(source)
                if not self.active:
                    break
                try:
                    text = self.recognizer.recognize_google(audio)
                    self.analyze_speech(text)
                    self.last_speech_time = time.time()
                    self.reset_pause_timer()
                except sr.UnknownValueError:
                    self.prompt_signal.emit("Could not understand audio")
                except sr.RequestError:
                    self.prompt_signal.emit("Error with the recognition service")
                self.check_pause()

    def start_monitoring(self):
        self.active = True
        self.start()

    def stop_monitoring(self):
        self.active = False

    def analyze_speech(self, text):
        words = text.split()
        num_words = len(words)
        duration = 60  # Assuming 60 seconds interval for analysis
        words_per_minute = num_words / (duration / 60)
        filler_words = re.findall(r'\b(um|uh|like|so|you know|er)\b', text, re.IGNORECASE)
        num_filler_words = len(filler_words)
        mood = self.detect_mood(text)  # Dummy function for mood detection

        if words_per_minute > 160:
            self.prompt_signal.emit("Slow down, you are speaking too fast")
        elif words_per_minute < 100:
            self.prompt_signal.emit("Speed up, you are speaking too slow")
        else:
            self.prompt_signal.emit("Good pacing! Keep it up")

        if num_filler_words > 15:
            self.prompt_signal.emit("Kindly refrain from using filler words")

        if mood:
            self.prompt_signal.emit(mood)

    def detect_mood(self, text):
        # Dummy mood detection logic
        mood_conditions = {
            'anger': r'\bangry\b',
            'sadness': r'\bsad\b',
            'fear': r'\bfear\b',
            'happiness': r'\bhappy\b',
            'neutral': r'\bneutral\b'
        }
        for mood, pattern in mood_conditions.items():
            if re.search(pattern, text, re.IGNORECASE):
                return f"I am sensing {mood} in your tone"
        return None

    def reset_pause_timer(self):
        if self.pause_timer:
            self.pause_timer.stop()
        self.pause_timer = QTimer()
        self.pause_timer.timeout.connect(self.on_pause_detected)
        self.pause_timer.start(15000)  # 15 seconds

    def check_pause(self):
        if self.last_speech_time and time.time() - self.last_speech_time > 10:
            self.prompt_signal.emit("I see you have paused")

    def on_pause_detected(self):
        self.prompt_signal.emit("I see you have paused")
        self.pause_timer.stop()

class AudioMonitorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.prompt_label = QLabel('Audio Monitor', self)
        self.start_button = QPushButton('Start Monitoring', self)
        self.stop_button = QPushButton('Stop Monitoring', self)
        self.stop_button.setEnabled(False)

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

        layout.addWidget(self.prompt_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

    def start(self):
        self.thread = AudioMonitorThread()
        self.thread.prompt_signal.connect(self.update_prompt)
        self.thread.start_monitoring()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop(self):
        self.thread.stop_monitoring()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_prompt(self, message):
        prompt = PromptWidget(message)
        prompt.show()
"""
#second code - hanging and speech captured sparsely
"""
class AudioMonitorThread(QObject, threading.Thread):
    prompt_signal = pyqtSignal(str)

    def __init__(self, display_prompt):
        super().__init__()
        threading.Thread.__init__(self)
        self.display_prompt = display_prompt
        self.recognizer = sr.Recognizer()
        self.is_running = False
        self.analyzer = SentimentIntensityAnalyzer()

    def run(self):
        self.is_running = True
        silence_threshold = 15  # seconds
        silence_start = time.time()

        while self.is_running:
            print("self.is_running")
            with sr.Microphone() as source:
                print("mic on")
                try:
                    audio = self.recognizer.listen(source, timeout=1)
                    speech_text = self.recognizer.recognize_google(audio)
                    print(speech_text)
                    # Reset silence timer as we have detected speech
                    silence_start = time.time()
                    self.analyze_speech(speech_text)
                except sr.WaitTimeoutError:
                    # Check if silence duration exceeds threshold
                    if time.time() - silence_start > silence_threshold:
                        self.display_prompt("Microphone is silent for too long, halting monitoring")
                        while time.time() - silence_start > silence_threshold:
                            time.sleep(1)
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    self.display_prompt(f"Could not request results; {e}")
                    continue

    def stop(self):
        self.is_running = False

    def analyze_speech(self, speech_text):
        words = speech_text.split()
        words_per_minute = len(words) * 60 / 1  # Assuming 1 minute of speech for simplicity

        if words_per_minute > 160:
            self.display_prompt("Slow down, you are speaking too fast")
        elif words_per_minute < 100:
            self.display_prompt("Speed up, you are speaking too slow")
        else:
            self.display_prompt("Good pacing! Keep it up")

        filler_words = ["um", "uh", "like", "you know"]
        filler_count = sum(1 for word in words if word in filler_words)

        if filler_count > 15:
            self.display_prompt("Kindly refrain from using filler words")

        # Tone Analysis using VADER
        sentiment_scores = self.analyzer.polarity_scores(speech_text)
        if sentiment_scores['compound'] >= 0.05:
            self.display_prompt("You sound happy! Keep it up!")
        elif sentiment_scores['compound'] <= -0.05:
            self.display_prompt("I am sensing sadness or anger in your tone")
        else:
            self.display_prompt("You are maintaining a neutral tone")

class AudioMonitorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.start_button = QPushButton('Start Monitoring', self)
        self.stop_button = QPushButton('Stop Monitoring', self)
        self.stop_button.setEnabled(False)

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

    def display_prompt(self, message):
        prompt = PromptWidget(message)
        prompt.show()

    def start(self):
        self.audio_thread = AudioMonitorThread(self.display_prompt)
        self.audio_thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop(self):
        self.audio_thread.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
"""
#third code - speech captured but hanging
"""
class AudioMonitorWorker(QObject):
    prompt_signal = pyqtSignal(str)

    def __init__(self, display_prompt):
        super().__init__()
        self.display_prompt = display_prompt
        self.recognizer = sr.Recognizer()
        self.is_running = False
        self.analyzer = SentimentIntensityAnalyzer()

    def start(self):
        self.is_running = True
        self.monitor_audio()

    def stop(self):
        self.is_running = False

    def monitor_audio(self):
        silence_threshold = 15  # seconds
        silence_start = time.time()

        while self.is_running:
            with sr.Microphone() as source:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                    self.process_audio(audio)
                    #speech_text = self.recognizer.recognize_google(audio)
                    #print(speech_text)
                    # Reset silence timer as we have detected speech
                    silence_start = time.time()
                    #self.analyze_speech(speech_text)
                except sr.WaitTimeoutError:
                    # Check if silence duration exceeds threshold
                    if time.time() - silence_start > silence_threshold:
                        self.display_prompt("Microphone is silent for too long, halting monitoring")
                        while time.time() - silence_start > silence_threshold:
                            time.sleep(1)
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    self.display_prompt(f"Could not request results; {e}")
                    continue

    def process_audio(self, audio):
        try:
            speech_text = self.recognizer.recognize_google(audio)
            self.analyze_speech(speech_text)
        except sr.UnknownValueError:
            self.prompt_signal.emit("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            self.prompt_signal.emit(f"Could not request results from Google Speech Recognition service; {e}")

    def analyze_speech(self, speech_text):
        words = speech_text.split()
        words_per_minute = len(words) * 60 / 1  # Assuming 1 minute of speech for simplicity

        if words_per_minute > 160:
            self.display_prompt("Slow down, you are speaking too fast")
        elif words_per_minute < 100:
            self.display_prompt("Speed up, you are speaking too slow")
        else:
            self.display_prompt("Good pacing! Keep it up")

        filler_words = ["um", "uh", "like", "you know"]
        filler_count = sum(1 for word in words if word in filler_words)

        if filler_count > 15:
            self.display_prompt("Kindly refrain from using filler words")

        # Tone Analysis using VADER
        sentiment_scores = self.analyzer.polarity_scores(speech_text)
        if sentiment_scores['compound'] >= 0.05:
            self.display_prompt("You sound happy! Keep it up!")
        elif sentiment_scores['compound'] <= -0.05:
            self.display_prompt("I am sensing sadness or anger in your tone")
        else:
            self.display_prompt("You are maintaining a neutral tone")

class AudioMonitorThread(QThread):
    def __init__(self, display_prompt):
        super().__init__()
        self.worker = AudioMonitorWorker(display_prompt)
        self.worker.moveToThread(self) #added due to hanging issue

    def run(self):
        self.worker.start()

    def stop(self):
        self.worker.stop()

class AudioMonitorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.start_button = QPushButton('Start Monitoring', self)
        self.stop_button = QPushButton('Stop Monitoring', self)
        self.stop_button.setEnabled(False)

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

    def display_prompt(self, message):
        notification = PromptWidget(message)
        notification.show()

    def start(self):
        self.audio_thread = AudioMonitorThread(self.display_prompt)
        self.audio_thread.worker.prompt_signal.connect(self.display_prompt)
        self.audio_thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop(self):
        self.audio_thread.stop()
        self.audio_thread.quit()
        self.audio_thread.wait()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
"""
#fourth code - speech captured, not hanging, needs improvement on filler words logic and historical score tracking
class AudioMonitorWorker(QObject):
    prompt_signal = pyqtSignal(str)
    total_filler_count = 0
    filler_time_ctr = 0
    #historical_score = [0]
    last_sentiment_category = None

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.is_running = False
        self.analyzer = SentimentIntensityAnalyzer()

    def start(self):
        self.is_running = True
        self.monitor_audio()

    def stop(self):
        self.is_running = False

    def monitor_audio(self):
        silence_threshold = 15  # seconds
        silence_start = time.time()

        while self.is_running:
            with sr.Microphone() as source:
                try:
                    audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                    self.process_audio(audio)
                    self.__class__.filler_time_ctr+=1
                    print("filler time counter = ",self.__class__.filler_time_ctr)
                    silence_start = time.time()
                except sr.WaitTimeoutError:
                    
                    """ self.recognizer.adjust_for_ambient_noise(source)
                    print("waiting and listening")
                    continue """
                    if time.time() - silence_start > silence_threshold:
                        self.prompt_signal.emit("Microphone is silent for too long, halting monitoring")
                        while time.time() - silence_start > silence_threshold:
                            time.sleep(1)
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    self.prompt_signal.emit(f"Could not request results; {e}")
                    continue

    def process_audio(self, audio):
        try:
            speech_text = self.recognizer.recognize_google(audio)
            print("speech_text -",speech_text)
            self.analyze_speech(speech_text)
        except sr.UnknownValueError:
            self.prompt_signal.emit("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            self.prompt_signal.emit(f"Could not request results from Google Speech Recognition service; {e}")

    def analyze_speech(self, speech_text):
        words = speech_text.split()
        words_per_minute = len(words) * 6  # Assuming 1 minute of speech for simplicity
        if self.__class__.filler_time_ctr==7:
            if words_per_minute > 160:
                self.prompt_signal.emit("Slow down, you are speaking too fast")
            elif words_per_minute < 100:
                self.prompt_signal.emit("Speed up, you are speaking too slow")
            else:
                self.prompt_signal.emit("Good pacing! Keep it up")
            self.__class__.filler_time_ctr=0

        filler_words = ["um", "uh", "like", "you know","so yeah" ,"like yeah"]
        filler_count = sum(1 for word in words if word in filler_words)
        self.__class__.total_filler_count += filler_count
        print("total filler word count = ",self.__class__.total_filler_count)
        if self.__class__.filler_time_ctr==6:
            if self.__class__.total_filler_count > 15:
                self.prompt_signal.emit("Kindly refrain from using filler words")
            #self.__class__.filler_time_ctr=0
            self.__class__.total_filler_count=0


        """ sentiment_scores = self.analyzer.polarity_scores(speech_text)
        self.__class__.historical_score.append(sentiment_scores['compound'])
        print("sentiment_scores -",sentiment_scores)
        previous_score=self.__class__.historical_score[self.__class__.historical_score.index(sentiment_scores['compound'])]
        if sentiment_scores['compound'] >= 0.05:
            if previous_score >= 0.05:
                pass
            else:
                self.prompt_signal.emit("You sound happy! Keep it up!")
        elif sentiment_scores['compound'] <= -0.05:
            if previous_score <= -0.05:
                pass
            else:
                self.prompt_signal.emit("I am sensing sadness or anger in your tone")
        else:
            if previous_score <= 0.05 and previous_score >= -0.05:
                pass
            else:
                self.prompt_signal.emit("You are maintaining a neutral tone") """
        
        sentiment_scores = self.analyzer.polarity_scores(speech_text)
        current_score = sentiment_scores['compound']
        """ self.__class__.historical_score.append(current_score) """

        # Determine current sentiment category
        if current_score >= 0.05:
            current_sentiment_category = "positive"
        elif current_score <= -0.05:
            current_sentiment_category = "negative"
        else:
            current_sentiment_category = "neutral"

        # Emit only if the sentiment category has changed
        if current_sentiment_category != self.__class__.last_sentiment_category:
            if current_sentiment_category == "positive":
                self.prompt_signal.emit("You sound happy! Keep it up!")
            elif current_sentiment_category == "negative":
                self.prompt_signal.emit("I am sensing sadness or anger in your tone")
            else:
                self.prompt_signal.emit("You are maintaining a neutral tone")

            # Update the last sentiment category after emitting
            self.__class__.last_sentiment_category = current_sentiment_category

class AudioMonitorThread(QThread):
    def __init__(self, worker):
        super().__init__()
        self.worker = worker
        self.worker.moveToThread(self)

    def run(self):
        self.worker.start()

    def stop(self):
        self.worker.stop()

class AudioMonitorPage(QWidget):
    def __init__(self,prompt_widget):
        super().__init__()
        self.initUI()
        self.notification = prompt_widget
        #self.notification = PromptWidget()
        self.timer = QTimer()  # Create a QTimer

    def initUI(self):
        layout = QVBoxLayout()

        self.prompt_label = QLabel('Audio Monitor', self)
        self.start_button = QPushButton('Start Monitoring', self)
        self.stop_button = QPushButton('Stop Monitoring', self)
        self.stop_button.setEnabled(False)

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

        layout.addWidget(self.prompt_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

    def display_prompt(self, message):
        #self.prompt_label.setText(message)
        print(message)
        self.notification.set_message(message)
        self.notification.show()
        self.timer.timeout.connect(self.notification.close)  # Connect the timer to close the notification
        self.timer.start(3000)  # Start the timer for 3 seconds

    def start(self):
        print("start audio monitoring")
        self.worker = AudioMonitorWorker()
        self.thread = AudioMonitorThread(self.worker)
        self.worker.prompt_signal.connect(self.display_prompt)
        self.thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop(self):
        print("stop audio monitoring")
        self.thread.stop()
        self.thread.quit()
        self.thread.wait()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    audio_monitor_page = AudioMonitorPage()
    audio_monitor_page.show()
    sys.exit(app.exec())
