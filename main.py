from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# Настройки сервера
hostName = "localhost"
serverPort = 8080


class MyHandler(SimpleHTTPRequestHandler):
    """ Обработчик HTTP-запросов """
    def do_GET(self):
        # Если запрашивается корень, перенаправляем на index.html
        if self.path == '/':
            self.path = 'index.html'
        elif self.path == '/catalog':
            self.path = 'catalog.html'
        elif self.path == '/about':
            self.path = 'about.html'
        elif self.path == '/contact':
            self.path = 'contact.html'
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        # Проверка, что запрос отправлен на /contact
        if self.path == '/contact':
            # Обработка POST-запроса
            content_length = int(self.headers['Content-Length'])  # Длина содержимого
            post_data = self.rfile.read(content_length).decode('utf-8')  # Чтение данных
            postvars = parse_qs(post_data)  # Парсинг данных из формы

            # Печать данных в консоль
            print("Получены данные POST-запроса:")
            if not postvars:
                print("Данные не были получены. Проверьте правильность формы.")
            for key, value in postvars.items():
                print(f"{key}: {value}")  # Выводим ключ и значения (каждый элемент)

            # Отправляем обратно HTML-страницу после получения POST-запроса
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # Чтение содержимого HTML-файла
            with open('contact.html', 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Отправка HTML-кода в ответе
            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.send_error(404, "File not found")


if __name__ == "__main__":
    # Инициализация веб-сервера
    webServer = HTTPServer((hostName, serverPort), MyHandler)
    print(f"Сервер запущен на http://{hostName}:{serverPort}")

    try:
        # Запуск сервера
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер
        pass

    # Остановка сервера
    webServer.server_close()
    print("Сервер остановлен.")
