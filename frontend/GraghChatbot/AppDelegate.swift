import UIKit

@main
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        window = UIWindow(frame: UIScreen.main.bounds)
        let chatViewController = ChatViewController() // Assuming ChatViewController is defined in ChatView.swift
        window?.rootViewController = chatViewController
        window?.makeKeyAndVisible()
        return true
    }
}