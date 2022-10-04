import sys
from turtle import left
from lead import get_chords, get_lead
from residue import get_residue_arpeggio
from harmonizer import get_harmonization
from vsthost import get_vsts
from trackExporter import TrackExporter
from pydub import AudioSegment
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

def merge_video(video_name, audio_name, output_name, fps=30):
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(video_name)
    audio_background = mpe.AudioFileClip(audio_name)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(output_name, fps)

def animate_data(data, res):

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    def animate(i):
        ax1.clear()

        # residue
        ax1.plot(res[0:i+1], color='blue')
        ax1.plot(i, res[i], 'o', color='blue')

        # aqi
        ax1.plot(data[0:i+1])
        ax1.plot(data, 'bo', markersize=0.1, markerfacecolor='none', markeredgecolor='none')
        ax1.plot(i, data[i], 'bo')

        ax1.set_title('PM2.5 Data - dd/mm/yyyy - ' + str(i))
        ax1.set_xlabel('Time')
        ax1.set_ylabel('AQI')
        plt.ylim(bottom=0)
        plt.xlim(left=0)

        # add orange line at 50 named 'bad', set label margin
        plt.axhline(y=50, color='orange', linestyle='-', label='bad')
        plt.text(1, 51, 'bad', color='orange')

        # add red line at 100 named 'hazardous'
        plt.axhline(y=100, color='red', linestyle='-', label='hazardous')
        plt.text(1, 101, 'hazardous', color='red')

        # add purple line at 150 named 'dangerous'
        plt.axhline(y=150, color='purple', linestyle='-', label='dangerous')
        plt.text(1, 151, 'dangerous', color='purple')

        # color zones
        plt.axhspan(0, 50, facecolor='green', alpha=0.2)
        plt.axhspan(50, 100, facecolor='orange', alpha=0.2)
        plt.axhspan(100, 150, facecolor='red', alpha=0.2)
        plt.axhspan(150, 1000, facecolor='purple', alpha=0.2)


    ani = animation.FuncAnimation(fig, animate, interval=500, frames=len(data))
    ani.save('animation.gif', fps=2, dpi=200)