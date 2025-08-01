import sys
import cv2
import random
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal, Qt
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
        "color": "#FF2400",
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
        "color": "#746E6E", 
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
    }
]

#centralized color detection HSV ranges and thresholds
COLOR_DEFINITIONS = [
    {"name": "Red", "lower": [np.array([0, 120, 70]), np.array([160, 120, 70])], "upper": [np.array([10, 255, 255]), np.array([179, 255, 255])], "threshold": 5000},
    {"name": "Yellow", "lower": [np.array([20, 100, 100])], "upper": [np.array([40, 255, 255])], "threshold": 5000},
    {"name": "Green", "lower": [np.array([40, 40, 40])], "upper": [np.array([80, 255, 255])], "threshold": 5000},
    {"name": "Blue", "lower": [np.array([100, 150, 0])], "upper": [np.array([140, 255, 255])], "threshold": 5000},
    {"name": "Purple", "lower": [np.array([125, 50, 50])], "upper": [np.array([155, 255, 255])], "threshold": 5000},
    {"name": "Orange", "lower": [np.array([5, 100, 100])], "upper": [np.array([25, 255, 255])], "threshold": 5000},
    {"name": "Black", "lower": [np.array([0, 0, 0])], "upper": [np.array([180, 255, 60])], "threshold": 100000},
    {"name": "White", "lower": [np.array([0, 0, 180])], "upper": [np.array([180, 45, 255])], "threshold": 15000},
    {"name": "Brown", "lower": [np.array([10, 100, 20])], "upper": [np.array([25, 255, 200])], "threshold": 5000},
    {"name": "Pink", "lower": [np.array([140, 80, 80])], "upper": [np.array([170, 255, 255])], "threshold": 5000},

]

# Video capture thread
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QPixmap, np.ndarray)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
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
            time.sleep(0.03)         # limiting frame rate to ~30 FPS

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
        title_label.setFont(QFont("Comic Sans MS", 28, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #00FFFF; background-color: transparent; padding: 10px; text-shadow: 3px 3px #000000;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(title_label)

        # Emotion name label
        self.emotion_label = QLabel("👇 SCAN AN OBJECT! 👇", self)
        self.emotion_label.setFont(QFont("Comic Sans MS", 36, QFont.Weight.Bold))
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
        self.reason_label = QLabel("Point the camera at a colorful object and hit the big red button to analyze its feelings.", self)
        self.reason_label.setFont(QFont("Comic Sans MS", 20))
        self.reason_label.setStyleSheet("color: #DDDDDD; background-color: transparent; border: none; padding: 15px;")
        self.reason_label.setWordWrap(True)
        self.reason_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(self.reason_label)

        funny_tagline = QLabel("Oh, humans think *they* invented feelings? My toaster is having an existential crisis about being buttered unevenly.", self)
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
        self.scan_button.setFont(QFont("Comic Sans MS", 28, QFont.Weight.Bold))
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
