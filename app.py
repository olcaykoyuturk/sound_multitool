import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import time

from tools import readfile
from tools import multitool
from tools import SoundGenerator
from tools.voice import VoicePlayer, VoiceRecorder, RealTime
from tools.DataContainer import DataContainer


def app_oscilloscope():
    for widget in app.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=app)
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    left_panel = panel()
    real_time = None

    label = tk.Label(left_panel, text="X Min:")
    label.place(x=10, y=130)
    x_min = tk.Entry(left_panel, width=20)
    x_min.place(x=70, y=130)

    label = tk.Label(left_panel, text="X Max:")
    label.place(x=10, y=170)
    x_max = tk.Entry(left_panel, width=20)
    x_max.place(x=70, y=170)

    label = tk.Label(left_panel, text="Real Time\nDisplay\nSeconds:")
    label.place(x=10, y=210)
    RT_display_seconds = tk.Entry(left_panel, width=20)
    RT_display_seconds.place(x=70, y=225)

    def start_real_time():
        nonlocal real_time
        try:
            display_seconds = float(RT_display_seconds.get())
        except ValueError:
            display_seconds = 5
            RT_display_seconds.delete(0, tk.END)
            RT_display_seconds.insert(0, str(display_seconds))

        real_time = RealTime(display_seconds=display_seconds)
        real_time.start()
        ani.event_source.start()

    def stop_real_time():
        if real_time is not None:
            real_time.stop()
            ani.event_source.stop()

    def update_graph(frame):
        if real_time is not None:
            data = real_time.update()
            ax.clear()
            ax.plot(np.linspace(0, real_time.DISPLAY_SECONDS, len(data)), data)
            ax.set_ylim([-32768, 32767])
            ax.set_title("Oscilloscope")
            ax.set_xlabel("Time [s]")
            ax.set_ylabel("Amplitude")

            try:
                min_val = float(x_min.get())
                max_val = float(x_max.get())
                ax.set_xlim(xmin=min_val, xmax=max_val)
            except ValueError:
                pass

        return ax

    def update_graph_file():
        stop_real_time()
        time, data = multitool.oscilloscope(data_container.get_time(), data_container.get_data())
        ax.clear()
        ax.plot(time, data)
        ax.set_title("Oscilloscope")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude")
        canvas.draw()

    ani = FuncAnimation(fig, update_graph, interval=50, save_count=100)

    real_label = tk.Label(left_panel, text="Real-Time", font=("Arial", 10, "bold"))
    real_label.place(x=153, y=10)

    real_time_btn = tk.Button(left_panel, text="Başlat", command=start_real_time)
    real_time_btn.place(x=140, y=50)

    real_stop_btn = tk.Button(left_panel, text="Durdur", command=stop_real_time)
    real_stop_btn.place(x=190, y=50)

    create_btn = tk.Button(left_panel, text="Oluştur", command=update_graph_file)
    create_btn.place(x=10, y=400)


