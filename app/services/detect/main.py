import os
import json
import cv2
import dlib
import numpy as np
from shapely.geometry import Polygon, Point
from ultralytics import YOLO
import argparse

BASE_DIR = os.getcwd()
DETECTIONS_DIR = os.path.join(BASE_DIR, '.temp/detections')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

ACNE_MODEL_PATH = os.path.join(SCRIPT_DIR, "model.pt")
PREDICTOR_PATH = os.path.join(SCRIPT_DIR, "dlib.dat")

ACNE_CLASSES = {
    0: "comedone",
    1: "nodules",
    2: "papules",
    3: "pustules"
}

CLASS_COLORS = {
    "comedone": (255, 255, 255), # branco
    "nodules": (0, 0, 255),      # vermelho
    "papules": (0, 165, 255),    # laranja
    "pustules": (0, 255, 255)    # amarelo
}

SEVERITY_WEIGHTS = {
    "comedone": 1,
    "papules": 2,
    "pustules": 3,
    "nodules": 4
}

GAGS_FACTORS = {
    'forehead': 2,
    'left-cheek': 2,
    'right-cheek': 2,
    'nose': 1,
    'chin': 1
}


def get_next_folder(base_path):
    """Cria pastas incrementais (0, 1, 2...) dentro do ID da consulta."""
    os.makedirs(base_path, exist_ok=True)
    existing = []
    for f in os.listdir(base_path):
        if f.isdigit():
            try:
                existing.append(int(f))
            except: continue
    next_number = max(existing, default=-1) + 1
    full_path = os.path.join(base_path, str(next_number))
    os.makedirs(full_path, exist_ok=True)
    return full_path

def get_dlib_regions(img, detector, predictor):
    """Segmenta o rosto usando Dlib + Convex Hull para evitar erros de rotação."""
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dets = detector(img_gray, 0)

    if len(dets) == 0:
        return None

    shape = predictor(img_gray, dets[0])
    pts = np.array([(shape.part(i).x, shape.part(i).y) for i in range(68)], dtype=np.int32)

    regions_coords = {}

    nose_top_y = pts[27, 1]
    vertical_span = pts[27, 1] - int((pts[21, 1] + pts[22, 1]) / 2)
    forehead_top_y = nose_top_y - int(vertical_span * 2.5)

    raw_forehead = np.array([
        pts[17], pts[21], pts[22], pts[26],
        [pts[26,0], forehead_top_y], [pts[17,0], forehead_top_y]
    ], dtype=np.int32)
    regions_coords['forehead'] = cv2.convexHull(raw_forehead)

    raw_nose = np.array([pts[27], pts[31], pts[33], pts[35]], dtype=np.int32)
    regions_coords['nose'] = cv2.convexHull(raw_nose)

    raw_chin = np.concatenate([pts[5:12], [pts[54], pts[48]]])
    regions_coords['chin'] = cv2.convexHull(raw_chin)

    raw_cheek_l = np.array([
        pts[0], pts[1], pts[2], pts[3], pts[4],
        pts[48], pts[31], pts[27], pts[21], pts[17]
    ], dtype=np.int32)
    regions_coords['left-cheek'] = cv2.convexHull(raw_cheek_l)

    raw_cheek_r = np.array([
        pts[16], pts[15], pts[14], pts[13], pts[12],
        pts[54], pts[35], pts[27], pts[22], pts[26]
    ], dtype=np.int32)
    regions_coords['right-cheek'] = cv2.convexHull(raw_cheek_r)

    return {k: [tuple(p[0]) for p in v] for k, v in regions_coords.items()}

