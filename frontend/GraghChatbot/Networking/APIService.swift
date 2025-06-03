import Foundation

class APIService {
    static let shared = APIService()
    private let baseURL = "http://localhost:1234" // Update with your backend URL

    private init() {}

    func sendMessage(_ message: String, model: String, completion: @escaping (String?) -> Void) {
        guard let url = URL(string: "\(baseURL)/chat") else {
            completion(nil)
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let parameters: [String: Any] = [
            "message": message,
            "model": model
        ]

        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: [])
        } catch {
            completion(nil)
            return
        }

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error: \(error)")
                completion(nil)
                return
            }

            guard let data = data else {
                completion(nil)
                return
            }

            if let responseString = String(data: data, encoding: .utf8) {
                completion(responseString)
            } else {
                completion(nil)
            }
        }

        task.resume()
    }

    func streamMessages(model: String, completion: @escaping (String?) -> Void) {
        guard let url = URL(string: "\(baseURL)/stream") else {
            completion(nil)
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error: \(error)")
                completion(nil)
                return
            }

            guard let data = data else {
                completion(nil)
                return
            }

            if let responseString = String(data: data, encoding: .utf8) {
                completion(responseString)
            } else {
                completion(nil)
            }
        }

        task.resume()
    }
}