# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QGroupBox, QPushButton, QHBoxLayout, QLineEdit, \
    QCheckBox
from PyQt5.QtCore import Qt
import sys
from PyQt5 import QtGui
from gmpy2 import *
from Crypto.Util.number import *



class WindowDemo(QWidget):
    def __init__(self):
        super().__init__()
        font = QtGui.QFont()
        font.setFamily("微软雅黑") #括号里可以设置成自己想要的其它字体
        font.setPointSize(12)   #括号里的数字可以设置成自己想要的字体大小

        self.resize(1200,400) 
        self.setWindowTitle("RSA大数据分解系统")
        operationgroup = QGroupBox("大数运算")
        operationgroup.setFont(font)
        operationgroup.setFlat(False)
        self.addbtn = QPushButton('加')
        self.subbtn = QPushButton('减')
        self.multibtn = QPushButton('乘')
        self.excebtn = QPushButton('模逆')
        self.rootbtn = QPushButton('开方')
        self.searchbtn = QPushButton('素数搜索')
        operationgrouplayout = QHBoxLayout()
        operationgrouplayout.addWidget(self.addbtn)
        operationgrouplayout.addWidget(self.subbtn)
        operationgrouplayout.addWidget(self.multibtn)
        operationgrouplayout.addWidget(self.excebtn)
        operationgrouplayout.addWidget(self.rootbtn)
        operationgrouplayout.addWidget(self.searchbtn)

        operationgroup.setLayout(operationgrouplayout)

        self.addbtn.clicked.connect(lambda: self.add())
        self.subbtn.clicked.connect(lambda: self.sub())
        self.multibtn.clicked.connect(lambda: self.mul())
        self.excebtn.clicked.connect(lambda: self.invert_mod())
        self.rootbtn.clicked.connect(lambda: self.root())
        self.searchbtn.clicked.connect(lambda: self.prime_find())

        algorithmgroup = QGroupBox("分解算法")
        algorithmgroup.setFont(font)        
        algorithmgroup.setFlat(False)
        self.divisionbtn = QPushButton('试除法')
        self.fermatbtn = QPushButton('fermat')
        self.pouardpbtn = QPushButton('pouard p-1')
        self.pouardbtn = QPushButton('pouard rho')

        algorithmgrouplayout = QHBoxLayout()
        algorithmgrouplayout.addWidget(self.divisionbtn)
        algorithmgrouplayout.addWidget(self.fermatbtn)
        algorithmgrouplayout.addWidget(self.pouardpbtn)
        algorithmgrouplayout.addWidget(self.pouardbtn)

        algorithmgroup.setLayout(algorithmgrouplayout)

        self.divisionbtn.clicked.connect(lambda: self.easy_factor())
        #self.subbtn.clicked.connect(lambda: self.easy_factor())
        self.fermatbtn.clicked.connect(lambda: self.fermat())
        self.pouardpbtn.clicked.connect(lambda: self.Pollards_p_1())
        self.pouardbtn.clicked.connect(lambda: self.pollard_rho())

        inputgroup = QGroupBox("输入")
        inputgroup.setFont(font)            
        inputgroup.setFlat(False)
        self.ip1le = QLineEdit()
        self.ip2le = QLineEdit()
        self.checkBox1 = QCheckBox("是否有第二参数")
        self.checkBox1.setChecked(True)
        self.checkBox1.stateChanged.connect(lambda: self.btnstate(self.checkBox1))

        inputgrouplayout = QHBoxLayout()
        inputgrouplayout.addWidget(QLabel('输入'))
        inputgrouplayout.addWidget(self.ip1le)
        inputgrouplayout.addWidget(self.checkBox1)
        inputgrouplayout.addWidget(self.ip2le)
        inputgroup.setLayout(inputgrouplayout)

        outputgroup = QGroupBox("输出")
        outputgroup.setFont(font)         
        outputgroup.setFlat(False)
        self.outle = QLineEdit()

        outputgrouplayout = QHBoxLayout()
        outputgrouplayout.addWidget(QLabel('输出'))
        outputgrouplayout.addWidget(self.outle)

        outputgroup.setLayout(outputgrouplayout)

        layout = QVBoxLayout()
        layout.addWidget(operationgroup)
        layout.addWidget(algorithmgroup)
        layout.addWidget(inputgroup)
        layout.addWidget(outputgroup)
        self.setLayout(layout)

    def btnstate(self,btn):
        if self.checkBox1.isChecked():
            self.ip2le.setFocusPolicy(Qt.ClickFocus)
        else:
            self.ip2le.setFocusPolicy(Qt.NoFocus)

    def add(self):
        result = int(self.ip1le.text()) + int(self.ip2le.text())
        self.outle.setText(str(result))

    def sub(self):
        result = int(self.ip1le.text()) - int(self.ip2le.text())
        self.outle.setText(str(result))

    def mul(self):
        result = int(self.ip1le.text()) * int(self.ip2le.text())
        self.outle.setText(str(result))

    def divi(self):
        result = int(self.ip1le.text()) / int(self.ip2le.text())
        self.outle.setText(str(result))

    def root(self):
        result = iroot(int(self.ip1le.text()),2)[0]
        self.outle.setText(str(result))

    def invert_mod(self):
        result = invert(int(self.ip1le.text()), int(self.ip2le.text()))
        self.outle.setText(str(result))

    def prime_find(self):
        a = int(self.ip1le.text())
        b = int(self.ip2le.text())
        l = []
        if a % 2 == 1:
            for i in range(a, b, 2):
                if isPrime(i):
                    l.append(i)
        else:
            for i in range(a + 1, b, 2):
                if isPrime(i):
                    l.append(i)

        self.outle.setText(str(l))


    def easy_factor(self):
        n = int(self.ip1le.text())
        if n%2 == 0:
            l = [2]
        else:
            l=[]
        for i in range(3, n//2, 2):
            if n%i == 0:
                l.append(i)
                l.append(n // i)
                break

        self.outle.setText(str(l))

    def fermat(self):
        num = int(self.ip1le.text())
        x = iroot(num, 2)[0]
        if x * x < num:
            x += 1

        # y^2 = x^2 - num
        while (True):
            y2 = x * x - num
            y = iroot(y2, 2)[0]
            if y * y == y2:
                break
            x += 1

        result = [int(x + y), int(x - y)]
        self.outle.setText(str(result))

    def Pollards_p_1(self):
        N = int(self.ip1le.text())
        l = []
        a = 2
        n = 2
        while True:
            a = pow(a, n, N)
            res = gcd(a - 1, N)
            if res != 1 and res != N:
                l.append(int(res))
                l.append(int(N // res))
                break
            n += 1
        self.outle.setText(str(l))

    def mapx(self, x, n):
        x = (pow(x, n - 1, n) + 3) % n  # pow(x,n-1,n)是为了减小数值，加速运算，
        return x

    def pollard_rho(self):
        n = int(self.ip1le.text())
        l = []
        x1 = 1
        x2 = 1
        while True:
            x1 = self.mapx(x1, n)
            x2 = self.mapx(self.mapx(x2, n), n)
            p = gcd(x1 - x2, n)
            if (p == n):
                print("fail")
                return
            elif (p != 1):

                l.append(int(p))
                l.append(int(n // p))
                break
        self.outle.setText(str(l))

# 用于测试
def prime_mul(n):
    s = 2
    for i in range(3,n+1,2):
        s = s * i
    return s

def GCD(a,b):
# *************begin************#
    if a<b:
        t=a
        a=b
        b=t
    while a%b!=0:
        temp=a%b
        a=b
        b=temp
    return b

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WindowDemo()
    win.show()
    sys.exit(app.exec_())

    # 测试数据：
    # n1用于试除法，只适用于有一个因子非常小
    # n1=44977650353919390254523616029962759106131643255937053520218827681034036037811548014143717611389880737797260093630597046831105341957937546464210654178434000189331210396426903199160396439
    # n2是费马分解 用于两个素数因子相差不大的时候
    # n2=29760626866185326989733731422262372448607519436821550579529135839741782953805367510848170403677177959581926975928858527382606519218500583865533422204083791005034283486702624105891443944081811440755525209606218662820512863197721593743215538452353008437166191349826475767661954335280526275349455356016723088457513949386422273277170909853229178578565029078634523028328082867862750037494076075735192097896651354262770943479476815074588976072470536772359716921079562997405423111080249686029305647754675819615049376959620243321809734083464529952903982615339018654023681440188817687542156910644039264873368343207362591793909
    # n3,n33是rho算法，他是一种平均性能较好的算法，但素数较大时也需要较长时间来处理
    # n3=495049796534103571         n33=667388241642009445263241687267250527
    # n4是p-1算法，适用于有一个因子为光滑数
    # n4 = 113124724574860967285237994605019409536526697313813926903433549578263017099416540610689286854794250320790998436475886590539842741077622513608097020512916007737373319044009789877569865349585381694009262844101976152870151175166975340737013575726055150964895741339376752482873927
