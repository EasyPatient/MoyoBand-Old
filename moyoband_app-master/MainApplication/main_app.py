from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from kivy.uix.button import Button
from csv import DictReader
import os
from kivy.core.text import LabelBase
from kivy.uix.carousel import Carousel

from NFC_script.ReadRFID import read_rfid
from data_base.CRUD import AddPatient, AddBand

# Including Century Gothic to project
LabelBase.register(name="century_gothic", fn_regular='century_gothic.ttf', fn_bold='century_gothicB.TTF')

# File path multi-user unification
MAIN_DIR_PATH = os.path.split(os.getcwd())[0]

GRAPHICS_DIR_NAME = 'App_Graphics'
DATA_DIR_NAME = 'fake_data_generator'

GRAPHICS_DIR_PATH = os.path.join(MAIN_DIR_PATH, GRAPHICS_DIR_NAME)
DATA_DIR_PATH = os.path.join(MAIN_DIR_PATH, DATA_DIR_NAME)


# returns list of patient data that looks like this
# [id, first_name, last_name, heart_rate, temperature, saturation, medical_description, age, weight, medicaments]
def get_data(bed_id):
    with open(os.path.join(DATA_DIR_PATH, 'fake_data.txt'), encoding="utf-8") as fake_data:
        csv_dict_reader = DictReader(fake_data)

        first_row = next(csv_dict_reader)
        if first_row['bed_id'] == str(bed_id):  # I know it's ugly but I don't have a better idea
            return first_row

        for line in csv_dict_reader:
            if line['bed_id'] == str(bed_id):
                return line


# Checks for the patient's life status returning 1 for acceptable and -1 for lack of patient
def get_patient_status(bed_id):
    label_data = get_data(bed_id)
    heart_rate = label_data['heart_rate']
    temperature = label_data['temperature']
    saturation = label_data['saturation']
    medical_description = label_data['medical_description']
    if medical_description == 'No Info\n':
        return -1
    if not (50 < float(heart_rate) < 120) or 37 < float(temperature) < 38 or float(saturation) < 70:
        return 0
    return 1


