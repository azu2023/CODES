import flet as ft
import base64
import cv2

cap = cv2.VideoCapture("Your video path")

class Countdown(ft.UserControl):
    def __init__(self):
        super().__init__()

    def did_mount(self):
        self.update_timer()

    def update_timer(self):
        while True:
            _, frame = cap.read()
            # frame = cv2.resize(frame,(400,400))
            _, im_arr = cv2.imencode('.png', frame)
            im_b64 = base64.b64encode(im_arr)
            self.img.src_base64 = im_b64.decode("utf-8")
            self.update()

    def build(self):
        self.img = ft.Image(
            border_radius=ft.border_radius.all(20)
        )
        return self.img

def height_changed(e):
    print(e.control.value)

section = ft.Container(
    margin=ft.margin.only(bottom=40),
    content=ft.Row([
        ft.Card(
            elevation=30,
            content=ft.Container(
                bgcolor=ft.colors.WHITE24,
                padding=10,
                border_radius = ft.border_radius.all(20),
                content=ft.Column([
                    Countdown(),
                    ft.Text("OPENCV WITH FLET",
                         size=20, weight="bold",
                         color=ft.colors.WHITE),
                ]
                ),
            )
        ),
        ft.Card(
            elevation=30,
            content=ft.Container(
                bgcolor=ft.colors.WHITE24,
                padding=10,
                border_radius=ft.border_radius.all(20),
                content=ft.Column([
                    ft.Slider(
                        min=500, max=900,on_change=lambda e:print(e.control.value)
                    ),
                    ft.Slider(
                        min=500, max=900,
                    )

                ]
                ),

            )
        )
    ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
)

def main(page: ft.Page):
    page.padding = 50
    page.window_left = page.window_left+100
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(
        section,
    )

if __name__ == '__main__':
    ft.app(target=main)
    cap.release()
    cv2.destroyAllWindows()
