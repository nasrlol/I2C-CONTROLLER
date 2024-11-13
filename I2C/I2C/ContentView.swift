import SwiftUI

struct ContentView: View {
	var header: some View {
		VStack {
			Text("Hello world!")
		}
		
	}
	var body: some View {
		VStack {
			Circle()
				.fill(.blue)
				.frame(width: 100, height: 100)
				.padding()
			header
			Button("VOICE RECOGNITION"){
				
			}
			Button("CPU UPTIME"){
				
			}
			Button("CPU INFO"){
				
			}
		}
	}
}



#Preview {
    ContentView()
}
