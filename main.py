__version__ = '0.0.5'
"""
Basic POC of admob integration into Kivy.

starting point is the screenmanager example from kivy, on where is added admob features:

- intersticial ad between screens (see on_pre_enter() for details).
- banner on screen, with a button to toogle its visibility.

"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty,ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock

from admob import Admob
from random import random

ad_inst = Admob()


Builder.load_string('''
#:import random random.random
#:import SlideTransition kivy.uix.screenmanager.SlideTransition
#:import SwapTransition kivy.uix.screenmanager.SwapTransition
#:import WipeTransition kivy.uix.screenmanager.WipeTransition
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import RiseInTransition kivy.uix.screenmanager.RiseInTransition
#:import FallOutTransition kivy.uix.screenmanager.FallOutTransition
#:import NoTransition kivy.uix.screenmanager.NoTransition

<CustomScreen>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size

    Label:
        font_size: 42
        text: root.name

    Button:
        text: 'Next screen'
        size_hint: None, None
        pos_hint: {'right': 1}
        size: 150, 50
        on_release: root.manager.current = root.manager.next()

    Button:
        text: 'Previous screen'
        size_hint: None, None
        size: 150, 50
        on_release: root.manager.current = root.manager.previous()

    BoxLayout:
        size_hint: .5, None
        height: 250
        pos_hint: {'center_x': .5}
        orientation: 'vertical'
        Button:
            id: toggleButton
            text: 'Show Ad Banner'
            on_press: root.toggleBanner()

        Button:
            text: 'Use SlideTransition with "up" direction'
            on_release: root.manager.transition = \
                        SlideTransition(direction="up")

        Button:
            text: 'Use SlideTransition with "down" direction'
            on_release: root.manager.transition = \
                        SlideTransition(direction="down")

        Button:
            text: 'Use SlideTransition with "left" direction'
            on_release: root.manager.transition = \
                        SlideTransition(direction="left")

        Button:
            text: 'Use SlideTransition with "right" direction'
            on_release: root.manager.transition = \
                        SlideTransition(direction="right")

        Button:
            text: 'Use SwapTransition'
            on_release: root.manager.transition = SwapTransition()

        Button:
            text: 'Use WipeTransition'
            on_release: root.manager.transition = WipeTransition()

        Button:
            text: 'Use FadeTransition'
            on_release: root.manager.transition = FadeTransition()

        Button:
            text: 'Use FallOutTransition'
            on_release: root.manager.transition = FallOutTransition()

        Button:
            text: 'Use RiseInTransition'
            on_release: root.manager.transition = RiseInTransition()
        Button:
            text: 'Use NoTransition'
            on_release: root.manager.transition = NoTransition(duration=0)
''')


class CustomScreen(Screen):
    hue = NumericProperty(0)
    
    def _showBanner(self,*args):
        ad_inst.request_Banner()

    def on_pre_enter(self,*args):
        if ad_inst.is_Banner_Visible():
            self.ids['toggleButton'].text="Hide Ad Banner"
        else:
            self.ids['toggleButton'].text="Show Ad Banner"
        ad_inst.show_Interstitial()

    def toggleBanner(self,*args):
        if ad_inst.is_Banner_Visible():
            ad_inst.hide_Banner()
            self.ids['toggleButton'].text="Show Ad Banner"
        else:
            ad_inst.request_Banner()
            self.ids['toggleButton'].text="Hide Ad Banner"

class ScreenManagerApp(App):
    def build(self):
        #initial request 
        ad_inst.request_Interstitial()
        ad_inst.request_Banner()
        root = ScreenManager()
        for x in range(4):
            root.add_widget(CustomScreen(name='Screen %d' % x))
        return root

    def on_pause(self):
        return True

    def on_resume(self):
        #request new interstitial if needed
        ad_inst.request_Interstitial()

if __name__ == '__main__':
    ScreenManagerApp().run()
