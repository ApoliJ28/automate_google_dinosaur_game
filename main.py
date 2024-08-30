import pyautogui
import time
from PIL import ImageGrab
import numpy as np

def get_dino_position(image_path='dino.png'):
    """Encuentra la posición del dinosaurio en la pantalla."""
    dino_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)
    return dino_location

def get_background_color():
    """Obtiene el color de fondo del juego en la posición actual del mouse utilizando Pillow."""
    mouse_pos = pyautogui.position()
    x, y = mouse_pos[0], mouse_pos[1]

    # Captura una pequeña región alrededor del mouse
    img = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
    pixel = img.getpixel((0, 0))
    
    return pixel

def is_obstacle_present(original_x, y_range, background_color):
    """Detecta si hay un obstáculo en la pantalla comparando los píxeles con el color de fondo."""
    for x in range(int(original_x), int(original_x) + 70): 
        for y in y_range:
            pixel_color = pyautogui.screenshot(region=(x, y, 1, 1)).getpixel((0, 0))
            if pixel_color != background_color:
                return True
    return False

def main():
    # Configuración inicial del navegador y apertura del juego
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://elgoog.im/dinosaur-game/")
    driver.maximize_window()

    time.sleep(2)  # Esperar a que se cargue el juego
    pyautogui.press('up')  # Iniciar el juego, salta

    time.sleep(5)  # Esperar a que el juego se estabilice

    # Obtener la posición inicial del dinosaurio y el color de fondo
    dino_position = get_dino_position()
    if dino_position is None:
        print("No se pudo encontrar el dinosaurio en la pantalla.")
        return
    
    print(f'Dino Position: {dino_position}')
    background_color = get_background_color()
    print(f'Background Color: {background_color}')

    original_x = 100
    y_range = range(760, 780)  # Rango vertical donde se buscan obstáculos

    is_jumping = False

    while True:
        if is_obstacle_present(original_x, y_range, background_color):
            if not is_jumping:
                pyautogui.press('up')  # Saltar si se detecta un obstáculo
                is_jumping = True

        # Ajusta el valor de original_x para el movimiento del juego
        original_x += 0.1

if __name__ == "__main__":
    main()
