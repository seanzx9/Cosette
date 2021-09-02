from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.animation import Animation
import cosette as c

#set window size
Window.size = (500, 500)

#.kv file
Builder.load_file("layout.kv")


class MyLayout(Widget):
    def process_input(self):
        #text input variable
        text = self.ids.input_field.text

        #process input and set output field to result
        self.ids.output_field.text = c.process(text)

        #exit program on command
        if self.ids.output_field.text == "Bye bye":
            exit()

        #animate text
        self.ids.output_field.x = 0
        self.ids.output_field.y = -Window.height
        animation = Animation(pos=(0, 0), duration=0.5, t="out_cubic")
        animation.start(self.ids.output_field)

        #clear input box
        self.ids.input_field.text = ""


class CosetteApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    CosetteApp().run()
