# Sound Analyzer and Generator

Bu proje, ses analizi ve oluşturma özelliklerini birleştiren bir uygulamadır. Proje, ses dalgalarını gerçek zamanlı olarak görselleştirir ve ses oluşturma, kayıt etme, çalma işlemlerini destekler. Aşağıdaki bileşenleri içerir:

- **Oscilloscope**: Ses dalgalarını gerçek zamanlı olarak gösterir.
- **FFT (Fast Fourier Transform)**: Frekans analizini yapar ve sesin frekans bileşenlerini görselleştirir.
- **Octave Analyzer**: Sesin oktav bazında analizini yapar.
- **Spectrogram**: Zaman içinde frekans değişimini gösterir.
- **Sound Generator**: Farklı türde sesler oluşturur:
  - **White Noise**
  - **Pink Noise**
  - **Sweep (Frekans Tarama)**
  - **Wave (Özelleştirilmiş Dalga Formları)**
- **Sound Player**: Ses dosyalarını çalar.
- **Sound Recorder**: Ses kaydeder.

## Özellikler

- **Gerçek Zamanlı Görselleştirme**: Ses verisi, osiloskop, FFT, Octave Analyzer ve Spectrogram gibi araçlarla görselleştirilebilir.
- **Ses Oluşturma**: White noise, pink noise, sweep ve farklı dalga formlarını ses olarak oluşturabilirsiniz.
- **Kayıt ve Çalma**: Mikrofon ile ses kaydedebilir, kayıtları oynatabilirsiniz.
- **FFT ve Spectrogram Görselleştirmeleri**: Sesin frekans bileşenlerini FFT ile analiz edip, zaman içinde nasıl değiştiğini Spectrogram ile izleyebilirsiniz.

## Görseller

### Ana Ekran
![Ana Ekran](https://github.com/olcaykoyuturk/sound_multitool/blob/main/image/1.png?raw=true)

### Oscilloscope
![Oscilloscope](https://github.com/olcaykoyuturk/sound_multitool/blob/main/image/2.png?raw=true)

### Oscilloscope (Gerçek Zamanlı)
![Oscilloscope Real Time](https://github.com/olcaykoyuturk/sound_multitool/blob/main/image/3.png?raw=true)

### FFT (Fast Fourier Transform)
![FFT](https://github.com/olcaykoyuturk/sound_multitool/blob/main/image/4.png?raw=true)

### Octave Analyzer
![Octave Analyzer](https://github.com/olcaykoyuturk/sound_multitool/blob/main/image/5.png?raw=true)

### Sound Player
![Sound Player](https://github.com/olcaykoyuturk/sound_multitool/blob/main/image/6.png?raw=true)

### Sound Recorder
![Sound Recorder](https://github.com/olcaykoyuturk/sound_multitool/blob/main/image/7.png?raw=true)

### Sound Generator Menü
![Sound Generator Menü](https://github.com/olcaykoyuturk/sound_multitool/blob/main/image/8.png?raw=true)

### White Noise Generator
![White Noise Generator](https://github.com/olcaykoyuturk/sound_multitool/blob/main/image/9.png?raw=true)

### Pink Noise Generator
![Pink Noise Generator](https://github.com/olcaykoyuturk/sound_multitool/blob/main/image/10.png?raw=true)

### Sweep Generator
![Sweep Generator](https://github.com/olcaykoyuturk/sound_multitool/blob/main/image/11.png?raw=true)

### Wave Generator
![Wave Generator](https://github.com/olcaykoyuturk/sound_multitool/blob/main/image/12.png?raw=true)

## Kullanım

### Gerekli Bağımlılıklar

Bu projeyi çalıştırmadan önce, aşağıdaki bağımlılıkların yüklendiğinden emin olun:

- Python
- numpy
- matplotlib
- pyaudio
- wave
- tkinter
- PIL
- time
- threading
