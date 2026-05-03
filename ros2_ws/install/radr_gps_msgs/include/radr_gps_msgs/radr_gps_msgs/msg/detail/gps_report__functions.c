// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from radr_gps_msgs:msg/GpsReport.idl
// generated code does not contain a copyright notice
#include "radr_gps_msgs/msg/detail/gps_report__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `time_utc`
// Member `date_ddmmyy`
// Member `gga_fix_code`
// Member `gga_fix_name`
// Member `hdop`
// Member `sats_used`
// Member `sats_in_view`
// Member `speed_kn`
// Member `course_true`
// Member `speed_kmh`
// Member `active_port`
// Member `summary_text`
#include "rosidl_runtime_c/string_functions.h"

bool
radr_gps_msgs__msg__GpsReport__init(radr_gps_msgs__msg__GpsReport * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    radr_gps_msgs__msg__GpsReport__fini(msg);
    return false;
  }
  // time_utc
  if (!rosidl_runtime_c__String__init(&msg->time_utc)) {
    radr_gps_msgs__msg__GpsReport__fini(msg);
    return false;
  }
  // date_ddmmyy
  if (!rosidl_runtime_c__String__init(&msg->date_ddmmyy)) {
    radr_gps_msgs__msg__GpsReport__fini(msg);
    return false;
  }
  // rmc_valid
  // gga_fix_code
  if (!rosidl_runtime_c__String__init(&msg->gga_fix_code)) {
    radr_gps_msgs__msg__GpsReport__fini(msg);
    return false;
  }
  // gga_fix_name
  if (!rosidl_runtime_c__String__init(&msg->gga_fix_name)) {
    radr_gps_msgs__msg__GpsReport__fini(msg);
    return false;
  }
  // latitude
  // longitude
  // altitude_msl
  // hdop
  if (!rosidl_runtime_c__String__init(&msg->hdop)) {
    radr_gps_msgs__msg__GpsReport__fini(msg);
    return false;
  }
  // sats_used
  if (!rosidl_runtime_c__String__init(&msg->sats_used)) {
    radr_gps_msgs__msg__GpsReport__fini(msg);
    return false;
  }
  // sats_in_view
  if (!rosidl_runtime_c__String__init(&msg->sats_in_view)) {
    radr_gps_msgs__msg__GpsReport__fini(msg);
    return false;
  }
  // speed_kn
  if (!rosidl_runtime_c__String__init(&msg->speed_kn)) {
    radr_gps_msgs__msg__GpsReport__fini(msg);
    return false;
  }
  // course_true
  if (!rosidl_runtime_c__String__init(&msg->course_true)) {
    radr_gps_msgs__msg__GpsReport__fini(msg);
    return false;
  }
  // speed_kmh
  if (!rosidl_runtime_c__String__init(&msg->speed_kmh)) {
    radr_gps_msgs__msg__GpsReport__fini(msg);
    return false;
  }
  // has_position
  // uart_connected
  // active_port
  if (!rosidl_runtime_c__String__init(&msg->active_port)) {
    radr_gps_msgs__msg__GpsReport__fini(msg);
    return false;
  }
  // summary_text
  if (!rosidl_runtime_c__String__init(&msg->summary_text)) {
    radr_gps_msgs__msg__GpsReport__fini(msg);
    return false;
  }
  return true;
}

