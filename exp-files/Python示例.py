import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, 
    QSplitter, QStatusBar, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QFont, QColor, QTextCharFormat, QSyntaxHighlighter
from PyQt5.QtCore import Qt

class DCCSyntaxHighlighter(QSyntaxHighlighter):
    """DCC 脚本语法高亮器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []
        
        # 关键字规则
        keywords = [
            "如果", "如果结束", "否则", "if", "else", "endif",
            "计次循环", "记次循环尾", "跳出循环", "到循环尾", "条件循环",
            "for", "endfor", "break", "continue", "while",
            "定义函数", "结束函数定义", "def", "enddef",
            "创建板块", "结束创建板块", "creatd", "endcd",
            "包裹体", "包裹体尾", "block", "endblock"
        ]
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(0, 0, 255))  # 蓝色
        self.rules.extend([(rf'\b{word}\b', keyword_format) for word in keywords])
        
        # 常量规则
        constant_format = QTextCharFormat()
        constant_format.setForeground(QColor(0, 128, 0))  # 绿色
        self.rules.append((r'#\w+', constant_format))
        
        # 布尔值规则
        boolean_format = QTextCharFormat()
        boolean_format.setForeground(QColor(128, 0, 128))  # 紫色
        self.rules.append((r'\b(true|false|真|假|TRUE|FALSE)\b', boolean_format))
        
        # 运算符规则
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor(255, 0, 0))  # 红色
        operators = r'[\*×\/÷%+\-&|^~!><]|&&|\|\||\^\^|\*\*|>>|<<|and|or|not|且|或|非'
        self.rules.append((operators, operator_format))
        
        # 字符串规则
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(165, 42, 42))  # 棕色
        self.rules.append((r'["“”][^"“”]*["“”]', string_format))
        
        # 注释规则
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(128, 128, 128))  # 灰色
        self.rules.append((r'[;；].*$', comment_format))
        self.rules.append((r'@.*?@', comment_format))
        self.rules.append((r'/\*.*?\*/', comment_format))
        
        # 嵌套块规则
        nested_format = QTextCharFormat()
        nested_format.setBackground(QColor(240, 240, 240))  # 浅灰色背景
        self.rules.append((r'[（(].*?[）)]', nested_format))
        
        # JSON 块规则
        json_format = QTextCharFormat()
        json_format.setBackground(QColor(255, 255, 200))  # 浅黄色背景
        self.rules.append((r'^===\s*$.*?^===\s*$', json_format))
        
        # C++ 块规则
        cpp_format = QTextCharFormat()
        cpp_format.setBackground(QColor(200, 255, 200))  # 浅绿色背景
        self.rules.append((r'^\+\+\+\s*$.*?^\+\+\+\s*$', cpp_format))
    
    def highlightBlock(self, text):
        """高亮文本块"""
        for pattern, format in self.rules:
            expression = re.compile(pattern, re.MULTILINE | re.DOTALL)
            for match in expression.finditer(text):
                start, end = match.span()
                length = end - start
                self.setFormat(start, length, format)

class DCCEditor(QTextEdit):
    """DCC 脚本编辑器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Consolas", 10))
        self.setAcceptRichText(False)
        self.highlighter = DCCSyntaxHighlighter(self.document())
    
    def get_code(self):
        """获取编辑器中的代码"""
        return self.toPlainText()

class DCCIDE(QMainWindow):
    """DCC Script IDE 主窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DCC Script IDE")
        self.resize(800, 600)
        
        # 创建主部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Vertical)
        layout.addWidget(splitter)
        
        # 创建代码编辑器
        self.editor = DCCEditor()
        splitter.addWidget(self.editor)
        
        # 创建输出窗口
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 10))
        splitter.addWidget(self.output)
        
        # 设置分割比例
        splitter.setSizes([400, 200])
        
        # 创建按钮栏
        button_layout = QVBoxLayout()
        layout.addLayout(button_layout)
        
        # 创建运行按钮
        self.run_button = QPushButton("运行 (F5)")
        self.run_button.clicked.connect(self.run_code)
        button_layout.addWidget(self.run_button)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
        # 设置快捷键
        self.run_button.setShortcut("F5")
        
        # 初始化编辑器内容
        self.editor.setPlainText(
            '输出 "欢迎使用DCC Script IDE!"\n'
            '如果 (输入) == 10\n'
            '    输出 "正确!"\n'
            '否则\n'
            '    输出 "错误!"\n'
            '如果结束\n'
            '\n'
            '=== 这是JSON块 ===\n'
            '{\n'
            '    "name": "张三",\n'
            '    "age": 30\n'
            '}\n'
            '=== === ===\n'
        )
    
    def run_code(self):
        """运行DCC脚本"""
        code = self.editor.get_code()
        self.output.clear()
        
        # 这里应该是实际的DCC解释器执行代码，但我还没写
        # 现在只做简单的模拟执行
        self.output.append(">>> 开始执行 DCC 脚本 <<<")
        
        # 模拟执行 - 简单输出代码行
        for i, line in enumerate(code.splitlines(), 1):
            if line.strip():
                self.output.append(f"行 {i}: {line}")
        
        self.output.append(">>> 脚本执行完成 <<<")
        self.status_bar.showMessage("脚本执行完成")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ide = DCCIDE()
    ide.show()
    sys.exit(app.exec_())