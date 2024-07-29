import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--port","-p",required=True,help="Port number <int>")

args = parser.parse_args()
port:int=int(args.port)
os.system(f"echo Running Webserver On Port {port}")
os.system(f"python3 -m http.server {port}")
