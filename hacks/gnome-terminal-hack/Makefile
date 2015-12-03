CFLAGS=`pkg-config gtk+-2.0 --cflags`

bottomtab.so: bottomtab.c
	gcc $(CFLAGS) -fPIC -shared -ldl -o bottomtab.so bottomtab.c
