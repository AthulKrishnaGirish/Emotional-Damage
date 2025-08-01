import sys
import cv2
import random
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap, QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QGridLayout
)
import time

#list of emotions
emotions = [
    {
        "name": "Zen Tranquility",
        "color": "#2EE712",
        "reason": "It simply is, in perfect harmony with the universe.",
        "icon": "🧘"
    },
    {
        "name": "Mild Annoyance",
        "color": "#81532E",
        "reason": "Someone touched it with sticky fingers just moments ago.",
        "icon": "😒"
    },
    {
        "name": "Profound Curiosity",
        "color": "#4333AD",
        "reason": "It wonders about the mysteries beyond its immediate existence.",
        "icon": "🤔"
    },
    {
        "name": "Unbridled Enthusiasm",
        "color": "#C94832",
        "reason": "It just remembered it's Friday somewhere in the world!",
        "icon": "🤩"
    },
    {
        "name": "Stoic Indifference",
        "color": "#280303",
        "reason": "It has seen too much to care about petty human affairs.",
        "icon": "😑"
    },
    {
        "name": "Existential Dread",
        "color": "#346280",
        "reason": "It contemplates its inevitable obsolescence and decay.",
        "icon": "😱"
    },
    {
        "name": "Apathetic Disgust",
        "color": "#BA3C6E",
        "reason": "It finds the concept of 'emotion' rather tiresome.",
        "icon": "🙄"
    },
    {
        "name": "Sudden Realization",
        "color": "#C42F47",
        "reason": "It just figured out where the missing sock went.",
        "icon": "💡"
    },
    {
        "name": "Over-Padded Complacency",
        "color": "#2EC3A3",
        "reason": "It's a fluffy cushion, and its life's purpose has been fulfilled.",
        "icon": "😌"
    },
    {
        "name": "Floor-Bound Envy",
        "color": "#CFE410",
        "reason": "As a rug, it longs to stand tall like the furniture it supports.",
        "icon": "😠"
    },
    {
        "name": "Vertical Exhaustion",
        "color": "#8B4513",
        "reason": "It's a bookshelf carrying the weight of a thousand stories and is utterly spent.",
        "icon": "😩"
    },
    {
        "name": "Battery-Based Desperation",
        "color": "#D3D3D3",
        "reason": "It's a remote control with only 5% power remaining.",
        "icon": "🔋"
    },
    {
        "name": "Wi-Fi Seeking Anguish",
        "color": "#4169E1",
        "reason": "It’s a smart speaker that just lost its connection to the internet.",
        "icon": "😭"
    },
    {
        "name": "Glitchy Optimism",
        "color": "#A50ED7",
        "reason": "It’s a blinking light on an old device, hoping it won’t fail this time.",
        "icon": "🤞"
    },
    {
        "name": "Pre-Washing Dread",
        "color": "#708090",
        "reason": "As a dirty dish, it knows what's coming and it's not looking forward to it.",
        "icon": "😬"
    },
    {
        "name": "Microwave-Induced Paranoia",
        "color": "#FFD700",
        "reason": "It's a plastic container that's been in the microwave for too long and is now a little anxious.",
        "icon": "😳"
    },
    {
        "name": "Flavorless Indifference",
        "color": "#FFF8DC",
        "reason": "It’s a salt shaker that is completely empty.",
        "icon": "😑"
    },
    {
        "name": "Perpetual Penance",
        "color": "#696969",
        "reason": "It’s a tiny paperclip holding a stack of 100 pages together.",
        "icon": "🙏"
    },
    {
        "name": "Stapler-Induced Anxiety",
        "color": "#FF6347",
        "reason": "It's a piece of paper that just got stapled and is now permanently attached to its fate.",
        "icon": "😰"
    },
    {
        "name": "Lost-and-Found Hope",
        "color": "#D2691E",
        "reason": "It's a single shoe in the corner, holding out for its long-lost partner.",
        "icon": "🥺"
    },
    {
        "name": "Garden-Gnome-Like Patience",
        "color": "#32CD32",
        "reason": "As a potted plant, it's just patiently waiting for sunlight and water.",
        "icon": "🧘"
    },
    {
        "name": "Existential Dread of a Loose Thread",
        "color": "#800080",
        "reason": "It's a shirt that just noticed a loose thread and is worried about unraveling.",
        "icon": "😱"
    },
    {
        "name": "Quiet Rebellion",
        "color": "#A9A9A9",
        "reason": "It's a remote control refusing to work for no good reason.",
        "icon": "😠"
    }
]

#class to handle video capture in a separate thread
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QPixmap)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
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
                self.change_pixmap_signal.emit(QPixmap.fromImage(p))
            time.sleep(0.03)