#include "meas_association.h"
#include <stdlib.h>
#include <math.h>   
#include <float.h>  // fabs()
#ifndef UTEST
#include "sys_shared.h"
#include "detections.h"
#include "track_data.h"
#endif

// APIs
void API_NewMeasAsn(MeasAsn *self);
#ifndef UTEST
static meta_meas_group_t *API_Association(MeasAsn *self, target_group_t *, const float);
#else
static meta_meas_group_t *API_Association(MeasAsn *self);
#endif 
// Methods
static void InitMeasAsn(MeasAsn *self);
static void RegisterAlgMinXY(MeasAsn *self);
static void InitAssociation(MeasAsn *self);
static int8_t BestExpVelPair(MeasAsn *self, meta_meas_t *);
static void Pairing(MeasAsn *self);
static int8_t PairingExpVel(MeasAsn *self, meta_meas_t *, meta_meas_t *, float *);
static meta_meas_t CalDeltaByMinXY(MeasAsn *self, meta_meas_t *, meta_meas_t *,
  int8_t, int8_t);
static meta_meas_t CalGateByMinXY(MeasAsn *self, meta_meas_t *, meta_meas_t *);
static int8_t IsGatePassedByMinXY(MeasAsn *self, meta_meas_t *, meta_meas_t *, 
  float *);
// Sub-Methods
static inline float EXP_VEL(const float, const float, const uint8_t);
static inline float ExpVel(const float, const float, const uint8_t);

/**************************************************
 * Globals                                        *
 **************************************************/
static meta_meas_t (*CalDelta)(MeasAsn *self, meta_meas_t *, meta_meas_t *, 
  int8_t, int8_t);
static meta_meas_t (*CalGate)(MeasAsn *self, meta_meas_t *, meta_meas_t *);
static int8_t (*IsGatePassed)(MeasAsn *self, meta_meas_t *, meta_meas_t *, 
  float *);

/**************************************************
 * API                                            *
 **************************************************/
void API_NewMeasAsn(MeasAsn *self)
{
  self->curr_idx = META_MEAS_GROUP_CAP - 1;
  self->API_Association = API_Association;
  self->curr = &self->mmg[self->curr_idx];
  self->prev = &self->mmg[self->curr_idx - 1];
  // register algorithm
  InitMeasAsn(self);
}

#ifndef UTEST
static meta_meas_group_t *API_Association(MeasAsn *self, target_group_t *tgg, 
                                          const float dt)
{
  InitAssociation(self);

  meta_meas_group_t *curr = self->curr;
  meta_meas_t *mm = curr->mm;
  float rad;

  self->time_delta = dt;
  curr->vel_max = tgg->vbins * tgg->vunit;

  for (uint8_t thru = 0; thru < tgg->tcnt; ++thru) {
    if ((target_t *tg = tgg->targets[thru]).angle == 180.0f)
      continue;

    rad = RADIAN_OF_DEGREE(tg->angle);
    mm->cos_val = COS(rad);
    mm->ang = tg->angle;
    mm->rng = tg->range * tgg->runit;
    mm->rng_x = mm->range * SIN(rad);
    mm->rng_y = mm->range * mm->cos_val;
    mm->vel = tg->velocity * tgg->vunit;
    mm->mag = tg->mag;
    mm->ang_ver = tg->vangle;
    mm->vbin = tg->velocity;
    ++mm;
  }
  curr->mm_cnt = mm - curr->mm;
  Pairing(self, m, self->prev);

  return self->curr;
}
/*
  InitAssociation(self);

  float rad;
  meta_meas_group_t *curr = self->curr;
  meta_meas_t *mm=curr->mm;
  target_t *tg=tgg->targets,*tg_end=tgg->targets+tgg->tcnt;

  curr->tgg = tgg;
  curr->vel_max = tgg->vbins * tgg->vunit;
  
  while (tg < tg_end) {
    if (tg->angle == 180.0f) {
      tg++;
      continue;
    }

    rad = RADIAN_OF_DEGREE(tg->angle);
    mm->cos_val =  COS(rad);
    mm->ang = tg->angle;
    mm->rng = tg->range * tgg->runit;
    mm->rng_x = mm->rng * SIN(rad);
    mm->rng_y = mm->rng * mm->cos_val;
    mm->vel = tg->velocity * tgg->vunit;
    mm->mag = tg->mag;
    mm->vangle = tg->vangle;
    mm->vbin = tg->velocity;
    mm++;
    tg++;
  }
  
  self->time_delta = dt;
  curr->mm_cnt = mm-curr->mm;
  for(meta_meas_t* m = curr->mm; m < mm; m++)
    ;//Pairing(self, m);
  
  return self->curr;
*/
}
#else
static meta_meas_group_t *API_Association(MeasAsn *self)
{
  InitAssociation(self);
  Pairing(self);
  
  return self->curr;
}
#endif

