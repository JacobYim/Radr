// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from radr_gps_msgs:msg/GpsReport.idl
// generated code does not contain a copyright notice

#ifndef RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__FUNCTIONS_H_
#define RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "radr_gps_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "radr_gps_msgs/msg/detail/gps_report__struct.h"

/// Initialize msg/GpsReport message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * radr_gps_msgs__msg__GpsReport
 * )) before or use
 * radr_gps_msgs__msg__GpsReport__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_radr_gps_msgs
bool
radr_gps_msgs__msg__GpsReport__init(radr_gps_msgs__msg__GpsReport * msg);

/// Finalize msg/GpsReport message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_radr_gps_msgs
void
radr_gps_msgs__msg__GpsReport__fini(radr_gps_msgs__msg__GpsReport * msg);

/// Create msg/GpsReport message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * radr_gps_msgs__msg__GpsReport__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_radr_gps_msgs
radr_gps_msgs__msg__GpsReport *
radr_gps_msgs__msg__GpsReport__create();

/// Destroy msg/GpsReport message.
/**
 * It calls
 * radr_gps_msgs__msg__GpsReport__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_radr_gps_msgs
void
radr_gps_msgs__msg__GpsReport__destroy(radr_gps_msgs__msg__GpsReport * msg);

/// Check for msg/GpsReport message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_radr_gps_msgs
bool
radr_gps_msgs__msg__GpsReport__are_equal(const radr_gps_msgs__msg__GpsReport * lhs, const radr_gps_msgs__msg__GpsReport * rhs);

/// Copy a msg/GpsReport message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_radr_gps_msgs
bool
radr_gps_msgs__msg__GpsReport__copy(
  const radr_gps_msgs__msg__GpsReport * input,
  radr_gps_msgs__msg__GpsReport * output);

/// Initialize array of msg/GpsReport messages.
/**
 * It allocates the memory for the number of elements and calls
 * radr_gps_msgs__msg__GpsReport__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_radr_gps_msgs
bool
radr_gps_msgs__msg__GpsReport__Sequence__init(radr_gps_msgs__msg__GpsReport__Sequence * array, size_t size);

/// Finalize array of msg/GpsReport messages.
/**
 * It calls
 * radr_gps_msgs__msg__GpsReport__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_radr_gps_msgs
void
radr_gps_msgs__msg__GpsReport__Sequence__fini(radr_gps_msgs__msg__GpsReport__Sequence * array);

/// Create array of msg/GpsReport messages.
/**
 * It allocates the memory for the array and calls
 * radr_gps_msgs__msg__GpsReport__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_radr_gps_msgs
radr_gps_msgs__msg__GpsReport__Sequence *
radr_gps_msgs__msg__GpsReport__Sequence__create(size_t size);

/// Destroy array of msg/GpsReport messages.
/**
 * It calls
 * radr_gps_msgs__msg__GpsReport__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_radr_gps_msgs
void
radr_gps_msgs__msg__GpsReport__Sequence__destroy(radr_gps_msgs__msg__GpsReport__Sequence * array);

/// Check for msg/GpsReport message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_radr_gps_msgs
bool
radr_gps_msgs__msg__GpsReport__Sequence__are_equal(const radr_gps_msgs__msg__GpsReport__Sequence * lhs, const radr_gps_msgs__msg__GpsReport__Sequence * rhs);

/// Copy an array of msg/GpsReport messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_radr_gps_msgs
bool
radr_gps_msgs__msg__GpsReport__Sequence__copy(
  const radr_gps_msgs__msg__GpsReport__Sequence * input,
  radr_gps_msgs__msg__GpsReport__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__FUNCTIONS_H_
