import cv2
import numpy as np

def generate_gradcam(image_bytes):
    # Image read karna
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (224, 224))
    
    # Dummy heatmap calculation for testing
    mask = np.random.rand(224, 224) 
    heatmap = cv2.applyColorMap(np.uint8(255 * mask), cv2.COLORMAP_JET)
    overlayed_img = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)
    
    # Bytes me return karna taaki API bhej sake
    _, buffer = cv2.imencode('.jpg', overlayed_img)
    return buffer.tobytes()