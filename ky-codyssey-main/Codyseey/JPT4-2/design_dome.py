import math

calculate_history = []

def sphere_area(diameter,material,thickness):
    volume = 0
    weight = 0


    ##################################################
    # 표면적 구하는 공식
    # volume = 2 * math.pi * (diameter / 2)**2
    ##################################################

    if thickness == "":
        thickness = 1
        
    try:
       diameter = float(diameter)
    except ValueError:
       raise ValueError(f"diameter : {diameter} 숫자가 아닙니다.")
    
    if diameter <= 0:
        raise ValueError(f"diameter : {diameter} 0보다 작습니다")

    try:
        thickness = float(thickness)
    except ValueError:
        raise ValueError(f"thickness : {thickness}  숫자가 아닙니다.")

    if thickness <= 0:
        raise ValueError(f"thickness : {thickness} 0보다 작습니다")
    
    volume = f"{(2 * math.pi * (float(diameter) / 2)**2):.3f}"

    ##################################################
    # 반구체돔 무게 구하는 공식
    # weight = volumn * Density
    # Density : 유리: 2.4, 알루미늄: 2.7, 탄소강: 7.85
    ##################################################

    density = {"유리": 2.4, "알루미늄":2.7,"탄소강":7.85}


    if material not in density:
        raise ValueError(f"올바른 재질이 아닙니다. 가능한 재질 : {', '.join(density.keys())}")
    
    density_value = density[material]
    
    # 반지름 (m >> cm)
    radius = (float(diameter) / 2) * 100

    # 표면적 (cm2)
    area = 2 * math.pi * (radius**2)

    # 무게 계산(g) : 표면적 * 두께 * 밀도 
    weight = area  * density_value * float(thickness)
    weight = (weight / 1000) *0.38

    
    ##################################################
    # 전역변수에 저장하기 위해 딕셔너리 객체 생성
    ##################################################

    result = {
        "지름" : diameter,
        "재질" : material,
        "두께" : thickness,
        "면적" : float(volume),
        "무게" : round(weight,3)
    }

    calculate_history.append(result)

    return material, thickness,diameter,volume,weight

def print_history():
    print("\n ===== 계산 기록 ===== ")
    for i, result in enumerate(calculate_history,1):
        print(f"{i}번째 계산")
        print(f"재질 => {[result['재질']]}, 지름 => {[result['지름']]}, 두께 => {[result['두께']]}, 면적 => {[result['면적']]},무게 => {[result['무게']]}")

while True:
    print("\n 돔 계산기 (종료 : 'q' , 전역확인 : 'h' 입력하세요)")
    print("_"*50)

    diameter = input("돔의 지름을 입력하세요 :")
    if diameter.lower() == "q":
        print("종료합니다.")
        break
    elif diameter.lower() == 'h':
        print_history()
        continue

    material = input("돔의 소재를 입력하세요 :")
    if material.lower() == "q":
        print("종료합니다.")
        break
    elif material.lower() == 'h':
        print_history()
        continue

    thickness = input("돔의 두께를 입력하세요 :")
    if thickness.lower() == "q":
        print("종료합니다.")
        break
    elif thickness.lower() == 'h':
        print_history()
        continue

    try:
        material, thickness,diameter,volume,weight = sphere_area(diameter,material,thickness)
        print(f"재질 => {material}, 지름 => {diameter}, 두께 => {thickness}, 면적 => {volume}  m², 무게 => {weight:.3f} kg" )
    except ValueError as e:
        print(f"오류가 발생했습니다 : {e}")


      


