from kivy.app import App
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import *
from kivy.logger import Logger


DEBUG=True
def log(message):
    if DEBUG:
        Logger.info(message)


class AdmobMock(EventDispatcher):
    mInterstitialAd = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(AdmobMock,self).__init__(**kwargs)
           
    def showBanner(self):
        log('Showing banner')

    def request_Interstitial(self):
        log('REQUEST interstitial AD...')
        
    def show_Interstitial(self):
        log('Showing show_Interstitial')

    def request_Banner(self):
        log('REQUESTING Banner AD')
        
    def hide_Banner(self):
        log('HIDING Banner AD')        

    def is_Banner_Visible(self):
        return True
