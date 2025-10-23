from math import pi

def sphere(diameter,material,thickness=1):
    MATERIAL_INDEX = {'유리':2.4,  '알루미늄':2.7, '탄소강':7.85}

# VOLUME : pi * diameter ** 2
# WEIGHT  : ((volume * 10000)* material_index * thickness * 0.38) / 1000
    try:
      volume = pi * (diameter ** 2)
  
      material_value = MATERIAL_INDEX[material]
      volume_cm3 = volume * 10000
      weight = (volume_cm3 * material_value * thickness * 0.38) / 1000

      return (volume,weight)
    except Exception:
      raise 
def main():
     try:
        diameter_input  = input("지름을 입력하세요 : ").strip()
        diameter_float   = float(diameter_input)
        if diameter_float <= 0:
           raise ValueError
 
        material_input  = input("재질을 입력하세요 : ").strip()
        if material_input not in ['유리','알루미늄','탄소강']:
           raise ValueError

        thickness_input = input("두께를 입력하세요 : ").strip()
        if thickness_input == "":
           thickness_int = 1
        else:
           thickness_int = float(thickness_input)
           print(thickness_int)
        if thickness_int <=0:
           raise ValueError
        volume,weight = sphere(diameter_float,material_input,thickness_int)
        print(f"재질 => {material_input}, 지름 => {diameter_float:g}, 두께 => {int(thickness_int):d}, 부피 => {volume:.3f},  무게 => {weight:.3f}Kg")

    
     except ValueError:
        print("Input Error : ")
        return 
     except Exception:
        print("Process Error")


if __name__ == '__main__':
    main()