def app_fft():
    for widget in app.winfo_children():
        widget.destroy()

    real_time = RealTime()
    left_panel = panel()

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=app)
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    label = tk.Label(left_panel, text="X Min:")
    label.place(x=10, y=130)
    x_min = tk.Entry(left_panel, width=20)
    x_min.place(x=70, y=130)

    label = tk.Label(left_panel, text="X Max:")
    label.place(x=10, y=170)
    x_max = tk.Entry(left_panel, width=20)
    x_max.place(x=70, y=170)

    label = tk.Label(left_panel, text="Vertical Axis: ")
    label.place(x=10, y=210)
    vertical_var = tk.StringVar(value='Lin')
    vertical_options = ['Lin', 'Log', 'dB']
    vertical_menu = tk.OptionMenu(left_panel, vertical_var, *vertical_options)
    vertical_menu.place(x=120, y=210)

    label = tk.Label(left_panel, text="Level Type: ")
    label.place(x=10, y=250)
    level_var = tk.StringVar(value='rms')
    level_options = ['pk', 'pp', 'rms']
    level_menu = tk.OptionMenu(left_panel, level_var, *level_options)
    level_menu.place(x=120, y=250)

    label = tk.Label(left_panel, text="Level Type(Pascal): ")
    label.place(x=10, y=290)
    level_pascal_var = tk.StringVar(value='pk')
    level_pascal_options = ['pk', 'pp', 'rms']
    level_pascal_menu = tk.OptionMenu(left_panel, level_pascal_var, *level_pascal_options)
    level_pascal_menu.place(x=120, y=290)

    label = tk.Label(left_panel, text="Smooth Band: ")
    label.place(x=10, y=330)
    smooth_band_var = tk.StringVar(value='1/1')
    smooth_band_options = ['1/1', '1/3', '1/6', '1/12', '1/24']
    smooth_band_menu = tk.OptionMenu(left_panel, smooth_band_var, *smooth_band_options)
    smooth_band_menu.place(x=120, y=330)

    def start_real_time():
        real_time.start()
        ani.event_source.start()

    def stop_real_time():
        real_time.stop()
        ani.event_source.stop()

    def update_graph(frame):
        data = real_time.update()
        if data is not None:
            fft_freq, fft_result, scaled_amplitudes = multitool.fft_graph(data, real_time.RATE, level_var.get())
            ax.clear()
            ax.plot(fft_freq, scaled_amplitudes)
            ax.set_title("FFT Analyzer")
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("Amplitude")

            try:
                min_val = float(x_min.get())
                max_val = float(x_max.get())
                ax.set_xlim(xmin=min_val, xmax=max_val)
            except ValueError:
                pass

            canvas.draw()

    def graph_update_file():
        stop_real_time()
        fft_freq, fft_result, scaled_amplitudes = multitool.fft_graph(data_container.get_data(),
                                                                      data_container.get_sample_rate(),
                                                                      level_var.get())
        ax.clear()
        ax.plot(fft_freq, scaled_amplitudes)
        ax.set_title("FFT Analyzer")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Amplitude")

        if vertical_var.get() is not None:
            if vertical_var.get() == "Lin":
                ax.set_ylabel("Amplitude [Lin] " + level_var.get())
                ax.set_yscale("linear")

            elif vertical_var.get() == "Log":
                ax.set_ylabel("Amplitude [Log] " + level_var.get())
                ax.set_yscale("log")

            elif vertical_var.get() == "dB":
                ax.set_ylabel("Amplitude [dB] " + level_var.get())
                ax.set_yscale("linear")
                ax.set_ylim(bottom=0.1)
                ax.plot(fft_freq, 20 * np.log10(scaled_amplitudes))

        try:
            min_val = float(x_min.get())
            max_val = float(x_max.get())
            ax.set_xlim(xmin=min_val, xmax=max_val)
        except ValueError:
            pass

        canvas.draw()

    ani = FuncAnimation(fig, update_graph, interval=50, save_count=100)

    def clear():
        ax.clear()

    def start_and_clear():
        clear()
        start_real_time()

    real_label = tk.Label(left_panel, text="Real-Time", font=("Arial", 10, "bold"))
    real_label.place(x=153, y=10)

    real_time_btn = tk.Button(left_panel, text="Başlat", command=start_and_clear)
    real_time_btn.place(x=140, y=50)

    real_stop_btn = tk.Button(left_panel, text="Durdur", command=stop_real_time)
    real_stop_btn.place(x=190, y=50)

    create_btn = tk.Button(left_panel, text="Oluştur", command=graph_update_file)
    create_btn.place(x=10, y=400)


