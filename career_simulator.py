def generate_simulation(role):

    simulations = {

        "Cloud Engineer": {
            "avatar": "☁️ Cloud Explorer",
            "quests": [
                "Complete Azure Fundamentals",
                "Build a Docker Project",
                "Deploy an Application to Azure"
            ],
            "future": [
                "3 Months → Cloud Trainee",
                "12 Months → Cloud Engineer",
                "3 Years → Senior Cloud Engineer"
            ]
        },

        "DevOps Engineer": {
            "avatar": "⚙️ DevOps Builder",
            "quests": [
                "Learn Linux",
                "Build CI/CD Pipeline",
                "Deploy Kubernetes Cluster"
            ],
            "future": [
                "3 Months → Junior DevOps Engineer",
                "12 Months → DevOps Engineer",
                "3 Years → Senior DevOps Engineer"
            ]
        },

        "Data Engineer": {
            "avatar": "📊 Data Architect",
            "quests": [
                "Master SQL",
                "Build ETL Pipeline",
                "Create Data Warehouse"
            ],
            "future": [
                "3 Months → Data Analyst",
                "12 Months → Data Engineer",
                "3 Years → Senior Data Engineer"
            ]
        }
    }

    return simulations[role]