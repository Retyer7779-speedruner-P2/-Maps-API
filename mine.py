import os
import sys
import requests
import arcade

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 450
WINDOW_TITLE = "MAP"
MAP_FILE = "map.png"


class GameView(arcade.Window):
    def setup(self):
        self.lon = 0
        self.lat = 0
        self.z = 2
        self.get_image()

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(
                (self.width - self.background.width) // 2,
                (self.height - self.background.height) // 2,
                self.background.width,
                self.background.height
            ),
        )

    def get_image(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        # Готовим запрос.

        params = {
            "ll": ",".join([str(self.lon), str(self.lat)]),
            "z": self.z,
            "apikey": api_key,
        }

        response = requests.get(server_address, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        with open(MAP_FILE, "wb") as file:
            file.write(response.content)

        self.background = arcade.load_texture(MAP_FILE)


def main():
    gameview = GameView(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    gameview.setup()
    arcade.run()
    # Удаляем за собой файл с изображением.
    os.remove(MAP_FILE)


if __name__ == "__main__":
    main()


