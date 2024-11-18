#include <gtk/gtk.h>

static void activate(GtkApplication *app, gpointer user_data) {
    // Create a new application window
    GtkWidget *window = gtk_application_window_new(app);
    gtk_window_set_title(GTK_WINDOW(window), "I2C CONTROLLER");
    gtk_window_set_default_size(GTK_WINDOW(window), 400, 200);

    // Show the window
    gtk_window_present(GTK_WINDOW(window));
}

int main(int argc, char *argv[]) {
    // Create a new GtkApplication
    GtkApplication *app = gtk_application_new("com.example.GTK4Test", G_APPLICATION_FLAGS_NONE);

    // Connect the activate signal
    g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);

    // Run the application
    int status = g_application_run(G_APPLICATION(app), argc, argv);

    // Clean up
    g_object_unref(app);

    return status;
}