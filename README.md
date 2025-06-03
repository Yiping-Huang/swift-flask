# Gragh Chatbot

Gragh Chatbot is a modern iOS application that provides a seamless chat experience powered by advanced AI models. This project is structured with a clear separation between the frontend and backend components, allowing for easy maintenance and scalability.

## Project Structure

```
gragh-chatbot
├── backend                # Contains the Flask backend application
│   ├── app.py            # Main entry point for the Flask application
│   ├── requirements.txt   # Lists backend dependencies
│   ├── models             # Contains model connectors
│   │   ├── openelm_connector.py  # Logic for local Open ELM model
│   │   └── azure_openai_connector.py  # Logic for Azure OpenAI API
│   ├── utils              # Utility functions
│   │   └── streaming.py   # Functions for streaming data
│   └── README.md          # Documentation for the backend
├── frontend               # Contains the iOS application
│   ├── GraghChatbot.xcodeproj  # Xcode project file
│   ├── GraghChatbot      # Main application directory
│   │   ├── AppDelegate.swift  # Application delegate
│   │   ├── SceneDelegate.swift  # Scene management
│   │   ├── Assets.xcassets  # Asset catalog
│   │   │   └── BoeingLogo.imageset  # Boeing logo assets
│   │   ├── Views          # UI components
│   │   │   └── ChatView.swift  # Chat interface
│   │   ├── Models         # Data models
│   │   │   └── Message.swift  # Chat message model
│   │   ├── Networking     # Networking layer
│   │   │   └── APIService.swift  # API service for network requests
│   │   └── Resources      # Application resources
│   │       └── Info.plist  # Application configuration
│   └── README.md          # Documentation for the frontend
└── README.md              # Overview of the entire project
```

## Features

- **User Model Selection**: Users can choose between Open ELM and Azure OpenAI for their chatbot experience.
- **Real-time Streaming**: The application supports real-time data streaming for a responsive chat experience.
- **Modern UI**: The iOS application features a modern and aesthetically pleasing user interface.

## Setup Instructions

### Backend

1. Navigate to the `backend` directory.
2. Install the required dependencies using:
   ```
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```
   python app.py
   ```

### Frontend

1. Open the `GraghChatbot.xcodeproj` file in Xcode.
2. Build and run the application on a simulator or a physical device.

## Usage

Once both the frontend and backend are running, users can interact with the chatbot through the iOS application. The app allows users to input their queries and receive responses in real-time.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.