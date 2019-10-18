#include <stdio.h>

#define SIMULATOR

#ifdef SIMULATOR
#undef PRINTF
#define PRINTF(...) printf(__VA_ARGS__)   
#endif

void PrintHello(void);

void PrintHello(void)
{
  PRINTF("Hello World!\n");
}
