import json

import nmap
from logger import Log

log = Log("nmap_scanner")


class NMAPHandler:
    """
    NMAP Handler class, responsible for scanning hosts with NMAP
    """

    def __init__(self):
        """
        Initialize the NMAPHandler
        """
        log.debug("Initializing NMAPHandler")
        self.scanner = nmap.PortScanner()

    def scan(self, hosts, arguments):
        """
        Scan hosts with NMAP
        :param hosts: The hosts to scan
        :param arguments: The arguments to scan with
        :return: The scan results
        """
        log.debug(f"Scanning {hosts} with arguments {arguments}")
        try:
            scan_result = self.scanner.scan(hosts=hosts, arguments=arguments)
            log.debug("Scan completed")
            processed_results = {host: self.scanner[host] for host in self.scanner.all_hosts()}
            log.debug("Scan results processed")
            return {"status": "success", "results": processed_results}
        except nmap.PortScannerError as e:
            log.error(f"Scan error: {e}")
            return {"status": "error", "message": str(e)}

    def handle_command(self, command):
        """
        Handle a command from the Nester server
        :param command: The command to handle
        :return: The command results
        """
        log.debug(f"Handling command {command}")
        parts = command.split(maxsplit=2)
        if len(parts) < 3:
            log.error("Invalid command format. Expected: NMAP <hosts> <arguments>")
            return json.dumps(
                {"status": "error", "message": "Invalid command format. Expected: NMAP <hosts> <arguments>"}, indent=4)

        _, hosts, arguments = parts

        scan_results = self.scan(hosts, arguments)

        response = {
            "status": scan_results["status"],
            "command": command,
            "results": scan_results.get("results", {}),
            "message": scan_results.get("message", "")
        }
        log.debug(f"Command handled, returning {response}")
        return json.dumps(response, indent=4)
