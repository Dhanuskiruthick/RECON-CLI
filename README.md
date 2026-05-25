# RECON CLI

A modular Python-based reconnaissance framework built from scratch to understand how real-world network enumeration, service fingerprinting, and intelligence gathering work internally.

**Built by Dhanus Kiruthick** — Integrated MTech Cybersecurity, VIT Bhopal | Learning by building security tools

---

## 📸 Project Overview

<img width="551" height="345" alt="image" src="https://github.com/user-attachments/assets/028acea4-c326-487b-86e8-e7f9eab808fd" />
<img width="1257" height="733" alt="image" src="https://github.com/user-attachments/assets/8e176eaf-d3a8-48a1-b388-523c9bcfe6b2" />
<img width="1251" height="677" alt="image" src="https://github.com/user-attachments/assets/2be26d77-f921-4a37-bb66-96b856194c2f" />


---

## ✨ Features

- **DNS Resolution** → Domain to IP conversion
- **TCP Port Scanning** → Multi-threaded port enumeration
- **Banner Grabbing** → Service metadata extraction
- **Service Detection** → Port-to-service mapping
- **HTTP Header Enumeration** → Web server fingerprinting
- **Risk Identification** → Information disclosure observations
- **Report Exporting** → Structured markdown/text reports
- **Modular Architecture** → Extensible, learner-friendly design

---

## 🎯 Why I Built This

Most cybersecurity students use tools like **Nmap** without understanding how reconnaissance actually works internally. I wanted to change that.

Instead of blindly running scanners, I built RECON CLI to deeply understand:

- **Socket programming** → How network communication works at the protocol level
- **TCP communication** → Connection handshakes, timeouts, error handling
- **Threading & concurrency** → Scaling port scanning efficiently
- **Service fingerprinting** → How tools identify services from metadata
- **Information leakage** → Why version disclosure becomes a security risk
- **Network enumeration workflows** → Real reconnaissance methodology

The goal: **Engineering fundamentals matter more than tool usage.**

---

## 🏗️ Architecture

RECON CLI follows a clean modular design:

```
User Input (target, port range)
    ↓
DNS Resolution (resolver.py)
    ↓
Threaded Port Scanning (scanner.py)
    ↓
Open Port Detection
    ↓
Banner Grabbing (banner.py)
    ↓
Service Identification (service_detector.py)
    ↓
HTTP Header Enumeration (http_recon.py)
    ↓
Risk Observation
    ↓
Report Generation (report_writer.py)
```

### Module Breakdown

| Module | Responsibility |
|--------|---|
| `main.py` | Orchestrates application flow and module integration |
| `resolver.py` | DNS resolution (domain → IP address) |
| `scanner.py` | Threaded TCP port scanning using raw sockets |
| `banner.py` | Service banner grabbing from open ports |
| `service_detector.py` | Maps ports to known services (HTTP, SSH, FTP, etc.) |
| `http_recon.py` | HTTP header enumeration and web server fingerprinting |
| `report_writer.py` | Generates structured reports from scan findings |
| `utils.py` | Formatting helpers and utility functions |

---

## 🚀 Usage

### Requirements

No external dependencies. Built using Python standard library:
- `socket` — Network communication
- `threading` — Multi-threaded scanning

### Installation & Running

```bash
git clone https://github.com/DhanusKiruthick/RECON-CLI.git
cd RECON-CLI

python main.py
```

### Interactive Workflow

```
Enter target domain: scanme.nmap.org
Enter starting port: 1
Enter ending port: 1000

[*] Resolving scanme.nmap.org...
[+] IP: 45.33.32.156

[*] Scanning 45.33.32.156 (1000 ports)...
[+] Port 22/tcp   → SSH
[+] Port 80/tcp   → HTTP
[+] Port 9929/tcp → Open

[*] Grabbing banners...
[+] 22/tcp: OpenSSH 6.6.1p1 Ubuntu
[+] 80/tcp: Apache 2.4.7

[*] Generating report...
[✓] Report saved to: report.txt
```

---

## 📚 What I Learned

### Technical Skills
- **Socket programming** — Raw TCP communication without libraries
- **Threading & concurrency** — Efficient multi-threaded port scanning
- **TCP handshakes** — Understanding connection states and timeouts
- **Service fingerprinting** — Identifying services from banners and metadata
- **HTTP protocol** — Manual socket-based HTTP requests

### Security Concepts
- **Reconnaissance methodology** — Information gathering workflows
- **Information disclosure** → How version exposure aids attackers
- **Port scanning tradeoffs** → Speed vs accuracy, detection risk
- **Defense-in-depth** → Why services should minimize version exposure

### Software Engineering
- **Modular architecture** → Separation of concerns
- **Code organization** → Building extensible tools
- **Error handling** → Graceful timeout and exception handling
- **Report generation** → Presenting security findings professionally

---

## ⚠️ Disclaimer

**This project was built strictly for educational and defensive security learning purposes.**

- Only scan systems you own or have **explicit written authorization** to test
- Unauthorized network scanning may violate laws in your jurisdiction
- Use responsibly for learning, not malicious purposes

---

## 🔗 Next Steps

This project taught me reconnaissance fundamentals. Next areas:

- Vulnerability scanning (service version → CVE mapping)
- Active directory enumeration
- Web application recon (robots.txt, sitemap, technology detection)
- Exploit integration

---

## 📖 Learn More

- **DNS & Networking**: DNS resolution, TCP/IP fundamentals
- **Socket Programming**: Python socket module documentation
- **Concurrent Scanning**: Threading limitations and thread pools
- **Service Fingerprinting**: IANA port registry, nmap-services database

---

**Built with curiosity and persistence.**

*Cybersecurity is learned by understanding systems, not just running tools.*
