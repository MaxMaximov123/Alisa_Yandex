from deep_translator import GoogleTranslator
to_translate = 'Привет, как тебя зовут, меня максим. Рад познакомиться'
translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
print(translated)