def read_log(path: str = 'C:\\codyssey\\david\\ky-codyssey-main\\Codyseey\\exercise\\mission_computer_main.log') -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
        
    except FileNotFoundError:
        raise
    except UnicodeDecodeError:
        raise
    except Exception:
        raise

def main(): 
    try:
        log = read_log()
        print(log)

        lines = log.strip().splitlines()
        if not lines or lines[0] != 'timestamp,event,message':
            raise ValueError

        pairs = list()
        for line in lines[1:]: #헤더 제외, 1번 행(내용만)터 출력
            parts = line.strip().split(',', 2)
    

            if len(parts) != 3:
                raise ValueError

            time, _, mess = parts

            if len(time) == 19:
                pairs.append((time, mess.strip()))   # (time, mess)
            else:    
                raise ValueError

 
        print(pairs)

        try:
            sorted_pairs = sorted(pairs, key=lambda item : item[0], reverse = True)
            result_dict = dict(sorted_pairs)
            print(sorted_pairs)
            print(result_dict)
        except:
            print('Processing Error.')
            return    

    except FileNotFoundError:
        print('File open error')
        return

    except UnicodeDecodeError:
        print('Decoding error.')
        return
    
    except (ValueError, IndexError):
        print('invalid log format')
        return
    
    except Exception:
        print('Processing error.')
        return

if __name__ == '__main__':
    main()