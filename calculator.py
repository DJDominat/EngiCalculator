import math
import matplotlib.pyplot as plt
import numpy as np


class History:
    """Класс для управления историей вычислений"""

    def __init__(self):
        self._history = []

    def add_record(self, category, operation, result):
        self._history.append({
            "category": category,
            "operation": operation,
            "result": result
        })

    def show(self):
        """Красивый постраничный вывод истории в консоль"""
        if not self._history:
            print("История пуста")
            return
        print("\n" + "=" * 50)
        print("ИСТОРИЯ ОПЕРАЦИЙ")
        print("=" * 50)
        for i, r in enumerate(self._history, 1):
            print(f"[Запись #{i}] [{r['category']}]")
            print(f"  Выражение: {r['operation']}")
            print(f"  Результат: {r['result']}")
            print("-" * 50)

    def clear(self):
        self._history.clear()


class BC:
    """Базовый класс (Арифметика)"""

    def __init__(self):
        self.history = History()
        self.mode = "rad"  # rad или degree

    def add(self, a, b):
        res = a + b
        self.history.add_record("Арифметика", f"{a} + {b}", res)
        return res

    def subtract(self, a, b):
        res = a - b
        self.history.add_record("Арифметика", f"{a} - {b}", res)
        return res

    def divide(self, a, b):
        if b == 0:
            res = "Ошибка: Деление на ноль!"
        else:
            res = a / b
        self.history.add_record("Арифметика", f"{a} / {b}", res)
        return res

    def multiply(self, a, b):
        res = a * b
        self.history.add_record("Арифметика", f"{a} * {b}", res)
        return res


class TrigCalculate(BC):
    """Инженерный класс (Тригонометрия)"""

    def _convert(self, val, to_rad=True):
        if self.mode == "degree":
            return math.radians(val) if to_rad else round(math.degrees(val), 10)
        return val

    def sin(self, a):
        res = round(math.sin(self._convert(a)), 10)
        self.history.add_record("Тригонометрия", f"sin({a})", res)
        return res

    def cos(self, a):
        res = round(math.cos(self._convert(a)), 10)
        self.history.add_record("Тригонометрия", f"cos({a})", res)
        return res

    def tan(self, a):
        if self.mode == "degree" and (a - 90) % 180 == 0:
            return "Ошибка угла!"
        res = round(math.tan(self._convert(a)), 10)
        self.history.add_record("Тригонометрия", f"tan({a})", res)
        return res

    def cot(self, a):
        if self.mode == "degree" and a % 180 == 0:
            return "Ошибка угла!"
        res = round(1 / math.tan(self._convert(a)), 10)
        self.history.add_record("Тригонометрия", f"cot({a})", res)
        return res

    def asin(self, val):
        if not (-1 <= val <= 1):
            return "Ошибка диапазона!"
        res = self._convert(math.asin(val), to_rad=False)
        self.history.add_record("Тригонометрия", f"asin({val})", res)
        return res

    def acos(self, val):
        if not (-1 <= val <= 1):
            return "Ошибка диапазона!"
        res = self._convert(math.acos(val), to_rad=False)
        self.history.add_record("Тригонометрия", f"acos({val})", res)
        return res

    def atan(self, val):
        res = self._convert(math.atan(val), to_rad=False)
        self.history.add_record("Тригонометрия", f"atan({val})", res)
        return res

    def acot(self, val):
        res = self._convert(math.pi / 2 - math.atan(val), to_rad=False)
        self.history.add_record("Тригонометрия", f"acot({val})", res)
        return res


class MatrixCalculate(TrigCalculate):
    """Высший класс цепочки (Матрицы)"""

    def matrix_add(self, m1, m2):
        if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
            return "Ошибка: Размеры матриц не совпадают!"
        res = [
            [m1[i][j] + m2[i][j] for j in range(len(m1[0]))]
            for i in range(len(m1))
        ]
        self.history.add_record("Матрицы", f"{m1} + {m2}", res)
        return res

    def matrix_multiply(self, m1, m2):
        if len(m1[0]) != len(m2):
            return "Ошибка: Несовместимые размеры матриц!"
        res = [
            [
                sum(m1[i][k] * m2[k][j] for k in range(len(m2)))
                for j in range(len(m2[0]))
            ]
            for i in range(len(m1))
        ]
        self.history.add_record("Матрицы", f"{m1} * {m2}", res)
        return res

    def matrix_det_2x2(self, m):
        if len(m) != 2 or len(m[0]) != 2:
            return "Ошибка: Матрица должна быть 2x2!"
        res = m[0][0] * m[1][1] - m[0][1] * m[1][0]
        self.history.add_record("Матрицы", f"det({m})", res)
        return res


