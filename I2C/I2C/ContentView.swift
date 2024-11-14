import SwiftUI

struct ContentView: View {
	let options = ["CPU INFO", "CPU UPTIME", "SPEECH TRANSCRIBER", "NOTES"]
	var body: some View {
		VStack {
			Button(
				RoundedRectangle(cornerRadius: 25)
				.fill(Color.red)
			)
		}
	}
}

#Preview {
    ContentView()
}