/**************************************************
 * Methods                                        *
 **************************************************/
static void InitMeasAsn(MeasAsn *self)
{
  RegisterAlgMinXY(self);  // default algorithm: MinXY
}

static void RegisterAlgMinXY(MeasAsn *self)
{
  CalDelta = CalDeltaByMinXY;
  CalGate = CalGateByMinXY;
  IsGatePassed = IsGatePassedByMinXY;
}

static void InitAssociation(MeasAsn *self)
{
  // update curr and prev
  self->curr_idx = (self->curr_idx + 1) % META_MEAS_GROUP_CAP;
  self->prev = self->curr;
  self->curr = &self->mmg[self->curr_idx];

  // init curr flip
  for (uint16_t thru = 0; thru < self->curr->mm_cnt; ++thru) {
    self->curr->mm[thru].flip = kNotPaired;
  }
}

static int8_t BestExpVelPair(MeasAsn *self, meta_meas_t *curr_mm)
{
  const float rng_gate = self->gate.rng;
  const float vel_gate = self->gate.vel;
  const float ang_gate = self->gate.ang;
  const float curr_vel_max = self->curr->vel_max;
  const float prev_vel_max = self->prev->vel_max;
  float rng_min_delta = 10000.0f;
  int8_t best_mult = kNotPaired;  // best (shortest range) current flip tag
  uint16_t thru_mm = 0;
  meta_meas_group_t *prev = self->prev;

  for (; thru_mm < prev->mm_cnt; ++thru_mm) {
    float rng_delta = curr_mm->rng - prev->mm[thru_mm].rng;
    if (rng_delta < -rng_gate)  // next curr_mm
      break;
    if (rng_delta > rng_gate)  // next prev_mm
      continue;

    for (int8_t curr_mult_vel = -self->mult_vel;
         curr_mult_vel < self->mult_vel + 1;
         ++curr_mult_vel) {
      // thru current multiples of vel
      int8_t prev_mult_vel; 
      int8_t prev_mult_vel_end;
      if (prev->mm[thru_mm].flip != kNotPaired) {  // if paired, no iteration
        prev_mult_vel = prev->mm[thru_mm].flip;
        prev_mult_vel_end = prev_mult_vel + 1;  
      } else {
        prev_mult_vel = -self->mult_vel;
        prev_mult_vel_end = self->mult_vel + 1;
      }

      for (; prev_mult_vel < prev_mult_vel_end; ++prev_mult_vel) {
        // thru previous multiples of vel
        float vel_delta = (curr_mm->vel + curr_mult_vel * curr_vel_max)
                          - (prev->mm[thru_mm].vel + prev_mult_vel * prev_vel_max);
        float ang_delta = curr_mm->ang - prev->mm[thru_mm].ang;
        if (vel_delta > -vel_gate && vel_delta < vel_gate
            && ang_delta > -ang_gate && ang_delta < ang_gate
            && rng_delta < rng_min_delta) {
          best_mult = curr_mult_vel;
          rng_min_delta = rng_delta;
        }
      }
    }
  }
  return best_mult;
}

static void Pairing(MeasAsn *self)
{
  meta_meas_group_t *curr = self->curr;
  meta_meas_group_t *prev = self->prev;
  meta_meas_t *curr_mm;
  meta_meas_t *prev_mm;
  float rng_within = MAX_VELOCITY_SUPPORTED * self->time_delta;

  for (uint16_t thru_c = 0; thru_c < curr->mm_cnt; ++thru_c) {
    float token = 10000.0f;
    int8_t flip;
    curr_mm = &curr->mm[thru_c];

    ASSO_DEBUG("Cu[%.1f,%.2f,%.1f]\n",curr_mm->rng, curr_mm->ang, curr_mm->vel);
    for (uint16_t thru_p = 0; thru_p < prev->mm_cnt; ++thru_p) {
      prev_mm = &prev->mm[thru_p];
      float rng_delta = curr_mm->rng - prev_mm->rng;

      if (rng_delta < -rng_within)  // next curr_mm
        break;
      if (rng_delta > rng_within)  // next prev_mm
        continue;

      ASSO_DEBUG("Pv[%.1f,%.2f,%.1f]\n", prev_mm->rng, prev_mm->ang, 
        prev_mm->vel);
      flip = PairingExpVel(self, &prev->mm[thru_c], &prev->mm[thru_p], &token);
      if (kNotPaired != flip)
        curr->mm[thru_c].flip = flip;
    }
  }
  return;
}

