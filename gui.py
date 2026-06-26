import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
import matplotlib.pyplot as plt
import numpy as np
import threading


class History:
    def __init__(self):
        self._history = []

    def add_records(self, category, operation, result):
        self._history.append({'category': category, 'operation': operation, 'result': result})

    def show(self):
        if not self._history:
            return 'История пуста'

        result = []
        for record in self._history:
            cat = record['category']
            op = record['operation']
            res = record['result']
            result.append(f'{cat}: {op} = {res}')
        return '\n'.join(result)

    def clear(self):
        self._history = []

    def get_history(self):
        return self._history


class BasedCalculator:
    def __init__(self, history):
        self._history = history

    def AddOperation(self, a, b):
        result = a + b
        self._history.add_records(category='Арифметика', operation=f'{a} + {b}', result=result)
        return result

    def MinusOperation(self, a, b):
        result = a - b
        self._history.add_records(category='Арифметика', operation=f'{a} - {b}', result=result)
        return result

    def UmnohOperation(self, a, b):
        result = a * b
        self._history.add_records(category='Арифметика', operation=f'{a} * {b}', result=result)
        return result

    def DeleniaOperation(self, a, b):
        if b == 0:
            error = 'Ошибка деление на ноль'
            self._history.add_records(category='Арифметика', operation=f'{a} / {b}', result=error)
            return error
        result = a / b
        self._history.add_records(category='Арифметика', operation=f'{a} / {b}', result=result)
        return result


class Trigonometria:
    def __init__(self, history):
        self._history = history

    def sin(self, degrees):
        radians = math.radians(degrees)
        result = math.sin(radians)
        self._history.add_records(category='Тригонометрия', operation=f'sin({degrees}°)', result=result)
        return result

    def cos(self, degrees):
        radians = math.radians(degrees)
        result = math.cos(radians)
        self._history.add_records(category='Тригонометрия', operation=f'cos({degrees}°)', result=result)
        return result

    def tan(self, degrees):
        radians = math.radians(degrees)
        result = math.tan(radians)
        self._history.add_records(category='Тригонометрия', operation=f'tan({degrees}°)', result=result)
        return result

    def asin(self, value):
        radians = math.asin(value)
        result = math.degrees(radians)
        self._history.add_records(category='Тригонометрия', operation=f'asin({value})', result=result)
        return result

    def acos(self, value):
        radians = math.acos(value)
        result = math.degrees(radians)
        self._history.add_records(category='Тригонометрия', operation=f'acos({value})', result=result)
        return result

    def atan(self, value):
        radians = math.atan(value)
        result = math.degrees(radians)
        self._history.add_records(category='Тригонометрия', operation=f'atan({value})', result=result)
        return result


class GraphCalculator:
    def __init__(self):
        pass

    def plot_expression(self, expression, x_min=-360, x_max=360):
        try:
            x_deg = np.linspace(x_min, x_max, 1000)
            x = np.radians(x_deg)

            allowed_names = {
                'x': x,
                'np': np,
                'sin': np.sin,
                'cos': np.cos,
                'tan': np.tan,
                'sqrt': np.sqrt,
                'pi': np.pi,
                'exp': np.exp,
                'log': np.log,
                'abs': np.abs
            }

            y = eval(expression, {"__builtins__": None}, allowed_names)

            plt.figure(figsize=(10, 5))
            plt.plot(x_deg, y, label=expression, color='blue', linewidth=2)
            plt.axhline(0, color='black', linewidth=0.5)
            plt.axvline(0, color='black', linewidth=0.5)
            plt.xticks(np.arange(x_min, x_max + 1, 90))
            plt.xlabel('Градусы (°)')
            plt.ylabel('Y')
            plt.title(f'График функции: {expression}')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()
            plt.show()
            return True, "График успешно построен"
        except Exception as e:
            return False, f"Ошибка при построении графика: {e}"


