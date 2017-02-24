from kivy import platform

__all__ = ('Admob',)

if platform == 'android':
    from admob4android import AdmobAndroid as Admob

elif platform == 'ios':
    from admob4ios import AdmobIos as Admob

else:
    from admobmock import AdmobMock as Admob
