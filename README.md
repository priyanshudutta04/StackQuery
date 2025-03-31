# StackQuery

StackQuery is an AI agent powered by LangChain and RAG to retrieve and summarize Stack Overflow solutions.

## Sample Response
<br>

![git-ban-final](https://raw.githubusercontent.com/priyanshudutta04/priyanshudutta04/refs/heads/main/git%20images/Screenshot%20(122).png)


## About

StackQuery is an AI-powered search assistant designed to streamline programming problem-solving by retrieving and summarizing relevant solutions from Stack Overflow. Built using LangChain, Retrieval-Augmented Generation (RAG), and Google Gemini, it leverages AI agents to analyze queries and extract precise answers. Additionally, ChromaDB ensures efficient document retrieval, enabling developers to quickly find the most relevant information for their coding challenges.

## Usage

1. Clone the repository
```
git clone https://github.com/priyanshudutta04/StackQuery.git
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Create a Virtual Environment (optional)
```
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows
```
4. Create a `.env` file in the root directory and add your Google API Key:
 ```
GOOGLE_API_KEY=api_key
```

5. Run the Python File
```
streamlit run main.py
```


## Contributing

Contributions are welcome! If you have ideas for improving the model or adding new features, please feel free to fork the repository and submit a pull request or open a issue.

## Support

If you like this project, do give it a ⭐and share it with your friends.