void
radr_gps_msgs__msg__GpsReport__fini(radr_gps_msgs__msg__GpsReport * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // time_utc
  rosidl_runtime_c__String__fini(&msg->time_utc);
  // date_ddmmyy
  rosidl_runtime_c__String__fini(&msg->date_ddmmyy);
  // rmc_valid
  // gga_fix_code
  rosidl_runtime_c__String__fini(&msg->gga_fix_code);
  // gga_fix_name
  rosidl_runtime_c__String__fini(&msg->gga_fix_name);
  // latitude
  // longitude
  // altitude_msl
  // hdop
  rosidl_runtime_c__String__fini(&msg->hdop);
  // sats_used
  rosidl_runtime_c__String__fini(&msg->sats_used);
  // sats_in_view
  rosidl_runtime_c__String__fini(&msg->sats_in_view);
  // speed_kn
  rosidl_runtime_c__String__fini(&msg->speed_kn);
  // course_true
  rosidl_runtime_c__String__fini(&msg->course_true);
  // speed_kmh
  rosidl_runtime_c__String__fini(&msg->speed_kmh);
  // has_position
  // uart_connected
  // active_port
  rosidl_runtime_c__String__fini(&msg->active_port);
  // summary_text
  rosidl_runtime_c__String__fini(&msg->summary_text);
}

bool
radr_gps_msgs__msg__GpsReport__are_equal(const radr_gps_msgs__msg__GpsReport * lhs, const radr_gps_msgs__msg__GpsReport * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // time_utc
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->time_utc), &(rhs->time_utc)))
  {
    return false;
  }
  // date_ddmmyy
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->date_ddmmyy), &(rhs->date_ddmmyy)))
  {
    return false;
  }
  // rmc_valid
  if (lhs->rmc_valid != rhs->rmc_valid) {
    return false;
  }
  // gga_fix_code
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->gga_fix_code), &(rhs->gga_fix_code)))
  {
    return false;
  }
  // gga_fix_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->gga_fix_name), &(rhs->gga_fix_name)))
  {
    return false;
  }
  // latitude
  if (lhs->latitude != rhs->latitude) {
    return false;
  }
  // longitude
  if (lhs->longitude != rhs->longitude) {
    return false;
  }
  // altitude_msl
  if (lhs->altitude_msl != rhs->altitude_msl) {
    return false;
  }
  // hdop
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->hdop), &(rhs->hdop)))
  {
    return false;
  }
  // sats_used
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->sats_used), &(rhs->sats_used)))
  {
    return false;
  }
  // sats_in_view
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->sats_in_view), &(rhs->sats_in_view)))
  {
    return false;
  }
  // speed_kn
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->speed_kn), &(rhs->speed_kn)))
  {
    return false;
  }
  // course_true
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->course_true), &(rhs->course_true)))
  {
    return false;
  }
  // speed_kmh
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->speed_kmh), &(rhs->speed_kmh)))
  {
    return false;
  }
  // has_position
  if (lhs->has_position != rhs->has_position) {
    return false;
  }
  // uart_connected
  if (lhs->uart_connected != rhs->uart_connected) {
    return false;
  }
  // active_port
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->active_port), &(rhs->active_port)))
  {
    return false;
  }
  // summary_text
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->summary_text), &(rhs->summary_text)))
  {
    return false;
  }
  return true;
}

