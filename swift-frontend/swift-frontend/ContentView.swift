import SwiftUI
import Combine
import MarkdownUI

struct Message: Identifiable, Codable {
    let id = UUID()
    let text: String
    let isUser: Bool
    let imageUrl: String? // 新增图片URL字段
}

struct ContentView: View {
    @State private var messages: [Message] = []
    @State private var userInput: String = ""
    @State private var selectedModel: String = "openELM"
    @State private var isLoading: Bool = false
    @State private var streamingText: String = ""
    @State private var keyboardHeight: CGFloat = 0
    // @State private var showImagePreview: Bool = false // 新增
    // @State private var previewImageUrl: URL? = nil    // 新增
    private var keyboardWillShow = NotificationCenter.default.publisher(for: UIResponder.keyboardWillShowNotification)
    private var keyboardWillHide = NotificationCenter.default.publisher(for: UIResponder.keyboardWillHideNotification)

    let models = ["openELM", "azure openai"]

    var body: some View {
        ZStack {
            WatermarkView(text: "GraphRAG")
            VStack {
                Image("boeing_logo")
                    .resizable()
                    .scaledToFit()
                    .frame(height: 80)
                    .padding(.top, 16)
                    .padding(.bottom, 16)

                Picker("Model", selection: $selectedModel) {
                    ForEach(models, id: \.self) { model in
                        Text(model.capitalized)
                    }
                }
                .pickerStyle(SegmentedPickerStyle())
                .padding(.horizontal)

                ScrollView {
                    VStack(alignment: .leading, spacing: 12) {
                        ForEach(messages) { message in
                            HStack {
                                if message.isUser {
                                    Spacer()
                                    Text(message.text)
                                        .padding()
                                        .background(Color.blue.opacity(0.2))
                                        .cornerRadius(12)
                                        .foregroundColor(.primary)
                                } else {
                                    VStack(alignment: .leading, spacing: 8) {
                                        if let imageUrl = message.imageUrl, let url = URL(string: imageUrl) {
                                            AsyncImage(url: url) { image in
                                            image
                                                .resizable()
                                                .scaledToFit()
                                                .frame(maxWidth: 800, maxHeight: 800)
                                                .cornerRadius(50)
                                                // .onTapGesture {
                                                //     previewImageUrl = url
                                                //     showImagePreview = true
                                                // }
                                            } placeholder: {
                                                ProgressView()
                                            }
                                        }
                                        Markdown(message.text).padding(.top, 8)
                                    }
                                    .padding()
                                    .background(Color.gray.opacity(0.15))
                                    .cornerRadius(12)
                                    .foregroundColor(.secondary)
                                    Spacer()
                                }
                            }
                        }
                        // Render the stream response
                        if isLoading || !streamingText.isEmpty {
                            HStack {
                                 Markdown(streamingText.isEmpty ? "..." : streamingText)
                                    .padding()
                                    .background(Color.gray.opacity(0.15))
                                    .cornerRadius(12)
                                    .foregroundColor(.secondary)
                                if isLoading {
                                    ProgressView()
                                }
                                Spacer()
                            }
                        }
                    }
                    .padding()
                }

                HStack {
                    TextField("Type in your question...", text: $userInput)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .disabled(isLoading)
                    Button(action: {
                        Task { await sendMessage() }
                    }) {
                        Image(systemName: "paperplane.fill")
                            .foregroundColor(.white)
                            .padding(10)
                            .background(userInput.isEmpty || isLoading ? Color.gray : Color.blue)
                            .clipShape(Circle())
                    }
                    .disabled(userInput.isEmpty || isLoading)
                    // 新增清空按钮
                    Button(action: {
                        messages.removeAll()
                    }) {
                        Image(systemName: "trash")
                            .foregroundColor(.white)
                            .padding(10)
                            .background(messages.isEmpty ? Color.gray : Color.red)
                            .clipShape(Circle())
                    }
                    .disabled(messages.isEmpty)
                }
                .padding()
            }
        }
        .onReceive(keyboardWillShow) { notification in
            if let frame = notification.userInfo?[UIResponder.keyboardFrameEndUserInfoKey] as? CGRect {
                withAnimation {
                    keyboardHeight = frame.height
                }
            }
        }
        .onReceive(keyboardWillHide) { _ in
            withAnimation {
                keyboardHeight = 0
            }
        }
        // .sheet(isPresented: $showImagePreview) {
        //     if let url = previewImageUrl {
        //         ZStack {
        //             Color.black.ignoresSafeArea()
        //             VStack {
        //                 Spacer()
        //                 AsyncImage(url: url) { image in
        //                     image
        //                         .resizable()
        //                         .scaledToFit()
        //                         .background(Color.black)
        //                 } placeholder: {
        //                     ProgressView()
        //                 }
        //                 Spacer()
        //                 Button(action: {
        //                     showImagePreview = false
        //                 }) {
        //                     Text("关闭")
        //                         .foregroundColor(.white)
        //                         .padding()
        //                         .background(Color.gray.opacity(0.7))
        //                         .cornerRadius(8)
        //                 }
        //                 .padding(.bottom, 30)
        //             }
        //         }
        //     }
        // }
    }

