
import numpy as np

from detect_face import DetectFace
from color_extract import DominantColors
from colormath.color_objects import LabColor, sRGBColor, HSVColor
from colormath.color_conversions import convert_color

def is_spring_light(color):
    spring_light_palette = [
        [255, 229, 180],  # 라이트 피치
        [250, 218, 221],  # 라이트 핑크
        [230, 230, 250],  # 라이트 라벤더
        [245, 245, 220],  # 라이트 베이지
        [240, 128, 128]   # 라이트 코랄
    ]
    count=0
    for spring_color in spring_light_palette:
        if np.allclose(color, spring_color, atol=10) :
            count+=1
    return count

def is_spring_vivid(color):
    spring_vivid_palette = [
        [255, 105, 180],  # 비비드 핑크
        [255, 165, 0],    # 비비드 오렌지
        [124, 252, 0],    # 비비드 그린
        [255, 255, 0],    # 비비드 옐로우
        [0, 191, 255]     # 비비드 블루
    ]
    count = 0
    for spring_color in spring_vivid_palette:
        if np.allclose(color, spring_color, atol=10):
            count += 1

    return count
def is_summer_light(color):
    summer_light_palette = [
        [255, 204, 204],  # 라이트 로즈
        [173, 216, 230],  # 라이트 블루
        [230, 230, 250],  # 라이트 퍼플
        [211, 211, 211],  # 라이트 그레이
        [152, 251, 152]   # 라이트 민트
    ]
    count=0
    for summer_color in summer_light_palette:
        if np.allclose(color, summer_color, atol=10):
            count += 1

    return count
def is_summer_muted(color):
    summer_muted_palette = [
        [219, 112, 147],  # 뮤트 로즈
        [95, 158, 160],   # 뮤트 블루
        [180, 138, 144],  # 뮤트 라벤더
        [169, 169, 169],  # 뮤트 그레이
        [128, 128, 0]     # 뮤트 올리브
    ]
    count =0
    for summer_color in summer_muted_palette:
        if np.allclose(color, summer_color, atol=10):
            count+=1
    return count
def is_autumn_muted(color):
    autumn_muted_palette = [
        [255, 140, 0],    # 뮤트 오렌지
        [139, 69, 19],    # 뮤트 브라운
        [165, 42, 42],    # 뮤트 레드
        [128, 128, 0],    # 뮤트 올리브
        [193, 154, 107]   # 뮤트 카멜
    ]
    count=0
    for autumn_color in autumn_muted_palette:
        if np.allclose(color, autumn_color, atol=10):
            count+=1
    return count

def is_autumn_deep(color):
    autumn_deep_palette = [
        [255, 140, 0],    # 딥 오렌지
        [101, 67, 33],    # 딥 브라운
        [139, 0, 0],      # 딥 레드
        [85, 107, 47],    # 딥 올리브
        [138, 121, 93]    # 딥 카멜
    ]
    count=0
    for autumn_color in autumn_deep_palette:
        if np.allclose(color, autumn_color, atol=10):
            count+=1
    return count

def is_winter_bright(color):
    winter_bright_palette = [
        [255, 20, 147],   # 브라이트 핑크
        [0, 0, 255],      # 브라이트 블루
        [128, 0, 128],    # 브라이트 퍼플
        [0, 255, 0],      # 브라이트 그린
        [255, 255, 0]     # 브라이트 옐로우
    ]
    count=0
    for winter_color in winter_bright_palette:
        if np.allclose(color, winter_color, atol=10):
            count+=1
    return count
def is_winter_deep(color):
    winter_deep_palette = [
        [255, 20, 147],   # 딥 핑크
        [0, 0, 139],      # 딥 블루
        [128, 0, 128],    # 딥 퍼플
        [0, 100, 0],      # 딥 그린
        [105, 105, 105]   # 딥 그레이
    ]
    count=0
    for winter_color in winter_deep_palette:
        if np.allclose(color, winter_color, atol=10):
            count+=1
    return count
