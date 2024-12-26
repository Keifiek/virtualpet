import tkinter as tk
from PIL import Image, ImageTk

# Crear la ventana principal
root = tk.Tk()
root.overrideredirect(True)
root.attributes('-topmost', True)
root.wm_attributes('-transparentcolor', 'white')


walk_path = r"3 Dude_Monster/Dude_Monster_Walk_6.png"
death_path = r"3 Dude_Monster/Dude_Monster_Death_8.png"
# Cargar el sprite sheet
sprite_sheet = Image.open(walk_path)
sprite_width_total, sprite_height = sprite_sheet.size
num_frames = 6

# Calcular el ancho de cada frame
sprite_width = sprite_width_total // num_frames
scaled_sprite_width = sprite_width * 2
scaled_sprite_height = sprite_height * 2

frames = []

sprite_sheet_delete = Image.open(death_path)  # Cargar el sprite sheet
sprite_width_total_death, sprite_height_death = sprite_sheet_delete.size  # Ancho total y altura de la imagen del sprite sheet
num_frames_death = 8  # Número de frames en el sprite sheet
sprite_width_death = sprite_width_total_death // num_frames_death
scaled_sprite_width_death = sprite_width_death * 2
scaled_sprite_height_death = sprite_height_death * 2

frames_death = []

for i in range(num_frames_death):
    frame = sprite_sheet_delete.crop((i * sprite_width_death, 0, (i + 1) * sprite_width_death, sprite_height_death))
    frame = frame.resize((scaled_sprite_width_death, scaled_sprite_height_death), Image.LANCZOS)  # Redimensionar al doble
    frames_death.append(ImageTk.PhotoImage(frame))

for i in range(num_frames):
    frame = sprite_sheet.crop((i * sprite_width, 0, (i + 1) * sprite_width, sprite_height))
    frame = frame.resize((scaled_sprite_width, scaled_sprite_height), Image.LANCZOS)  # Redimensionar al doble
    frames.append(ImageTk.PhotoImage(frame))

# Crear los frames invertidos (espejo horizontal) usando Pillow
flipped_frames = []
for i in range(num_frames):
    frame = sprite_sheet.crop((i * sprite_width, 0, (i + 1) * sprite_width, sprite_height))
    flipped_frame = frame.transpose(Image.FLIP_LEFT_RIGHT)  # Invertir el frame
    flipped_frame = flipped_frame.resize((scaled_sprite_width, scaled_sprite_height),
                                         Image.LANCZOS)  # Redimensionar al doble
    flipped_frames.append(ImageTk.PhotoImage(flipped_frame))

# Ajustar el tamaño de la ventana al tamaño del sprite escalado
root.geometry(f"{scaled_sprite_width}x{scaled_sprite_height}")  # Ajustar la ventana al tamaño del frame escalado

# Etiqueta para mostrar la imagen
label = tk.Label(root, bd=0, bg="white")  # El fondo es blanco para que sea transparente
label.pack()

# Estado de movimiento
direction = 1  # 1 = derecha, -1 = izquierda
current_frames = frames  # Por defecto, empieza con los frames normales

# Variables para manejar el arrastre con el mouse
start_x = 0
start_y = 0


# Función para cambiar los frames de la animación
def animation(ind):
    frame = current_frames[ind]
    ind += 1
    if ind == len(current_frames):
        ind = 0
    label.config(image=frame)
    root.after(100, animation, ind)


# Función para mover al personaje por la pantalla y cambiar dirección si llega al borde
def move_shimeji():
    global direction, current_frames

    # Obtener la posición actual
    current_x = root.winfo_x() + (2 * direction)
    current_y = root.winfo_y()

    # Detectar los bordes de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Ajustar la posición en Y por encima de la barra de tareas (20-40 píxeles más arriba de la parte inferior)
    taskbar_height = 40  # Ajusta según el tamaño de tu barra de tareas
    current_y = screen_height - scaled_sprite_height - taskbar_height

    # Cambiar de dirección si llega al borde derecho o izquierdo
    if current_x <= 0:
        direction = 1  # Cambiar a la derecha
        current_frames = frames  # Usar los frames originales
    elif current_x + scaled_sprite_width >= screen_width:
        direction = -1  # Cambiar a la izquierda
        current_frames = flipped_frames  # Usar los frames invertidos (espejo)

    # Mover la ventana
    root.geometry(f"+{current_x}+{current_y}")

    # Volver a llamar a la función después de 50 ms
    root.after(50, move_shimeji)


# Funciones para manejar el arrastre con el mouse
def on_click(event):
    global start_x, start_y

    start_x = event.x
    start_y = event.y


def on_drag(event):
    new_x = root.winfo_x() + (event.x - start_x)
    new_y = root.winfo_y() + (event.y - start_y)

    root.geometry(f"+{new_x}+{new_y}")

def delete(event):
    global current_frames
    current_frames = frames_death
    root.after(600, root.destroy)




# Vincular los eventos de clic y arrastre del mouse a la ventana
label.bind("<Button-1>", on_click)  # Detectar el clic
label.bind("<B1-Motion>", on_drag)  # Detectar el movimiento mientras se mantiene el clic

label.bind("<Button-3>", delete)

# Iniciar la animación y el movimiento
root.after(0, animation, 0)
root.after(0, move_shimeji)

# Iniciar el loop de la ventana
root.mainloop()
