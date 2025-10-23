from math import pi
def sphere(diameter,material,thickness):
   try:
      MATERIAL_INDEX = {'유리':2.4, '알루미늄':2.7,'탄소강':7.85} 
      # 표면적 : (PI * R**2)  단위 : M
      volume = pi * (diameter ** 2)

      # 무게(g) : volume (cm3 으로 변환) * MATERIAL_INDEX *  0.38
      # 무게(Kg) : 무게(g) / 1000
      material_value = MATERIAL_INDEX[material]
      volume_cm3 = volume * 10000
      weight_cm3  = volume_cm3 * material_value * 0.38 * thickness
      weight = weight_cm3 / 1000
      return(volume,weight)
   except Exception:
       raise 

def main():
   try:
      diameter_str=input("지름을 입력하세요 : ").strip()
      diameter_float = float(diameter_str)
      if diameter_float <= 0:
         raise ValueError
       
      material_str = input("재질을 입력하세요 : ").strip()
      if material_str not in ['유리','알루미늄','탄소강']:
        raise ValueError
    
      thickness_str = input("두께를 입력하세요 : ").strip()
      if thickness_str == "":
        thickness_int = 1
        
      thickness_int = int(thickness_int)
      
      if thickness_int <= 0:
        raise ValueError
      
      volume,weight = sphere(diameter_float, material_str,thickness_int)
      print(f"재질 => {material_str},  지름 => {diameter_float:g},  두께 => {thickness_int:d},  부피 => {volume:.3f}, 무게 => {weight:.3f}Kg")
   except ValueError:
     print("Input Error")
     return
   except Exception:
     print("Processing Error")
     return

if __name__ == ('__main__'):
     main()