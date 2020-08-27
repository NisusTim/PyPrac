# Ref:
# https://zgljl2012.com/pythonshe-ji-mo-shi-factory-method-gong-han-fang-fa-mo-shi/

'''
if lang == 'English'
  cat, dog = 'cat', 'dog'
elif lang == 'Chinese'
  cat, dog = '貓', '狗'
'''

def get_localizer(lang):  
  locales = {}
  locales['English'] = dict(cat='cat', dog='dog')
  locales['Chinese'] = dict(cat='貓', dog='狗')
  return locales[lang]

if __name__ == '__main__':  
  lang = 'English'
  locale = get_localizer(lang)
  print(locale['cat'])
  print(locale['dog'])