def app_octave():
    for widget in app.winfo_children():
        widget.destroy()

    left_panel = panel()
    real_time = RealTime()

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=app)
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def start_real_time():
        real_time.start()
        ani.event_source.start()

    def stop_real_time():
        real_time.stop()
        ani.event_source.stop()

    def update_graph(frame):
        data = real_time.update()
        if data is not None:
            octave_centers, octave_levels, center_freq = multitool.octave_calculator(data, real_time.RATE)
            ax.clear()
            ax.bar(octave_centers, octave_levels, width=[center_freq / 2 for center_freq in octave_centers],
                   edgecolor='black')
            ax.grid(True)
            ax.set_title("Octave Band Analysis (dBA)")
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("Level (dBA)")
            ax.set_xscale('log')
            ax.set_xticks(octave_centers, labels=[str(int(center_freq)) for center_freq in octave_centers])
            canvas.draw()

    def graph_update_file():
        stop_real_time()
        ax.clear()
        octave_centers, octave_levels, center_freq = multitool.octave_calculator(data_container.get_data(),
                                                                                 data_container.get_sample_rate())
        ax.bar(octave_centers, octave_levels, width=[center_freq / 2 for center_freq in octave_centers],
               edgecolor='black')
        ax.grid(True)
        ax.set_title("Octave Band Analysis (dBA)")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Level (dBA)")
        ax.set_xscale('log')
        ax.set_xticks(octave_centers, labels=[str(int(center_freq)) for center_freq in octave_centers])
        canvas.draw()

    ani = FuncAnimation(fig, update_graph, interval=50, save_count=100)

    def clear():
        ax.clear()

    def start_and_clear():
        clear()
        start_real_time()

    real_label = tk.Label(left_panel, text="Real-Time", font=("Arial", 10, "bold"))
    real_label.place(x=153, y=10)

    real_time_btn = tk.Button(left_panel, text="Başlat", command=start_and_clear)
    real_time_btn.place(x=140, y=50)

    real_stop_btn = tk.Button(left_panel, text="Durdur", command=stop_real_time)
    real_stop_btn.place(x=190, y=50)

    create_btn = tk.Button(left_panel, text="Oluştur", command=graph_update_file)
    create_btn.place(x=10, y=400)


def app_spectrogram():
    global colorbar_widget
    for widget in app.winfo_children():
        widget.destroy()

    left_panel = panel()
    real_time = RealTime()

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=app)
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    label = tk.Label(left_panel, text="Window_size:")
    label.place(x=10, y=130)
    window_size_gen = tk.Entry(left_panel, width=20)
    window_size_gen.insert(0, '1024')
    window_size_gen.place(x=120, y=130)

    label = tk.Label(left_panel, text="Overlap:")
    label.place(x=10, y=170)
    overlap_gen = tk.Entry(left_panel, width=20)
    overlap_gen.insert(0, '512')
    overlap_gen.place(x=120, y=170)

    def start_real_time():
        real_time.start()
        ani.event_source.start()

    def stop_real_time():
        real_time.stop()
        ani.event_source.stop()

    colorbar_widget = None

    def update_graph(frame):
        global colorbar_widget
        data = real_time.update()
        if data is not None:
            time, frequencies, spectrogram = multitool.spectrogram_calculator(data,
                                                                              int(window_size_gen.get()),
                                                                              int(overlap_gen.get()),
                                                                              real_time.RATE)
            if colorbar_widget is not None:
                colorbar_widget.remove()
                colorbar_widget = None

            ax.clear()
            graph = ax.pcolormesh(time, frequencies, 10 * np.log10(spectrogram), shading='auto')
            ax.set_ylabel('Frequency [Hz]')
            ax.set_xlabel('Time [sec]')
            ax.set_title('Spectrogram')
            colorbar_widget = fig.colorbar(graph, ax=ax, label='Intensity [dB]')
            canvas.draw()

    def graph_update_file():
        stop_real_time()
        global colorbar_widget
        try:
            time, frequencies, spectrogram = multitool.spectrogram_calculator(
                data_container.get_data(),
                int(window_size_gen.get()),
                int(overlap_gen.get()),
                data_container.get_sample_rate()
            )

            if colorbar_widget is not None:
                colorbar_widget.remove()
                colorbar_widget = None

            ax.clear()
            graph = ax.pcolormesh(time, frequencies, 10 * np.log10(spectrogram), shading='auto')
            ax.set_ylabel('Frequency [Hz]')
            ax.set_xlabel('Time [sec]')
            ax.set_title('Spectrogram')
            colorbar_widget = fig.colorbar(graph, ax=ax, label='Intensity [dB]')
            canvas.draw()
        except ValueError as e:
            messagebox.showinfo("Hata", f"Eksik veri: {e}")

    ani = FuncAnimation(fig, update_graph, interval=50, save_count=100)

    real_label = tk.Label(left_panel, text="Real-Time", font=("Arial", 10, "bold"))
    real_label.place(x=153, y=10)

    real_time_btn = tk.Button(left_panel, text="Başlat", command=start_real_time)
    real_time_btn.place(x=140, y=50)

    real_stop_btn = tk.Button(left_panel, text="Durdur", command=stop_real_time)
    real_stop_btn.place(x=190, y=50)

    update_button = tk.Button(left_panel, text="Oluştur", command=graph_update_file)
    update_button.place(x=120, y=210)


