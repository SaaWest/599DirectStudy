import os
import subprocess
from dotenv import load_dotenv
import json
import time
from datetime import datetime

def find_containerID():
 load_dotenv()
 password = os.getenv("DB_PASSWORD")

 env = os.environ.copy()
 env["DB_PASSWORD"] = password

 result = subprocess.check_output(["sudo docker ps -a | awk 'NR > 1 {print $1}'"], shell=True, env=env).decode().strip()
 print(result)
 return result

def network_query(container_id):
 container_id = find_containerID()

 load_dotenv()
 password = os.getenv("DB_PASSWORD")
 env = os.environ.copy()
 env["DB_PASSWORD"] = password

 #net_query = f"SELECT name,  network_rx_bytes, network_tx_bytes FROM docker_container_stats WHERE id = '{container_id}';"
 try:
  while True:

   timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") 

   output_file = f"system_logs/networkLog_{timestamp}.json"

   query = f"SELECT name, network_rx_bytes, network_tx_bytes FROM docker_container_stats WHERE id= '{container_id}';"
   command = f'echo "{password}" | sudo -S osqueryi --json "{query}" > {output_file}'
   print('first try')
   try:
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    print("second try")
   except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")

   time.sleep(10)

 except KeyboardInterrupt:
  print("done")

if __name__ == "__main__":
 container_id = find_containerID()
 network_query(container_id)
