#!/bin/bash
# entrypoint.sh

echo "

██████╗ ██╗███╗   ██╗ ██████╗ ██╗   ██╗███████╗
██╔══██╗██║████╗  ██║██╔════╝ ██║   ██║██╔════╝
██║  ██║██║██╔██╗ ██║██║  ███╗██║   ██║███████╗
██║  ██║██║██║╚██╗██║██║   ██║██║   ██║╚════██║
██████╔╝██║██║ ╚████║╚██████╔╝╚██████╔╝███████║
╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚══════╝
                                               
"

# Start FastAPI in the background
uvicorn dingus.main:app --host 0.0.0.0 --port 8000 --reload
