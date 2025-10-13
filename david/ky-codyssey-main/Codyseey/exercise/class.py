# Class 생성
import random
import datetime
import os

class DummySensor:
  def __init__(self):
          self.env_values = {'mars_base_internal_temperature' : 0,
                      'mars_base_external_temperature' : 0,
                      'mars_base_internal_humidity'      : 0,
                      'mars_base_external_illuminance'  : 0,
                      'mars_base_internal_co2'            : 0,
                      'mars_base_internal_oxygen'       :0
    }
  def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18,30)
        self.env_values['mars_base_external_temperature'] = random.randint(0,21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50,60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500,715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02,0.1)
        self.env_values['mars_base_internal_oxygen'] = random.randint(4,7)
  def get_env(self):
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        log_value = f"{now_str}, {self.env_values['mars_base_internal_temperature']}, {self.env_values['mars_base_external_temperature']}, {self.env_values['mars_base_internal_humidity']}, {self.env_values['mars_base_external_illuminance']}, {self.env_values['mars_base_internal_co2']}, {self.env_values['mars_base_internal_oxygen']}\n"
        file_dir = os.path.dirname(os.path.abspath(__file__))
        file_src = 'sensor.log'
        file_path = os.path.join(file_dir,file_src)
        with open(file_path,'a',encoding='utf-8') as fd:
           fd.write(log_value)
        return self.env_values

if __name__==('__main__'):
    ds = DummySensor()
    print(ds.env_values)
    ds.set_env()
    print(ds.get_env())