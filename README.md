# Valkyrie Secure Messaging System

## Overview

Valkyrie is a secure real-time messaging system built using Python. It demonstrates core concepts in software security including authentication, symmetric encryption, key exchange concepts, and secure websocket communication.

The system is designed as a learning project to simulate how modern secure messaging applications work (similar to WhatsApp or Signal at a simplified level).

---

## Features

### 1. User Authentication

- User registration and login system
- Passwords stored using secure hashing (e.g., SHA-256 / bcrypt)
- Token-based session handling
- Basic session lifecycle (login / logout)

---

### 2. Real-Time Communication

- WebSocket-based messaging system using FastAPI (server)
- Python CLI client using `websockets`
- Persistent bidirectional communication between users

---

### 3. Symmetric Encryption (AES-GCM)

- Messages are encrypted before sending
- AES-GCM used for confidentiality and integrity
- Each message includes:
  - nonce
  - ciphertext

- Messages are decrypted only by the intended receiver

---

### 4. Message Relay System

- Server acts only as a relay (does NOT read message content)
- Maintains active user connections
- Supports private messaging between users

---

### 5. WebSocket Connection Manager

- Tracks online users
- Handles connect/disconnect events
- Routes messages to correct recipient

---

## Architecture

```
Client A (CLI)
   ↓
AES Encryption
   ↓
WebSocket
   ↓
FastAPI Server (Relay Only)
   ↓
WebSocket
   ↓
Client B (CLI)
   ↓
AES Decryption
```

---

## Security Concepts Demonstrated

### Confidentiality

- Achieved using AES-GCM encryption

### Integrity

- Built-in AES-GCM authentication tag ensures message is not modified

### Authentication (Basic)

- Token-based login system

### Threat Simulation (planned/ongoing)

- Man-in-the-Middle (MITM)
- Replay attacks
- Brute force attempts

---

## Upcoming Improvements

- RSA-based key exchange (secure AES key sharing)
- HMAC-based message verification
- Replay attack prevention using message IDs / timestamps
- Improved session management
- Logging system for security events
- Online user discovery API improvements

---

## Tech Stack

- Python 3.10+
- FastAPI (WebSocket server)
- websockets (client)
- cryptography library (AES-GCM)
- hashlib / bcrypt (authentication hashing)

---

## Purpose of Project

This project is built for educational purposes to understand:

- How secure messaging systems work internally
- How encryption protects data in transit
- How real-world applications manage secure sessions
- How attacks like MITM and replay are mitigated

---

## Author

Student Project – Software Security Coursework
