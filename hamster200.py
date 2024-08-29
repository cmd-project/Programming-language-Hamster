import time
import re
import sys
import os

class HamsterInterpreter:
    def __init__(self):
        self.variables = {}
        self.styles = {}

    def execute(self, code):
        lines = code.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('print_text'):
                self.handle_print_text(line)
            elif line.startswith('time.s'):
                self.handle_time_s(line)
            elif line.startswith('print_text_var'):
                self.handle_print_text_var(line)
            elif line.startswith('time_print'):
                self.handle_time_print(line)
            elif line.startswith('var'):
                self.handle_variable_declaration(line)
            elif line.startswith('@style'):
                self.handle_style_declaration(line)
            elif '+' in line or '-' in line:
                self.handle_addition(line)
            elif line.startswith('/*') and line.endswith('*/'):
                pass  # Comment, ignore it

    def handle_print_text(self, line):
        match = re.match(r'print_text\["(.*)"\]', line)
        if match:
            print(match.group(1))

    def handle_time_s(self, line):
        match = re.match(r'time\.s\(n\("(\d+)"\)\)', line)
        if match:
            seconds = int(match.group(1))
            time.sleep(seconds)

    def handle_print_text_var(self, line):
        match = re.match(r'print_text_var(?:\(id="(.*?)"\))? => #(.*)', line)
        if match:
            var_id = match.group(1)
            var_name = f'#{match.group(2)}'
            value = self.variables.get(var_name, '')
            if var_id and var_id in self.styles:
                style = self.styles[var_id]
                print(f'\033[{style}m{value}\033[0m')
            else:
                print(value)

    def handle_time_print(self, line):
        match = re.match(r'time_print(?:\(id="(.*?)"\))?', line)
        if match:
            print(time.strftime("%Y-%m-%d %H:%M:%S"))

    def handle_variable_declaration(self, line):
        match = re.match(r'var #(\w+) === "(.*)"', line)
        if match:
            var_name = f'#{match.group(1)}'
            value = match.group(2)
            self.variables[var_name] = value

    def handle_style_declaration(self, line):
        match = re.match(r'@style\{\s*id === (\w+) = color: (\w+)\s*\}', line)
        if match:
            var_id = match.group(1)
            color = match.group(2)
            color_code = {
                'red': '31',
                'green': '32',
                'blue': '34',
            }.get(color, '0')  # Default to no color
            self.styles[var_id] = color_code

    def handle_addition(self, line):
        match = re.match(r'(\d+)\s*([+-])\s*(\d+)', line)
        if match:
            num1 = int(match.group(1))
            operator = match.group(2)
            num2 = int(match.group(3))
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            print(result)

def run_hamster_file(file_path):
    if not file_path.endswith('.hamster'):
        print("Error: The file must have a '.hamster' extension.")
        return

    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    with open(file_path, 'r') as file:
        code = file.read()

    interpreter = HamsterInterpreter()
    interpreter.execute(code)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hamster_interpreter.py <filename.hamster>")
    else:
        filename = sys.argv[1]
        run_hamster_file(filename)