def app_soundplay():
    global file_label

    for widget in app.winfo_children():
        widget.destroy()

    left_panel = tk.Frame(app, width=300, bg="lightgrey")
    left_panel.pack(side=tk.RIGHT, fill=tk.Y)
    left_panel.pack_propagate(False)

    back_btn = tk.Button(left_panel, text="Geri", command=back)
    back_btn.place(x=10, y=10)

    file_btn = tk.Button(left_panel, text="Dosya Yükle", command=load_file)
    file_btn.place(x=10, y=50)
    file_label = tk.Label(left_panel, text=data_container.get_file_path())
    file_label.place(x=10, y=90)

    play_button1 = tk.Button(left_panel, text="Başlat",
                             command=lambda: voice_player.play(data_container.get_file_path()))
    play_button1.place(x=10, y=130)

    stop_button1 = tk.Button(left_panel, text="Durdur", command=voice_player.stop)
    stop_button1.place(x=10, y=170)


def app_sound_record():
    global recording_label, time_label, start_time

    for widget in app.winfo_children():
        widget.destroy()

    left_panel = tk.Frame(app, width=300, bg="lightgrey")
    left_panel.pack(side=tk.RIGHT, fill=tk.Y)
    left_panel.pack_propagate(False)

    back_btn = tk.Button(left_panel, text="Geri", command=back)
    back_btn.place(x=10, y=10)

    def start_recording(file_path):
        global start_time
        if not file_path:
            messagebox.showwarning("Uyarı", "Lütfen bir dosya yolu girin!")
            return

        voice_recorder.record(file_path)
        start_time = time.time()
        recording_label.config(text="Kayıt durumu: Başladı")
        update_timer()

    def stop_recording():
        voice_recorder.stop()
        recording_label.config(text="Kayıt durumu: Durdu")

    def update_timer():
        if voice_recorder.stop_flag.is_set():
            return

        elapsed_time = int(time.time() - start_time)
        time_label.config(text=f"Zaman: {elapsed_time} saniye")
        app.after(1000, update_timer)

    file_name = tk.Label(left_panel, text=".Wav Dosya adı:")
    file_name.place(x=10, y=50)

    file_path_entry = tk.Entry(left_panel, width=20)
    file_path_entry.place(x=10, y=90)

    record_button = tk.Button(left_panel, text="Başlat", command=lambda: start_recording(file_path_entry.get()))
    record_button.place(x=10, y=130)

    stop_button = tk.Button(left_panel, text="Kaydet", command=stop_recording)
    stop_button.place(x=10, y=170)

    recording_label = tk.Label(left_panel, text="Kayıt durumu: Durdu")
    recording_label.place(x=10, y=210)

    time_label = tk.Label(left_panel, text="Zaman: 0 saniye")
    time_label.place(x=10, y=250)


