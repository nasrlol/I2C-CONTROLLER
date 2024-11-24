#include <gtk/gtk.h>
#include <stdio.h>
#include <string.h>

// Define the features array
char *features[] = {"recourses", "greeting", "pomodoro", "weather", "speech", "command center"};

// Function to create a button with a label
void create_button(const char *label) {
    GtkWidget *button = gtk_button_new_with_label(label);
    // You can set the button properties or add it to a container here
    g_print("Button created: %s\n", label);  // For debugging purposes
}

static void activate(GtkApplication *app, gpointer user_data) {
    // Create the window
    GtkWidget *window = gtk_application_window_new(app);
    gtk_window_set_title(GTK_WINDOW(window), "I2C CONTROLLER");
    gtk_window_set_default_size(GTK_WINDOW(window), 400, 400);

    // Create a container for buttons (e.g., vertical box)
    GtkWidget *vbox = gtk_box_new(GTK_ORIENTATION_VERTICAL, 5);
    gtk_container_add(GTK_CONTAINER(window), vbox);

    // Calculate the number of features
    int features_count = sizeof(features) / sizeof(features[0]);

    // Create a button for each feature
    for (int i = 0; i < features_count; i++) {
        GtkWidget *button = gtk_button_new_with_label(features[i]);
        gtk_box_pack_start(GTK_BOX(vbox), button, FALSE, FALSE, 0);
        gtk_widget_set_size_request(button, 200, 100);
    }

    // Show all widgets
    gtk_widget_show_all(window);
}

int main(int argc, char *argv[]) {
    // Create the application
    GtkApplication *app = gtk_application_new("com.example.GTK4Test", G_APPLICATION_FLAGS_NONE);

    // Connect the "activate" signal to the callback function
    g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);

    // Run the application
    int status = g_application_run(G_APPLICATION(app), argc, argv);

    // Clean up
    g_object_unref(app);

    return status;
}