bool
radr_gps_msgs__msg__GpsReport__copy(
  const radr_gps_msgs__msg__GpsReport * input,
  radr_gps_msgs__msg__GpsReport * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // time_utc
  if (!rosidl_runtime_c__String__copy(
      &(input->time_utc), &(output->time_utc)))
  {
    return false;
  }
  // date_ddmmyy
  if (!rosidl_runtime_c__String__copy(
      &(input->date_ddmmyy), &(output->date_ddmmyy)))
  {
    return false;
  }
  // rmc_valid
  output->rmc_valid = input->rmc_valid;
  // gga_fix_code
  if (!rosidl_runtime_c__String__copy(
      &(input->gga_fix_code), &(output->gga_fix_code)))
  {
    return false;
  }
  // gga_fix_name
  if (!rosidl_runtime_c__String__copy(
      &(input->gga_fix_name), &(output->gga_fix_name)))
  {
    return false;
  }
  // latitude
  output->latitude = input->latitude;
  // longitude
  output->longitude = input->longitude;
  // altitude_msl
  output->altitude_msl = input->altitude_msl;
  // hdop
  if (!rosidl_runtime_c__String__copy(
      &(input->hdop), &(output->hdop)))
  {
    return false;
  }
  // sats_used
  if (!rosidl_runtime_c__String__copy(
      &(input->sats_used), &(output->sats_used)))
  {
    return false;
  }
  // sats_in_view
  if (!rosidl_runtime_c__String__copy(
      &(input->sats_in_view), &(output->sats_in_view)))
  {
    return false;
  }
  // speed_kn
  if (!rosidl_runtime_c__String__copy(
      &(input->speed_kn), &(output->speed_kn)))
  {
    return false;
  }
  // course_true
  if (!rosidl_runtime_c__String__copy(
      &(input->course_true), &(output->course_true)))
  {
    return false;
  }
  // speed_kmh
  if (!rosidl_runtime_c__String__copy(
      &(input->speed_kmh), &(output->speed_kmh)))
  {
    return false;
  }
  // has_position
  output->has_position = input->has_position;
  // uart_connected
  output->uart_connected = input->uart_connected;
  // active_port
  if (!rosidl_runtime_c__String__copy(
      &(input->active_port), &(output->active_port)))
  {
    return false;
  }
  // summary_text
  if (!rosidl_runtime_c__String__copy(
      &(input->summary_text), &(output->summary_text)))
  {
    return false;
  }
  return true;
}

radr_gps_msgs__msg__GpsReport *
radr_gps_msgs__msg__GpsReport__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  radr_gps_msgs__msg__GpsReport * msg = (radr_gps_msgs__msg__GpsReport *)allocator.allocate(sizeof(radr_gps_msgs__msg__GpsReport), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(radr_gps_msgs__msg__GpsReport));
  bool success = radr_gps_msgs__msg__GpsReport__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
radr_gps_msgs__msg__GpsReport__destroy(radr_gps_msgs__msg__GpsReport * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    radr_gps_msgs__msg__GpsReport__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
radr_gps_msgs__msg__GpsReport__Sequence__init(radr_gps_msgs__msg__GpsReport__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  radr_gps_msgs__msg__GpsReport * data = NULL;

  if (size) {
    data = (radr_gps_msgs__msg__GpsReport *)allocator.zero_allocate(size, sizeof(radr_gps_msgs__msg__GpsReport), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = radr_gps_msgs__msg__GpsReport__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        radr_gps_msgs__msg__GpsReport__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
radr_gps_msgs__msg__GpsReport__Sequence__fini(radr_gps_msgs__msg__GpsReport__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      radr_gps_msgs__msg__GpsReport__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

radr_gps_msgs__msg__GpsReport__Sequence *
radr_gps_msgs__msg__GpsReport__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  radr_gps_msgs__msg__GpsReport__Sequence * array = (radr_gps_msgs__msg__GpsReport__Sequence *)allocator.allocate(sizeof(radr_gps_msgs__msg__GpsReport__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = radr_gps_msgs__msg__GpsReport__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
radr_gps_msgs__msg__GpsReport__Sequence__destroy(radr_gps_msgs__msg__GpsReport__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    radr_gps_msgs__msg__GpsReport__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
radr_gps_msgs__msg__GpsReport__Sequence__are_equal(const radr_gps_msgs__msg__GpsReport__Sequence * lhs, const radr_gps_msgs__msg__GpsReport__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!radr_gps_msgs__msg__GpsReport__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
radr_gps_msgs__msg__GpsReport__Sequence__copy(
  const radr_gps_msgs__msg__GpsReport__Sequence * input,
  radr_gps_msgs__msg__GpsReport__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(radr_gps_msgs__msg__GpsReport);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    radr_gps_msgs__msg__GpsReport * data =
      (radr_gps_msgs__msg__GpsReport *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!radr_gps_msgs__msg__GpsReport__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          radr_gps_msgs__msg__GpsReport__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!radr_gps_msgs__msg__GpsReport__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