def app_sound_generator():
    for widget in app.winfo_children():
        widget.destroy()

    set_background()

    left_panel = tk.Frame(app, width=300, bg="lightgrey")
    left_panel.pack(side=tk.RIGHT, fill=tk.Y)
    left_panel.pack_propagate(False)

    back_btn = tk.Button(left_panel, text="Geri", command=back)
    back_btn.place(x=10, y=10)

    def app_white_generator():
        for widget in app.winfo_children():
            widget.destroy()

        left_panel = tk.Frame(app, width=300, bg="lightgrey")
        left_panel.pack(side=tk.RIGHT, fill=tk.Y)
        left_panel.pack_propagate(False)

        back_btn = tk.Button(left_panel, text="Geri", command=app_sound_generator)
        back_btn.place(x=10, y=10)

        label = tk.Label(left_panel, text="White Generator", font=("Arial", 10, "bold"))
        label.place(x=125, y=90)

        label = tk.Label(left_panel, text="Süre:")
        label.place(x=10, y=130)
        time_gen = tk.Entry(left_panel, width=20)
        time_gen.place(x=120, y=130)

        label = tk.Label(left_panel, text="Sample Rate (Hz):")
        label.place(x=10, y=170)
        samplerate_gen = tk.Entry(left_panel, width=20)
        samplerate_gen.place(x=120, y=170)

        label = tk.Label(left_panel, text="Genlik: ")
        label.place(x=10, y=210)
        amplitude_gen = tk.Entry(left_panel, width=20)
        amplitude_gen.place(x=120, y=210)

        label = tk.Label(left_panel, text="Pan: ")
        label.place(x=10, y=250)
        pan_gen = tk.Entry(left_panel, width=20)
        pan_gen.place(x=120, y=250)

        label = tk.Label(left_panel, text="Dosya Adı: ")
        label.place(x=10, y=290)
        file_gen = tk.Entry(left_panel, width=20)
        file_gen.place(x=120, y=290)

        def sound_generator():
            a = float(time_gen.get())
            b = int(samplerate_gen.get())
            c = float(amplitude_gen.get())
            d = float(pan_gen.get())
            e = str(file_gen.get())

            try:
                sound_gen = SoundGenerator.generate_white_noise(a, b, c, d)
                SoundGenerator.save_wave_file(e, sound_gen, b)
                messagebox.showinfo("Başarılı", "Dosya başarıyla yüklendi!")
            except ValueError as e:
                messagebox.showerror("Hata", f"Dosya yüklenirken bir hata oluştu!: {e}")

        gen_btn = tk.Button(left_panel, text="Oluştur", command=sound_generator)
        gen_btn.place(x=10, y=330)

    def app_pink_generator():
        for widget in app.winfo_children():
            widget.destroy()

        left_panel = tk.Frame(app, width=300, bg="lightgrey")
        left_panel.pack(side=tk.RIGHT, fill=tk.Y)
        left_panel.pack_propagate(False)

        back_btn = tk.Button(left_panel, text="Geri", command=app_sound_generator)
        back_btn.place(x=10, y=10)

        label = tk.Label(left_panel, text="Pink Generator", font=("Arial", 10, "bold"))
        label.place(x=125, y=90)

        label = tk.Label(left_panel, text="Süre:")
        label.place(x=10, y=130)
        time_gen = tk.Entry(left_panel, width=20)
        time_gen.place(x=120, y=130)

        label = tk.Label(left_panel, text="Sample Rate (Hz):")
        label.place(x=10, y=170)
        samplerate_gen = tk.Entry(left_panel, width=20)
        samplerate_gen.place(x=120, y=170)

        label = tk.Label(left_panel, text="Genlik: ")
        label.place(x=10, y=210)
        amplitude_gen = tk.Entry(left_panel, width=20)
        amplitude_gen.place(x=120, y=210)

        label = tk.Label(left_panel, text="Pan: ")
        label.place(x=10, y=250)
        pan_gen = tk.Entry(left_panel, width=20)
        pan_gen.place(x=120, y=250)

        label = tk.Label(left_panel, text="Dosya Adı: ")
        label.place(x=10, y=290)
        file_gen = tk.Entry(left_panel, width=20)
        file_gen.place(x=120, y=290)

        def sound_generator():
            a = float(time_gen.get())
            b = int(samplerate_gen.get())
            c = float(amplitude_gen.get())
            d = float(pan_gen.get())
            e = str(file_gen.get())

            try:
                sound_gen = SoundGenerator.generate_pink_noise(a, b, c, d)
                SoundGenerator.save_wave_file(e, sound_gen, b)
                messagebox.showinfo("Başarılı", "Dosya başarıyla yüklendi!")
            except ValueError as e:
                messagebox.showerror("Hata", f"Dosya yüklenirken bir hata oluştu!: {e}")

        gen_btn = tk.Button(left_panel, text="Oluştur", command=sound_generator)
        gen_btn.place(x=10, y=330)

    def app_sweep_generator():
        for widget in app.winfo_children():
            widget.destroy()

        left_panel = tk.Frame(app, width=300, bg="lightgrey")
        left_panel.pack(side=tk.RIGHT, fill=tk.Y)
        left_panel.pack_propagate(False)

        back_btn = tk.Button(left_panel, text="Geri", command=app_sound_generator)
        back_btn.place(x=10, y=10)

        label = tk.Label(left_panel, text="Sweep Generator", font=("Arial", 10, "bold"))
        label.place(x=125, y=90)

        label = tk.Label(left_panel, text="Süre:")
        label.place(x=10, y=130)
        time_gen = tk.Entry(left_panel, width=20)
        time_gen.place(x=120, y=130)

        label = tk.Label(left_panel, text="Sample Rate (Hz):")
        label.place(x=10, y=170)
        samplerate_gen = tk.Entry(left_panel, width=20)
        samplerate_gen.place(x=120, y=170)

        label = tk.Label(left_panel, text="Genlik: ")
        label.place(x=10, y=210)
        amplitude_gen = tk.Entry(left_panel, width=20)
        amplitude_gen.place(x=120, y=210)

        label = tk.Label(left_panel, text="Pan: ")
        label.place(x=10, y=250)
        pan_gen = tk.Entry(left_panel, width=20)
        pan_gen.place(x=120, y=250)

        label = tk.Label(left_panel, text="Lower_freq: ")
        label.place(x=10, y=290)
        lower_freq = tk.Entry(left_panel, width=20)
        lower_freq.place(x=120, y=290)

        label = tk.Label(left_panel, text="Upper_freq: ")
        label.place(x=10, y=330)
        upper_freq = tk.Entry(left_panel, width=20)
        upper_freq.place(x=120, y=330)

        repeat_var = tk.BooleanVar()
        repeat_chk = tk.Checkbutton(left_panel, text="Tekrarla", variable=repeat_var, onvalue=True, offvalue=False,
                                    bg="lightgrey")
        repeat_chk.place(x=10, y=370)

        swept_sine_var = tk.BooleanVar()
        swept_sine_chk = tk.Checkbutton(left_panel, text="Sine Sweep", variable=swept_sine_var, onvalue=True,
                                        offvalue=False, bg="lightgrey")
        swept_sine_chk.place(x=120, y=370)

        label = tk.Label(left_panel, text="Dosya Adı: ")
        label.place(x=10, y=410)
        file_gen = tk.Entry(left_panel, width=20)
        file_gen.place(x=120, y=410)

        def sound_generator():
            a = float(time_gen.get())
            b = int(samplerate_gen.get())
            c = float(amplitude_gen.get())
            d = float(pan_gen.get())
            e = int(upper_freq.get())
            f = int(lower_freq.get())
            g = str(file_gen.get())
            h = repeat_var.get()
            i = swept_sine_var.get()

            try:
                sound_gen = SoundGenerator.generate_sweep(f, e, a, b, c, d, h, i)
                SoundGenerator.save_wave_file(g, sound_gen, b)
                messagebox.showinfo("Başarılı", "Dosya başarıyla yüklendi!")
            except ValueError as e:
                messagebox.showerror("Hata", f"Dosya yüklenirken bir hata oluştu!: {e}")

        gen_btn = tk.Button(left_panel, text="Oluştur", command=sound_generator)
        gen_btn.place(x=10, y=450)

    def app_wave_generator():
        for widget in app.winfo_children():
            widget.destroy()

        left_panel = tk.Frame(app, width=300, bg="lightgrey")
        left_panel.pack(side=tk.RIGHT, fill=tk.Y)
        left_panel.pack_propagate(False)

        back_btn = tk.Button(left_panel, text="Geri", command=app_sound_generator)
        back_btn.place(x=10, y=10)

        label = tk.Label(left_panel, text="Wave Generator", font=("Arial", 10, "bold"))
        label.place(x=125, y=90)

        label = tk.Label(left_panel, text="Süre:")
        label.place(x=10, y=130)
        time_gen = tk.Entry(left_panel, width=20)
        time_gen.place(x=120, y=130)

        label = tk.Label(left_panel, text="Sample Rate (Hz):")
        label.place(x=10, y=170)
        samplerate_gen = tk.Entry(left_panel, width=20)
        samplerate_gen.place(x=120, y=170)

        label = tk.Label(left_panel, text="Genlik: ")
        label.place(x=10, y=210)
        amplitude_gen = tk.Entry(left_panel, width=20)
        amplitude_gen.place(x=120, y=210)

        label = tk.Label(left_panel, text="Pan: ")
        label.place(x=10, y=250)
        pan_gen = tk.Entry(left_panel, width=20)
        pan_gen.place(x=120, y=250)

        label = tk.Label(left_panel, text="Frequency: ")
        label.place(x=10, y=290)
        freq = tk.Entry(left_panel, width=20)
        freq.place(x=120, y=290)

        label = tk.Label(left_panel, text="Wave Type: ")
        label.place(x=10, y=330)
        waveform_var = tk.StringVar(value='sine')
        waveform_options = ['sine', 'square', 'triangle', 'sawtooth']
        waveform_menu = tk.OptionMenu(left_panel, waveform_var, *waveform_options)
        waveform_menu.place(x=120, y=330)

        label = tk.Label(left_panel, text="Dosya Adı: ")
        label.place(x=10, y=370)
        file_gen = tk.Entry(left_panel, width=20)
        file_gen.place(x=120, y=370)

        def sound_generator():
            a = float(time_gen.get())
            b = int(samplerate_gen.get())
            c = float(amplitude_gen.get())
            d = float(pan_gen.get())
            e = int(freq.get())
            f = str(waveform_var.get())
            g = str(file_gen.get())

            try:
                sound_gen = SoundGenerator.generate_waveform(f, e, a, b, c, d)
                SoundGenerator.save_wave_file(g, sound_gen, b)
                messagebox.showinfo("Başarılı", "Dosya başarıyla yüklendi!")
            except ValueError as e:
                messagebox.showerror("Hata", f"Dosya yüklenirken bir hata oluştu!: {e}")

        gen_btn = tk.Button(left_panel, text="Oluştur", command=sound_generator)
        gen_btn.place(x=10, y=450)

    white_sound = tk.Button(app, text="White Sound Generator", command=app_white_generator, **button_style)
    white_sound.pack(pady=10)

    pink_sound = tk.Button(app, text="Pink Sound Generator", command=app_pink_generator, **button_style)
    pink_sound.pack(pady=10)

    sweep_sound = tk.Button(app, text="Sweep Sound Generator", command=app_sweep_generator, **button_style)
    sweep_sound.pack(pady=10)

    wave_sound = tk.Button(app, text="Wave Sound Generator", command=app_wave_generator, **button_style)
    wave_sound.pack(pady=10)


