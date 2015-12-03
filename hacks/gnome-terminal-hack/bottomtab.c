#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <dlfcn.h>
#include <gtk/gtk.h>

__attribute__((constructor)) void init(void) {
    unsetenv("LD_PRELOAD");
}

GtkWidget* gtk_notebook_new(void)
{
    static GtkWidget* (*original_fn)(void);
    if (!original_fn) {
        original_fn = dlsym(RTLD_NEXT, "gtk_notebook_new");
    }

    GtkWidget* notebook = original_fn();
    gtk_notebook_set_tab_pos(GTK_NOTEBOOK(notebook), GTK_POS_BOTTOM);
    return notebook;
}

