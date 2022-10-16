import matplotlib.animation as animation
import matplotlib.pyplot as plt
import moviepy.editor as mpe

def merge_video(video_name, audio_name, output_name, fps=30):
    my_clip = mpe.VideoFileClip(video_name)
    audio_background = mpe.AudioFileClip(audio_name)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(output_name, fps)

# TODO CHANGE INDEX NAME and rows
def animate_data(data, res, filename):

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    def animate(i):

        # prepare plot
        ax1.clear()
        ax1.set_title('PM2.5 Data - dd/mm/yyyy - ' + str(i))
        ax1.set_xlabel('Time')
        ax1.set_ylabel('AQI')

        # plot residue
        ax1.plot(res[0:i+1], color='blue')
        if res[i] > 0:
            ax1.plot(i, res[i], 'o', color='blue')

        # plot aqi
        ax1.plot(data[0:i+1])
        ax1.plot(data, 'bo', markersize=0.1, markerfacecolor='none', markeredgecolor='none')
        ax1.plot(i, data[i], 'bo')

        # set plot limits
        plt.ylim(bottom=0)
        plt.xlim(left=0)

        # orange line at 50 named 'bad'
        plt.axhline(y=50, color='orange', linestyle='-', label='bad')
        plt.text(1, 51, 'bad', color='orange')

        # red line at 100 named 'hazardous'
        plt.axhline(y=100, color='red', linestyle='-', label='hazardous')
        plt.text(1, 101, 'hazardous', color='red')

        # purple line at 150 named 'dangerous'
        plt.axhline(y=150, color='purple', linestyle='-', label='dangerous')
        plt.text(1, 151, 'dangerous', color='purple')

        # color zones
        plt.axhspan(0, 50, facecolor='green', alpha=0.2)
        plt.axhspan(50, 100, facecolor='orange', alpha=0.2)
        plt.axhspan(100, 150, facecolor='red', alpha=0.2)
        plt.axhspan(150, 1000, facecolor='purple', alpha=0.2)

    ani = animation.FuncAnimation(fig, animate, interval=500, frames=len(data))
    ani.save(filename, fps=2, dpi=200)