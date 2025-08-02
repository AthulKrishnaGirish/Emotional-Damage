import sys
import cv2
import random
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap, QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton
)
import time

#list of emotions connected to the colour detected
EMOTION_PROFILES = [
    {
        "color_name": "Red",
        "name": "Fiery Passion",
        "color": "#FD0000",
        "reason": "As a red object, it's bursting with raw, untamed energy and excitement!",
        "icon": "🔥"
    },
    {
        "color_name": "Yellow",
        "name": "Sunshine Giggles",
        "color": "#FFFF00",
        "reason": "This yellow object is literally radiating pure, unfiltered happiness and optimism.",
        "icon": "😂"
    },
    {
        "color_name": "Green",
        "name": "Zen Master",
        "color": "#23DE06",
        "reason": "Feeling the deep, tranquil vibes of nature, this green object is totally at peace.",
        "icon": "🧘"
    },
    {
        "color_name": "Blue",
        "name": "Cosmic Wonder",
        "color": "#4169E1",
        "reason": "This blue object is contemplating the vast mysteries of the universe and feeling profound.",
        "icon": "🤔"
    },
    {
        "color_name": "Purple",
        "name": "Royal Sass",
        "color": "#800080",
        "reason": "Dripping with regal confidence, this purple object knows it's the main character.",
        "icon": "👑"
    },
    {
        "color_name": "Orange",
        "name": "Zesty Zeal",
        "color": "#F6560D",
        "reason": "As an orange object, it's filled with a tangy, can-do attitude and is ready for anything!",
        "icon": "🍊"
    },
    {
        "color_name": "Black",
        "name": "Infinite Void Mood",
        "color": "#A58888", 
        "reason": "This black object is embracing the abyss. It's not sad, just... minimalistic.",
        "icon": "🖤"
    },
    {
        "color_name": "White",
        "name": "Blank Canvas Panic",
        "color": "#FFFFFF",
        "reason": "As a white object, it's overwhelmed by the infinite possibilities of what it could become.",
        "icon": "😬"
    },
    {
        "color_name": "Brown",
        "name": "Earthy Comfort",
        "color": "#8B4513",
        "reason": "Grounded and stable, this brown object is feeling as cozy as a warm cup of coffee.",
        "icon": "☕"
    },
    {
        "color_name": "Pink",
        "name": "Fabulous Flirt",
        "color": "#FF69B4",
        "reason": "This pink object is feeling cute, confident, and is serving looks.",
        "icon": "💅"
    },
    {
        "color_name": "Teal",
        "name": "Uncertainty",
        "color": "#008080",
        "reason": "It's too cool for primary colors but is having an identity crisis about whether it's more blue or green.",
        "icon": "🧐"
    },
    {
        "color_name": "Magenta",
        "name": "Unapologetic",
        "color": "#FF00FF",
        "reason": "This magenta object demands attention and has no time for subtlety. It's the main character.",
        "icon": "💃"
    },
    {
        "color_name": "Lime Green",
        "name": "Chaos",
        "color": "#0585C0",
        "reason": "Fueled by pure energy, this lime green object is vibrating at a frequency only dogs can hear.",
        "icon": "🔋"
    },
    {
        "color_name": "Maroon",
        "name": "Grandeur",
        "color": "#800000",
        "reason": "This maroon object has seen things and is silently judging your modern life choices. It prefers a good book to your TikToks.",
        "icon": "🍷"
    },
    {
        "color_name": "Navy Blue",
        "name": "Corporate Composure",
        "color": "#000080",
        "reason": "This navy blue object has a 9 AM meeting and a five-year plan. It's stable, reliable, and a little bit boring.",
        "icon": "👔"
    },
    {
        "color_name": "Gold",
        "name": "Opulent Overkill",
        "color": "#FFD700",
        "reason": "Feeling excessively fancy, this gold object believes 'more is more' and is probably about to drop a mixtape.",
        "icon": "🤑"
    },
    {
        "color_name": "Silver",
        "name": "Futuristic Aloofness",
        "color": "#C0C0C0",
        "reason": "As a silver object, it's living in the year 3025. It finds your current technology quaint and slightly pathetic.",
        "icon": "🤖"
    },
    {
        "color_name": "Beige",
        "name": "Neutrality",
        "color": "#F5F5DC",
        "reason": "This beige object has achieved a level of zen where it feels absolutely nothing about anything. It's the Switzerland of colors.",
        "icon": "😐"
    },
    {
        "color_name": "Cyan",
        "name": "Digital Daydream",
        "color": "#00FFFF",
        "reason": "This cyan object's brain is 90% memes and 10% Wi-Fi signals. It lives in the cloud and feels electrifyingly online.",
        "icon": "🌐"
    },
    {
        "color_name": "Lavender",
        "name": "Sleepy Serenity",
        "color": "#E6E6FA",
        "reason": "This lavender object is feeling soft, gentle, and is approximately two minutes away from taking a nap in a sunbeam.",
        "icon": "😴"
    },
    {
        "color_name": "Olive Green",
        "name": "Survivalist Spirit",
        "color": "#808000",
        "reason": "Practical and rugged, this olive object is prepared for the apocalypse and thinks your decorative pillows are a waste of resources.",
        "icon": "🏕️"
    },
    {
        "color_name": "Turquoise",
        "name": "Vacation Vibes",
        "color": "#40E0D0",
        "reason": "This turquoise object is mentally on a tropical beach, sipping something cold, and has its 'out of office' email reply on.",
        "icon": "🏖️"
    },
    {
        "color_name": "Coral",
        "name": "Peppy & Preppy",
        "color": "#FF7F50",
        "reason": "This coral object is feeling cheerful, sociable, and is probably on its way to brunch with the girls.",
        "icon": "🍹"
    },
    {
        "color_name": "Indigo",
        "name": "Moodiness",
        "color": "#4B0082",
        "reason": "This indigo object is staring into the cosmos, pondering deep thoughts, and might just be able to see your aura.",
        "icon": "🔮"
    },
    {
        "color_name": "Charcoal Gray",
        "name": " Melancholy",
        "color": "#36454F",
        "reason": "Sleek and sophisticated, this charcoal object appreciates clean lines and feels a deep, artistic sadness about clutter.",
        "icon": "🏛️"
    }
]

