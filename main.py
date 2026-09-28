import random
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
from googletrans import Translator


# Kelime sözlüğümüz
seviyeye_gore_kelimeler = {
    "kolay": ["kedi", "köpek", "elma", "süt", "güneş", "ay"],
    "orta": ["muz", "okul", "arkadaş", "pencere", "sari"],
    "zor": ["teknoloji", "üniversite", "bilgi", "telaffuz", "hayal gücü"]
}


# Ayarlar
translator = Translator()
sample_rate = 44100
sure = 5


# Başlangıç ekranı
print("=" * 40)
print(" LİNGO VOİCE CHALLENGE ")
print("=" * 40)
print("🌍 İngilizce konuşma oyununa hoş geldin! 🌍")
print()

print("Zorluk seviyesini seç lütfen:")
print("1️⃣ Kolay")
print("2️⃣ Orta")
print("3️⃣ Zor")

secim = input("\nSeçimin: ")


if secim == "1":
    seviye = "kolay"

elif secim == "2":
    seviye = "orta"

elif secim == "3":
    seviye = "zor"

else:
    print("❌ Geçersiz seçim! Kolay seviye seçildi.")
    seviye = "kolay"


# Oyun değişkenleri
puan = 0
hata = 0
tur = 0
maksimum_tur = 10

recognizer = sr.Recognizer()


# Oyun başlıyor
print("\n🚀 OYUN BAŞLIYOR!")
print("📢 Türkçe kelimeyi görünce İngilizcesini söyle.")
print("❤️ 3 hata yaparsan oyun biter!")
print()


while hata < 3 and tur < maksimum_tur:

    tur += 1

    # 🎲 Rastgele Türkçe kelime seç
    turkce_kelime = random.choice(
        seviyeye_gore_kelimeler[seviye]
    )

    # 🌍 İngilizceye çevir
    ceviri = translator.translate(
        turkce_kelime,
        src="tr",
        dest="en"
    )

    ingilizce_kelime = ceviri.text.lower()

    print("_" * 40)
    print(f"🎯 Tur: {tur}/{maksimum_tur}")
    print(f"🇹🇷 Kelime: {turkce_kelime}")
    print(" Şimdi İngilizcesini söyle!")
    print("⏺️ Kayit başliyor...")

    try:

        # 🎙️ Ses kaydı
        kayit = sd.rec(
            int(sure * sample_rate),
            samplerate=sample_rate,
            channels=1
        )

        sd.wait()

        write(
            "ses.wav",
            sample_rate,
            kayit
        )

        print("⏹️ Kayit tamamlandi!")

        # 🧠 Konuşmayı tanı
        with sr.AudioFile("ses.wav") as source:

            audio = recognizer.record(source)

            recognized = recognizer.recognize_google(
                audio,
                language="en-US"
            )

        recognized = recognized.lower()

        print(f" Senin söylediğin: {recognized}")
        print(f"✅ Doğru cevap: {ingilizce_kelime}")

        # 🏆 Cevabı kontrol et
        if recognized == ingilizce_kelime:

            print("🎉 DOĞRU!")
            puan += 10

        else:

            print("❌ Yanliş!")
            hata += 1

            print(f"❤️ Hata: {hata}/3")

    # Konuşma anlaşılamadıysa
    except sr.UnknownValueError:

        print(" Konuşman anlaşilamadi.")
        hata += 1

    # Google konuşma tanıma servisine bağlanılamadıysa
    except sr.RequestError:

        print("🌐 Konuşma tanima servisine bağlanilamadi.")
        hata += 1

    # Diğer hatalar
    except Exception as e:

        print("⚠️ Bir hata oluştu:")
        print(e)
        hata += 1

    print(f"⭐ Puanin: {puan}")


# 🏁 Oyun sonu
print()

print("=" * 40)
print("🏁 OYUN BİTTİ!")
print("=" * 40)

print(f"⭐ Toplam puanin: {puan}")
print(f"❌ Hata sayin: {hata}")
print(f"🎯 Oynanan tur: {tur}")


if hata >= 3:

    print("💥 3 hata yaptin!")
    print("😎 Tekrar denemek ister misin?")

elif tur >= maksimum_tur:

    print("🏆 10 turu tamamladin!")


if puan >= 80:

    print("🔥 MUHTEŞEM! İngilizcen çok iyi!")

elif puan >= 50:

    print("👏 Harika gidiyorsun!")

else:

    print("💪 Biraz daha pratik yapabilirsin!")