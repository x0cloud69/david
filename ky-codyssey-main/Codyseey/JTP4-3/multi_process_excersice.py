import multiprocessing
import time

def pro1(conn, shared_list):
    for i in range(5):
        # Pipe를 통해 메시지 전송
        conn.send(f"item_{i}")
        shared_list.append(f"item_{i}")
        time.sleep(0.5)
        print(f"pro1: Pipe로 item_{i} 전송, 리스트에 item_{i} 추가")
    
    # 종료 신호
    conn.send("END")
    conn.close()
    print("pro1 완료")
    
def pro2(conn, shared_list):
    while True:
        try:
            item = conn.recv()
            time.sleep(1.5)
            if item == "END":
                break
            print(f"pro2: Pipe에서 {item} 수신")
        except:
            break
    
    print(f"pro2: 공유 리스트 = {shared_list}")
    conn.close()

if __name__ == '__main__':
    # Pipe 생성 (양방향 통신)
    conn1, conn2 = multiprocessing.Pipe()
    
    # Manager를 통한 공유 리스트 생성
    with multiprocessing.Manager() as manager:
        shared_list = manager.list()
        
        p1 = multiprocessing.Process(target=pro1, args=(conn1, shared_list))
        p2 = multiprocessing.Process(target=pro2, args=(conn2, shared_list))
        
        p1.start()
        p2.start()
        
        p1.join()
        p2.join()
        
        print(f"최종 공유 리스트: {shared_list}")
        print("Pipe를 통한 통신 완료") 