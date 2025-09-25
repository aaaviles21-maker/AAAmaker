import tkinter as tk
from tkinter import messagebox

class DivisibilityVisualizer(tk.tk):
    """
    Una aplicación visual para entender la divisibilidad de los números,
    los números primos y los compuestos.
    """
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Divisibilidad")
        self.geometry("850x700")

        # --- Marcos (Frames) para organizar la ventana ---
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)

        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(pady=10, expand=True, fill=tk.BOTH)
        
        # --- Controles de Usuario (Entradas y Botón) ---
        tk.Label(control_frame, text="Número (1-100):").grid(row=0, column=0, padx=5)
        self.number_entry = tk.Entry(control_frame, width=10)
        self.number_entry.grid(row=0, column=1, padx=5)

        tk.Label(control_frame, text="Agrupar en grupos de:").grid(row=0, column=2, padx=5)
        self.group_size_entry = tk.Entry(control_frame, width=10)
        self.group_size_entry.grid(row=0, column=3, padx=5)

        self.visualize_button = tk.Button(control_frame, text="Visualizar Agrupación", command=self.visualize)
        self.visualize_button.grid(row=0, column=4, padx=10)

        # --- Lienzo para dibujar ---
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # --- Etiquetas para mostrar mensajes ---
        self.message_label = tk.Label(self, text="Ingresa un número y un tamaño de grupo para comenzar.", font=("Arial", 12))
        self.message_label.pack(pady=10)

        self.prime_composite_label = tk.Label(self, text="", font=("Arial", 14, "bold"))
        self.prime_composite_label.pack(pady=5)
        
        self.divisors_label = tk.Label(self, text="", font=("Arial", 11))
        self.divisors_label.pack(pady=5)

    def is_prime(self, n):
        """Verifica si un número es primo."""
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def get_divisors(self, n):
        """Obtiene todos los divisores de un número."""
        divisors = []
        for i in range(1, n + 1):
            if n % i == 0:
                divisors.append(i)
        return divisors

    def visualize(self):
        """Función principal que maneja la visualización."""
        try:
            number = int(self.number_entry.get())
            group_size = int(self.group_size_entry.get())

            if not (1 <= number <= 100):
                messagebox.showerror("Error", "Por favor, ingresa un número entre 1 y 100.")
                return
            if group_size <= 0:
                messagebox.showerror("Error", "El tamaño del grupo debe ser un número positivo.")
                return

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa números enteros válidos.")
            return

        self.canvas.delete("all")
        
        # --- Lógica de Divisibilidad ---
        is_divisible = (number % group_size == 0)

        if is_divisible:
            self.message_label.config(text=f"¡División Exacta! {number} es divisible por {group_size}.", fg="green")
        else:
            self.message_label.config(text=f"División No Exacta. {number} no es divisible por {group_size}.", fg="red")

        # --- Lógica de Números Primos y Compuestos ---
        divisors = self.get_divisors(number)
        if self.is_prime(number):
            self.prime_composite_label.config(text=f"{number} es un número PRIMO", fg="#00008B") # DarkBlue
        else:
            self.prime_composite_label.config(text=f"{number} es un número COMPUESTO", fg="#FF8C00") # DarkOrange
        self.divisors_label.config(text=f"Divisores de {number}: {', '.join(map(str, divisors))}")

        # --- Lógica de Dibujo ---
        ball_radius = 15
        padding = 10
        balls_per_row = 10 
        
        x_start = 40
        y_start = 40
        x, y = x_start, y_start
        
        balls_drawn = 0
        group_id = 0

        while balls_drawn < number:
            balls_in_this_group = min(group_size, number - balls_drawn)
            
            # Determinar el color del grupo
            is_complete = (balls_in_this_group == group_size)
            outline_color = "green" if is_complete else "red"

            coords = []
            
            group_x_start, group_y_start = x, y

            for i in range(balls_in_this_group):
                x1, y1 = x - ball_radius, y - ball_radius
                x2, y2 = x + ball_radius, y + ball_radius
                self.canvas.create_oval(x1, y1, x2, y2, fill="skyblue", outline="blue", width=2)
                coords.append((x1, y1, x2, y2))
                
                balls_drawn += 1
                
                if (i + 1) % balls_per_row == 0:
                    x = group_x_start
                    y += ball_radius * 2 + padding
                else:
                    x += ball_radius * 2 + padding
            
            # --- Dibujar el rectángulo alrededor del grupo ---
            if coords:
                min_x = min(c[0] for c in coords) - padding
                min_y = min(c[1] for c in coords) - padding
                max_x = max(c[2] for c in coords) + padding
                max_y = max(c[3] for c in coords) + padding
                self.canvas.create_rectangle(min_x, min_y, max_x, max_y, outline=outline_color, width=3)

            # Preparar la posición para el siguiente grupo
            y = group_y_start
            x = max_x + padding * 2
            
            if x > self.canvas.winfo_width() - (balls_per_row * (ball_radius * 2 + padding)):
                x = x_start
                y = max_y + padding * 2

if __name__ == "__main__":
    app = DivisibilityVisualizer()

    app.mainloop()
