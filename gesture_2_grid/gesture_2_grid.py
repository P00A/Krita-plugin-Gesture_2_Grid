from krita import DockWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QComboBox
import os
from PyQt5.QtCore import Qt
import subprocess
import json
from PyQt5.QtGui import QPainterPath

from PyQt5.QtGui import QPainterPath



class GestureToGrid(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("G2G - Gesture to Grid")

        main_widget = QWidget()
        layout = QVBoxLayout()
        # -------------------------
        # GRID DENSITY SLIDER
        # -------------------------
        self.spacing_label = QLabel("Grid Density: 100")
        layout.addWidget(self.spacing_label)
        self.spacing_slider = QSlider(Qt.Horizontal)
        self.spacing_slider.setMinimum(20)
        self.spacing_slider.setMaximum(300)
        self.spacing_slider.setValue(100)
        self.spacing_slider.valueChanged.connect(
             lambda v: self.spacing_label.setText(f"Grid Density: {v}")
             )
        layout.addWidget(self.spacing_slider)
        # -------------------------
        # LINE THICKNESS (visual control)
        # -------------------------
        self.thickness_label = QLabel("Line Strength: 1")
        layout.addWidget(self.thickness_label)
        self.thickness_slider = QSlider(Qt.Horizontal)
        self.thickness_slider.setMinimum(1)
        self.thickness_slider.setMaximum(5)
        self.thickness_slider.setValue(1)
        self.thickness_slider.valueChanged.connect(
            lambda v: self.thickness_label.setText(f"Line Strength: {v}")
            )
        layout.addWidget(self.thickness_slider)
        # -------------------------
        # PERSPECTIVE MODE
        # -------------------------
        self.mode_label = QLabel("Perspective Mode")
        layout.addWidget(self.mode_label)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Auto", "1-Point", "2-Point", "3-Point"])
        layout.addWidget(self.mode_combo)

        # -------------------------
        # BUTTON
        # -------------------------
        btn = QPushButton("Generate Grid")
        btn.clicked.connect(self.run_g2g)
        layout.addWidget(btn)
        
        main_widget.setLayout(layout)

        self.setWidget(main_widget)

    
    def run_g2g(self):
        doc = Krita.instance().activeDocument()
        node = doc.activeNode()

        plugin_dir = os.path.dirname(os.path.abspath(__file__))

        # -------------------------
        # TEMP FOLDER
        # -------------------------
        temp_dir = os.path.join(plugin_dir, "temp")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        input_img = os.path.join(temp_dir, "input.png")
        output_json = os.path.join(temp_dir, "output.json")

        # -------------------------
        # SAVE IMAGE FROM KRITA
        # -------------------------
        node.save(input_img, 0, 0, doc.width(), doc.height())

        # -------------------------
        # OPEN-CV ENGINE PATHS
        # -------------------------
        python_exe = os.path.join(plugin_dir, "python_env", "python.exe")
        script = os.path.join(plugin_dir, "opencv_engine", "process.py")

        # -------------------------
        # RUN ENGINE
        # -------------------------
        subprocess.run([
            python_exe,
            script,
            input_img,
            output_json
        ])

        # -------------------------
        # READ RESULTS
        # -------------------------
        if not os.path.exists(output_json):
            print(" Engine failed")
            return

        with open(output_json, "r") as f:
            data = json.load(f)

        lines = data.get("lines", [])
        vps = data.get("vanishing_points", [])

        print("Lines:", len(lines))
        print("Vanishing Points:", vps)
        self.draw_grid(doc, vps)


    def draw_grid(self, doc, vps):
        root = doc.rootNode()

        # Create vector layer
        grid_layer = doc.createVectorLayer("G2G Grid")
        root.addChildNode(grid_layer, None)

        width = doc.width()
        height = doc.height()

        spacing =  self.spacing_slider.value() # distance between grid rays

        def draw_line(x1, y1, x2, y2):
            thickness = self.thickness_slider.value()
        

        for i in range(thickness):  
            path = QPainterPath()
            path.moveTo(x1 + i, y1 + i)
            path.lineTo(x2 + i, y2 + i)
            grid_layer.addShape(path)

    
        mode = self.mode_combo.currentText()

        if mode == "1-Point":
            vps = vps[:1]
        elif mode == "2-Point":
            vps = vps[:2]
        elif mode == "3-Point":
            vps = vps[:3]

    
        if len(vps) == 1:
            vx, vy = vps[0]

            for x in range(0, width, spacing):
                draw_line(x, 0, x, height)

            for x in range(0, width, spacing):
                draw_line(x, height, vx, vy)

        elif len(vps) == 2:
            vp1 = vps[0]
            vp2 = vps[1]

            for x in range(0, width, spacing):
                draw_line(x, height, vp1[0], vp1[1])
                draw_line(x, height, vp2[0], vp2[1])

        elif len(vps) >= 3:
            vp1, vp2, vp3 = vps[:3]

            for x in range(0, width, spacing):
                draw_line(x, height, vp1[0], vp1[1])
                draw_line(x, height, vp2[0], vp2[1])

            for y in range(0, height, spacing):
                draw_line(0, y, vp3[0], vp3[1])
                draw_line(width, y, vp3[0], vp3[1])

        doc.refreshProjection()
