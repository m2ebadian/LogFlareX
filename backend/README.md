# LogflareX Backend

A high-performance FastAPI + PostgreSQL logging system with production-grade observability using Prometheus and Grafana.  

---

## 🚀 Features

- **FastAPI-based API** for ingesting and viewing logs.
- **PostgreSQL** database for persistent log storage.
- **Prometheus metrics** for real-time monitoring.
- **Grafana dashboards & alerts** for proactive incident detection.
- **Error-rate alerting** (triggers when ERROR logs exceed thresholds).

---

## 📂 Project Structure

- backend/
- ├── app/
- │ ├── main.py # FastAPI entry point
- │ ├── models.py # SQLAlchemy models
- │ ├── database.py # Database connection & table initialization
- │ ├── routes/ # API routes (logs & alerts)
- │ ├── metrics.py # Prometheus counters
- ├── venv/ # Virtual environment (not committed)
- ├── requirements.txt # Python dependencies
- └── README.md


