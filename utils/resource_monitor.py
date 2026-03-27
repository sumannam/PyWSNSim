import os
import psutil
import threading

class ResourceMonitor:
    def __init__(self, interval=0.5):
        """
        interval: 자원을 측정하는 주기 (초 단위, 기본값 0.5초)
        """
        self.process = psutil.Process(os.getpid())
        self.interval = interval
        self.is_running = False
        self.cpu_records = []
        self.mem_records = []
        self.thread = None

    def _monitor(self):
        # 첫 호출 시 0.0을 반환하는 psutil 특성상 한 번 버려줌
        self.process.cpu_percent()
        while self.is_running:
            self.cpu_records.append(self.process.cpu_percent(interval=self.interval))
            # RSS 메모리를 MB 단위로 변환하여 저장
            self.mem_records.append(self.process.memory_info().rss / (1024 * 1024))

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self._monitor)
        self.thread.daemon = True  # 메인 스레드 종료 시 함께 종료되도록 설정
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join()
        
        # 통계 계산
        avg_cpu = sum(self.cpu_records) / len(self.cpu_records) if self.cpu_records else 0
        max_cpu = max(self.cpu_records) if self.cpu_records else 0
        max_mem = max(self.mem_records) if self.mem_records else 0
        avg_mem = sum(self.mem_records) / len(self.mem_records) if self.mem_records else 0
        
        # 딕셔너리 형태로 결과 반환
        return {
            'avg_cpu': avg_cpu,
            'max_cpu': max_cpu,
            'avg_mem': avg_mem,
            'max_mem': max_mem,
            'cpu_history': self.cpu_records,
            'mem_history': self.mem_records
        }