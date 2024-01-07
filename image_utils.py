import io
import base64
import matplotlib.pyplot as plt
from matplotlib import colors

def generate_base64_images(matrix, title):
    cmap = colors.ListedColormap(
        ['#000000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00',
         '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25'])
    norm = colors.Normalize(vmin=0, vmax=9)

    # Creating a figure for the matrix
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(matrix, cmap=cmap, norm=norm)
    ax.axis('off')
    ax.set_title(title)

    # Saving the matrix figure
    image_buf = io.BytesIO()
    fig.savefig(image_buf, format="png", bbox_inches='tight', pad_inches=0)
    b64_encoded_image = base64.b64encode(image_buf.getvalue()).decode('utf-8')

    # Closing the figure to free up resources
    plt.close(fig)

    return b64_encoded_image
