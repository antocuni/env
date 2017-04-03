#https://lwn.net/Articles/572911/

N=512
echo $(($N*2*1024*1024)) > /proc/sys/vm/dirty_bytes
echo $(($N*1024*1024)) > /proc/sys/vm/dirty_background_bytes
