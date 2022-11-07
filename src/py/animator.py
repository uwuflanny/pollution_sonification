import matplotlib.animation as animation
import matplotlib.pyplot as plt
import moviepy.editor as mpe
import math
import ffmpeg
from measures import BAD, MODERATE, SEVERE, UNHEALTHY, VERY_UNHEALTHY, HAZARDOUS, MIN_THRESH
import subprocess

def merge_video(video_name, audio_name, output_name, fps=30):

    # using ffmpeg, merge wav and gif into avi
    cmd = 'ffmpeg -i '+video_name+' -i '+audio_name+' -c:v copy -c:a aac '+output_name
    subprocess.call(cmd, shell=True)

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
            return '#f2e607'
        else:
            return 'green'

    def animate(i):

        # prepare plot
        ax1.clear()
        ax1.set_title(index + ' - ' + days[i].replace('T', ' '))
        ax1.set_xlabel('Time')
        ax1.set_ylabel('AQI')

        # color zones
        plt.axhspan(0, BAD, facecolor='lightgreen', alpha=0.4)
        plt.axhspan(BAD, MODERATE, facecolor='yellow', alpha=0.4)
        plt.axhspan(MODERATE, SEVERE, facecolor='orange', alpha=0.4)
        plt.axhspan(SEVERE, UNHEALTHY, facecolor='red', alpha=0.4)
        plt.axhspan(UNHEALTHY, VERY_UNHEALTHY, facecolor='purple', alpha=0.4)
        plt.axhspan(VERY_UNHEALTHY, HAZARDOUS, facecolor='black', alpha=0.4)   

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