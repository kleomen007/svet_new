from gpiozero import MotionSensor
from picamera import PiCamera
import requests
import logging
from time import sleep
from urllib.request import urlopen
from signal import pause

# Настройки
TOKEN = '7010897855:AAEH5EPyYjn9HE7s9bC1uAjC6wSVnzHOnLk'
CHAT_ID = '2190977460'
PIR_PIN = 18
PHOTO_PATH = '/tmp/photo.jpg'
CAMERA_RESOLUTION = (1024, 768)

# Настройка логгирования
logging.basicConfig(
    filename='/var/log/camera_motion.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_camera():
    try:
        camera = PiCamera()
        camera.rotation = 180  # Поворот на 180°
        camera.resolution = CAMERA_RESOLUTION
        sleep(2)  # Прогрев камеры
        return camera
    except Exception as e:
        logging.error(f"Ошибка камеры: {str(e)}")
        return None

def check_internet():
    try:
        urlopen("https://google.com", timeout=3)
        return True
    except:
        return False

def send_photo():
    try:
        with open(PHOTO_PATH, 'rb') as photo:
            url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
            response = requests.post(url, files={'photo': photo}, data={'chat_id': CHAT_ID})
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Ошибка отправки: {str(e)}")
        return False

def take_photo(camera):
    try:
        camera.capture(PHOTO_PATH)
        return True
    except Exception as e:
        logging.error(f"Ошибка съёмки: {str(e)}")
        return False

def main():
    logging.info("Запуск скрипта...")
    
    # Ждём интернет (если нужно)
    for _ in range(10):
        if check_internet():
            break
        sleep(3)
    else:
        logging.error("Нет интернета!")
        return

    # Инициализация камеры
    camera = setup_camera()
    if not camera:
        return

    # Настройка датчика движения
    pir = MotionSensor(PIR_PIN)
    
    def on_motion():
        logging.info("Движение обнаружено!")
        if take_photo(camera) and check_internet():
            send_photo()
    
    pir.when_motion = on_motion
    logging.info("Ожидание движения...")
    pause()

if __name__ == "__main__":
    main()