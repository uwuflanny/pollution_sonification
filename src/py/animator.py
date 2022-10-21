import matplotlib.animation as animation
import matplotlib.pyplot as plt
import moviepy.editor as mpe
from measures import BAD, MODERATE, SEVERE, UNHEALTHY, VERY_UNHEALTHY, HAZARDOUS

def merge_video(video_name, audio_name, output_name, fps=30):
    my_clip = mpe.VideoFileClip(video_name)
    audio_background = mpe.AudioFileClip(audio_name)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(output_name, fps)

def animate_data(index, data, days, res, filename):

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    def animate(i):

        # prepare plot
        ax1.clear()
        ax1.set_title(index + ' - ' + days[i].replace('T', ' '))
        ax1.set_xlabel('Time')
        ax1.set_ylabel('AQI')

        # plot residue
        ax1.plot(res[0:i+1], color='blue')
        if res[i] > 0:
            ax1.plot(i, res[i], '-', color='blue')

        # plot aqi
        ax1.plot(data[0:i+1])
        ax1.plot(data, 'bo', markersize=0.1, markerfacecolor='none', markeredgecolor='none')
        ax1.plot(i, data[i], 'bo')

        # set plot limits
        plt.ylim(bottom=0)
        plt.xlim(left=0)

        # orange line at 50 named 'bad'
        plt.axhline(y=BAD, color='orange', linestyle='-', label='bad')
        plt.text(1, BAD+1, 'bad', color='orange')

        # red line at 100 named 'hazardous'
        plt.axhline(y=MODERATE, color='red', linestyle='-', label='moderate')
        plt.text(1, MODERATE+1, 'moderate', color='red')

        # purple line at 150 named 'dangerous'
        plt.axhline(y=SEVERE, color='magenta', linestyle='-', label='severe')
        plt.text(1, SEVERE+1, 'severe', color='magenta')

        # color zones
        plt.axhspan(0, BAD, facecolor='green', alpha=0.2)
        plt.axhspan(BAD, MODERATE, facecolor='orange', alpha=0.2)
        plt.axhspan(MODERATE, SEVERE, facecolor='red', alpha=0.2)
        plt.axhspan(SEVERE, HAZARDOUS, facecolor='purple', alpha=0.2)

    ani = animation.FuncAnimation(fig, animate, interval=500, frames=len(data))
    ani.save(filename, fps=2, dpi=200)