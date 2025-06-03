import Foundation

struct Message {
    let content: String
    let sender: SenderType
    let timestamp: Date

    enum SenderType {
        case user
        case bot
    }
}