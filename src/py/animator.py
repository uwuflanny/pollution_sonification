import matplotlib.animation as animation
import matplotlib.pyplot as plt
import moviepy.editor as mpe
import math
from measures import BAD, MODERATE, SEVERE, UNHEALTHY, VERY_UNHEALTHY, HAZARDOUS, MIN_THRESH

def merge_video(video_name, audio_name, output_name, fps=30):
    my_clip = mpe.VideoFileClip(video_name)
    audio_background = mpe.AudioFileClip(audio_name)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(output_name, fps)

def animate_data(index, data, days, res, filename):

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    def get_color(aqi):
        if aqi >= VERY_UNHEALTHY:
            return 'black'
        elif aqi >= UNHEALTHY:
            return 'purple'
        elif aqi >= SEVERE:
            return 'red'
        elif aqi >= MODERATE:
            return 'orange'
        elif aqi >= BAD:
            return 'yellow'
        else:
            return 'green'

    def animate(i):

        # prepare plot
        ax1.clear()
        ax1.set_title(index + ' - ' + days[i].replace('T', ' '))
        ax1.set_xlabel('Time')
        ax1.set_ylabel('AQI')

        # color zones
        plt.axhspan(0, BAD, facecolor='lightgreen', alpha=0.5)
        plt.axhspan(BAD, MODERATE, facecolor='yellow', alpha=0.5)
        plt.axhspan(MODERATE, SEVERE, facecolor='orange', alpha=0.5)
        plt.axhspan(SEVERE, UNHEALTHY, facecolor='red', alpha=0.5)
        plt.axhspan(UNHEALTHY, VERY_UNHEALTHY, facecolor='purple', alpha=0.5)
        plt.axhspan(VERY_UNHEALTHY, HAZARDOUS, facecolor='black', alpha=0.5)   

        # plot residue
        ax1.plot(res[0:i+1], color='black')

        # add data to as bar graph
        sub = data[0:i+1]
        for i in range(len(sub)):
            ax1.bar(i, sub[i], color=get_color(sub[i]))

        # set plot limits
        top_y = 500 if max(data) > 450 else math.ceil(max(data) / MIN_THRESH) * MIN_THRESH
        plt.ylim(bottom=0, top=top_y)
        plt.xlim(left=-0.5, right=len(data)-0.5)

        # add a lgend with colors
        plt.legend(bbox_to_anchor=(1, 1), handles=[
            plt.Line2D([0], [0], color='black', lw=1, label='Residue'),
            plt.Rectangle((0,0),1,1, color='lightgreen', label='Good'),
            plt.Rectangle((0,0),1,1, color='yellow', label='Moderate'),
            plt.Rectangle((0,0),1,1, color='orange', label='Severe'),
            plt.Rectangle((0,0),1,1, color='red', label='Unhealthy'),
            plt.Rectangle((0,0),1,1, color='purple', label='Very Unhealthy'),
            plt.Rectangle((0,0),1,1, color='black', label='Hazardous')
        ])

        # extend plot to show legend
        plt.tight_layout()

    ani = animation.FuncAnimation(fig, animate, interval=500, frames=len(data))
    ani.save(filename, fps=2, dpi=200)