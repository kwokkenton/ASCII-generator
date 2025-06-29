"""
@author: Viet Nguyen <nhviet1009@gmail.com>
"""
import argparse

import cv2
import ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

from utils import get_bbox_from_font, get_data, get_data_new


def reencode_mp4(input_path: str, output_path: str, codec: str = 'libx264', fps: int = None):
    """
    Re-encode an MP4 video using ffmpeg-python.
    
    Args:
        input_path (str): Path to the input video.
        output_path (str): Path to save the re-encoded video.
        codec (str): Video codec to use (e.g., 'libx264', 'libx265', 'mpeg4').
        fps (int, optional): Frames per second override.
    """
    stream = ffmpeg.input(input_path)
    
    kwargs = {'vcodec': codec, 'pix_fmt': 'yuv420p'}
    if fps:
        kwargs['r'] = fps

    stream = ffmpeg.output(stream, output_path, **kwargs).overwrite_output()
    ffmpeg.run(stream)
    
def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, default="data/input.mp4", help="Path to input video")
    parser.add_argument("--output", type=str, default="data/output.mp4", help="Path to output video")
    parser.add_argument("--mode", type=str, default="complex", choices=["simple", "complex"],
                        help="10 or 70 different characters")
    parser.add_argument("--background", type=str, default="black", choices=["black", "white"],
                        help="background's color")
    parser.add_argument("--num_cols", type=int, default=100, help="number of character for output's width")
    parser.add_argument("--scale", type=int, default=1, help="upsize output")
    parser.add_argument("--fps", type=int, default=0, help="frame per second")
    parser.add_argument("--overlay_ratio", type=float, default=0.2, help="Overlay width ratio")
    args = parser.parse_args()
    return args

def main(opt:dict ):

    if opt.mode == "simple":
        CHAR_LIST = '@%#*+=-:. '
    else:
        CHAR_LIST = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
        CHAR_LIST = "LARISSA"

    if opt.background == "white":
        bg_code = (255, 255, 255)
    else:
        bg_code = (0, 0, 0)
    font = ImageFont.truetype("fonts/DejaVuSansMono-Bold.ttf", size=int(10 * opt['scale']))
    cap = cv2.VideoCapture(opt.input)
    if opt.fps == 0:
        fps = int(cap.get(cv2.CAP_PROP_FPS))
    else:
        fps = opt.fps
    num_chars = len(CHAR_LIST)
    num_cols = opt.num_cols
    while cap.isOpened():
        flag, frame = cap.read()
        if flag:
            image = frame
        else:
            break
        height, width, _ = image.shape
        cell_width = width / opt.num_cols
        cell_height = 2 * cell_width
        num_rows = int(height / cell_height)
        if num_cols > width or num_rows > height:
            print("Too many columns or rows. Use default setting")
            cell_width = 6
            cell_height = 12
            num_cols = int(width / cell_width)
            num_rows = int(height / cell_height)
        # char_width, char_height = font.getbbox("A")
        char_width, char_height = get_bbox_from_font(font, 'A')

        out_width = char_width * num_cols
        out_height = 2 * char_height * num_rows
        out_image = Image.new("RGB", (out_width, out_height), bg_code)
        draw = ImageDraw.Draw(out_image)
        for i in range(num_rows):
            for j in range(num_cols):
                partial_image = image[int(i * cell_height):min(int((i + 1) * cell_height), height),
                                int(j * cell_width):min(int((j + 1) * cell_width), width), :]
                partial_avg_color = np.sum(np.sum(partial_image, axis=0), axis=0) / (cell_height * cell_width)
                partial_avg_color = tuple(partial_avg_color.astype(np.int32).tolist())
                char = CHAR_LIST[min(int(np.mean(partial_image) * num_chars / 255), num_chars - 1)]
                draw.text((j * char_width, i * char_height), char, fill=partial_avg_color, font=font)

        if opt.background == "white":
            cropped_image = ImageOps.invert(out_image).getbbox()
        else:
            cropped_image = out_image.getbbox()
        out_image = out_image.crop(cropped_image)
        out_image = np.array(out_image)
        try:
            out
        except:
            out = cv2.VideoWriter(opt.output, cv2.VideoWriter_fourcc(*"XVID"), fps,
                                  ((out_image.shape[1], out_image.shape[0])))

        if opt.overlay_ratio:
            height, width, _ = out_image.shape
            overlay = cv2.resize(frame, (int(width * opt.overlay_ratio), int(height * opt.overlay_ratio)))
            out_image[height - int(height * opt.overlay_ratio):, width - int(width * opt.overlay_ratio):, :] = overlay
        out.write(out_image)
    cap.release()
    out.release()

