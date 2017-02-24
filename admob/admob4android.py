from kivy.app import App
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import *
from kivy.logger import Logger

from jnius import autoclass, JavaClass,PythonJavaClass, MetaJavaClass, java_method, cast


from android import activity
from android.runnable import run_on_ui_thread


PythonActivity = autoclass('org.renpy.android.PythonActivity')
mactivity = PythonActivity.mActivity
InterstitialAd = autoclass('com.google.android.gms.ads.InterstitialAd')
AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
AdView = autoclass('com.google.android.gms.ads.AdView')
AdSize = autoclass('com.google.android.gms.ads.AdSize')
View = autoclass('android.view.View')

AdMobAdapter = autoclass('com.google.ads.mediation.admob.AdMobAdapter')
Bundle = autoclass('android.os.Bundle')

ViewGroupLayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
RelativeLayout = autoclass('android.widget.RelativeLayout')
LayoutParams = autoclass('android.widget.RelativeLayout$LayoutParams')

from kivy.core.window import Window

import settings


DEBUG=True
def log(message):
    if DEBUG:
        Logger.info(message)


        

class AdmobAndroid(EventDispatcher):
    mInterstitialAd = ObjectProperty(None)
    mAdView = ObjectProperty(None)
    isBannerDisplayed=BooleanProperty(False)
    testDeviceHash = ListProperty(settings.ANDROID_TEST_HASH)
    directedToChild = BooleanProperty(True)
    
    def __init__(self,**kwargs):
        super(AdmobAndroid,self).__init__(**kwargs)
        self.mInterstitialAd = InterstitialAd(mactivity)
        self.mAdView = AdView(mactivity)
        
        #FIXME: doesn't work: onAdLoaded is logged fine, but the app freezes before it shows the ad...
        #WORKAROUND: call requestAd() on app's resume, to be sure a new ad will be shown.
        
        self.mInterstitialAd.setAdUnitId(settings.INTERSTITIAL_UNIT_ID)
        self.mAdView.setAdUnitId(settings.BANNER_UNIT_ID)
        self.mAdView.setAdSize(getattr(AdSize,settings.BANNER_TYPE))

    @run_on_ui_thread
    def request_Interstitial(self):
        if not self.mInterstitialAd.isLoaded():
            log('REQUESTING interstitial AD')
            adRequestBuilder = AdRequestBuilder()
            if self.directedToChild:
                adRequestBuilder.tagForChildDirectedTreatment(True)
                #add designed for families stuff
                extras = Bundle()
                extras.putBoolean("is_designed_for_families", True)


            for i in self.testDeviceHash:
                adRequestBuilder.addTestDevice(i)
            #adRequestBuilder.addNetworkExtrasBundle(AdMobAdapter, extras)
            #FIXME: enable this if the app is intended to make part of the 'designed for families program'

            adRequest = adRequestBuilder.build()
            self.mInterstitialAd.loadAd(adRequest)
        else:
            log('NO NEED TO REQUEST interstitial AD,already loaded...')
    
    @run_on_ui_thread
    def show_Interstitial(self):
        if self.mInterstitialAd.isLoaded():
            self.mInterstitialAd.show()
            return True
        return False
   
    @run_on_ui_thread
    def request_Banner(self):
        self.mAdView.setEnabled(True)
        self.mAdView.setVisibility(View.VISIBLE)
        log('REQUESTING Banner AD')
        adRequestBuilder = AdRequestBuilder()
        for i in self.testDeviceHash:
            adRequestBuilder.addTestDevice(i)
        if self.directedToChild:
            adRequestBuilder.tagForChildDirectedTreatment(True)
        adRequest = adRequestBuilder.build()
        self.mAdView.loadAd(adRequest)
        log('REQUEST Banner AD DONE!!..')
        if not self.isBannerDisplayed:
            adsParams = LayoutParams(ViewGroupLayoutParams.WRAP_CONTENT, ViewGroupLayoutParams.WRAP_CONTENT)
            adsParams.addRule(getattr(RelativeLayout,settings.BANNER_POS))
            adsParams.addRule(RelativeLayout.CENTER_IN_PARENT)            
            mactivity.addContentView(self.mAdView, adsParams)
            self.isBannerDisplayed=True

    @run_on_ui_thread
    def hide_Banner(self):
        if self.is_Banner_Visible():
            self.mAdView.setEnabled(False)
            self.mAdView.setVisibility(View.GONE)
            
    def is_Banner_Visible(self):
        return self.mAdView.getVisibility() == View.VISIBLE
