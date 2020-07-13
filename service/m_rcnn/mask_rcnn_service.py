#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Title   : mask rcnn 物体检测
    1. 表格检测
@File    :   mask_rcnn_service.py    
@Author  : minjianxu
@Time    : 2020/5/26 3:27 下午
@Version : 1.0 
'''
import numpy as np
from service.m_rcnn.utils.bbox_utils import BboxUtil
from service.m_rcnn.utils.image_utils import ImageUtils
from service.m_rcnn.utils.mask_util import MaskUtil
from service.m_rcnn.utils.anchor_utils import AnchorUtils
from service.m_rcnn.config import cfg
from service.model_call.model_call_service import MaskRcnnCall
from server.conf import system_config


class MaskRCNN(object):

    def __init__(self):
        self.bbox_util = BboxUtil()
        self.anchor_utils = AnchorUtils()
        self.image_utils = ImageUtils()
        self.mask_util = MaskUtil()

    def detect(self, images_info_list, verbose=0, params=None, mode='single', mode_name="table"):
        """
            Runs the detection pipeline.
        :param images_info_list: List of images, potentially of different sizes.
        :param verbose:
        :param mode: 回调函数，调用模型计算
        :param mode_name: #TODO 因为回调函数是类成员函数，所以要把实例拿过来方便回调
        :return: a list of dicts, one dict per image. The dict contains:
            rois: [N, (y1, x1, y2, x2)] detection bounding boxes
            class_ids: [N] int class IDs
            scores: [N] float probability scores for the class IDs
            masks: [H, W, N] instance binary masks
        """
        if verbose:
            print("processing {} image_info.".format(len(images_info_list)))
            for image_info in images_info_list:
                print("image_info: {}".format(image_info))
                pass
            pass

        # Mold inputs to format expected by the neural network
        molded_images_list, image_metas_list, windows_list = self.image_utils.mode_input(images_info_list)

        # Validate image sizes
        # All images in a batch MUST be of the same size
        image_shape = molded_images_list[0].shape
        for g in molded_images_list[1:]:
            assert g.shape == image_shape, \
                "After resizing, all images must have the same size. Check IMAGE_RESIZE_MODE and image sizes."
            pass

        # Anchors
        anchors = self.anchor_utils.get_anchors(image_shape)
        # Duplicate across the batch dimension because Keras requires it
        # TODO: can this be optimized to avoid duplicating the anchors?
        anchors = np.broadcast_to(anchors, (cfg.TEST.BATCH_SIZE,) + anchors.shape)

        if verbose:
            print("molded_images_list: ", molded_images_list)
            print("image_metas_list: ", image_metas_list)
            print("anchors: ", anchors)
            pass
        # TODO
        mrcnn_call = MaskRcnnCall(mode, system_config.table_detect_params)
        # 这个图片做了转换，需要处理一下之后才能调用
        input_params = (molded_images_list, image_metas_list, anchors)
        detections, _, _, mrcnn_mask, _, _, _ = mrcnn_call.call(input_params)

        # Process detections
        results_list = []
        for i, image_info in enumerate(images_info_list):
            molded_image_shape = molded_images_list[i].shape
            final_rois, final_class_ids, final_scores, final_masks = self.un_mold_detections(detections[i],
                                                                                             mrcnn_mask[i],
                                                                                             image_info.shape,
                                                                                             molded_image_shape,
                                                                                             windows_list[i])
            results_list.append({"rois": final_rois,
                                 "class_ids": final_class_ids,
                                 "scores": final_scores,
                                 "masks": final_masks,
                                 })
        return results_list

    def un_mold_detections(self, detections, mrcnn_mask, original_image_shape,
                           image_shape, window):
        """
            Reformats the detections of one image from the format of the neural
            network output to a format suitable for use in the rest of the
            application.
        :param detections: [N, (y1, x1, y2, x2, class_id, score)] in normalized coordinates
        :param mrcnn_mask: [N, height, width, num_classes]
        :param original_image_shape: [H, W, C] Original image shape before resizing
        :param image_shape: [H, W, C] Shape of the image after resizing and padding
        :param window: [y1, x1, y2, x2] Pixel coordinates of box in the image where the real
                        image is excluding the padding.
        :return:
            boxes: [N, (y1, x1, y2, x2)] Bounding boxes in pixels
            class_ids: [N] Integer class IDs for each bounding box
            scores: [N] Float probability scores of the class_id
            masks: [height, width, num_instances] Instance masks
        """

        # How many detections do we have?
        # Detections array is padded with zeros. Find the first class_id == 0.
        zero_ix = np.where(detections[:, 4] == 0)[0]
        n = zero_ix[0] if zero_ix.shape[0] > 0 else detections.shape[0]

        # Extract boxes, class_ids, scores, and class-specific masks
        boxes = detections[: n, :4]
        class_ids = detections[: n, 4].astype(np.int32)
        scores = detections[: n, 5]
        masks = mrcnn_mask[np.arange(n), :, :, class_ids]

        # Translate normalized coordinates in the resized image to pixel
        # coordinates in the original image before resizing
        window = self.bbox_util.norm_boxes(window, image_shape[:2])
        wy1, wx1, wy2, wx2 = window
        shift = np.array([wy1, wx1, wy1, wx1])
        wh = wy2 - wy1  # window height
        ww = wx2 - wx1  # window width
        scale = np.array([wh, ww, wh, ww])
        # Convert boxes to normalized coordinates on the window
        boxes = np.divide(boxes - shift, scale)
        # Convert boxes to pixel coordinates on the original image
        boxes = self.bbox_util.denorm_boxes(boxes, original_image_shape[:2])

        # Filter out detections with zero area. Happens in early training when
        # network weights are still random
        exclude_ix = np.where(
            (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1]) <= 0)[0]
        if exclude_ix.shape[0] > 0:
            boxes = np.delete(boxes, exclude_ix, axis=0)
            class_ids = np.delete(class_ids, exclude_ix, axis=0)
            scores = np.delete(scores, exclude_ix, axis=0)
            masks = np.delete(masks, exclude_ix, axis=0)
            n = class_ids.shape[0]

        # Resize masks to original image size and set boundary threshold.
        full_masks = []
        for i in range(n):
            # Convert neural network mask to full size mask
            full_mask = self.mask_util.unmold_mask(masks[i], boxes[i], original_image_shape)
            full_masks.append(full_mask)
            pass
        full_masks = np.stack(full_masks, axis=-1) if full_masks else np.empty(original_image_shape[:2] + (0,))

        return boxes, class_ids, scores, full_masks
        pass
