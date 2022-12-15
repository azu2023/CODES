from tkinter import Label, Scale, Tk,Button,StringVar,Entry
from PIL import Image, ImageTk
import cv2
import numpy as np


win = Tk()
win.geometry('750x600+600+100')
win_color = '#c8bdad'
win.configure(bg=win_color)
lens_img = cv2.imread('./lens.png') #your lens image , png transparent image
background = cv2.imread('./cat.jpg')
background = cv2.resize(background, (500, 400))
lens_img = cv2.resize(lens_img, (80, 80))
H, W = background.shape[:2]
h,w = 80,80

hints = StringVar()
hints2 = StringVar()
class Lense():
    def __init__(self):
        self.screen = Label(win, bg='red', bd=1)
        self.screen.place(x=10, y=10)
        self.lens = Label(self.screen, bg='red', bd=1)
        self.zoom = Scale(win, from_=2, to_=45,bg=win_color, fg="red", orient='horizontal')
        self.zoom.set(20)
        self.zoom.place(x=10, y=H + 30, width=W)
        self.picker_btn = Button(win,text='Picker off',bd=0,command=self.Picker)
        self.picker_btn.place(x=W+50,y=30,width=80)
        self.color_label = Label(win,bg="gray17")
        self.color_label.place(x=W+50,y=110,width=80,height=100)
        self.picker_count = 0
        self.picker_key = False
        self.input = Entry(win)
        self.input.place(x=W+50,y=240,width=80)
        self.input2 = Entry(win)
        self.input2.place(x=W + 50, y=340, width=80)

        self.Play()

    def Picker(self):
        self.picker_count +=1
        if self.picker_count ==1:
            self.picker_key = True
            self.picker_btn['text']='Picker on'
        if self.picker_count ==2:
            self.picker_key = False
            self.picker_btn['text']='Picker off'
            self.picker_count = 0

    def rgb2hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def capture_color(self, img, y, x):
        color = img[y, x, :]
        

        b, g, r = color
        rgb = self.rgb2hex((r, g, b))
        hints.set(rgb)
        self.input['textvariable'] = hints
        hints2.set(f"{r},{g},{b}")#for opencv and rgb for the rest of use
        self.input2['textvariable'] = hints2
        self.color_label['bg'] = rgb

    def to_pil(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img)
        pic = ImageTk.PhotoImage(image)
        return pic

    def put_lense(self, background, width, height, x, y):
        border = self.zoom.get()
        magn = background[y + border:(h + y) - border, x + border:(w + x) - border]
        magn = cv2.resize(magn, (h, w))
        return magn

    def mouse_move(self, e):
        x, y = e.x, e.y
        if x + w >= W:
            x = W - w
        if y + h >= H:
            y = H - h
        if x <= 0:
            x = 0
        if y <= 0:
            y = 0

        mag = self.put_lense(background, w, h, x, y)
        if self.picker_key == True:
            cv2.circle(mag, (int(w/2),int(h/2)), 5, (0, 0, 220), 2)
            self.capture_color(mag,int(h/2),int(w/2))
        else:
            pass
        pic = self.to_pil(mag)
        self.lens.config(image=pic)
        self.lens.image = pic
        self.lens.place(x=x, y=y)

    def Play(self):
        self.screen.bind('<B1-Motion>', self.mouse_move)
        pic = self.to_pil(background)
        self.screen.configure(image=pic)
        self.screen.image = pic

if __name__ == '__main__':
    Lense()
    win.mainloop()
cv2.destroyAllWindows()
