def identify_service(port):

    common_services = {

        21: "FTP",
        22: "SSH",
        23: "TELNET",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        139: "NETBIOS",
        143: "IMAP",
        443: "HTTPS",
        3306: "MYSQL",
        3389: "RDP"
    }

    return common_services.get(port, "UNKNOWN")