#include <stdlib.h>
#include <stdio.h>
#include <time.h>


void main(void)
{

    time_t now;
    time(&now);

    printf("Now is %s\n", ctime(&now));
    return;
}

