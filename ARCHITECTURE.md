# RECON CLI — Architecture & Design

## System Overview

RECON CLI is designed as a modular reconnaissance framework that decouples concerns across independent components. This document outlines the architecture, data flow, and design decisions.

---

## 🔄 Data Flow Pipeline

```
┌─────────────────┐
│   User Input    │  (target domain, port range)
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ DNS Resolution  │  resolver.py → socket.gethostbyname()
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   IP Address    │  Validated target IP
└────────┬────────┘
         │
         ↓
┌──────────────────────────────┐
│ Threaded Port Scanner        │  scanner.py → socket.socket(AF_INET, SOCK_STREAM)
│ (Multi-threaded TCP SYN)     │  Attempts connection on each port
└────────┬─────────────────────┘
         │
         ↓
┌──────────────────────────────┐
│   Open Ports Detected        │  Stores successful connections in list
└────────┬─────────────────────┘
         │
         ↓
┌──────────────────────────────┐
│   Banner Grabbing            │  banner.py → socket.recv() on open ports
│   (Service Metadata)         │  Retrieves version strings
└────────┬─────────────────────┘
         │
         ↓
┌──────────────────────────────┐
│   Service Identification     │  service_detector.py → Port:Service mapping
│   (Port → Service Mapping)   │  (80→HTTP, 22→SSH, 3306→MySQL, etc.)
└────────┬─────────────────────┘
         │
         ↓
┌──────────────────────────────┐
│   HTTP Header Enumeration    │  http_recon.py → Raw HTTP GET requests
│   (Web Server Fingerprinting)│  Extracts Server, X-Powered-By, etc.
└────────┬─────────────────────┘
         │
         ↓
┌──────────────────────────────┐
│   Risk Observation           │  Identifies information disclosure
│   (Security Implications)    │  Notes version exposure risks
└────────┬─────────────────────┘
         │
         ↓
┌──────────────────────────────┐
│   Report Generation          │  report_writer.py → Structured output
│   (Findings Aggregation)     │  Markdown/text report file
└────────┬─────────────────────┘
         │
         ↓
┌──────────────────────────────┐
│   report.txt (Output)        │  Final deliverable with all findings
└──────────────────────────────┘
```

---

## 📦 Module Responsibilities

### **main.py** — Orchestration Layer

**Purpose**: Control application flow and coordinate module interactions

**Key Functions**:
- Accept user input (target, port range)
- Validate inputs
- Call resolver → scanner → banner → http_recon → report_writer in sequence
- Handle errors and provide status messages
- Display progress to user

**Design Decision**: Single entry point ensures clean application flow

---

### **resolver.py** — DNS Resolution

**Purpose**: Convert domain names to IP addresses

**How It Works**:
```python
socket.gethostbyname("scanme.nmap.org")  # → "45.33.32.156"
```

**Key Considerations**:
- Error handling for invalid domains
- Validates IP address format
- Supports both domain names and direct IP inputs

**Why It Matters**: 
Network tools need IP addresses. This module abstracts DNS lookup complexity.

---

### **scanner.py** — Threaded Port Scanning

**Purpose**: Efficiently scan multiple ports using multi-threading

**Core Logic**:
```
For each port in range:
    Create socket (AF_INET, SOCK_STREAM)
    Attempt connection with 2-second timeout
    If successful: Add to open_ports list
    Close socket
```

**Threading Strategy**:
- Creates thread pool (default: 100 threads)
- Each thread scans a subset of ports
- Scales scanning speed while limiting resource usage

**Key Metrics**:
- Scanning 1-1000 ports: ~10-15 seconds (vs. 1000+ seconds sequentially)
- Timeout per port: 2 seconds (prevents hanging)
- Threading overhead: Negligible at 100 threads

**Why Threading Matters**:
Sequential scanning is too slow for practical reconnaissance. Threading enables realistic scanning speeds.

---

### **banner.py** — Service Banner Grabbing

**Purpose**: Retrieve service metadata from open ports

**How It Works**:
```python
socket.send()  # Send initial request/handshake
banner = socket.recv(1024).decode()  # Receive response
# Example: "SSH-2.0-OpenSSH_6.6.1p1 Ubuntu 2ubuntu2.13"
```

**Services Handled**:
- **SSH**: Automatic banner (port 22)
- **HTTP**: Send "GET / HTTP/1.0\r\n\r\n"
- **FTP**: Automatic banner (port 21)
- **SMTP**: Automatic banner (port 25)
- **Generic TCP**: Send empty request, capture response

**Error Handling**:
- Services that don't send banners return "[No Banner]"
- Timeouts handled gracefully
- Decoding errors caught and logged

**Why This Matters**:
Version strings are information leakage vectors. Gathering them teaches how fingerprinting works defensively.

---

### **service_detector.py** — Port-to-Service Mapping

**Purpose**: Map ports to known services

**Database Structure**:
```python
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    # ... additional common ports
}
```

**Design Decision**: 
Hardcoded dictionary is fast and sufficient for learning. Real tools (nmap) use external databases.

**Why It Matters**:
Reconnaissance is about pattern recognition. Knowing which services run on which ports is fundamental.

---

### **http_recon.py** — HTTP Header Enumeration

**Purpose**: Fingerprint web servers using HTTP headers

**How It Works**:
```
1. Send raw HTTP request: "GET / HTTP/1.0\r\nHost: target\r\n\r\n"
2. Receive HTTP response
3. Parse headers (Server, X-Powered-By, X-AspNet-Version, etc.)
4. Extract version information
```

