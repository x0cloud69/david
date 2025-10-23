from math import pi
from sys import intern

def sphere_area(diameter: float, material: str, thickness: float = 1.0) -> tuple[float, float]:
    MATERIALS = {'유리': 2.4, '알루미늄': 2.7, '탄소강': 7.85}
    if diameter <= 0 or thickness <= 0 or material not in MATERIALS:
        raise ValueError

    try:
        density_g_cm3 = MATERIALS[material]
        area_m2 = pi * (diameter ** 2)
        area_cm2 = area_m2 * 10000
        volume_cm3 = area_cm2 * thickness
        mass_kg = (density_g_cm3 * volume_cm3) / 1000
        mars_weight_kg = mass_kg * 0.38
        return (area_m2, mars_weight_kg)
    except Exception:
        raise

def main():
     try: 
        d_str = input("지름을 입력하세요 : ")
        diameter = float(d_str)
        if diameter <= 0:
           raise ValueError
           
        d_str = input("재질을 입력하세요 : ")
        material = d_str.strip()
        if material not in ['유리','알루미늄','탄소강']:
            raise ValueError

        d_str = input("두께를 입력하세요 : ")
      
        if d_str.strip() == '':
           d_str = 1
        thickness = int(d_str)
        if thickness <= 0:
            raise ValueError

        area_m, mars_weight = sphere_area(diameter, material, thickness) 
        print(f"재질 : {material},  지름 : {diameter:g} , 두께 : {thickness:d}, 면적 : {area_m:.3f}, 무게 : {mars_weight:.3f} kg")
    
     except ValueError:
           print("Input Error")
           return
     except Exception:
           print("Processing Error")
           return   

if __name__ == '__main__':
   main()