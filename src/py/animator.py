import matplotlib.animation as animation
import matplotlib.pyplot as plt
import moviepy.editor as mpe
import math
import ffmpeg
from measures import bad, moderate, severe, unhealthy, very_unhealthy, hazardous, min_thresh, max_thresh
import subprocess

def merge_video(video_name, audio_name, output_name, fps=30):

    # using ffmpeg, merge wav and gif into avi
    cmd = 'ffmpeg -i '+video_name+' -i '+audio_name+' -c:v copy -c:a aac '+output_name
    subprocess.call(cmd, shell=True)

def animate_data(index, data, days, res, filename):

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    days_only = [day.split('T')[0] for day in days]

    def get_color(aqi):
        if aqi >= very_unhealthy:
            return 'black'
        elif aqi >= unhealthy:
            return 'purple'
        elif aqi >= severe:
            return 'red'
        elif aqi >= moderate:
            return 'orange'
        elif aqi >= bad:
            return '#f2e607'
        else:
            return 'green'

    def animate(i):

        # prepare plot
        ax1.clear()
        ax1.set_title(index.upper() + ' - ' + days[i].replace('T', ' '))
        ax1.set_ylabel(index.upper())

        # color zones
        plt.axhspan(0, bad, facecolor='lightgreen', alpha=0.4)
        plt.axhspan(bad, moderate, facecolor='yellow', alpha=0.4)
        plt.axhspan(moderate, severe, facecolor='orange', alpha=0.4)
        plt.axhspan(severe, unhealthy, facecolor='red', alpha=0.4)
        plt.axhspan(unhealthy, very_unhealthy, facecolor='purple', alpha=0.4)
        plt.axhspan(very_unhealthy, hazardous, facecolor='black', alpha=0.4)   

        # plot residue
        ax1.plot(res[0:i+1], color='black')

        # add data to as bar graph
        sub = data[0:i+1]
        for i in range(len(sub)):
            ax1.bar(i, sub[i], color=get_color(sub[i]))
        # set xticks to days_only without repetitions
        ax1.set_xticks(range(0, len(days_only), 24))
        ax1.set_xticklabels(days_only[::24])



        # set plot limits
        top_y = max_thresh if max(data) > max_thresh-50 else math.ceil(max(data) / min_thresh) * min_thresh
        plt.xticks(fontsize=8)
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