**Headers Extracted**:
- `Server` → Web server type (Apache, Nginx, IIS, etc.)
- `X-Powered-By` → Backend framework (PHP, ASP.NET, etc.)
- `X-AspNet-Version` → .NET version disclosure
- `X-Original-URL` → Server header inconsistencies

**Why This Matters**:
HTTP headers leak critical information. Learning header enumeration teaches web server fingerprinting.

---

### **report_writer.py** — Report Generation

**Purpose**: Aggregate findings into structured output

**Report Structure**:
```
═════════════════════════════════════════════════
RECON CLI — Reconnaissance Report
═════════════════════════════════════════════════

TARGET: scanme.nmap.org (45.33.32.156)
SCAN DATE: 2024-01-15 14:32:10
PORT RANGE: 1-1000

═════════════════════════════════════════════════
OPEN PORTS (3 found)
═════════════════════════════════════════════════

[OPEN] 22/tcp   → SSH
[BANNER] SSH-2.0-OpenSSH_6.6.1p1 Ubuntu
[RISK] Version disclosure aids attackers

[OPEN] 80/tcp   → HTTP
[BANNER] (HTTP Server)
[HEADERS] Server: Apache/2.4.7

[OPEN] 9929/tcp → Unknown/Custom
[BANNER] (No banner response)

═════════════════════════════════════════════════
KEY FINDINGS
═════════════════════════════════════════════════

→ Version disclosure detected on SSH
→ Apache version exposed via HTTP
→ 3 open ports identified in scan range

═════════════════════════════════════════════════
```

**Design Decision**: 
Plain text + markdown formatting for readability and portability. Could extend to JSON/XML later.

---

### **utils.py** — Helper Utilities

**Purpose**: Common formatting and utility functions

**Functions**:
- `format_port_status()` → Colorized output
- `validate_ip()` → IP address validation
- `is_valid_port_range()` → Port range validation
- `get_timestamp()` → Consistent timestamps
- `log_message()` → Status output

**Why Separate**: 
Keeps modules focused. Utilities can be reused and tested independently.

---

## 🎯 Key Design Decisions

### 1. **No External Dependencies**
- Uses only Python standard library (socket, threading, time, sys, json, datetime)
- **Why**: Portability, security, and learning focus (not library documentation)

### 2. **Modular Architecture**
- Each module has a single responsibility
- Modules communicate through simple data structures (lists, dicts)
- **Why**: Easy to understand, extend, and test independently

### 3. **Threading Over Async**
- Used `threading.Thread` instead of `asyncio`
- **Why**: Simpler for learners; sufficient for this use case

### 4. **Socket-Level Implementation**
- Used raw sockets instead of `requests` library
- **Why**: Teaches TCP/IP concepts; shows how HTTP/SSH work at protocol level

### 5. **Synchronous Scanning**
- Each module waits for previous step to complete
- **Why**: Clear control flow; avoids race conditions

---

## ⚙️ Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| Scanning 1-1000 ports | ~10-15 sec | With 100 thread pool |
| Timeout per port | 2 seconds | Prevents hanging |
| Banner grabbing | ~0.5 sec per open port | Sequential retrieval |
| Memory usage | ~5-10 MB | Minimal for small scans |
| Max threads | 100 (configurable) | Can adjust for larger scans |

---

## 🔐 Security Considerations

### What RECON CLI Does Well
- ✅ Demonstrates reconnaissance methodology
- ✅ Shows information disclosure risks
- ✅ Teaches socket programming
- ✅ Illustrates threading limitations

### What It Doesn't Do
- ❌ Detect firewalls or IDS systems
- ❌ Perform vulnerability scanning
- ❌ Handle advanced evasion techniques
- ❌ Scale to enterprise environments

**By Design**: This is a learning tool, not a production scanner.

---

## 🚀 Extensibility

RECON CLI is designed to be extended:

### Planned Enhancements
1. **Vulnerability Scanning** → Map service versions to CVEs
2. **Active Directory Enumeration** → Kerberos, LDAP probing
3. **Web Application Recon** → robots.txt, sitemap.xml, technology detection
4. **Exploit Integration** → Framework hooks for automated exploitation
5. **Evasion Techniques** → Timing randomization, decoy packets

### How to Extend
1. Add new module (e.g., `vulnerability_scanner.py`)
2. Implement standard interface (takes scan results, outputs findings)
3. Integrate into `main.py` orchestration
4. Update report generation to include new findings

---

## 📊 Architecture Advantages

| Aspect | Benefit |
|--------|---------|
| **Modularity** | Easy to test, extend, and understand each component |
| **No Dependencies** | Portable, secure, educational |
| **Clear Data Flow** | Debugging is straightforward |
| **Threading** | Realistic scanning speeds |
| **Socket Programming** | Deep protocol understanding |
| **Report Generation** | Professional findings presentation |

---

## 🧠 Learning Value

Building RECON CLI teaches:

1. **Networking Fundamentals** → TCP/IP, DNS, HTTP protocols
2. **System Programming** → Sockets, file I/O, error handling
3. **Concurrency** → Threading, synchronization, race conditions
4. **Software Architecture** → Modular design, separation of concerns
5. **Cybersecurity** → Reconnaissance methodology, information leakage
6. **Professional Development** → Code organization, documentation, reporting

---

## 📝 Conclusion

RECON CLI demonstrates that **understanding is better than blind tool usage**. By building reconnaissance tools from first principles, we learn not just how tools work, but *why* they work that way.

This architectural approach prioritizes clarity and learning over raw performance—exactly as intended for an educational project.
