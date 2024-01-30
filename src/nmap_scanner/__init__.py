"""
# Example usage
handler = NMAPHandler()
command = "NMAP 127.0.0.1 -sV"  # Example command, replace with your target and desired scan options
try:
    response = handler.handle_command(command)
    print(response)
except NotImplementedError as e:
    response = {
        "status": "error",
        "message": str(e)
    }
    print(json.dumps(response, indent=4))
"""

from .nmap_scanner import NMAPHandler
