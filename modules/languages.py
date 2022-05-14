def translate(language_to_translate_to):
    if "afrikaans" in language_to_translate_to.lower():
        translate_language = "aa"

    elif "arabic" in language_to_translate_to.lower():
        translate_language = "ar"

    elif "assamese" in language_to_translate_to.lower():
        translate_language = "as"

    elif "bihari" in language_to_translate_to.lower():
        translate_language = "bh"

    elif "bengali" in language_to_translate_to.lower():
        translate_language = "bn"

    elif "tibetan" in language_to_translate_to.lower():
        translate_language = "bo"

    elif "bosnian" in language_to_translate_to.lower():
        translate_language = "bs"

    elif "german" in language_to_translate_to.lower():
        translate_language = "de"

    elif "greek" in language_to_translate_to.lower():
        translate_language = "el"

    elif "english" in language_to_translate_to.lower():
        translate_language = "en"

    elif "spanish" in language_to_translate_to.lower():
        translate_language = "es"

    elif "french" in language_to_translate_to.lower():
        translate_language = "fr"

    elif "gujarati" in language_to_translate_to.lower():
        translate_language = "gu"

    elif "hindi" in language_to_translate_to.lower():
        translate_language = "hi"

    elif "kashmiri" in language_to_translate_to.lower():
        translate_language = "ks"

    elif "malayalam" in language_to_translate_to.lower():
        translate_language = "ml"

    elif "marathi" in language_to_translate_to.lower():
        translate_language = "mr"

    elif "burmese" in language_to_translate_to.lower():
        translate_language = "my"

    elif "nepali" in language_to_translate_to.lower():
        translate_language = "ne"

    elif "oriya" in language_to_translate_to.lower():
        translate_language = "or"

    elif "punjabi" in language_to_translate_to.lower():
        translate_language = "pa"

    elif "sanskrit" in language_to_translate_to.lower():
        translate_language = "sa"

    elif "albanian" in language_to_translate_to.lower():
        translate_language = "sq"

    elif "tamil" in language_to_translate_to.lower():
        translate_language = "ta"

    elif "telugu" in language_to_translate_to.lower():
        translate_language = "te"

    elif "urdu" in language_to_translate_to.lower():
        translate_language = "ur"

    elif "chinese" in language_to_translate_to .lower():
        translate_language = "zh"

    elif "russian" in language_to_translate_to .lower():
        translate_language = "ru"

    else:
        translate_language = "Undetected"

    return translate_language