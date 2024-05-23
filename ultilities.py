from gtts import gTTS
from base64 import b64encode
import io


def get_voice(chinese: str):
    tts = gTTS(text=chinese, lang='zh-CN')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    voice = b64encode(fp.getvalue()).decode('utf-8')
    return voice
