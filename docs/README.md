


### Soon to be Project Structure: 

```
auditbuddy/
├── .github/
│   └── workflows/
│       └── main.yml
├── services/
│   ├── framework/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── soc2.py
│   │   ├── iso27001.py
│   │   ├── nist800-53v5.py
│   │   └── mappings.py
│   ├── providers/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── aws.py
│   │   ├── azure.py
│   │   ├── gcp.py
│   │   └── okta.py
│   ├── utils/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── auth.py
│   │   ├── format.py
│   │   └── git.py
├── docker-compose.yml
├── tests/
│   ├── framework/
│   ├── providers/
│   └── utils/
├── README.md
└── config.yaml
```
