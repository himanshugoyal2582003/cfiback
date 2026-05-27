from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd


#title
app = FastAPI(
    title="Crypto Wallet Fraud Intelligence API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#read files
risk_df = pd.read_csv(
    "app/data/risk_scores.csv"
)    

anomaly_df = pd.read_csv(
    "app/data/anomalies.csv"
)

community_df = pd.read_csv(
    "app/data/community_analysis.csv"
)

centrality_df = pd.read_csv(
    "app/data/centrality_results.csv"
)




#home api
@app.get("/")
def home():
    return {
        "message": "Crypto Fraud Intelligence API"
    }

#risk scores api
@app.get("/risk-scores")
def get_risk_scores():
    return risk_df.head(20).to_dict(
        orient="records"
    )



#top risk api
@app.get("/top-risk")
def get_top_risk():

    top_risk = risk_df.sort_values(
        by="risk_score",
        ascending=False
    )

    return top_risk.head(20).to_dict(
        orient="records"
    )


#anomalies api
@app.get("/anomalies")
def get_anomalies():
    return anomaly_df.head(20).to_dict(
        orient="records"
    )


#communities api
@app.get("/communities")
def get_communities():
    return community_df.head(20).to_dict(
        orient="records"
    )

#centrality api
@app.get("/centrality")
def get_centrality():
    return centrality_df.head(20).to_dict(
        orient="records"
    )


#stats api
@app.get("/stats")
def get_stats():

    total_transactions = len(risk_df)

    total_anomalies = len(anomaly_df)

    total_communities = len(
        community_df
    )

    avg_risk_score = float(
        risk_df["risk_score"].mean()
    )

    return {
        "total_transactions":
            total_transactions,

        "total_anomalies":
            total_anomalies,

        "total_communities":
            total_communities,

        "average_risk_score":
            avg_risk_score
    }



@app.get("/graph")
def get_graph():

    sample_edges = pd.read_csv(
        "app/data/sample_edges.csv"
    )

    nodes = []

    unique_nodes = set(
        sample_edges['txId1']
    ).union(
        set(sample_edges['txId2'])
    )

    for node in unique_nodes:
        nodes.append({
            "id": str(node)
        })

    links = []

    for _, row in sample_edges.iterrows():

        links.append({
            "source": str(row['txId1']),
            "target": str(row['txId2'])
        })

    return {
        "nodes": nodes,
        "links": links
    }