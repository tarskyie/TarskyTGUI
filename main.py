import sys
import random
from random import randint, seed
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QLineEdit, QPushButton, QWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from llama_cpp import Llama

class LlamaGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def getmodel(self, modelname, seed, ctx, threads):
        modelpath = "./models/" + modelname
        print(modelpath)
        if seed == "-1" or seed == "":
            seed = random.randint(1, 10000000)
        if ctx == "":
            ctx = 4096
        print("SEED: " + str(seed))
        self.model = Llama(model_path = modelpath, n_ctx=abs(int(ctx)), seed=int(seed), n_threads=int(threads))

    def initUI(self):
        # Set dark theme colors
        self.setStyleSheet("background-color: #222; color: #FFF;")

        self.setWindowTitle("Tarsky TGUI")

        self.output_label = QLabel("Game story:", self)
        self.output_label.move(20, 20)
        self.output_label.resize(960, 30)
        self.output_label.setStyleSheet("color: #FFF;")

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(False)
        self.output_text.move(20, 50)
        self.output_text.resize(960, 400)
        self.output_text.setText("TarskyTGUI is a game that uses power of AI to generate game story on run. Game gives you seed for your journey and you input your actions to continue story. Have fun!\nNow you can ask it generate you a story")
        self.output_text.setStyleSheet("background-color: #333; color: #FFF;")

        self.input_label = QLabel("Enter a prompt:", self)
        self.input_label.move(20, 470)
        self.input_label.setStyleSheet("color: #FFF;")

        self.predict_label = QLabel("n_predict", self)
        self.predict_label.move(640, 470)
        self.input_label.setStyleSheet("color: #FFF;")

        #Do Say Story
        self.dosay = QPushButton("Do:", self)
        self.dosay.move(20, 500)
        self.dosay.resize(60, 30)
        self.dosay.setStyleSheet("background-color: #555; color: #FFF;")
        self.dosay.clicked.connect(self.dosay_logic)

        self.input_entry = QLineEdit(self)
        self.input_entry.move(100, 500)
        self.input_entry.resize(520, 30)
        self.input_entry.setStyleSheet("background-color: #444; color: #FFF;")

        self.predict_entry = QLineEdit(self)
        self.predict_entry.move(640, 500)
        self.predict_entry.resize(80, 30)
        self.predict_entry.setValidator(QIntValidator())
        self.predict_entry.setText(str(70))

        self.generate_button = QPushButton("Generate", self)
        self.generate_button.move(740, 500)
        self.generate_button.resize(100, 30)
        self.generate_button.setStyleSheet("background-color: #555; color: #FFF;")
        self.generate_button.clicked.connect(self.generate_text)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.move(860, 500)
        self.clear_button.resize(100, 30)
        self.clear_button.setStyleSheet("background-color: #555; color: #FFF;")
        self.clear_button.clicked.connect(self.clear_text)

        self.setGeometry(100, 100, 1000, 550)
        self.show()

    def dosay_logic(self):
        if self.dosay.text() == "Do:":
            self.dosay.setText("Say:")
        elif self.dosay.text() == "Say:":
            self.dosay.setText("Story:")
        elif self.dosay.text() == "Story:":
            self.dosay.setText("Ask an AI:")
        else:
            self.dosay.setText("Do:")

    def generate_text(self):
        prompt = self.output_text.toPlainText() + "User: " + self.dosay.text() + self.input_entry.text() + "\nGame story:"
        generated_raw = self.model(prompt, max_tokens=int(self.predict_entry.text()), stop=["\n"], temperature=0.8)
        choices = generated_raw["choices"]
        generated_text = str(choices[0]["text"])
        print(generated_text)
        self.output_text.append(self.dosay.text() + " " + self.input_entry.text() + "\nGame story: " + generated_text)
        self.input_entry.clear()

    def clear_text(self):
        self.output_text.setText("TarskyTGUI is a game that uses power of AI to generate game story on run. Game gives you seed for your journey and you input your actions to continue story. Have fun!\nNow you can ask it generate you a story")
        self.input_entry.clear()

class LlamaSettings(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setStyleSheet("background-color: #222; color: #FFF;")
        self.setWindowTitle("Open Dungeon Launcher")

        self.model_entry = QLineEdit(self)
        try: 
            pmodel = open("pmodel.txt", "r")
            self.model_entry.setText(pmodel.read())
            pmodel.close()
        except:
            print("no such file as 'pmodel.txt'")
        self.model_entry.resize(520, 30)
        self.model_entry.setStyleSheet("background-color: #444; color: #FFF;")
        self.model_entry.setPlaceholderText("model name (put models in 'models' folder)")

        self.seedEntry = QLineEdit("-1", self)
        self.seedEntry.setValidator(QIntValidator())
        self.seedEntry.resize(100, 30)
        self.seedEntry.setStyleSheet("background-color: #444; color: #FFF;")
        self.seedEntry.move(0, 40)
        self.seedEntry.setPlaceholderText("seed")

        self.ctxEntry = QLineEdit("4096", self)
        self.ctxEntry.setValidator(QIntValidator())
        self.ctxEntry.resize(100, 30)
        self.ctxEntry.setStyleSheet("background-color: #444; color: #FFF;")
        self.ctxEntry.move(110, 40)
        self.ctxEntry.setPlaceholderText("n_ctx")

        self.threadEntry = QLineEdit("2", self)
        self.threadEntry.setValidator(QIntValidator())
        self.threadEntry.resize(100, 30)
        self.threadEntry.setStyleSheet("background-color: #444; color: #FFF;")
        self.threadEntry.move(220, 40)
        self.threadEntry.setPlaceholderText("threads")

        self.apply_button = QPushButton("Apply", self)
        self.apply_button.clicked.connect(self.applied)
        self.apply_button.move(0, 80)
        self.apply_button.setStyleSheet("background-color: #555; color: #FFF;")

        #self.txt_instruction = QLabel("Enter the name of your model file(the file must be in 'models' folder)", self)
        #self.txt_instruction.move(110, 80)
        #self.txt_instruction.resize(410, 30)
        #self.txt_instruction.setStyleSheet("color: #FFF;")

        self.setGeometry(100, 100, 520, 120)
        self.show()
    def applied(self): 
        prev_model = open("pmodel.txt", "w")
        prev_model.write(self.model_entry.text())
        prev_model.close()
        self.w = LlamaGUI()
        self.w.show()
        self.w.getmodel(self.model_entry.text(), self.seedEntry.text(), self.ctxEntry.text(), self.threadEntry.text())
        print("Ready!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LlamaSettings()
    sys.exit(app.exec_())