def is_warm(lab_b, a):


    warm_b_std = [11.6518, 11.71445, 3.6484]
    cool_b_std = [4.64255, 4.86635, 0.18735]

    warm_dist = 0
    cool_dist = 0

    body_part = ['skin', 'eyebrow', 'eye']
    for i in range(3):
        warm_dist += abs(lab_b[i] - warm_b_std[i]) * a[i]

        cool_dist += abs(lab_b[i] - cool_b_std[i]) * a[i]

    if(warm_dist <= cool_dist):
        return 1 #warm
    else:
        return 0 #cool

def is_spr(hsv_s, a):


    spr_s_std = [18.59296, 30.30303, 25.80645]#skin, hair, eye
    fal_s_std = [27.13987, 39.75155, 37.5]

    spr_dist = 0
    fal_dist = 0

    body_part = ['skin', 'eyebrow', 'eye']
    for i in range(3):
        spr_dist += abs(hsv_s[i] - spr_s_std[i]) * a[i]

        fal_dist += abs(hsv_s[i] - fal_s_std[i]) * a[i]

    if(spr_dist <= fal_dist):
        return 1 #spring
    else:
        return 0 #fall

def is_smr(hsv_s, a):


    smr_s_std = [12.5, 21.7195, 24.77064]#skin, eyebrow, eye
    wnt_s_std = [16.73913, 24.8276, 31.3726]
    a[1] = 0.5

    smr_dist = 0
    wnt_dist = 0

    body_part = ['skin', 'eyebrow', 'eye']
    for i in range(3):
        smr_dist += abs(hsv_s[i] - smr_s_std[i]) * a[i]

        wnt_dist += abs(hsv_s[i] - wnt_s_std[i]) * a[i]

    if(smr_dist <= wnt_dist):
        return 1 #summer
    else:
        return 0 #winter



def analysis(imgpath):

    df = DetectFace(imgpath)
    face = [df.left_cheek, df.right_cheek,
            df.left_eyebrow, df.right_eyebrow,
            df.left_eye, df.right_eye]


    temp = []
    clusters = 3
    for f in face:
        dc = DominantColors(f, clusters)
        face_part_color, _ = dc.getHistogram()

        temp.append(np.array(face_part_color[0]))

    cheek = np.mean([temp[0], temp[1]], axis=0)
    eyebrow = np.mean([temp[2], temp[3]], axis=0)
    eye = np.mean([temp[4], temp[5]], axis=0)

    Lab_b, hsv_s = [], []
    color = [cheek, eyebrow, eye]
    for i in range(3):
        rgb = sRGBColor(color[i][0], color[i][1], color[i][2], is_upscaled=True)
        lab = convert_color(rgb, LabColor, through_rgb_type=sRGBColor)
        hsv = convert_color(rgb, HSVColor, through_rgb_type=sRGBColor)
        Lab_b.append(float(format(lab.lab_b,".2f")))
        hsv_s.append(float(format(hsv.hsv_s,".2f"))*100)

    Lab_weight = [30, 20, 5]
    hsv_weight = [10, 1, 1]
    color=cheek
    if(is_warm(Lab_b, Lab_weight)):
        if(is_spr(hsv_s, hsv_weight)) and is_spring_light(color) >= is_spring_vivid(color):
            return '봄 라이트'
        elif (is_spr(hsv_s, hsv_weight)) and is_spring_light(color) < is_spring_vivid(color):
            return '봄 비비드'
        elif not (is_spr(hsv_s, hsv_weight)) and is_autumn_muted(color) >= is_autumn_deep(color):
            return '가을 뮤트'
        else:
            return '가을 딥'
    else:

        if (is_spr(hsv_s, hsv_weight)) and is_summer_light(color) >= is_summer_muted(color):
            return ' 여름 라이트'
        elif (is_spr(hsv_s, hsv_weight)) and is_summer_light(color) < is_summer_muted(color):
            return '여름 뮤트'
        elif not (is_spr(hsv_s, hsv_weight)) and is_winter_bright(color) >= is_winter_deep(color):
            return '겨울 브라이트'
        else:
            return '겨울 딥'
