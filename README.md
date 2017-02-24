##ABOUT:
this piece of code is a proof of concept for the integration of admob in a Kivy project. it used to work fairly well with the old toolchain of python-for-android, as well as on iOS8+.

##ANDROID:

1. Open the Android SDK Manager and download "Google Repository" and "Google Play services" which are in the Extras category.


2. Copy the google-play-services_lib folder from
ANDROIDSDK/extras/google/google_play_services/libproject
to your app folder (where you keep your main.py)


3. Edit your buildozer.spec and add
```
android.meta_data = com.google.android.gms.version=@integer/google_play_services_version
android.library_references = google-play-services_lib
```


4. Update your android project to take google play services into account:
```
$ android update project --subprojects -t 1 -p ./google-play-services_lib/
```


5. Add an activity to the Androidmanifest.tmpl.xml to handle the ads:
```
<activity android:name="com.google.android.gms.ads.AdActivity"
            android:configChanges="keyboard|keyboardHidden|orientation|screenLayout|uiMode|screenSize|smallestScreenSize"
            android:theme="@android:style/Theme.Translucent" 
            android:process=":python"
/>
```

6. Update your settings.py with your admob unitID and devices hashes
```
$ cp settings.py.sample settings.py && vim settings.py
````

7. Build your android app 
```
$ buildozer android debug
````

=> DONE

##IOS:
1. create kivy-ios project

2. follow 
https://developers.google.com/admob/ios/quick-start#manually_using_the_sdk_download
to add the mandatory frameworks.

3. run on a testing device.

 
##Important notes:
- Don't mess with Google by cliquing on your own ads to generate traffic, you will be catched, and then banned from the service.
