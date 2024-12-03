# OCR App

A Flask-based OCR application for extracting text, tables, and key-value pairs from PDF documents using PaddleOCR and OpenCV. This app is containerized using Docker for easy deployment.

## Features
- Convert PDF files into images.
- Perform OCR using PaddleOCR.
- Classify pages and extract key-value pairs and tables.
- Combine extracted information and generate results.

## Prerequisites
Before you start, ensure you have the following installed:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Getting Started

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ocr-app
```
