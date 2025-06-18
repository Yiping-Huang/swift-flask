# Streamlit Frontend Chatbot

This project is a Streamlit application designed to function as a chatbot interface, resembling an iPad application. It features a clean and modern UI with a Boeing logo at the top, a GraphRAG watermark in the center, and an input box at the bottom for user interactions.

## Project Structure

```
streamlit-frontend
├── src
│   ├── app.py               # Main entry point for the Streamlit application
│   ├── components
│   │   ├── sidebar.py       # Sidebar component for model selection and chat management
│   │   ├── chat_input.py     # Chat input component for user messages
│   │   └── watermark.py      # Watermark component displaying the GraphRAG watermark
│   └── assets
│       └── boeing_logo.svg  # SVG image of the Boeing logo
├── requirements.txt         # Required Python packages for the application
└── README.md                # Documentation for the project
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd streamlit-frontend
   ```

2. **Install Requirements**
   It is recommended to create a virtual environment before installing the requirements.
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   Start the Streamlit application using the following command:
   ```bash
   streamlit run src/app.py
   ```

## Usage

- Upon launching the application, you will see the Boeing logo at the top.
- The GraphRAG watermark will be displayed in the center of the page.
- Use the input box at the bottom to send messages to the chatbot.
- The sidebar allows you to clear chat history and select different models for the chatbot.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.