from resolver import resolve_target
from scanner import scan_ports
from banner import grab_banner
from utils import line
from service_detector import identify_service
from http_recon import get_http_headers
from report_writer import save_report


def banner():

    print(r"""
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝

        RECON CLI v1.0 by Dhanus Kiruthick
""")


banner()

target = input("\nEnter target: ")

start_port = int(input("Start Port: "))
end_port = int(input("End Port: "))

ip = resolve_target(target)

if ip is None:

    print("Could not resolve target")

    exit()

print(f"\nResolved IP: {ip}")

line()

report_data = ""

open_ports = scan_ports(ip, start_port, end_port)

for port in open_ports:

    service = identify_service(port)

    print(f"[OPEN] {port}/tcp → {service}")

    report_data += f"[OPEN] {port}/tcp → {service}\n"

    banner_data = grab_banner(ip, port)

    if banner_data:

        print(f"[BANNER] {banner_data}")

        report_data += f"[BANNER] {banner_data}\n"

        if "/" in banner_data:

            print("[RISK] Possible version disclosure")

            report_data += "[RISK] Possible version disclosure\n"

    if port == 80:

        headers = get_http_headers(target)

        if headers:

            print("\n[HTTP HEADERS]\n")

            print(headers[:500])

            report_data += "\n[HTTP HEADERS]\n"

            report_data += headers[:500]

    line()

save_report(report_data)

print("\nReport saved to report.txt")