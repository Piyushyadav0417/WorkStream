import threading
import queue
import time

task_queue = queue.Queue()

def worker_function(worker_id):
    while True:
        task = task_queue.get()
        try:
            action = task.get("action")
            request = task.get("request")
            project_id = task.get("project_id")
            data = task.get("data")

            if action == "GET":
                if project_id:
                    print(f"[Worker {worker_id}] 🔍 Fetching project ID {project_id} for {request.user}")
                    time.sleep(5)
                    print(f"[Worker {worker_id}] ✅ Done fetching project ID {project_id}")
                else:
                    print(f"[Worker {worker_id}] 📋 Fetching all projects for {request.user}")
                    time.sleep(5)
                    print(f"[Worker {worker_id}] ✅ Done fetching all projects")
            
            elif action == "POST":
                print(f"[Worker {worker_id}] 🛠 Creating project for {request.user}: {data}")
                time.sleep(5)
                print(f"[Worker {worker_id}] ✅ Done creating project")

        except Exception as e:
            print(f"[{str(e)}")

        task_queue.task_done()

# Start 5 worker threads
NUM_WORKERS = 5
for i in range(NUM_WORKERS):
    t = threading.Thread(target=worker_function, args=(i+1,), daemon=True)
    t.start()