def assign_and_calculate_gags(detections, regions_coords):
    """
    Atribui espinhas às regiões (com lógica de proximidade) e calcula score.
    detections: lista de (x1, y1, x2, y2, class_name)
    regions_coords: dict de pontos
    """
    shapely_polys = {r: Polygon(pts) for r, pts in regions_coords.items()}

    region_counts = {r: {k: 0 for k in ACNE_CLASSES.values()} for r in GAGS_FACTORS.keys()}

    for x1, y1, x2, y2, cls_name in detections:
        center = Point((x1+x2)/2, (y1+y2)/2)
        assigned_region = None

        for r_name, poly in shapely_polys.items():
            if poly.contains(center):
                assigned_region = r_name
                break

        if not assigned_region:
            min_dist = float('inf')
            closest_r = None

            for r_name, poly in shapely_polys.items():
                dist = poly.distance(center)
                if dist < min_dist:
                    min_dist = dist
                    closest_r = r_name

            if closest_r and min_dist < 150:
                assigned_region = closest_r

        if assigned_region:
            region_counts[assigned_region][cls_name] += 1

    # fator * peso da pior lesão na região
    total_score = 0
    for region, counts in region_counts.items():
        factor = GAGS_FACTORS.get(region, 0)
        max_severity = 0

        for l_type, count in counts.items():
            if count > 0:
                w = SEVERITY_WEIGHTS.get(l_type, 0)
                if w > max_severity:
                    max_severity = w

        total_score += factor * max_severity

    if total_score == 0: severity = 'Nenhuma'
    elif total_score <= 18: severity = 'Leve'
    elif total_score <= 30: severity = 'Moderada'
    elif total_score <= 38: severity = 'Grave'
    else: severity = 'Muito grave'

    return total_score, severity, region_counts

# ==============================================================================
# FUNÇÃO PRINCIPAL
# ==============================================================================
def process_image(image_path, consulta_id, conf=0.25):
    """
    Executa todo o pipeline
    """
    if not os.path.exists(image_path): raise FileNotFoundError("Imagem não encontrada")
    if not os.path.exists(PREDICTOR_PATH): raise FileNotFoundError("Modelo Dlib não encontrado")
    if not os.path.exists(ACNE_MODEL_PATH): raise FileNotFoundError("Modelo YOLO não encontrado")

    img = cv2.imread(image_path)
    if img is None:
        raise RuntimeError(
            "Falha ao ler a imagem. Verifique se o arquivo enviado é um formato de imagem válido."
        )

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)
    yolo_model = YOLO(ACNE_MODEL_PATH)

    regions_coords = get_dlib_regions(img, detector, predictor)

    if regions_coords is None:
        regions_coords = {}
        error_msg = "Rosto não detectado pelo Dlib"
    else:
        error_msg = None

    results = yolo_model.predict(img, conf=conf, verbose=False)[0]
    detections = []

    if results.boxes:
        boxes_cpu = results.boxes.cpu()
        for box, cls_id in zip(boxes_cpu.xyxy, boxes_cpu.cls):
            
            x1, y1, x2, y2 = map(int, box)

            cls_name = ACNE_CLASSES.get(int(cls_id))
            if cls_name is None:
                continue
            detections.append((x1, y1, x2, y2, cls_name))

            color = CLASS_COLORS.get(cls_name, (0, 0, 0))
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

    if not error_msg and regions_coords:
        score, severity, region_counts = assign_and_calculate_gags(detections, regions_coords)
    else:
        score, severity, region_counts = 0, "Não calculado", {}

    base_folder = os.path.join(DETECTIONS_DIR, consulta_id)
    final_folder = get_next_folder(base_folder)

    cv2.imwrite(os.path.join(final_folder, 'detected_image.jpg'), img)

    result_data = {
        "gags_score": score,
        "gags_severity": severity,
        "region_counts": region_counts,
        "image_path": os.path.join(final_folder, 'detected_image.jpg'),
        "error": error_msg
    }

    with open(os.path.join(final_folder, 'result.json'), 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=4, ensure_ascii=False)

    return final_folder



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--image", required=True, help="Caminho da imagem")
    parser.add_argument("--consulta_id", required=True)
    parser.add_argument("--conf", type=float, default=0.25)

    args = parser.parse_args()

    folder = process_image(
        args.image,
        args.consulta_id,
        args.conf
    )

    print(json.dumps({
        "output_folder": folder
    }))