def exit_app():
    app.quit()
    app.destroy()


def back():
    for widget in app.winfo_children():
        widget.destroy()

    set_background()
    create_button()


def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        try:
            data, time, channels, sample_width, sample_rate, n_frames = readfile.read_data(file_path)

            data_container.set_data(data)
            data_container.set_time(time)
            data_container.set_channels(channels)
            data_container.set_sample_width(sample_width)
            data_container.set_sample_rate(sample_rate)
            data_container.set_n_frames(n_frames)
            data_container.set_file_path(file_path)

            print(data_container.get_data(), data_container.get_time(), data_container.get_channels(),
                  data_container.get_file_path())

            messagebox.showinfo("Başarılı", "Dosya başarıyla yüklendi!")
            file_label.config(text=data_container.get_file_path())

        except Exception as e:
            messagebox.showerror("Hata", f"Dosya yüklenirken bir hata oluştu!: {e}")


def panel():
    global file_label

    left_panel = tk.Frame(app, width=300, bg="lightgrey")
    left_panel.pack(side=tk.RIGHT, fill=tk.Y)
    left_panel.pack_propagate(False)

    back_btn = tk.Button(left_panel, text="Geri", command=back)
    back_btn.place(x=10, y=10)

    file_btn = tk.Button(left_panel, text="Dosya Yükle", command=load_file)
    file_btn.place(x=10, y=50)

    file_label = tk.Label(left_panel, text=data_container.get_file_path())
    file_label.place(x=10, y=90)

    return left_panel