class ImageButton(ButtonBehavior, Image):
    pressed = BooleanProperty(False)
    changed_data = BooleanProperty(False)

    def __init__(self, bed_id, **kwargs):
        super().__init__(**kwargs)
        self.bed_id = bed_id
        self.popup = MyPopup(self.bed_id)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = True
            return True
        return super(ImageButton, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        if not self.pressed:
            return
        self.update_info()  # updates heart_rate, temperature and so on before displaying this info
        self.pressed = False
        self.popup.open()

    def update_info(self):
        self.popup = MyPopup(self.bed_id)


# Created solely for the freedom of available number of widgets (Popup default only takes 1) also lets more control
# of the Popup's behaviour letting update the data in Label
class MyPopup(Popup):
    opened = BooleanProperty(True)

    def __init__(self, bed_id, **kwargs):
        super(MyPopup, self).__init__(**kwargs)
        self.bed_id = bed_id
        self.label_data = get_data(self.bed_id)
        self.title = f'Bed of number: {self.bed_id}'
        self.title_size = 35
        self.title_font = 'century_gothic'
        self.title_color = [77 / 256, 125 / 256, 147 / 256, 1]
        self.separator_color = [77 / 256, 125 / 256, 147 / 256, 1]
        self.size_hint = 0.45, 0.7
        if Window.size == (1920, 1080):
            self.y = 30
        elif Window.size == (1366, 768):
            self.y = 20
        self.background = os.path.join(GRAPHICS_DIR_PATH, 'background2.png')
        self.content = RelativeLayout()
        self.label = self.get_label()
        self.content.add_widget(self.label)
        # self.content.add_widget(Button(size_hint=(0.15, 0.20), pos_hint={'right': 1.01, 'top': 1.18},
        #                                background_normal=join(GRAPHICS_DIR_PATH, 'x.png'),
        #                                background_down=join(GRAPHICS_DIR_PATH, 'x_down.png'), on_press=self.dismiss))
        self.content.add_widget(Image(source=os.path.join(GRAPHICS_DIR_PATH, 'patient_history.png'),
                                      size_hint=(0.09, 0.09), pos_hint={'top': 0.9005}))
        self.content.add_widget(Image(source=os.path.join(GRAPHICS_DIR_PATH, 'medicaments.png'),
                                      size_hint=(0.09, 0.09), pos_hint={'top': 0.791}))
        self.content.add_widget(Image(source=os.path.join(GRAPHICS_DIR_PATH, 'pulse.png'),
                                      size_hint=(0.09, 0.09), pos_hint={'top': 0.289}))
        self.content.add_widget(Image(source=os.path.join(GRAPHICS_DIR_PATH, 'saturation.png'),
                                      size_hint=(0.09, 0.09), pos_hint={'top': 0.237}))
        self.content.add_widget(Image(source=os.path.join(GRAPHICS_DIR_PATH, 'temperature.png'),
                                      size_hint=(0.09, 0.09), pos_hint={'top': 0.185}))

    def get_label(self):
        text = self.get_text()
        return Label(text=text, markup=True, id='med_label', color=[77 / 256, 125 / 256, 147 / 256, 1],
                     font_size=self.y, font_name='century_gothic', pos_hint={'top': 1, 'right': 1})

    def get_text(self):
        return (f'[color=4d7d93][b]Medical description: [/b]{self.label_data["medical_description"]}' +
                f'\n[b]Medicaments: [/b]{self.label_data["medicaments"]}' +
                f'\n\n\n[b]First name: [/b]{self.label_data["first_name"]}' +
                f'\n[b]Surname: [/b]{self.label_data["last_name"]}' +
                f'\n[b]Age: [/b]{self.label_data["age"]} years old' +
                f'\n[b]Weight: [/b]{self.label_data["weight"]} kg' +
                f'\n\n\n[b]Heart rate: [/b]{self.label_data["heart_rate"]} bpm' +
                f'\n[b]Saturation: [/b]{self.label_data["saturation"]}%' +
                f'\n[b]Temperature: [/b]{self.label_data["temperature"]}°C[/color]')

    def update_info(self):
        self.label_data = get_data(self.bed_id)
        self.label.text = self.get_text()


# Creating Room - Button Layout
class MyWidget(FloatLayout):
    def __init__(self, rooms_num, bed_count, **kwargs):
        super().__init__(**kwargs)
        self.rooms_num = 0
        self.beds_per_room = [0] * rooms_num
        self.beds = dict()
        self.background_source = os.path.join(GRAPHICS_DIR_PATH, 'background.png')
        self.room_source = os.path.join(GRAPHICS_DIR_PATH, 'room')
        self.blue_source = os.path.join(GRAPHICS_DIR_PATH, 'blue')
        self.grey_source = os.path.join(GRAPHICS_DIR_PATH, 'grey')
        self.red_source = os.path.join(GRAPHICS_DIR_PATH, 'red')
        self.green_source = os.path.join(GRAPHICS_DIR_PATH, 'green')
        self.add_widget(Image(source=self.background_source, size=self.size, pos=self.pos))
        for room_num in range(1, rooms_num + 1):
            self.add_room()
            for bed_num in range(1, bed_count + 1):
                self.add_bed(room_num)
                
                
        cen_x = .15 + .033 * 3 + .2 * 1
        cen_y = .22
        add_patient_button = Button(size_hint=(.033, .1), pos_hint={'center_x': cen_x, 'center_y': cen_y})

        def wait_for_band(instance):
            #nfc_result = bytearray([0x5F,0xA3,0xF8,0x28,0xB0,0x94,0x20])
            mac = read_rfid()
            name = "kac"
            surname = "sala"
            age = 69
            sex = "male"
            room = 2
            bed = 1

            # adding patient and band to database
            # AddPatient(name, surname, age, sex)
            # AddBand(surname, mac, room, bed)
            
            pl = BoxLayout(orientation='vertical')

            name_in = TextInput(text="name")
            surname_in = TextInput(text="surname")
            age_in = TextInput(text="age")
            sex_in = TextInput(text="sex")
            cb = Button(text="Cancel")

            pl.add_widget(name_in)
            pl.add_widget(surname_in)
            pl.add_widget(age_in)
            pl.add_widget(sex_in)
            pl.add_widget(cb)

            band_wait_popup = Popup(title="Wait for band to connect", content=pl, size_hint=(None, None),
                                    size=(400, 400))
            cb.bind(on_press=band_wait_popup.dismiss)
            band_wait_popup.open()

        add_patient_button.bind(on_press=wait_for_band)
        self.add_widget(add_patient_button)

        Clock.schedule_interval(self.update_beds, 1)  # calls update_info every 4s

    def add_room(self):
        self.rooms_num += 1
        self.beds_per_room.append(0)
        if self.rooms_num <= 4:
            pos_hint = {'center_x': .2 + .2 * (self.rooms_num - 1), 'center_y': .7}
        else:
            pos_hint = {'center_x': .2 + .2 * (self.rooms_num - 5), 'center_y': .3}

        room_source = self.room_source + str(self.rooms_num) + '.png'
        size_hint = (.2, .35)
        room = Image(source=room_source, pos_hint=pos_hint, size_hint=size_hint)
        self.add_widget(room)

    def add_bed(self, room_num):
        self.beds_per_room[room_num - 1] += 1
        bed_num = self.beds_per_room[room_num - 1]
        bed_id = 10 * room_num + bed_num
        color_source = self.get_color_source(bed_id)

        if room_num <= 4:
            if bed_num <= 4:
                cen_x = .15 + .033 * (bed_num - 1) + .2 * (room_num - 1)
                cen_y = .75
            else:
                cen_x = .15 + .033 * ((bed_num - 1) - 4) + .2 * (room_num - 1)
                cen_y = .63
        else:
            if bed_num <= 4:
                cen_x = .15 + .033 * (bed_num - 1) + .2 * (room_num - 5)
                cen_y = .35
            else:
                cen_x = .15 + .033 * ((bed_num - 1) - 4) + .2 * (room_num - 5)
                cen_y = .22

        size_hint = (.033, .1)
        pos_hint = {'center_x': cen_x, 'center_y': cen_y}
        bed = ImageButton(source=color_source, pos_hint=pos_hint, size_hint=size_hint, bed_id=str(bed_id))
        self.add_widget(bed)
        self.beds[str(bed_id)] = bed

    def get_color_source(self, bed_id):
        bed_num = bed_id % 10
        extension = '.png'
        if get_patient_status(bed_id) == 1:
            return self.green_source + str(bed_num) + extension
        elif get_patient_status(bed_id) == -1:
            return self.grey_source + str(bed_num) + extension
        else:
            return self.red_source + str(bed_num) + extension

    def update_beds(self, dt):
        for room_num in range(1, self.rooms_num + 1):
            for bed_num in range(1, self.beds_per_room[room_num - 1]):
                bed_id = 10 * room_num + bed_num
                color_source = self.get_color_source(bed_id)
                bed = self.beds[str(bed_id)]
                bed.source = color_source
                if bed.popup.opened:
                    bed.popup.update_info()


class LoopApp(App):
    def build(self):
        carousel = Carousel(direction='right')
        my_widgets_num = 2
        room_count = 8
        bed_count = 8
        for i in range(my_widgets_num):
            carousel.add_widget(MyWidget(room_count, bed_count))
        return carousel

    def on_start(self):
        if not ImageButton.pressed:
            return False
        ImageButton.changed_data = True


def main():
    # Fullsreen mode with setable resolution
    Window.size = (1920, 1080)
    # Window.size = (1366, 768)
    Window.fullscreen = True
    LoopApp().run()


if __name__ == '__main__':
    main()
