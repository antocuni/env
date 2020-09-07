/*
 * Copyright (C) 2017 Alberts Muktupāvels
 *               2020 Antonio Cuni
 *
 * 
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 *
 * Compile with:
 * gcc toggle-decorations.c -Wall -o toggle-decorations `pkg-config --cflags --libs x11`
 *
 * Usage:
 * toggle-decorations 0x1234567
 *
 * Support me:
 * https://www.patreon.com/muktupavels
 */

#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <X11/Xlib.h>

typedef struct
{
  unsigned long flags;
  unsigned long functions;
  unsigned long decorations;
  long input_mode;
  unsigned long status;
} MotifWmHints;

static MotifWmHints *
get_motif_wm_hints (Display *display,
                    Window   window)
{
  Atom property;
  int result;
  Atom actual_type;
  int actual_format;
  unsigned long nitems;
  unsigned long bytes_after;
  unsigned char *data;

  property = XInternAtom (display, "_MOTIF_WM_HINTS", False);
  result = XGetWindowProperty (display, window, property,
                               0, LONG_MAX, False, AnyPropertyType,
                               &actual_type, &actual_format,
                               &nitems, &bytes_after, &data);

  if (result == Success && data != NULL)
    {
      size_t data_size;
      size_t max_size;
      MotifWmHints *hints;

      data_size = nitems * sizeof (long);
      max_size = sizeof (*hints);

      hints = calloc (1, max_size);

      memcpy (hints, data, data_size > max_size ? max_size : data_size);
      XFree (data);

      return hints;
    }

  return NULL;
}

static void
set_window_decorations(Display *display, Window window, char op)
{
  MotifWmHints *hints;
  Atom property;
  int nelements;

  hints = get_motif_wm_hints (display, window);
  if (hints == NULL)
    {
      hints = calloc (1, sizeof (*hints));
      hints->decorations = (1L << 0);
    }

  hints->flags |= (1L << 1);
  switch (op) {
  case 't':
      hints->decorations = hints->decorations == 0 ? (1L << 0) : 0;
      break;
  case '0':
      hints->decorations = 0;
      break;
  case '1':
      hints->decorations = 1;
      break;
  }

  property = XInternAtom (display, "_MOTIF_WM_HINTS", False);
  nelements = sizeof (*hints) / sizeof (long);

  XChangeProperty (display, window, property, property, 32, PropModeReplace,
                   (unsigned char *) hints, nelements);

  free (hints);
}

static int
usage(void)
{
      printf("Usage: set-x11-decoration WINDOW-ID [DECORATION]\n");
      printf("  DECORATION:    t    toogle (default)\n");
      printf("                 0    undecorate\n");
      printf("                 1    decorate\n");
      return 1;
}

int main (int   argc, char *argv[])
{
  Display *display;
  Window window = 0;
  char op = 't';

  if (argc != 2 && argc != 3)
      return usage();

  if (argc == 2 || argc == 3) {
      sscanf (argv[1], "0x%lx", &window);
      if (window == 0)
        sscanf (argv[1], "%lu", &window);
  }
  if (argc == 3) {
      sscanf(argv[2], "%c", &op);
      if (op != 't' && op != '0' && op != '1')
          return usage();
  }

  if (window == 0)
    return 1;

  display = XOpenDisplay (NULL);
  if (display == NULL)
    return 1;

  set_window_decorations (display, window, op);
  XCloseDisplay (display);

  return 0;
}
