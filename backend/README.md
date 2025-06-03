# Gragh Chatbot Backend

This is the backend component of the Gragh Chatbot project, which is designed to facilitate communication between a Swift-driven iOS application and either a local Open ELM model or the Azure OpenAI API.

## Project Structure

- **app.py**: The main entry point for the Flask backend. It sets up the Flask application and defines the RESTful API endpoints.
- **requirements.txt**: Lists the dependencies required for the backend, including Flask and any libraries needed for connecting to Open ELM or Azure OpenAI.
- **models/**: Contains the logic for connecting to the respective models.
  - **openelm_connector.py**: Logic for connecting to the local Open ELM model.
  - **azure_openai_connector.py**: Logic for connecting to the Azure OpenAI API.
- **utils/**: Provides utility functions for streaming data.
  - **streaming.py**: Handles the streaming of responses in real-time.

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/gragh-chatbot.git
   cd gragh-chatbot/backend
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```
   python app.py
   ```

## API Usage

The backend exposes RESTful API endpoints that the frontend can use to send user queries and receive responses. The API supports streaming data for real-time interaction.

### Endpoints

- **POST /api/query**: Send a user query to the selected model and receive a response.
  - Request Body:
    ```json
    {
      "model": "openelm" | "azure_openai",
      "query": "Your question here"
    }
    ```
  - Response:
    - Streams the response back to the frontend.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.