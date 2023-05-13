#include <stdio.h>
#include <stdint.h>
#include <pthread.h>

__thread int var = 0;   // var定义为线程变量，每个数线拥有一份

void* worker(void* arg)  {
    for (int i = 0; i < 1e4; i++) {
        var++;
    }   
        
    printf("child thread [%lu] var(%p)=%d\n", pthread_self(), &var, var);
    return 0;
} 

int main(){  
    pthread_t pid1, pid2;  
    printf("var=%d\n", var);

    pthread_create(&pid1, NULL, worker, (void *)0);  
    pthread_create(&pid2, NULL, worker, (void *)1);  

    pthread_join(pid1, NULL);  
    pthread_join(pid2, NULL);  

    printf("main thread [%lu] var(%p)=%d\n", pthread_self(), &var, var);

    return 0;  
}