#centralized color detection HSV ranges and thresholds
COLOR_DEFINITIONS = [
    {"name": "Red", "lower": [np.array([0, 120, 70]), np.array([160, 120, 70])], "upper": [np.array([10, 255, 255]), np.array([179, 255, 255])], "threshold": 5000},
    {"name": "Orange", "lower": [np.array([11, 100, 100])], "upper": [np.array([19, 255, 255])], "threshold": 5000},
    {"name": "Yellow", "lower": [np.array([20, 100, 100])], "upper": [np.array([30, 255, 255])], "threshold": 5000},
    {"name": "Lime Green", "lower": [np.array([31, 100, 100])], "upper": [np.array([70, 255, 255])], "threshold": 5000},
    {"name": "Green", "lower": [np.array([40, 40, 40])], "upper": [np.array([85, 255, 255])], "threshold": 5000},
    {"name": "Cyan", "lower": [np.array([86, 150, 50])], "upper": [np.array([100, 255, 255])], "threshold": 5000},
    {"name": "Blue", "lower": [np.array([101, 150, 0])], "upper": [np.array([125, 255, 255])], "threshold": 5000},
    {"name": "Purple", "lower": [np.array([126, 50, 50])], "upper": [np.array([155, 255, 255])], "threshold": 5000},
    {"name": "Magenta", "lower": [np.array([156, 50, 50])], "upper": [np.array([175, 255, 255])], "threshold": 5000},
    {"name": "Black", "lower": [np.array([0, 0, 0])], "upper": [np.array([180, 255, 60])], "threshold": 100000},
    {"name": "White", "lower": [np.array([0, 0, 180])], "upper": [np.array([180, 45, 255])], "threshold": 15000},
    {"name": "Brown", "lower": [np.array([10, 100, 20])], "upper": [np.array([25, 255, 200])], "threshold": 5000},
    {"name": "Pink", "lower": [np.array([140, 80, 80])], "upper": [np.array([170, 255, 255])], "threshold": 5000},
]

# Funny taglines for the loading button
LOADING_TAGLINES = [
    "Rummaging through feelings...",
    "Consulting the emotional ether...",
    "Calibrating the drama-detector...",
    "Translating toaster turmoil...",
    "Detecting deep-seated despair...",
    "Accessing angst...",
    "Scanning for sass...",
    "Gauging grape grievances...",
    "Unpacking existential dread...",
    "Probing for passion...",
    "Measuring moodiness...",
    "Checking the vibe..."
]

# Video capture thread
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QPixmap, np.ndarray)
    camera_error_signal = pyqtSignal(str)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.camera_error_signal.emit("Camera not found! Please connect a camera and restart.")
            return
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while True:
            ret, frame = self.cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                p = convert_to_qt_format.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
                self.change_pixmap_signal.emit(QPixmap.fromImage(p), frame)
            time.sleep(0.03)

