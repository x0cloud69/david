from math import pi

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
      v_diameter = float(input("지름(m)을 입력하세요"))
      v_material = str(input("재질(유리/알리미늄/탄소강) 을 입력하세요"))
      v_thickness = float(input("두께를 입력하세요"))
      v_area,v_mars_weight_kg = sphere_area(v_diameter,v_material,v_thickness)
      print(f"재질 : {v_material},  지름 : {v_diameter:.3f},  두께 : {v_thickness},  면적 : {v_area:.3f}, 무게 : {v_mars_weight_kg:.3f}kg")
      
   except ValueError:
      print("Invalid Input Error.")
      return 
   except Exception:
        print("오류가 발생 했습니다.")
        return 

if __name__ == '__main__':
    main()