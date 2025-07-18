pipeline_output = {
    "tooltip": {
        "show": True,
        "formatter": "{b}",
    },
    "legend": {
        "data": [
            "Short-Term",
            "Medium-Term",
            "Long-Term",
            "Meta Core",
            "Decision Engine",
        ],
        "textStyle": {"color": "#fff"},
    },
    "series": [
        {
            "type": "graph",
            "layout": "force",
            "roam": True,
            "label": {"show": True, "color": "#ffffff"},
            "force": {
                "repulsion": 300,
                "gravity": 0.2,
                "edgeLength": 120,
            },
            "categories": [
                {"name": "Short-Term"},
                {"name": "Medium-Term"},
                {"name": "Long-Term"},
                {"name": "Meta Core"},
                {"name": "Decision Engine"},
            ],
            "data": [
                # Short-Term
                {"name": "FinBERT", "itemStyle": {"color": "#00e5ff"}, "category": 0},
                {"name": "LSTM", "itemStyle": {"color": "#00e5ff"}, "category": 0},
                {"name": "XGBoost", "itemStyle": {"color": "#00e5ff"}, "category": 0},
                {"name": "CatBoost", "itemStyle": {"color": "#00e5ff"}, "category": 0},

                # Medium-Term
                {"name": "Prophet", "itemStyle": {"color": "#ff9100"}, "category": 1},
                {"name": "ARIMA", "itemStyle": {"color": "#ff9100"}, "category": 1},
                {"name": "TimesNet", "itemStyle": {"color": "#ff9100"}, "category": 1},

                # Long-Term
                {"name": "RLlib", "itemStyle": {"color": "#d500f9"}, "category": 2},
                {"name": "Markowitz", "itemStyle": {"color": "#d500f9"}, "category": 2},
                {"name": "HRP", "itemStyle": {"color": "#d500f9"}, "category": 2},

                # Meta Core
                {"name": "Model Ensembler", "itemStyle": {"color": "#ff4081"}, "category": 3},
                {"name": "Bayesian Net", "itemStyle": {"color": "#ff4081"}, "category": 3},
                {"name": "AutoML", "itemStyle": {"color": "#ff4081"}, "category": 3},
                {"name": "LLM Agent", "itemStyle": {"color": "#ff4081"}, "category": 3},

                # Decision Engine Core
                {
                    "name": "Decision Engine",
                    "itemStyle": {"color": "#ffffff"},
                    "symbolSize": 60,
                    "category": 4,
                    "symbol": "circle",
                },
            ],
            "links": [
                {"source": model, "target": "Decision Engine"} for model in [
                    "FinBERT", "LSTM", "XGBoost", "CatBoost",
                    "Prophet", "ARIMA", "TimesNet",
                    "RLlib", "Markowitz", "HRP",
                    "Model Ensembler", "Bayesian Net", "AutoML", "LLM Agent"
                ]
            ],
            "lineStyle": {"color": "source"},
            "emphasis": {
                "focus": "adjacency",
                "lineStyle": {"width": 3}
            },
            "draggable": True,
            "focusNodeAdjacency": True,
        }
    ]
}
