#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
그래프 테스트 스크립트
MySQL 연결 없이 matplotlib 그래프가 제대로 작동하는지 확인
"""

import matplotlib
matplotlib.use('TkAgg')  # GUI 백엔드 설정
import matplotlib.pyplot as plt
import numpy as np

def test_simple_graph():
    """간단한 그래프 테스트"""
    print("="*50)
    print("간단한 그래프 테스트 시작...")
    
    try:
        # 샘플 데이터 생성
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        # 그래프 생성
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'b-', linewidth=2, label='sin(x)')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Simple Test Graph')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # 저장 및 표시
        plt.savefig('simple_test_graph.png', dpi=300, bbox_inches='tight')
        print("✅ 그래프 저장 완료: simple_test_graph.png")
        
        plt.show()
        print("✅ 그래프 표시 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

def test_korean_graph():
    """한글 그래프 테스트"""
    print("\n" + "="*50)
    print("한글 그래프 테스트 시작...")
    
    try:
        # 한글 폰트 설정
        try:
            plt.rcParams['font.family'] = 'Malgun Gothic'
            print("✅ 한글 폰트 설정 성공: Malgun Gothic")
        except:
            try:
                plt.rcParams['font.family'] = 'DejaVu Sans'
                print("⚠️ 대체 폰트 사용: DejaVu Sans")
            except:
                print("⚠️ 기본 폰트 사용")
        
        plt.rcParams['axes.unicode_minus'] = False
        
        # 샘플 데이터
        times = ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00']
        temps = [22, 24, 26, 28, 27, 25, 23]
        
        # 그래프 생성
        plt.figure(figsize=(12, 6))
        plt.plot(times, temps, marker='o', linewidth=2, markersize=8, 
                color='#FF6B6B', label='온도')
        
        plt.xlabel('시간', fontsize=12, fontweight='bold')
        plt.ylabel('온도 (°C)', fontsize=12, fontweight='bold')
        plt.title('시간별 온도 변화', fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 저장 및 표시
        plt.savefig('korean_test_graph.png', dpi=300, bbox_inches='tight')
        print("✅ 한글 그래프 저장 완료: korean_test_graph.png")
        
        plt.show()
        print("✅ 한글 그래프 표시 완료!")
        
    except Exception as e:
        print(f"❌ 한글 그래프 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("matplotlib 그래프 테스트 시작...")
    print(f"matplotlib 백엔드: {matplotlib.get_backend()}")
    
    # 간단한 그래프 테스트
    test_simple_graph()
    
    # 한글 그래프 테스트
    test_korean_graph()
    
    print("\n" + "="*50)
    print("모든 테스트 완료!")