class IntegrationCalculator:
    """Класс для численного интегрирования"""

    def __init__(self, history):
        self._history = history
        self.functions = {}

    def add_function(self, name, func):
        self.functions[name] = func

    def integrate(self, func_name, a, b, n=1000):
        """
        Вычисляет определенный интеграл методом трапеций
        func_name - имя функции (строка)
        a - нижняя граница
        b - верхняя граница
        n - количество шагов разбиения
        """
        if func_name not in self.functions:
            raise ValueError(f"Функция '{func_name}' не найдена!")

        func = self.functions[func_name]

        if n <= 0:
            raise ValueError("Количество шагов разбиения должно быть больше нуля!")

        h = (b - a) / n
        total = 0.5 * (func(a) + func(b))
        for i in range(1, n):
            total += func(a + i * h)

        result = total * h
        self._history.add_record(
            "Интегрирование",
            f"∫ от {a} до {b} для {func_name} (n={n})",
            result
        )
        return result


class InteractiveGraphCalculator:
    """Графический калькулятор с поддержкой общей истории"""

    def __init__(self, history):
        self._history = history
        self.functions_to_plot = []
        self.plots_data = []
        self.current_index = 0
        self.x = np.linspace(-10, 10, 500)
        self.fig = None
        self.ax = None

    def plot_operation(self, *functions):
        """
        Построение одного или нескольких графиков.
        Пример:
        graph.plot_operation("np.sin(x)", "np.cos(x)", "x**2")
        """
        self.functions_to_plot = list(functions)
        self.plots_data = []
        self.current_index = 0

        self.fig, self.ax = plt.subplots(figsize=(11, 6))
        self.fig.canvas.mpl_connect("key_press_event", self._on_key)

        self._prepare_data()

        if self.plots_data:
            self._update_graph()
            plt.show()
        else:
            print("Нет корректных функций для построения.")

    def _prepare_data(self):
        for expr in self.functions_to_plot:
            try:
                y = eval(
                    expr,
                    {"__builtins__": None},
                    {"np": np, "x": self.x}
                )
                self.plots_data.append({
                    "expr": expr,
                    "y": y,
                    "type": "single"
                })
                self._history.add_record(
                    "Графики",
                    f"Построение y={expr}",
                    "Успешно"
                )
            except Exception as e:
                self._history.add_record(
                    "Графики",
                    f"Построение y={expr}",
                    f"Ошибка: {type(e).__name__}"
                )
                print(f"Ошибка в функции {expr}")

        if self.plots_data:
            self.plots_data.append({"type": "history"})

    def _update_graph(self):
        self.ax.clear()
        self.ax.axhline(0, color="black")
        self.ax.axvline(0, color="black")
        self.ax.grid(True)

        current = self.plots_data[self.current_index]

        if current["type"] == "single":
            self.ax.plot(
                self.x,
                current["y"],
                linewidth=2,
                label=f"y={current['expr']}"
            )
            self.ax.set_title(
                f"График {self.current_index+1} из {len(self.plots_data)-1}\n"
                "Пробел — следующий график"
            )
            y = current["y"][np.isfinite(current["y"])]
            if len(y):
                self.ax.set_ylim(
                    max(np.min(y)-1, -20),
                    min(np.max(y)+1, 20)
                )
            self.ax.legend()

        else:
            ymin = -5
            ymax = 5
            for plot in self.plots_data[:-1]:
                self.ax.plot(
                    self.x,
                    plot["y"],
                    label=f"y={plot['expr']}"
                )
                y = plot["y"][np.isfinite(plot["y"])]
                if len(y):
                    ymin = min(ymin, np.min(y)-1)
                    ymax = max(ymax, np.max(y)+1)

            self.ax.set_ylim(
                max(ymin, -30),
                min(ymax, 30)
            )
            self.ax.set_title(
                "Все графики\nПробел — вернуться к первому"
            )
            self.ax.legend(bbox_to_anchor=(1, 1), loc="upper left")

        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.fig.canvas.draw()

    def _on_key(self, event):
        if event.key == " ":
            self.current_index += 1
            if self.current_index >= len(self.plots_data):
                self.current_index = 0
            self._update_graph()


# ============================================================
# СОЗДАНИЕ ОБЩЕГО КАЛЬКУЛЯТОРА
# ============================================================

class EngineeringCalculator(MatrixCalculate):
    """Супер-калькулятор, объединяющий всю функциональность"""

    def __init__(self):
        super().__init__()
        self.integration = IntegrationCalculator(self.history)
        self.graph = InteractiveGraphCalculator(self.history)