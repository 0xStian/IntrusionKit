import nmap

nm = nmap.PortScanner()


def scanPorts(target, ports, vulnscan=False, verbose=False):
    #convert to comma seperated string
    ports_str = ','.join(str(port) for port in ports)

    args = ''
    if verbose:
        args += '-v -v '
    if vulnscan:
        args += '--script=vuln'


    print(f"{target}, {ports}, {args}")
    nm.scan(hosts=target, ports=ports_str, arguments=args)


    for host in nm.all_hosts():
        print(f"Host: {host} ({nm[host].hostname()})")
        print("Open ports and potential vulnerabilities:")
        for proto in nm[host].all_protocols():
            open_ports = nm[host][proto].keys()
            for port in open_ports:
                print(f"Port: {port}")
                if vulnscan:
                    for script, output in nm[host][proto][port].get('script', {}).items():
                        print(f"Vulnerability: {script}")
                        print(f"Output: {output}")


scanPorts("127.0.0.1", [80], vulnscan=True, verbose=True)