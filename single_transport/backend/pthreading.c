// C function showing how to do time delay
#include <stdio.h>

#include <unistd.h>
// To use time library of C
#include <pthread.h>

void *do_loop() {
    int i;
    for (i = 0; i < 10; i++) {
        // delay of one second
        usleep(1000*1000);
        printf("new thread!: %d seconds have passed\n", i + 1);
    }
    
} 


// Driver code to test above function
int main()
{
    pthread_t thid;
    void *ret;

    if (pthread_create(&thid, NULL, do_loop, "thread 1") != 0) {
        perror("pthread_create() error");
        
    }
    else {
        int i;
        for (i = 0; i < 10; i++) {
            // delay of one second
            usleep(1000*1000);
            printf("Yo la-lai: %d seconds have passed\n", i + 1);
        }
        return 0;


        if (pthread_join(thid, ret) != 0) {
            perror("pthread_join() error");
        }

    }


    
}