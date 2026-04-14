# Inference called with Python.NET. Uses Hailo YOLO

import numpy as np
from hailo_platform import HEF, VDevice, InferVStreams, ConfigureParams, InputVStreamParams, OutputVStreamParams

# Global variables to hold the hardware state
infer_pipeline = None
input_vstream_info = None
output_vstream_info = None

def initialize_hailo(hef_path):
    """Initializes the Hailo-8 hardware and loads the model."""
    global infer_pipeline, input_vstream_info, output_vstream_info
    
    # 1. Load HEF
    hef = HEF(hef_path)
    
    # 2. Configure the device
    target = VDevice()
    configure_params = ConfigureParams.create_from_hef(hef, interface=HailoStreamInterface.PCIe)
    network_group = target.configure(hef, configure_params)[0]
    
    # 3. Create Virtual Streams for input and output
    input_vstreams_params = InputVStreamParams.make_from_network_group(network_group)
    output_vstreams_params = OutputVStreamParams.make_from_network_group(network_group)
    
    infer_pipeline = InferVStreams(network_group, input_vstreams_params, output_vstreams_params)
    input_vstream_info = hef.get_input_vstream_infos()
    output_vstream_info = hef.get_output_vstream_infos()
    
    print(f"Hailo-8 Initialized with model: {hef_path}")

def perform_detection(image_np):
    """Runs inference on the provided NumPy array."""
    global infer_pipeline, input_vstream_info, output_vstream_info
    
    # 1. Run Hardware Inference
    input_data = {input_vstream_info[0].name: np.expand_dims(image_np, axis=0).astype(np.uint8)}
    with infer_pipeline:
        raw_results = infer_pipeline.infer(input_data)
    
    # 2. Extract the NMS Output Tensor
    # Hailo NMS output shape is typically [1, 1, 1, 100, 6] 
    # [image_index, ?, ?, max_detections, (y1, x1, y2, x2, score, class_id)]
    output_node_name = output_vstream_info[0].name
    detections_tensor = raw_results[output_node_name][0]
    
    img_h, img_w, _ = image_np.shape
    detections = []

    # 3. Translate Tensors to C# Dictionary Format
    for i in range(detections_tensor.shape[1]):
        # [y_min, x_min, y_max, x_max, confidence, class_id]
        row = detections_tensor[0, 0, i]
        confidence = float(row[4])
        
        if confidence < 0.25: # Filter by threshold
            continue
            
        # Hailo often returns normalized coordinates (0.0 to 1.0)
        # We convert them to absolute pixel values for the C# Rectangle
        ymin, xmin, ymax, xmax = row[0], row[1], row[2], row[3]
        
        detections.append({
            "label": f"Class_{int(row[5])}", # Map this to a name list if you have one
            "confidence": confidence,
            "x": xmin * img_w,
            "y": ymin * img_h,
            "width": (xmax - xmin) * img_w,
            "height": (ymax - ymin) * img_h
        })
        
    return detections