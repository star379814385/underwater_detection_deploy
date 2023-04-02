# import cv2
# import numpy as np
# import copy
# from pathlib import Path
# import torch 

# class Detector:
#     def __init__(self, model_path, classes, colors, imgsize, score_thr=0.25, nms_thr=0.45) -> None:
#         self.model = cv2.dnn.readNetFromONNX(model_path)
#         # self.model = torch.jit.load(model_path)
#         self.classes = classes
#         self.colors = colors
#         self.imgsize = imgsize
#         self.score_thr = score_thr
#         self.nms_thr = nms_thr
        
        
#     def predict(self, original_image):
#         model = self.model
#         CLASSES = self.classes
#         imgsize = self.imgsize
        
#         [height, width, _] = original_image.shape
#         length = max((height, width))
#         image = np.zeros((length, length, 3), np.uint8)
#         image[0:height, 0:width] = original_image
#         scale = length / imgsize

#         blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(imgsize, imgsize))
#         model.setInput(blob)
#         outputs = model.forward()

#         # outputs = model(torch.from_numpy(blob))
#         # outputs = outputs.numpy()

#         outputs = np.array([cv2.transpose(outputs[0])])
#         rows = outputs.shape[1]

#         boxes = []
#         scores = []
#         class_ids = []

#         for i in range(rows):
#             classes_scores = outputs[0][i][4:]
#             (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
#             if maxScore >= self.score_thr:
#                 box = [
#                     outputs[0][i][0] - (0.5 * outputs[0][i][2]), outputs[0][i][1] - (0.5 * outputs[0][i][3]),
#                     outputs[0][i][2], outputs[0][i][3]]
#                 boxes.append(box)
#                 scores.append(maxScore)
#                 class_ids.append(maxClassIndex)

#         result_boxes = cv2.dnn.NMSBoxes(boxes, scores, self.score_thr, self.nms_thr, 0.5)

#         detections = []
#         for i in range(len(result_boxes)):
#             index = result_boxes[i]
#             box = boxes[index]
#             detection = {
#                 'class_id': class_ids[index],
#                 'class_name': CLASSES[class_ids[index]],
#                 'confidence': scores[index],
#                 'box': box,
#                 'scale': scale}
#             detections.append(detection)
            
#             self.draw_bounding_box(original_image, class_ids[index], scores[index], round(box[0] * scale), round(box[1] * scale),
#                             round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale))
#         return detection, original_image

#     def draw_bounding_box(self, img, class_id, confidence, x, y, x_plus_w, y_plus_h):
#         CLASSES = self.classes
#         colors = self.colors
        
#         label = f'{CLASSES[class_id]} ({confidence:.2f})'
#         color = colors[class_id]
#         cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
#         cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


# class URPC_Detector(Detector):
#     def __init__(self, model_path) -> None:
#         super().__init__(
#             model_path, 
#             classes=("holothurian", "echinus", "scallop", "starfish"), 
#             colors=(
#                 (31, 119, 180), 
#                 (255, 127, 14),
#                 (44, 160, 44),
#                 (214, 39, 40),
#             ), 
#             imgsize=960, 
#             score_thr=0.25, 
#             nms_thr=0.45
#             )


# def read_image(img_path, cv2_imread_flag=cv2.IMREAD_COLOR):
#     img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), flags=cv2_imread_flag)
#     return img

# def save_image(img, save_path):
#     cv2.imencode(str(Path(save_path).suffix), img)[1].tofile(save_path)

# if __name__ == '__main__':
#     net_path = "./urpc_yolov8s_960.onnx"
#     # net_path = "./urpc_yolov8s_960.torchscript"
#     img_path = "000001.jpg"

#     detector = URPC_Detector(net_path)
#     img = read_image(img_path)
#     detection, img_vis = detector.predict(copy.deepcopy(img))
#     save_path = f"{Path(img_path).stem}_result.jpg"
#     save_image(img_vis, save_path)