def set_background():
    global bg_image_label

    bg_image = Image.open("image/background.jpg")
    bg_image = bg_image.resize((1280, 720), Image.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image)

    bg_image_label = tk.Label(app, image=bg_image_tk)
    bg_image_label.image = bg_image_tk
    bg_image_label.place(relwidth=1, relheight=1)


def create_button():
    oscilloscope_btn = tk.Button(app, text="Oscilloscope", command=app_oscilloscope, **button_style)
    oscilloscope_btn.pack(pady=10)

    fft_btn = tk.Button(app, text="FFT Analyzer", command=app_fft, **button_style)
    fft_btn.pack(pady=10)

    octave_btn = tk.Button(app, text="Octave Analyzer", command=app_octave, **button_style)
    octave_btn.pack(pady=10)

    spectrogram_btn = tk.Button(app, text="Spectrogram", command=app_spectrogram, **button_style)
    spectrogram_btn.pack(pady=10)

    soundplay_btn = tk.Button(app, text="Sound Player", command=app_soundplay, **button_style)
    soundplay_btn.pack(pady=10)

    sound_record_btn = tk.Button(app, text="Sound Record", command=app_sound_record, **button_style)
    sound_record_btn.pack(pady=10)

    sound_generator_btn = tk.Button(app, text="Sound Generator", command=app_sound_generator, **button_style)
    sound_generator_btn.pack(pady=10)

    exit_btn = tk.Button(app, text="Exit", command=exit_app, bg="red", fg="white", font=("Arial", 12, "bold"), bd=2,
                         relief="raised", activebackground="#c60000", activeforeground="white", padx=10, pady=5,
                         width=20)
    exit_btn.pack(pady=10)

    label1 = tk.Label(app, text="Version_Alpha 0.0.1", font=("Arial", 12, "bold"))
    label1.pack(pady=20)


global recording_label, time_label, start_time, colorbar_widget, file_label

data_container = DataContainer()
voice_player = VoicePlayer()
voice_recorder = VoiceRecorder()

button_style = {
    "bg": "#4CAF50",
    "fg": "white",
    "font": ("Arial", 12, "bold"),
    "bd": 2,
    "relief": "raised",
    "activebackground": "black",
    "activeforeground": "white",
    "padx": 10,
    "pady": 5,
    "width": 20
}

app = tk.Tk()
app.title("Multitool App")
app.geometry("1280x720")
app.minsize(width=640, height=360)

set_background()
create_button()
app.mainloop()
