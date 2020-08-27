// library form:
// gcc -fPIC -shared -o <libsrc.so> <src.c> -lm
// executable form:
// gcc -o <src> <src.c> -lm
#include <stdio.h>
#include <stdint.h>
#include <math.h>    // gcc flag: -lm

typedef struct {
  uint16_t cnt;
} cnt_t;

typedef struct {
  char name[8];
  uint16_t vec_x;
  uint16_t vec_y;
  cnt_t *  n;
} coord_t;

double CalAvg(int x, int y);
double CalDistance(coord_t *x, coord_t *y);
void ResetOrigin(coord_t *x);

static void demo_cal_avg(int x, int y);
static void demo_cal_distance(coord_t *x, coord_t *y);
static void demo_reset_origin(coord_t *x);

int main(void)
{
  demo_cal_avg(7, 8);

  coord_t A = {"point A", 8, 7, NULL};
  coord_t B = {"point B", 5, 3, NULL};
  demo_cal_distance(&A, &B);

  demo_reset_origin(&A);
}

double CalAvg(int x, int y)
{
  double avg = (double)(x + y) / 2;
  return avg;
}

double CalDistance(coord_t *x, coord_t *y)
{
  double sq_sum = sqrt(pow(x->vec_x - y->vec_x, 2) + 
                       pow(x->vec_y - y->vec_y, 2));
  return sq_sum;
}

void ResetOrigin(coord_t *x)
{
  x->vec_x = x->vec_y = 0;
}

static void demo_cal_avg(int x, int y)
{
  printf("  (x, y): (%d, %d)\n", x, y);
  printf("  CalAvg(%d, %d): %.2f\n", x, y, CalAvg(x, y));
  printf("\n");
}

static void demo_cal_distance(coord_t *x, coord_t *y)
{
  printf("  %s(%d, %d)\n", x->name, x->vec_x, x->vec_y);
  printf("  %s(%d, %d)\n", y->name, y->vec_x, y->vec_y);
  printf("  CalDistance(%s, %s): %.2f\n", x->name, y->name, CalDistance(x, y));
  printf("\n");
}

static void demo_reset_origin(coord_t *x)
{
  printf("  before: %s(%d, %d)\n", x->name, x->vec_x, x->vec_y);
  ResetOrigin(x);
  printf("  ResetOrigin(%s)\n", x->name);
  printf("  after : %s(%d, %d)\n", x->name, x->vec_x, x->vec_y);
  printf("\n");
}
