Создаём сервис:
sudo nano /etc/systemd/system/camera_motion.service

Вставляем конфиг:
#----------------------------

[Unit]
Description=Мой Python-скрипт
After=network.target  # Зависимости (например, ждём загрузки сети)

[Service]
Type=simple
User=username       # Пользователь, от которого запускается скрипт
WorkingDirectory=/path/to/script  # Директория, где лежит скрипт
ExecStart=/usr/bin/python3 /path/to/script/your_script.py  # Команда запуска
Restart=on-failure  # Перезапускать при ошибках
RestartSec=5        # Ждать 5 секунд перед перезапуском

[Install]
WantedBy=multi-user.target  # Запускать при загрузке системы


#---------------------------

Включаем сервис:
sudo systemctl daemon-reload
sudo systemctl enable camera_motion.service
sudo systemctl start camera_motion.service

Проверка работы
journalctl -u camera_motion.service -f  # Логи в реальном времени
cat /var/log/camera_motion.log          # Файловые логи

pip install -r requirements.txt
