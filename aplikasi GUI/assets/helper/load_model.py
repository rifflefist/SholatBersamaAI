import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Hentikan logging absl (Google logging framework yg dipakai TF)
import logging
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)
logging.getLogger('tensorflow').setLevel(logging.ERROR)

import tensorflow as tf
import numpy as np
import cv2
from assets.helper.get_resource import resource_path

# Import matplotlib libraries
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as patches


class load_model():
    def __init__(self):
        model_path_movenet = resource_path("assets/model/movenet_thunder_int8.tflite")
        # Initialize the TFLite interpreter
        self.interpreter = tf.lite.Interpreter(model_path=model_path_movenet)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def _keypoints_and_edges_for_display(keypoints_with_scores, height, width, keypoint_threshold=0.11):
        # Maps bones to a matplotlib color name.
        KEYPOINT_EDGE_INDS_TO_COLOR = {
            (0, 1): 'm',
            (0, 2): 'c',
            (1, 3): 'm',
            (2, 4): 'c',
            (0, 5): 'm',
            (0, 6): 'c',
            (5, 7): 'm',
            (7, 9): 'm',
            (6, 8): 'c',
            (8, 10): 'c',
            (5, 6): 'y',
            (5, 11): 'm',
            (6, 12): 'c',
            (11, 12): 'y',
            (11, 13): 'm',
            (13, 15): 'm',
            (12, 14): 'c',
            (14, 16): 'c'
        }
        
        # Dictionary that maps from joint names to keypoint indices.
        KEYPOINT_DICT = {
            'nose': 0,
            'left_eye': 1,
            'right_eye': 2,
            'left_ear': 3,
            'right_ear': 4,
            'left_shoulder': 5,
            'right_shoulder': 6,
            'left_elbow': 7,
            'right_elbow': 8,
            'left_wrist': 9,
            'right_wrist': 10,
            'left_hip': 11,
            'right_hip': 12,
            'left_knee': 13,
            'right_knee': 14,
            'left_ankle': 15,
            'right_ankle': 16
        }
    
        keypoints_all = []
        keypoint_edges_all = []
        edge_colors = []
        num_instances, _, _, _ = keypoints_with_scores.shape
        for idx in range(num_instances):
            kpts_x = keypoints_with_scores[0, idx, :, 1]
            kpts_y = keypoints_with_scores[0, idx, :, 0]
            kpts_scores = keypoints_with_scores[0, idx, :, 2]
            kpts_absolute_xy = np.stack(
                [width * np.array(kpts_x), height * np.array(kpts_y)], axis=-1)
            kpts_above_thresh_absolute = kpts_absolute_xy[
                kpts_scores > keypoint_threshold, :]
            keypoints_all.append(kpts_above_thresh_absolute)

            for edge_pair, color in KEYPOINT_EDGE_INDS_TO_COLOR.items():
                if (kpts_scores[edge_pair[0]] > keypoint_threshold and kpts_scores[edge_pair[1]] > keypoint_threshold):
                    x_start = kpts_absolute_xy[edge_pair[0], 0]
                    y_start = kpts_absolute_xy[edge_pair[0], 1]
                    x_end = kpts_absolute_xy[edge_pair[1], 0]
                    y_end = kpts_absolute_xy[edge_pair[1], 1]
                    line_seg = np.array([[x_start, y_start], [x_end, y_end]])
                    keypoint_edges_all.append(line_seg)
                    edge_colors.append(color)
        if keypoints_all:
            keypoints_xy = np.concatenate(keypoints_all, axis=0)
        else:
            keypoints_xy = np.zeros((0, 17, 2))

        if keypoint_edges_all:
            edges_xy = np.stack(keypoint_edges_all, axis=0)
        else:
            edges_xy = np.zeros((0, 2, 2))
        return keypoints_xy, edges_xy, edge_colors


    def draw_prediction_on_image(self,
        image, keypoints_with_scores, crop_region=None, close_figure=False,
        output_image_height=None):
        
        height, width, channel = image.shape
        aspect_ratio = float(width) / height
        fig, ax = plt.subplots(figsize=(12 * aspect_ratio, 12))
        # To remove the huge white borders
        fig.tight_layout(pad=0)
        ax.margins(0)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        plt.axis('off')

        im = ax.imshow(image)
        line_segments = LineCollection([], linewidths=(4), linestyle='solid')
        ax.add_collection(line_segments)
        # Turn off tick labels
        scat = ax.scatter([], [], s=60, color='#FF1493', zorder=3)

        (keypoint_locs, keypoint_edges,
        edge_colors) = self._keypoints_and_edges_for_display(
            keypoints_with_scores, height, width)

        line_segments.set_segments(keypoint_edges)
        line_segments.set_color(edge_colors)
        if keypoint_edges.shape[0]:
            line_segments.set_segments(keypoint_edges)
            line_segments.set_color(edge_colors)
        if keypoint_locs.shape[0]:
            scat.set_offsets(keypoint_locs)

        if crop_region is not None:
            xmin = max(crop_region['x_min'] * width, 0.0)
            ymin = max(crop_region['y_min'] * height, 0.0)
            rec_width = min(crop_region['x_max'], 0.99) * width - xmin
            rec_height = min(crop_region['y_max'], 0.99) * height - ymin
            rect = patches.Rectangle(
                (xmin,ymin),rec_width,rec_height,
                linewidth=1,edgecolor='b',facecolor='none')
            ax.add_patch(rect)

        fig.canvas.draw()
        image_from_plot = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        image_from_plot = image_from_plot.reshape(
            fig.canvas.get_width_height()[::-1] + (4,))
        image_from_plot = image_from_plot[:, :, :3]
        plt.close(fig)
        if output_image_height is not None:
            output_image_width = int(output_image_height / height * width)
            image_from_plot = cv2.resize(
                image_from_plot, dsize=(output_image_width, output_image_height),
                interpolation=cv2.INTER_CUBIC)
        return image_from_plot

    def movenet(self, input_image):
        input_image = tf.cast(input_image, dtype=tf.uint8)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_image.numpy())
        # Invoke inference.
        self.interpreter.invoke()
        # Get the model prediction.
        keypoints_with_scores = self.interpreter.get_tensor(self.output_details[0]['index'])
        return keypoints_with_scores

    def load_movenet(self, image_path):
        # Load the input image.
        image = tf.io.read_file(image_path)
        image = tf.image.decode_jpeg(image)

        # Resize and pad the image to keep the aspect ratio and fit the expected size.
        input_image = tf.expand_dims(image, axis=0)
        input_image = tf.image.resize_with_pad(input_image, 256, 256)

        # Run model inference.
        keypoints_with_scores = self.movenet(input_image)
        
        return keypoints_with_scores

    def normalize_hip_center(self, keypoints_with_scores):
        
        # Get all keypoints
        keypoints = keypoints_with_scores[ :, :2]  # shape: (17, 2)
        scores = keypoints_with_scores[ :, 2]      # Confidence scores
        
        confidence_threshold = 0.3
        
        # Get center of body (hip)
        left_hip = keypoints[11]
        right_hip = keypoints[12]
        
        # Get the hip center (if confidence > threshold)
        if scores[11] > confidence_threshold and scores[12] > confidence_threshold :
            hip_center = (left_hip + right_hip) / 2
        else:
            # Fallback: use the mean of all the keypoints
            valid_indices = np.where(scores > confidence_threshold)[0]
            hip_center = np.mean(keypoints[valid_indices], axis=0) if len(valid_indices) > 0 else np.zeros(2)
        
        # Change the keypoints to hip oriented
        keypoints_centered = keypoints - hip_center
        
        # Height estimation from shoulder to hip
        left_shoulder = keypoints[5]
        right_shoulder = keypoints[6]
        
        # Normalization with height estimation (if confidence > threshold)
        if scores[5] > confidence_threshold and scores[6] > confidence_threshold and np.linalg.norm(left_shoulder - right_shoulder) > 0:
            shoulder_center = (left_shoulder + right_shoulder) / 2
            body_height = np.linalg.norm(shoulder_center - hip_center)
            keypoints_normalized = keypoints_centered / body_height
        else:
            # Fallback: use a normal case body_height shoulder-to-hip 0.3 - 0.5
            keypoints_normalized = keypoints_centered / 0.4

        
        return keypoints_normalized

    def get_predict(self, input_image):
        
        predict = [[]]
        
        keypoints = self.movenet(input_image)[0, 0, :, :]
        if np.mean(keypoints[:, 2]) > 0.5:
        
            normalized_keypoints = self.normalize_hip_center(keypoints)
            
            input = normalized_keypoints.flatten().reshape(1, -1)
            
            model_gerakan = resource_path("assets/model/deteksi_gerakan.tflite")
            
            interpreter_gerakan = tf.lite.Interpreter(model_path=model_gerakan)
            interpreter_gerakan.allocate_tensors()
            
            input_details = interpreter_gerakan.get_input_details()
            output_details = interpreter_gerakan.get_output_details()

            interpreter_gerakan.set_tensor(input_details[0]['index'], input)

            interpreter_gerakan.invoke()

            predict = interpreter_gerakan.get_tensor(output_details[0]['index'])
        
        return predict