def video_to_video(opt:dict ):
    out_images = []

    char_list, font, sample_character, scale = get_data_new(opt["sentence"])

    if opt['background'] == "white":
        bg_code = (255, 255, 255)
    else:
        bg_code = (0, 0, 0)
    font = ImageFont.truetype("fonts/DejaVuSansMono-Bold.ttf", size=int(10 * opt['scale']))
    cap = cv2.VideoCapture(opt['input'])

    if opt['fps'] == 0:
        fps = int(cap.get(cv2.CAP_PROP_FPS))
    else:
        fps = opt['fps']
    num_chars = len(char_list)
    num_cols = opt['num_cols']

    while cap.isOpened():
        flag, frame = cap.read()
        if flag:
            image = frame
        else:
            break
        height, width, _ = image.shape
        cell_width = width / opt['num_cols']
        cell_height = 2 * cell_width
        num_rows = int(height / cell_height)
        if num_cols > width or num_rows > height:
            print("Too many columns or rows. Use default setting")
            cell_width = 6
            cell_height = 12
            num_cols = int(width / cell_width)
            num_rows = int(height / cell_height)
        char_width, char_height = get_bbox_from_font(font, 'A')

        out_width = char_width * num_cols
        out_height = 2 * char_height * num_rows
        out_image = Image.new("RGB", (out_width, out_height), bg_code)
        draw = ImageDraw.Draw(out_image)
        for i in range(num_rows):
            for j in range(num_cols):
                partial_image = image[int(i * cell_height):min(int((i + 1) * cell_height), height),
                                int(j * cell_width):min(int((j + 1) * cell_width), width), :]
                partial_avg_color = np.sum(np.sum(partial_image, axis=0), axis=0) / (cell_height * cell_width)
                partial_avg_color = tuple(partial_avg_color.astype(np.int32).tolist())
                char = char_list[min(int(np.mean(partial_image) * num_chars / 255), num_chars - 1)]
                draw.text((j * char_width, i * char_height), char, fill=partial_avg_color, font=font)

        if opt["background"] == "white":
            cropped_image = ImageOps.invert(out_image).getbbox()
        else:
            cropped_image = out_image.getbbox()
        out_image = np.array(out_image.crop(cropped_image))
        
        out_images.append(out_image)

        # Overlay original image ontop of new one
        # if opt.get('overlay_ratio'):
        #     height, width, _ = out_image.shape
        #     overlay = cv2.resize(frame, (int(width * opt['overlay_ratio']), int(height * opt['overlay_ratio'])))
        #     out_image[height - int(height * opt['overlay_ratio']):, width - int(width * opt['overlay_ratio']):, :] = overlay

    cap.release()

    assert all(img.shape == out_images[0].shape for img in out_images)
    # Save video
    out = cv2.VideoWriter(opt['output'], cv2.VideoWriter_fourcc(*'mp4v'), fps,
                    ((out_image.shape[1], out_image.shape[0])))
    for out_frame in out_images:

        out.write(out_frame)
    
    out.release()

    reencode_mp4(input_path = opt['output'], output_path = opt['output_reencoded'])


if __name__ == '__main__':
    opt = get_args()
    input_path = 'data/in.mp4'
    output_path = 'data/out.mp4'
    sentence = 'hello '
    options = {
            "input": input_path,
            "output": output_path,
            "sentence": sentence,
            "language": "english",
            "mode": "standard",
            "background": "black",
            "scale": 2,
            "num_cols": 60,
            'fps' : 0
        }
    video_to_video(options)
