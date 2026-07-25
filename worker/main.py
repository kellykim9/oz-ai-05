import time
import json
from worker.redis_client import get_sync_redis_client

def run_worker():
    client = get_sync_redis_client()
    print("AI Worker started and listening to task queue...")
    
    while True:
        try:
            task_data = client.brpop("pneumonia_tasks", timeout=5)
            if task_data:
                _, task_json = task_data
                task = json.loads(task_json)
                task_id = task.get("task_id")
                image_path = task.get("image_path")
                
                print(f"Processing task {task_id} for image {image_path}...")
                
                # TODO: 실제 폐렴 예측 모델 추론 수행
                time.sleep(2)
                result = {"task_id": task_id, "status": "success", "prediction": "Normal (Sample)"}
                
                client.set(f"result:{task_id}", json.dumps(result))
                print(f"Task {task_id} completed and result saved.")
        except Exception as e:
            print(f"Error in worker: {e}")

if __name__ == "__main__":
    run_worker()