static int8_t PairingExpVel(
  MeasAsn *self, meta_meas_t *curr_mm, meta_meas_t *prev_mm, float *token)
{
  int8_t flip = kNotPaired;

  for (int8_t curr_mult_vel = -self->mult_vel; 
       curr_mult_vel < self->mult_vel + 1;
       ++curr_mult_vel) {
    // thru current multiples of vel
    int8_t prev_mult_vel; 
    int8_t prev_mult_vel_end;
    if (kNotPaired != prev_mm->flip) {  // if paired, no iteration
      prev_mult_vel = prev_mm->flip;
      prev_mult_vel_end = prev_mult_vel;  
    } else {
      prev_mult_vel = -self->mult_vel;
      prev_mult_vel_end = self->mult_vel;
    }

    for (; prev_mult_vel < prev_mult_vel_end + 1; ++prev_mult_vel) {
      // thru previous multiples of vel
      meta_meas_t gate = CalGate(self, curr_mm, prev_mm);
      meta_meas_t delta = CalDelta(self, curr_mm, prev_mm, 
                                   curr_mult_vel, prev_mult_vel);
      ASSO_DEBUG("F[%d,%d],D[%.1f,%.1f,%.1f]\n", curr_mult_vel, prev_mult_vel,
        delta.rng_y, delta.vel);
      if (IsGatePassed(self, &gate, &delta, token)) {
        flip = curr_mult_vel;
      }
    }
  }
  return flip;
}

static meta_meas_t CalGateByMinXY(
  MeasAsn *self, meta_meas_t *curr_mm, meta_meas_t *prev_mm)
{
  return self->gate;
}

static meta_meas_t CalDeltaByMinXY(
  MeasAsn *self, meta_meas_t *curr_mm, meta_meas_t *prev_mm, int8_t curr_mult, 
  int8_t prev_mult)
{
  const float dt = self->time_delta;  // second
  const float curr_v_max = self->curr->vel_max;
  const float prev_v_max = self->curr->vel_max;
  const float vel_y = EXP_VEL(prev_mm->vel, prev_v_max, prev_mult) / 
    prev_mm->cos_val;  // vel / cos(theta)
  meta_meas_t delta = {0};

  delta.rng_x = curr_mm->rng_x - prev_mm->rng_x;
  delta.rng_y = curr_mm->rng_y - (prev_mm->rng_y + vel_y * dt);
  delta.vel = EXP_VEL(curr_mm->vel, curr_v_max, curr_mult) - 
    EXP_VEL(prev_mm->vel, prev_v_max, prev_mult);
  return delta;
}

static int8_t IsGatePassedByMinXY(
  MeasAsn *self, meta_meas_t *gate, meta_meas_t *delta, float *token)
{
  float xy_sq_sum;

  if (gate->rng_x <= fabs(delta->rng_x) && gate->rng_y <= fabs(delta->rng_y) &&
      gate->vel <= fabs(delta->vel)) {
    xy_sq_sum = delta->rng_x*delta->rng_x + delta->rng_y*delta->rng_y;
    if (*token > xy_sq_sum) {
      *token = xy_sq_sum;
      return 1;
    }
  }
  return 0;
}

/**************************************************
 * Sub-Methods                                    *
 **************************************************/
static inline float EXP_VEL(const float v, const float v_max, const uint8_t m)
{
  return v + m * v_max;
}

static inline float ExpVel(const float v, const float v_max, const uint8_t m)
{
  int8_t sign = (v >= 0) ^ (m % 2) ? (+1) : (-1);
  uint8_t mul = (m + 1) / 2;
  return v + sign * mul * v_max;
}
