import os
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


DATA_DIR = Path(__file__).resolve().parent / "data"


def read_dataset(filename: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / filename)


def configured_origins() -> list[str]:
    value = os.getenv("FRONTEND_ORIGINS", "*")
    origins = [origin.strip() for origin in value.split(",") if origin.strip()]
    return origins or ["*"]


risk_df = read_dataset("risk_scores.csv")
anomaly_df = read_dataset("anomalies.csv")
community_df = read_dataset("community_analysis.csv")
centrality_df = read_dataset("centrality_results.csv")
edges_df = read_dataset("sample_edges.csv")

origins = configured_origins()
allow_all_origins = "*" in origins

app = FastAPI(
    title="Crypto Wallet Fraud Intelligence API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all_origins else origins,
    allow_credentials=not allow_all_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Crypto Fraud Intelligence API",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.get("/risk-scores")
def get_risk_scores():
    return risk_df.head(20).to_dict(orient="records")


@app.get("/top-risk")
def get_top_risk():
    top_risk = risk_df.sort_values(by="risk_score", ascending=False)
    return top_risk.head(20).to_dict(orient="records")


@app.get("/anomalies")
def get_anomalies():
    return anomaly_df.head(20).to_dict(orient="records")


@app.get("/communities")
def get_communities():
    return community_df.head(20).to_dict(orient="records")


@app.get("/centrality")
def get_centrality():
    return centrality_df.head(20).to_dict(orient="records")


@app.get("/stats")
def get_stats():
    return {
        "total_transactions": len(risk_df),
        "total_anomalies": len(anomaly_df),
        "total_communities": len(community_df),
        "average_risk_score": float(risk_df["risk_score"].mean()),
    }


@app.get("/graph")
def get_graph():
    unique_nodes = set(edges_df["txId1"]).union(set(edges_df["txId2"]))

    return {
        "nodes": [{"id": str(node)} for node in unique_nodes],
        "links": [
            {
                "source": str(row.txId1),
                "target": str(row.txId2),
            }
            for row in edges_df.itertuples()
        ],
    }
