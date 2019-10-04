// library form:
// gcc -fPIC -shared -o <libsrc.so> <src.c> -lm
// executable form:
// gcc -o <src> <src.c> -lm
#include <stdio.h>
#include <stdint.h>
#include <math.h>  // gcc flag: -lm

#define HELLO 87

typedef struct {
  uint16_t num;
} num_t;

typedef struct {
  char name[16];
  uint16_t x;
  uint16_t y;
  num_t *  n;
} coord_t;

double CalDistance(coord_t *, coord_t *);
double CalAvg(int x, int y);
void ResetOrigin(coord_t *);

int main(void)
{
  printf("CalAvg: %.2f\n", CalAvg(10, 1));
  coord_t A = {"A", 8, 7};
  coord_t B = {"B", 5, 3};
  printf("CalDistance([8, 7], [5, 3]): %.2f\n", CalDistance(&A, &B));
}

double CalDistance(coord_t *A, coord_t *B)
{
  double sq_sum = (pow(A->x - B->x, 2) + pow(A->y - B->y, 2));
  return sqrt(sq_sum);
}

double CalAvg(int x, int y)
{
  double avg = (double)(x + y) / 2;
  return avg;
}

void ResetOrigin(coord_t *X)
{
  X->x = X->y = 0;
  ++X->n->num;
}
