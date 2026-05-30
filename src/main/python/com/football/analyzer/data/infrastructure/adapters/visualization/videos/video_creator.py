import cv2
import io
import numpy as np
from typing import List, Optional, Tuple
from matplotlib.figure import Figure
from PIL import Image


class VideoCreator:

    def __init__(self, fps: int = 1, codec: str = 'mp4v'):
        self.fps = fps
        self.codec = codec

    def create_video_from_figures(
        self,
        figures: List[Figure],
        output_path: str,
        frame_size: Optional[Tuple[int, int]] = None
    ) -> None:
        frames = [self.figure_to_array(fig) for fig in figures]
        self._write_video(frames, output_path, frame_size)

    def create_video_from_arrays(
        self,
        frames: List[np.ndarray],
        output_path: str,
        frame_size: Optional[Tuple[int, int]] = None
    ) -> None:
        self._write_video(frames, output_path, frame_size)

    @staticmethod
    def figure_to_array(fig: Figure) -> np.ndarray:
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        return np.array(img)

    def _write_video(
        self,
        frames: List[np.ndarray],
        output_path: str,
        frame_size: Optional[Tuple[int, int]]
    ) -> None:
        if not frames:
            raise ValueError("No frames provided")
        if frame_size is None:
            height, width = frames[0].shape[:2]
            frame_size = (width, height)
        fourcc = cv2.VideoWriter_fourcc(*self.codec)
        out = cv2.VideoWriter(output_path, fourcc, self.fps, frame_size)
        for frame in frames:
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            if frame_bgr.shape[1] != frame_size[0] or frame_bgr.shape[0] != frame_size[1]:
                frame_bgr = cv2.resize(frame_bgr, frame_size)
            out.write(frame_bgr)
        out.release()
        cv2.destroyAllWindows()