class MatrixCalc:
    def __init__(self, history):
        self._history = history

    def _get_dimensions(self, matrix):
        return len(matrix), len(matrix[0])

    def MatrixAdd(self, A, B):
        if self._get_dimensions(A) != self._get_dimensions(B):
            return "Ошибка: матрицы должны быть одинакового размера"

        result = [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
        self._history.add_records(category="Матрицы", operation=f"{A} + {B}", result=result)
        return result

    def MatrixMinus(self, A, B):
        if self._get_dimensions(A) != self._get_dimensions(B):
            return "Ошибка: матрицы должны быть одинакового размера"

        result = [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
        self._history.add_records(category="Матрицы", operation=f"{A} - {B}", result=result)
        return result

    def MatrixUmn(self, A, B):
        rows_A, cols_A = self._get_dimensions(A)
        rows_B, cols_B = self._get_dimensions(B)

        if cols_A != rows_B:
            return "Ошибка: число столбцов матрицы A должно быть равно числу строк матрицы B"

        result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] += A[i][k] * B[k][j]

        self._history.add_records(category="Матрицы", operation=f"{A} * {B}", result=result)
        return result

    def MatrixDel(self, A, b):
        if b == 0:
            return "Ошибка: деление матрицы на ноль"

        result = [[A[i][j] / b for j in range(len(A[0]))] for i in range(len(A))]
        self._history.add_records(category="Матрицы", operation=f"{A} / {b}", result=result)
        return result


class IntegrationCalculator:
    def __init__(self, history):
        self._history = history

    def IntegrateOperation(self, func, a, b, n=1000):
        if n <= 0:
            raise ValueError("Количество шагов разбиения должно быть больше нуля!")

        h = (b - a) / n
        total = 0.5 * (func(a) + func(b))
        for i in range(1, n):
            total += func(a + i * h)

        result = total * h
        func_name = getattr(func, '__name__', 'f(x)')
        self._history.add_records(
            category="Интегрирование",
            operation=f"∫ от {a} до {b} для {func_name} (n={n})",
            result=result
        )
        return result


def func1(x):
    return x ** 2 + 3 * x


def func2(x):
    return x ** 2 + 3 * x + 1


def func3(x):
    return x ** 3 - 2 * x + 5


def func4(x):
    return math.sin(x) + math.cos(x)


def func5(x):
    return 2 * x ** 2 - 4 * x + 1


def square(x):
    return x ** 2


def sine(x):
    return math.sin(x)


def exp_plus_x(x):
    return math.exp(x) + x


def linear(x):
    return 3 * x + 1


def polynomial(x):
    return x ** 4 - 2 * x ** 3 + 3 * x ** 2 - 4 * x + 5


class EngineeringCalc:
    def __init__(self):
        self._history = History()
        self.arithmetic = BasedCalculator(self._history)
        self.trigonometria = Trigonometria(self._history)
        self.matrix = MatrixCalc(self._history)
        self.integration = IntegrationCalculator(self._history)

    def show_history(self):
        return self._history.show()

    def get_history(self):
        return self._history.get_history()

    def clear_history(self):
        self._history.clear()


class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Инженерный калькулятор")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        self.calculator = EngineeringCalc()

        self.create_widgets()
        self.update_history()

    def create_widgets(self):
        # Создаем вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Вкладки
        self.arithmetic_tab = ttk.Frame(self.notebook)
        self.trigonometry_tab = ttk.Frame(self.notebook)
        self.matrix_tab = ttk.Frame(self.notebook)
        self.integration_tab = ttk.Frame(self.notebook)
        self.graph_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.arithmetic_tab, text="Арифметика")
        self.notebook.add(self.trigonometry_tab, text="Тригонометрия")
        self.notebook.add(self.matrix_tab, text="Матрицы")
        self.notebook.add(self.integration_tab, text="Интегрирование")
        self.notebook.add(self.graph_tab, text="Графики")
        self.notebook.add(self.history_tab, text="История")

        self.create_arithmetic_tab()
        self.create_trigonometry_tab()
        self.create_matrix_tab()
        self.create_integration_tab()
        self.create_graph_tab()
        self.create_history_tab()

    # ---------- АРИФМЕТИКА ----------
    def create_arithmetic_tab(self):
        title = ttk.Label(self.arithmetic_tab, text="Арифметические операции", font=("Arial", 16))
        title.pack(pady=10)

        input_frame = ttk.Frame(self.arithmetic_tab)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Число A:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_a = ttk.Entry(input_frame, width=20)
        self.entry_a.grid(row=0, column=1, padx=5, pady=5)
        self.entry_a.insert(0, "10")

        ttk.Label(input_frame, text="Число B:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_b = ttk.Entry(input_frame, width=20)
        self.entry_b.grid(row=1, column=1, padx=5, pady=5)
        self.entry_b.insert(0, "5")

        ttk.Label(input_frame, text="Операция:").grid(row=2, column=0, padx=5, pady=5)
        self.arithmetic_operation = ttk.Combobox(
            input_frame,
            values=["+", "-", "*", "/"],
            state="readonly",
            width=17
        )
        self.arithmetic_operation.grid(row=2, column=1, padx=5, pady=5)
        self.arithmetic_operation.current(0)

        btn_frame = ttk.Frame(self.arithmetic_tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Вычислить", command=self.calculate_arithmetic).pack()

        self.arithmetic_result_label = ttk.Label(
            self.arithmetic_tab,
            text="Результат: ",
            font=("Arial", 13)
        )
        self.arithmetic_result_label.pack(pady=10)

    def calculate_arithmetic(self):
        try:
            a = float(self.entry_a.get().replace(",", "."))
            b = float(self.entry_b.get().replace(",", "."))
            operation = self.arithmetic_operation.get()

            if operation == "+":
                result = self.calculator.arithmetic.AddOperation(a, b)
            elif operation == "-":
                result = self.calculator.arithmetic.MinusOperation(a, b)
            elif operation == "*":
                result = self.calculator.arithmetic.UmnohOperation(a, b)
            elif operation == "/":
                result = self.calculator.arithmetic.DeleniaOperation(a, b)
            else:
                raise ValueError("Неизвестная операция")

            self.arithmetic_result_label.config(text=f"Результат: {result}")
            self.update_history()

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Введите корректные числа: {e}")

    # ---------- ТРИГОНОМЕТРИЯ ----------
    def create_trigonometry_tab(self):
        title = ttk.Label(self.trigonometry_tab, text="Тригонометрические функции", font=("Arial", 16))
        title.pack(pady=10)

        input_frame = ttk.Frame(self.trigonometry_tab)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Значение:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_trig = ttk.Entry(input_frame, width=20)
        self.entry_trig.grid(row=0, column=1, padx=5, pady=5)
        self.entry_trig.insert(0, "45")

        ttk.Label(input_frame, text="Функция:").grid(row=1, column=0, padx=5, pady=5)
        self.trig_operation = ttk.Combobox(
            input_frame,
            values=["sin", "cos", "tan", "asin", "acos", "atan"],
            state="readonly",
            width=17
        )
        self.trig_operation.grid(row=1, column=1, padx=5, pady=5)
        self.trig_operation.current(0)

        btn_frame = ttk.Frame(self.trigonometry_tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Вычислить", command=self.calculate_trigonometry).pack()

        self.trigonometry_result_label = ttk.Label(
            self.trigonometry_tab,
            text="Результат: ",
            font=("Arial", 13)
        )
        self.trigonometry_result_label.pack(pady=10)

    def calculate_trigonometry(self):
        try:
            value = float(self.entry_trig.get().replace(",", "."))
            operation = self.trig_operation.get()

            if operation == "sin":
                result = self.calculator.trigonometria.sin(value)
            elif operation == "cos":
                result = self.calculator.trigonometria.cos(value)
            elif operation == "tan":
                result = self.calculator.trigonometria.tan(value)
            elif operation == "asin":
                if -1 <= value <= 1:
                    result = self.calculator.trigonometria.asin(value)
                else:
                    messagebox.showerror("Ошибка", "Арксинус определен только для значений [-1, 1]")
                    return
            elif operation == "acos":
                if -1 <= value <= 1:
                    result = self.calculator.trigonometria.acos(value)
                else:
                    messagebox.showerror("Ошибка", "Арккосинус определен только для значений [-1, 1]")
                    return
            elif operation == "atan":
                result = self.calculator.trigonometria.atan(value)
            else:
                raise ValueError("Неизвестная функция")

            self.trigonometry_result_label.config(text=f"Результат: {result:.4f}")
            self.update_history()

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Введите корректное число: {e}")

    # ---------- МАТРИЦЫ ----------
    def create_matrix_tab(self):
        title = ttk.Label(self.matrix_tab, text="Операции с матрицами", font=("Arial", 16))
        title.pack(pady=10)

        input_frame = ttk.Frame(self.matrix_tab)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Матрица A (строки через ;, элементы через ,):").grid(row=0, column=0, padx=5,
                                                                                          pady=5)
        self.matrix_a_text = tk.Text(input_frame, height=4, width=30)
        self.matrix_a_text.grid(row=0, column=1, padx=5, pady=5)
        self.matrix_a_text.insert('1.0', "1,2;3,4")

        ttk.Label(input_frame, text="Матрица B (строки через ;, элементы через ,):").grid(row=1, column=0, padx=5,
                                                                                          pady=5)
        self.matrix_b_text = tk.Text(input_frame, height=4, width=30)
        self.matrix_b_text.grid(row=1, column=1, padx=5, pady=5)
        self.matrix_b_text.insert('1.0', "5,6;7,8")

        ttk.Label(input_frame, text="Операция:").grid(row=2, column=0, padx=5, pady=5)
        self.matrix_operation = ttk.Combobox(
            input_frame,
            values=["Сложение", "Вычитание", "Умножение", "Деление на число"],
            state="readonly",
            width=17
        )
        self.matrix_operation.grid(row=2, column=1, padx=5, pady=5)
        self.matrix_operation.current(0)

        ttk.Label(input_frame, text="Делитель (для деления):").grid(row=3, column=0, padx=5, pady=5)
        self.entry_matrix_div = ttk.Entry(input_frame, width=20)
        self.entry_matrix_div.grid(row=3, column=1, padx=5, pady=5)
        self.entry_matrix_div.insert(0, "2")

        btn_frame = ttk.Frame(self.matrix_tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Вычислить", command=self.calculate_matrix).pack()

        self.result_matrix_label = ttk.Label(
            self.matrix_tab,
            text="Результат: ",
            font=("Arial", 11)
        )
        self.result_matrix_label.pack(pady=10)

        self.matrix_result_text = tk.Text(self.matrix_tab, height=4, width=50, state="disabled")
        self.matrix_result_text.pack(pady=5)

    def parse_matrix(self, text):
        try:
            rows = text.strip().split(';')
            matrix = []
            for row in rows:
                elements = row.strip().split(',')
                matrix.append([float(e.strip()) for e in elements if e.strip()])
            return matrix
        except:
            return None

    def calculate_matrix(self):
        try:
            A = self.parse_matrix(self.matrix_a_text.get('1.0', tk.END))
            B = self.parse_matrix(self.matrix_b_text.get('1.0', tk.END))

            if A is None:
                messagebox.showerror("Ошибка", "Неверный формат матрицы A. Используйте: 1,2;3,4")
                return

            operation = self.matrix_operation.get()

            if operation == "Сложение":
                if B is None:
                    messagebox.showerror("Ошибка", "Неверный формат матрицы B")
                    return
                result = self.calculator.matrix.MatrixAdd(A, B)
            elif operation == "Вычитание":
                if B is None:
                    messagebox.showerror("Ошибка", "Неверный формат матрицы B")
                    return
                result = self.calculator.matrix.MatrixMinus(A, B)
            elif operation == "Умножение":
                if B is None:
                    messagebox.showerror("Ошибка", "Неверный формат матрицы B")
                    return
                result = self.calculator.matrix.MatrixUmn(A, B)
            elif operation == "Деление на число":
                divisor = float(self.entry_matrix_div.get().replace(",", "."))
                result = self.calculator.matrix.MatrixDel(A, divisor)
            else:
                raise ValueError("Неизвестная операция")

            self.result_matrix_label.config(
                text="Результат:" if not isinstance(result, str) else f"Результат: {result}")

            self.matrix_result_text.config(state="normal")
            self.matrix_result_text.delete('1.0', tk.END)
            if isinstance(result, str):
                self.matrix_result_text.insert('1.0', result)
            else:
                for row in result:
                    self.matrix_result_text.insert(tk.END, f"{row}\n")
            self.matrix_result_text.config(state="disabled")

            self.update_history()

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Введите корректные данные: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # ---------- ИНТЕГРИРОВАНИЕ ----------
    def create_integration_tab(self):
        title = ttk.Label(self.integration_tab, text="Численное интегрирование", font=("Arial", 16))
        title.pack(pady=10)

        functions = {
            'func1': 'x² + 3x',
            'func2': 'x² + 3x + 1',
            'func3': 'x³ - 2x + 5',
            'func4': 'sin(x) + cos(x)',
            'func5': '2x² - 4x + 1',
            'square': 'x²',
            'sine': 'sin(x)',
            'exp_plus_x': 'e^x + x',
            'linear': '3x + 1',
            'polynomial': 'x⁴ - 2x³ + 3x² - 4x + 5'
        }

        self.function_map = {
            'func1': func1, 'func2': func2, 'func3': func3,
            'func4': func4, 'func5': func5, 'square': square,
            'sine': sine, 'exp_plus_x': exp_plus_x,
            'linear': linear, 'polynomial': polynomial
        }

        input_frame = ttk.Frame(self.integration_tab)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Функция:").grid(row=0, column=0, padx=5, pady=5)
        self.func_combobox = ttk.Combobox(
            input_frame,
            values=list(functions.values()),
            state="readonly",
            width=25
        )
        self.func_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.func_combobox.current(0)
        self.func_combobox.bind('<<ComboboxSelected>>', self.update_function_name)
        self.current_func_name = 'func1'

        ttk.Label(input_frame, text="Нижний предел:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_integ_a = ttk.Entry(input_frame, width=20)
        self.entry_integ_a.grid(row=1, column=1, padx=5, pady=5)
        self.entry_integ_a.insert(0, "0")

        ttk.Label(input_frame, text="Верхний предел:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_integ_b = ttk.Entry(input_frame, width=20)
        self.entry_integ_b.grid(row=2, column=1, padx=5, pady=5)
        self.entry_integ_b.insert(0, "2")

        ttk.Label(input_frame, text="Количество шагов:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_integ_n = ttk.Entry(input_frame, width=20)
        self.entry_integ_n.grid(row=3, column=1, padx=5, pady=5)
        self.entry_integ_n.insert(0, "1000")

        btn_frame = ttk.Frame(self.integration_tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Вычислить интеграл", command=self.calculate_integration).pack()

        self.result_integ_label = ttk.Label(
            self.integration_tab,
            text="Результат: ",
            font=("Arial", 13)
        )
        self.result_integ_label.pack(pady=10)

    def update_function_name(self, event):
        functions = {
            'x² + 3x': 'func1',
            'x² + 3x + 1': 'func2',
            'x³ - 2x + 5': 'func3',
            'sin(x) + cos(x)': 'func4',
            '2x² - 4x + 1': 'func5',
            'x²': 'square',
            'sin(x)': 'sine',
            'e^x + x': 'exp_plus_x',
            '3x + 1': 'linear',
            'x⁴ - 2x³ + 3x² - 4x + 5': 'polynomial'
        }
        self.current_func_name = functions.get(self.func_combobox.get(), 'func1')

    def calculate_integration(self):
        try:
            a = float(self.entry_integ_a.get().replace(",", "."))
            b = float(self.entry_integ_b.get().replace(",", "."))
            n = int(self.entry_integ_n.get())

            if n <= 0:
                raise ValueError("Количество шагов должно быть положительным")

            func = self.function_map.get(self.current_func_name)
            if func is None:
                messagebox.showerror("Ошибка", "Функция не найдена")
                return

            result = self.calculator.integration.IntegrateOperation(func, a, b, n)
            self.result_integ_label.config(text=f"Результат: {result:.6f}")
            self.update_history()

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверные данные: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # ---------- ГРАФИКИ ----------
    def create_graph_tab(self):
        title = ttk.Label(self.graph_tab, text="Построение графиков", font=("Arial", 16))
        title.pack(pady=10)

        input_frame = ttk.Frame(self.graph_tab)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Выражение (используйте x):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_graph = ttk.Entry(input_frame, width=40)
        self.entry_graph.grid(row=0, column=1, padx=5, pady=5)
        self.entry_graph.insert(0, "sin(x)")

        ttk.Label(input_frame, text="От x (градусы):").grid(row=1, column=0, padx=5, pady=5)
        self.entry_graph_min = ttk.Entry(input_frame, width=20)
        self.entry_graph_min.grid(row=1, column=1, padx=5, pady=5)
        self.entry_graph_min.insert(0, "-360")

        ttk.Label(input_frame, text="До x (градусы):").grid(row=2, column=0, padx=5, pady=5)
        self.entry_graph_max = ttk.Entry(input_frame, width=20)
        self.entry_graph_max.grid(row=2, column=1, padx=5, pady=5)
        self.entry_graph_max.insert(0, "360")

        examples_label = ttk.Label(
            self.graph_tab,
            text="Примеры: sin(x), cos(x), tan(x), sqrt(x), sin(x)*cos(x)",
            font=("Arial", 10)
        )
        examples_label.pack(pady=5)

        btn_frame = ttk.Frame(self.graph_tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Построить график", command=self.plot_graph).pack()

        self.result_graph_label = ttk.Label(
            self.graph_tab,
            text="",
            font=("Arial", 10)
        )
        self.result_graph_label.pack(pady=5)

    def plot_graph(self):
        expression = self.entry_graph.get().strip()
        if not expression:
            messagebox.showerror("Ошибка", "Введите выражение")
            return

        try:
            x_min = float(self.entry_graph_min.get().replace(",", "."))
            x_max = float(self.entry_graph_max.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные границы")
            return

        if x_min >= x_max:
            messagebox.showerror("Ошибка", "Нижняя граница должна быть меньше верхней")
            return

        # Используем root.after для выполнения в главном потоке
        def plot_in_main_thread():
            graph_calc = GraphCalculator()
            success, msg = graph_calc.plot_expression(expression, x_min, x_max)
            self.result_graph_label.config(text=msg)
            if not success:
                messagebox.showerror("Ошибка", msg)

        # Запускаем построение в главном потоке через after
        self.root.after(100, plot_in_main_thread)

    # ---------- ИСТОРИЯ ----------
    def create_history_tab(self):
        title = ttk.Label(self.history_tab, text="История вычислений", font=("Arial", 16))
        title.pack(pady=10)

        self.history_text = scrolledtext.ScrolledText(
            self.history_tab,
            width=80,
            height=20,
            state="normal"
        )
        self.history_text.pack(padx=10, pady=10, fill="both", expand=True)

        btn_frame = ttk.Frame(self.history_tab)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Обновить", command=self.update_history).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Очистить историю", command=self.clear_history).pack(side='left', padx=5)

    def update_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)

        history_text = self.calculator.show_history()
        self.history_text.insert("1.0", history_text)
        self.history_text.config(state="disabled")

    def clear_history(self):
        self.calculator.clear_history()
        self.update_history()
        messagebox.showinfo("История", "История очищена.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()