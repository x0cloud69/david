from math import pi


# RETURN 값 : VOLUME, WEIGHT
# volume : PI * 지름^2 (단위 : M)
# weight : volume * MATERIAL_INDEX * 고유값 * 두께  (여기서 volume=volume * 10000)  , weight 는 Kg 단위로 (/1000)
def sphere(diameter,material,thickness):
      MATERIAL_INDEX = {'유리':2.4, '알루미늄':2.7,'탄소강':7.85}
      try:
         volume = pi * (diameter ** 2)
         material_value = MATERIAL_INDEX[material]
         weight = ((volume * 10000) * material_value * thickness * 0.38) / 1000
         return (volume,weight)
      except Exception:
         raise

def main():
     try:
        diameter_input = input("지름을 입력하세요 : ").strip()
        diameter_input = float(diameter_input)
        if diameter_input <= 0:
           raise ValueError
        
        material_input = input("재질을 입력하세요 : ").strip()
        if material_input not in ['유리','알루미늄','탄소강']:
           raise ValueError

        thickness_input = input("두께를 입력 하세요 : ").strip()
        if thickness_input == "":
           thickness_input = "1"
        thickness_input = int(thickness_input) 
        if thickness_input <=0:
           raise ValueError

        volume,weight = sphere(diameter_input, material_input,thickness_input)
        print(f"지름 => {diameter_input:g}, 제질 => {material_input},  두께 => {thickness_input:d}, 부피 => {volume:.3f}, 무게 => {weight:.3f}Kg")
     except ValueError:
        print("Input Error")
     except Exception as e:
       print(e)
if __name__ == '__main__':
   main()

      

     