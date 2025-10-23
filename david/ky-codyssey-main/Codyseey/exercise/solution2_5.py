from math import pi

def sphere(diameter,material,thickness=1):
    try:
       material_index={'유리':2.4, '알루미늄':2.7, '탄소강':7.85}

       volume = pi * (diameter ** 2)
       material_value = material_index[material]
       weight  = ((volume * 10000) *  material_value * thickness * 0.38) / 1000

       return (volume,weight)
    except Exception:
        raise

def main():
  try:
       diameter_input = input("지름을 입력하세요. : ").strip()
       diameter_float   = float(diameter_input)

       if diameter_float <=0 :
          raise ValueError
       
       material_input = input("재질을 입력 하세요 : ").strip()
       if material_input not in ['유리','알루미늄','탄소강']:
          raise ValueError

       thickness_input = input("두께를 입력 하세요 : ").strip()
       if not thickness_input:
          thickness_float = 1
       thickness_float  = float(thickness_float)
       if thickness_float <= 0:
          raise ValueError
      
       volume,weight = sphere(diameter_float,material_input,thickness_float)     
       print(f"재질 => {material_input}, 지름 => {diameter_float:g},  두께 => {int(thickness_float):d},  부피 => {volume:.3f},  무게 => {weight:.3f}Kg")
  except ValueError:
       print("Input Error : ")
       return
  except Exception:
       print("Processing error.")
       return

if __name__ == '__main__':
   main()       