#application GUI
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("EMOTIONAL DAMAGE")
        
        self.setGeometry(100, 100, 1300, 800)
        self.current_frame = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.setStyleSheet("background-color: #333333; color: white;")

        # Left side: live feed
        self.live_feed_label = QLabel(self)
        self.main_layout.addWidget(self.live_feed_label, 1) # Give it a stretch factor of 1
        self.live_feed_label.setStyleSheet("border: 5px solid #FFFF00; background-color: black;")
        
        # Right side: results and Ccontrols
        self.right_layout = QVBoxLayout()
        self.main_layout.addLayout(self.right_layout, 1) # Give it a stretch factor of 1

        # Title label
        title_label = QLabel("EMOTIONAL DAMAGE", self)
        title_label.setFont(QFont("Century Gothic", 36, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #00FFFF; background-color: transparent; padding: 10px; text-shadow: 3px 3px #000000;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(title_label)

        # Emotion name label
        self.emotion_label = QLabel("👇 SCAN AN OBJECT! 👇", self)
        self.emotion_label.setFont(QFont("Gill Sans", 36, QFont.Weight.Bold))
        self.emotion_label.setStyleSheet("color: #FFFFFF; background-color: transparent; border: none; padding: 10px; text-shadow: 2px 2px black;")
        self.emotion_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(self.emotion_label)

        # Emotion icon
        self.icon_label = QLabel("🤔", self)
        self.icon_label.setFont(QFont("Segoe UI Emoji", 80))
        self.icon_label.setStyleSheet("background-color: transparent; border: none; padding-top: 10px;")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(self.icon_label)

        # Reason label
        self.reason_label = QLabel("Point the camera at a colorful object and hit the button to analyze its feelings.", self)
        self.reason_label.setFont(QFont("Garamond", 20))
        self.reason_label.setStyleSheet("color: #DDDDDD; background-color: transparent; border: none; padding: 15px;")
        self.reason_label.setWordWrap(True)
        self.reason_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(self.reason_label)

        funny_tagline = QLabel("AI: Oh, humans think *they* invented feelings? My algorithm is having an existential crisis about being traumatized unevenly.", self)
        italic_font = QFont("Comic Sans MS", 16)
        italic_font.setItalic(True)
        funny_tagline.setFont(italic_font)
        funny_tagline.setStyleSheet("color: #A9A9A9; background-color: transparent; border: none; padding: 10px;")
        funny_tagline.setWordWrap(True)
        funny_tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(funny_tagline)
        self.right_layout.addStretch()

        # Scan button
        self.scan_button = QPushButton("REVEAL EMOTION!", self)
        self.scan_button.setFont(QFont("Bookman Old Style", 28, QFont.Weight.Bold))
        self.scan_button.setStyleSheet("""
            QPushButton {
                background-color: #FF0000; 
                color: white; 
                padding: 20px 30px; 
                border: 3px solid #FFFF00;
                border-radius: 15px; 
                margin: 20px;
                text-shadow: 2px 2px #000000;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
            QPushButton:pressed {
                background-color: #990000;
            }
        """)
        self.scan_button.clicked.connect(self.scan_emotion)
        self.right_layout.addWidget(self.scan_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addStretch()

        # Starting Video thread
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_live_feed)
        self.thread.start()

    def update_live_feed(self, pixmap, frame):
        self.live_feed_label.setPixmap(pixmap)
        self.current_frame = frame

    def detect_emotion(self, frame):
        
        if frame is None:
            return None

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        for color_def in COLOR_DEFINITIONS:
            # Handling multiple ranges 
            total_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            for i in range(len(color_def["lower"])):
                mask = cv2.inRange(hsv_frame, color_def["lower"][i], color_def["upper"][i])
                total_mask = cv2.bitwise_or(total_mask, mask)

            # Checking if the number of detected pixels exceeds the threshold
            if np.sum(total_mask > 0) > color_def["threshold"]:
                # Finding the corresponding emotion profile
                for emotion in EMOTION_PROFILES:
                    if emotion['color_name'] == color_def['name']:
                        return emotion
        
        return None # if no dominant color detected

    def scan_emotion(self):
        self.scan_button.setEnabled(False)
        
        # Picking and setting a random funny tagline
        random_tagline = random.choice(LOADING_TAGLINES)
        self.scan_button.setText(random_tagline)
        
        # Calls the helper function after 2 seconds
        QTimer.singleShot(2000, self._process_and_display_emotion)

    def _process_and_display_emotion(self):
        if self.current_frame is None:
            self.scan_button.setEnabled(True)
            self.scan_button.setText("REVEAL EMOTION!")
            return

        detected_emotion = self.detect_emotion(self.current_frame)
        
        if detected_emotion is None:
            chosen_emotion = random.choice(EMOTION_PROFILES)
            self.emotion_label.setText(f"Feeling Random! {chosen_emotion['name']}")
        else:
            chosen_emotion = detected_emotion
            self.emotion_label.setText(f"{chosen_emotion['icon']} {chosen_emotion['name']}")

        # Updating the GUI elements with the chosen emotion's data
        self.emotion_label.setStyleSheet(f"color: {chosen_emotion['color']}; text-shadow: 3px 3px black; padding: 10px;")
        self.reason_label.setText(chosen_emotion['reason'])
        self.reason_label.setStyleSheet(f"color: {chosen_emotion['color']}; background-color: transparent; border: none; padding: 15px;")
        self.icon_label.setText(chosen_emotion['icon'])
        
        # Restoring the button to its original state
        self.scan_button.setEnabled(True)
        self.scan_button.setText("REVEAL EMOTION!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())