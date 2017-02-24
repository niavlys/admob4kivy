#STATUS:
# interstitial working, banners not implemented yet...

from pyobjus import autoclass, objc_str, protocol, objc_py_types
from pyobjus.dylib_manager import load_framework, INCLUDE

from kivy.app import App
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import *
from kivy.logger import Logger

GADRequest=autoclass('GADRequest')
GADInterstitial=autoclass('GADInterstitial')
UIApplication = autoclass('UIApplication')

NSString = autoclass('NSString')
NSArray = autoclass("NSArray")

import settings

DEBUG=True
def log(message):
    if DEBUG:
        Logger.info(message)


class AdmobIos(EventDispatcher):
    testDevicesList=ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        log('Google AD version is %s'%GADRequest.sdkVersion().cString())   
        string_for_array = NSString.alloc().initWithUTF8String_(settings.IOS_TEST_HASH)
        self.testDevicesList = NSArray.arrayWithObject_(string_for_array)
        super(AdmobIos,self).__init__(**kwargs)
           
    def showBanner(self):
        log('Showing banner')

    def request_Interstitial(self):
        log('REQUEST interstitial AD...')
        self.mInterstitialAd = GADInterstitial.alloc().initWithAdUnitID_(settings.INTERSTITIAL_UNIT_ID)
        request = GADRequest.alloc()
        request.testDevices = self.testDevicesList
        self.mInterstitialAd.loadRequest_(request)
        log('REQUEST interstitial AD DONE...')
        
    def show_Interstitial(self):
        if self.mInterstitialAd.isReady:
            topviewController = UIApplication.sharedApplication().keyWindow.subviews().lastObject().nextResponder()
            log('Showing show_Interstitial')
            self.mInterstitialAd.presentFromRootViewController_(topviewController)
            #reload next interstitial ad...
            self.request_Interstitial()
        else:
            log("CAN'T SHOW interstitial AD ;(")
            
    def request_Banner(self):
        log('REQUESTING Banner AD')
        
    def hide_Banner(self):
        log('HIDING Banner AD')        

    def is_Banner_Visible(self):
        return False