    // ...existing code...
    func sendMessage() async {
        let question = userInput.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !question.isEmpty else { return }
        messages.append(Message(text: question, isUser: true, imageUrl: nil))
        userInput = ""
        isLoading = true
        streamingText = ""

        guard let url = URL(string: "http://127.0.0.1:1234/api/chat") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let chatHistory = messages.map { ["role": $0.isUser ? "user" : "assistant", "content": $0.text] }
        let body: [String: Any] = [
            "history": chatHistory,
            "question": question,
            "model": selectedModel
        ]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)

        // 判断是否需要非流式（包含"please draw a plot"）
        let lowercasedQuestion = question.lowercased()
        let shouldUseNonStream = lowercasedQuestion.contains("please draw a plot")

        if shouldUseNonStream {
            // 非流式：直接用 dataTask，处理图片
            let task = URLSession.shared.dataTask(with: request) { data, response, error in
                if let data = data,
                    let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                    let answer = json["answer"] as? String {
                    let imageUrl = json["image_url"] as? String
                    DispatchQueue.main.async {
                        streamingText = ""
                        messages.append(Message(text: answer, isUser: false, imageUrl: imageUrl))
                        isLoading = false
                    }
                } else if let error = error {
                    DispatchQueue.main.async {
                        streamingText = ""
                        messages.append(Message(text: "Network Error: \(error.localizedDescription)", isUser: false, imageUrl: nil))
                        isLoading = false
                    }
                }
            }
            task.resume()
        } else {
            // 流式：只处理文本
            if #available(iOS 15.0, *) {
                do {
                    let streamTask = try await URLSession.shared.bytes(for: request)
                    Task {
                        do {
                            var accumulated = ""
                            for try await byte in streamTask.0 {
                                if let chunk = String(data: Data([byte]), encoding: .utf8) {
                                    accumulated += chunk
                                    DispatchQueue.main.async {
                                        streamingText = accumulated
                                    }
                                }
                            }
                            // Stream does not deal with image here
                            DispatchQueue.main.async {
                                messages.append(Message(text: accumulated, isUser: false, imageUrl: nil))
                                streamingText = ""
                                isLoading = false
                            }
                        } catch {
                            DispatchQueue.main.async {
                                streamingText = ""
                                messages.append(Message(text: "Stream Connection Error", isUser: false, imageUrl: nil))
                                isLoading = false
                            }
                        }
                    }
                } catch {
                    DispatchQueue.main.async {
                        streamingText = ""
                        messages.append(Message(text: "Stream connection initialization Error: \(error.localizedDescription)", isUser: false, imageUrl: nil))
                        isLoading = false
                    }
                }
            } else {
                // 兼容旧系统，直接用 dataTask 但不处理图片
                let task = URLSession.shared.dataTask(with: request) { data, response, error in
                    if let data = data,
                        let answer = String(data: data, encoding: .utf8) {
                        DispatchQueue.main.async {
                            streamingText = ""
                            messages.append(Message(text: answer, isUser: false, imageUrl: nil))
                            isLoading = false
                        }
                    } else if let error = error {
                        DispatchQueue.main.async {
                            streamingText = ""
                            messages.append(Message(text: "Network Error: \(error.localizedDescription)", isUser: false, imageUrl: nil))
                            isLoading = false
                        }
                    }
                }
                task.resume()
            }
        }
    }
}

struct WatermarkView: View {
    let text: String
    var body: some View {
        GeometryReader { geo in
            ZStack {
                Color(.systemGroupedBackground)
                Text(text)
                    .font(.system(size: 80, weight: .bold))
                    .foregroundColor(Color.gray.opacity(0.12))
                    .rotationEffect(.degrees(0))
                    .frame(width: geo.size.width, height: geo.size.height, alignment: .center)
            }
        }
        .allowsHitTesting(false)
    }
}

#Preview {
    ContentView()
}
