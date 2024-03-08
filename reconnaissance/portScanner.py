import asyncio
import nmap3

nmap = nmap3.Nmap()

#TODO: error if fields are empty
#TODO: fix all ports option, add scan common ports, and port range

async def format_result(scan_results, target, vulnscan, callback=None):
    message = f""
    if target in scan_results:
        host_info = scan_results[target]
        if 'ports' in host_info:
            ports = host_info['ports']
            open_ports = [port for port in ports if port['state'] == 'open']
            if open_ports:
                message += "Open Ports and Services:\n"
                for port_info in open_ports:
                    port_id = port_info['portid']
                    service_info = port_info.get('service', {})
                    service_name = service_info.get('name', 'unknown service')
                    product = service_info.get('product', '')
                    version = service_info.get('version', '')
                    extra_info = service_info.get('extrainfo', '')
                    product_info = f"{product} {version} {extra_info}".strip()
                    message += f"\n  Port {port_id}/TCP - {service_name} {product_info}\n"
                    if 'scripts' in port_info and vulnscan:
                        message += "    Vulnerabilities:\n"
                        for script in port_info['scripts']:
                            script_name = script.get('name')
                            script_output = script.get('raw', 'No additional details provided.')
                            message += f"      {script_name}: {script_output}\n"
            else:
                message += "No open ports found.\n"
        else:
            message += "No port information available.\n"
    else:
        message += "No information for host.\n"
    
    if callback:
        callback(message)

async def scanPorts(target, ports, vulnscan=False, callback=None):
    args = f'-p{ports}'
    if vulnscan:
        args += ' --script vuln'
    
    loop = asyncio.get_running_loop()
    results = await loop.run_in_executor(None, lambda: nmap.nmap_version_detection(target, args=args))
    await format_result(results, target, vulnscan, callback)

async def main(target, ports, vulnscan=False, callback=None):
    await scanPorts(target, ports, vulnscan, callback)

def startPortScanner(target, ports, vulnscan=False, callback=None, completion_callback=None):
    asyncio.run(main(target, ports, vulnscan=vulnscan, callback=callback))
    if completion_callback:
        completion_callback()
