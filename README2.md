Создаём сервис:
sudo nano /etc/systemd/system/camera_motion.service

Вставляем конфиг:
#----------------------------

[Unit]
Description=Motion Camera Telegram Bot
After=network-online.target  # Ждём интернет!
Wants=network-online.target  # Обязательно для Wi-Fi

[Service]
Type=simple
User=pi
ExecStart=/usr/bin/python3 /home/pi/your_script.py
Restart=on-failure  # Перезапуск при ошибках
RestartSec=10s      # Ждать 10 сек перед перезапуском
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target

#---------------------------

Включаем сервис:
sudo systemctl daemon-reload
sudo systemctl enable camera_motion.service
sudo systemctl start camera_motion.service

Проверка работы
journalctl -u camera_motion.service -f  # Логи в реальном времени
cat /var/log/camera_motion.log          # Файловые логи

pip install -r requirements.txt