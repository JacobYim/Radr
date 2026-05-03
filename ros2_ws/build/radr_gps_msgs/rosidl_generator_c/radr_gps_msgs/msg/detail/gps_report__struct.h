// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from radr_gps_msgs:msg/GpsReport.idl
// generated code does not contain a copyright notice

#ifndef RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__STRUCT_H_
#define RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'time_utc'
// Member 'date_ddmmyy'
// Member 'gga_fix_code'
// Member 'gga_fix_name'
// Member 'hdop'
// Member 'sats_used'
// Member 'sats_in_view'
// Member 'speed_kn'
// Member 'course_true'
// Member 'speed_kmh'
// Member 'active_port'
// Member 'summary_text'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/GpsReport in the package radr_gps_msgs.
/**
  * Parsed GPS summary (aligned with gps_parsed_live GpsDisplayState / as_lines).
 */
typedef struct radr_gps_msgs__msg__GpsReport
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__String time_utc;
  rosidl_runtime_c__String date_ddmmyy;
  bool rmc_valid;
  rosidl_runtime_c__String gga_fix_code;
  rosidl_runtime_c__String gga_fix_name;
  double latitude;
  double longitude;
  double altitude_msl;
  rosidl_runtime_c__String hdop;
  rosidl_runtime_c__String sats_used;
  rosidl_runtime_c__String sats_in_view;
  rosidl_runtime_c__String speed_kn;
  rosidl_runtime_c__String course_true;
  rosidl_runtime_c__String speed_kmh;
  bool has_position;
  bool uart_connected;
  rosidl_runtime_c__String active_port;
  /// Multi-line human-readable block (same shape as gps_parsed_live as_lines)
  rosidl_runtime_c__String summary_text;
} radr_gps_msgs__msg__GpsReport;

// Struct for a sequence of radr_gps_msgs__msg__GpsReport.
typedef struct radr_gps_msgs__msg__GpsReport__Sequence
{
  radr_gps_msgs__msg__GpsReport * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} radr_gps_msgs__msg__GpsReport__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__STRUCT_H_
