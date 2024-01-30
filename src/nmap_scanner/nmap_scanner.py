import json
import nmap

# Assuming the logger setup is correctly defined elsewhere
from logger import Log
log = Log("nmap_scanner")

class NMAPHandler:
    def __init__(self):
        log.debug("Initializing NMAPHandler")
        self.scanner = nmap.PortScanner()

    def scan(self, hosts, arguments):
        try:
            log.debug(f"Scanning {hosts} with arguments {arguments}")
            scan_result = self.scanner.scan(hosts=hosts, arguments=arguments)
            log.debug("Scan completed")

            #Processing scan results for easier interpretation
            processed_results = {host: self.scanner[host] for host in self.scanner.all_hosts()}
            log.debug("Scan results processed")
            return {"status": "success", "results": processed_results}
        except nmap.PortScannerError as e:
            log.error(f"Scan error: {e}")
            return {"status": "error", "message": str(e)}

    def handle_command(self, command):
        log.debug(f"Handling command {command}")
        parts = command.split(maxsplit=2)
        if len(parts) < 3:
            log.error("Invalid command format. Expected: NMAP <hosts> <arguments>")
            return json.dumps({"status": "error", "message": "Invalid command format. Expected: NMAP <hosts> <arguments>"}, indent=4)

        _, hosts, arguments = parts

        scan_results = self.scan(hosts, arguments)

        # Packaging the answer in a JSON format
        response = {
            "status": scan_results["status"],
            "command": command,
            "results": scan_results.get("results", {}),
            "message": scan_results.get("message", "")
        }
        log.debug(f"Command handled, returning {response}")
        return json.dumps(response, indent=4)

# Usage example
if __name__ == "__main__":
    nmap_handler = NMAPHandler()
    command = "NMAP 127.0.0.1 -sV"
    response = nmap_handler.handle_command(command)
    print(response)
