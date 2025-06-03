import SwiftUI

struct ChatView: View {
    @State private var userInput: String = ""
    @State private var messages: [Message] = []
    
    var body: some View {
        VStack {
            ScrollView {
                ForEach(messages) { message in
                    Text(message.content)
                        .padding()
                        .background(message.isUser ? Color.blue : Color.gray)
                        .cornerRadius(10)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity, alignment: message.isUser ? .trailing : .leading)
                }
            }
            .padding()
            
            HStack {
                TextField("Type your message...", text: $userInput)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()
                
                Button(action: sendMessage) {
                    Text("Send")
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
            }
            .padding()
        }
        .navigationTitle("Graph Chatbot")
        .navigationBarTitleDisplayMode(.inline)
    }
    
    private func sendMessage() {
        let newMessage = Message(content: userInput, isUser: true)
        messages.append(newMessage)
        userInput = ""
        
        // Call API to send user input and receive response
        APIService.sendMessage(newMessage.content) { response in
            let botMessage = Message(content: response, isUser: false)
            messages.append(botMessage)
        }
    }
}

struct ChatView_Previews: PreviewProvider {
    static var previews: some View {
        ChatView()
    }
}