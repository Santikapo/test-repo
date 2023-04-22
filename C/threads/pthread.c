#include <stdio.h>
#include <pthread.h>
#include <math.h>

void *computation(void* num);

int main() {

    pthread_t thread1, thread2, thread3, thread4;


    pthread_create(&thread1, NULL, computation, (void*) 1);
    pthread_create(&thread2, NULL, computation, (void*) 2);
    pthread_create(&thread3, NULL, computation, (void*) 3);
    pthread_create(&thread4, NULL, computation, (void*) 4);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    pthread_join(thread3, NULL);
    pthread_join(thread4, NULL);


    return 0;
}

void *computation(void* num) {
    int n = (int) num;
    for(int i = 0; i < 10000; i++) {
        printf("%i - %.3f\n", n, sin(i));
    }

    return NULL;
}