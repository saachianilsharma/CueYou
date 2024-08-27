import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from PyQt6.QtCore import pyqtSignal, QThread, QObject, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication, QLabel
import cv2
import time
from prompt import PromptWidget
from PyQt6.QtGui import QImage, QPixmap
from deepface import DeepFace  
#from fer import FER


class VideoMonitorWorker(QObject):
    prompt_signal = pyqtSignal(str)
    frame_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.is_running = False
        self.last_emotion = None
        self.last_emotion_time = None
        self.last_prompt_time = None  # Track time of last prompt
        self.prompt_displayed = False
        #self.detector = FER() #FER

    def start(self):
        self.is_running = True
        self.monitor_video()

    def stop(self):
        self.is_running = False
    
    #Preprocessing frame 
    def preprocess_frame(self,frame):
        # Convert to grayscale (optional depending on model input requirement)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Histogram Equalization
        equalized_frame = cv2.equalizeHist(gray)

        # Denoising the image
        denoised_frame = cv2.fastNlMeansDenoising(equalized_frame, h=30)

        # Optionally, convert back to BGR if the model expects colored images
        final_frame = cv2.cvtColor(denoised_frame, cv2.COLOR_GRAY2BGR)

        return final_frame
    
    #t1 - basic
    """ def monitor_video(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            self.prompt_signal.emit("Unable to access the camera")
            print("Unable to access the camera")
            return

        last_emotion = None
        last_emotion_time = time.time()

        while self.is_running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                self.prompt_signal.emit("Failed to capture video frame")
                print("Failed to capture video frame")
                break

            try:
                # Analyze the face in the frame
                analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                dominant_emotion = analysis[0]['dominant_emotion']
                if dominant_emotion != last_emotion or time.time() - last_emotion_time > 5:
                    self.process_emotion(dominant_emotion)
                    last_emotion = dominant_emotion
                    last_emotion_time = time.time()

            except Exception as e:
                self.prompt_signal.emit(f"Error in processing video: {e}")
                print(f"Error in processing video: {e}")
                continue

            # Display the frame with a short delay
            cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows() """
    #t2 - monitor video with 5 second 
    def monitor_video(self):
        
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        frame_skip = 10
        frame_count = 0
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not cap.isOpened():
            self.prompt_signal.emit("Unable to access the camera")
            frame_count += 1
            if frame_count ==5:
                frame_count=0
            return

        while self.is_running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                self.prompt_signal.emit("Failed to capture video frame")
                break
            if frame_count % frame_skip == 0:

                try:
                    # Preprocess the frame 
                    preprocessed_frame = self.preprocess_frame(frame)
                    # Analyze the face in the frame using deepface
                    analysis = DeepFace.analyze(preprocessed_frame, actions=['emotion'], enforce_detection=False)
                    dominant_emotion = analysis[0]['dominant_emotion']
                    # Analyze the face in the frame using FER
                    """ analysis = self.detector.detect_emotions(preprocessed_frame)
                    if analysis:
                        dominant_emotion = self.detector.top_emotion(frame)  """
                
                    if self.last_emotion is None or dominant_emotion != self.last_emotion:
                        # If the emotion has changed, reset the timer
                        self.last_emotion = dominant_emotion
                        self.last_emotion_time = time.time()
                        self.prompt_displayed = False
                    else:
                        # If the emotion is constant, check the time
                        if time.time() - self.last_emotion_time > 5:
                            #self.process_emotion(dominant_emotion)
                            # Check if enough time has passed since the last prompt
                            if self.last_prompt_time is None or not self.prompt_displayed:
                                self.process_emotion(dominant_emotion)
                                self.prompt_displayed = True  # Mark the prompt as displayed
                                self.last_prompt_time = time.time()  # Update the last prompt time
                    # Convert frame to QImage to display in PyQt
                    """ rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_frame.shape
                    bytes_per_line = ch * w
                    qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                    self.frame_signal.emit(qt_image)
                    """
                except Exception as e:
                    self.prompt_signal.emit(f"Error in processing video: {e}")
                    continue

            # Display the frame with a short delay
            #cv2.waitKey(1) --- giving cv2.error cuz this function cannot be processed
            time.sleep(0.03)

        cap.release()
        #cv2.destroyAllWindows()


    def process_emotion(self, emotion):
        prompts = {
            "happy": "You look happy! That’s great",
            "sad": "You seem to be sad... All ok?",
            "angry": "I am sensing some anger",
            "fear": "You seem to be a little scared, it's all okay",
            "neutral": "Looking neutral, we are good",
            "disgust": "Looking a bit disgusted... let's neutralize that",
            "surprise": "You seem surprised!",
        }

        self.prompt_signal.emit(prompts.get(emotion, f"Detected emotion: {emotion}"))
        print(prompts.get(emotion, f"Detected emotion: {emotion}"))
        self.last_emotion = None  # Reset after processing

class VideoMonitorThread(QThread):
    def __init__(self):
        super().__init__()
        self.worker = VideoMonitorWorker()

    def run(self):
        self.worker.start()

    def stop(self):
        self.worker.stop()

class VideoMonitorPage(QWidget):
    def __init__(self,prompt_widget):
        super().__init__()
        self.initUI()
        self.notification = prompt_widget
        #self.notification = PromptWidget()
        self.timer = QTimer()  # Create a QTimer

    def initUI(self):
        layout = QVBoxLayout()

        """ 
        self.start_button = QPushButton('Start Video Monitoring', self)
        self.stop_button = QPushButton('Stop Video Monitoring', self)
        self.stop_button.setEnabled(False)

        self.start_button.clicked.connect(self.start_monitoring)
        self.stop_button.clicked.connect(self.stop_monitoring)

        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout) """
        self.prompt_label = QLabel('Video Monitor', self)
        self.start_button = QPushButton('Start Monitoring', self)
        self.stop_button = QPushButton('Stop Monitoring', self)
        self.stop_button.setEnabled(False)
        #self.video_label = QLabel(self)
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

        layout.addWidget(self.prompt_label)
        #layout.addWidget(self.video_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

    def display_prompt(self, message):
        print(message)
        self.notification.set_message(message)
        self.notification.show()
        self.timer.timeout.connect(self.notification.close)  # Connect the timer to close the notification
        self.timer.start(3000)  # Start the timer for 3 seconds

    def start(self):
        print("starting video monitoring")
        self.video_thread = VideoMonitorThread()
        self.video_thread.worker.prompt_signal.connect(self.display_prompt)
        #self.video_thread.worker.frame_signal.connect(self.update_frame)  # Connect to update the video feed
        self.video_thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop(self):
        print("stopping video monitoring")
        if self.video_thread.isRunning():
            self.video_thread.worker.stop()
            self.video_thread.quit()
            self.video_thread.wait()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    audio_monitor_page = VideoMonitorPage()
    audio_monitor_page.show()
    sys.exit(app.exec())
