// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from radr_gps_msgs:msg/GpsReport.idl
// generated code does not contain a copyright notice
#include "radr_gps_msgs/msg/detail/gps_report__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "radr_gps_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "radr_gps_msgs/msg/detail/gps_report__struct.h"
#include "radr_gps_msgs/msg/detail/gps_report__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // active_port, course_true, date_ddmmyy, gga_fix_code, gga_fix_name, hdop, sats_in_view, sats_used, speed_kmh, speed_kn, summary_text, time_utc
#include "rosidl_runtime_c/string_functions.h"  // active_port, course_true, date_ddmmyy, gga_fix_code, gga_fix_name, hdop, sats_in_view, sats_used, speed_kmh, speed_kn, summary_text, time_utc
#include "std_msgs/msg/detail/header__functions.h"  // header

// forward declare type support functions
ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_radr_gps_msgs
size_t get_serialized_size_std_msgs__msg__Header(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_radr_gps_msgs
size_t max_serialized_size_std_msgs__msg__Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_radr_gps_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, std_msgs, msg, Header)();


using _GpsReport__ros_msg_type = radr_gps_msgs__msg__GpsReport;

static bool _GpsReport__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _GpsReport__ros_msg_type * ros_message = static_cast<const _GpsReport__ros_msg_type *>(untyped_ros_message);
  // Field name: header
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, std_msgs, msg, Header
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->header, cdr))
    {
      return false;
    }
  }

  // Field name: time_utc
  {
    const rosidl_runtime_c__String * str = &ros_message->time_utc;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: date_ddmmyy
  {
    const rosidl_runtime_c__String * str = &ros_message->date_ddmmyy;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: rmc_valid
  {
    cdr << (ros_message->rmc_valid ? true : false);
  }

  // Field name: gga_fix_code
  {
    const rosidl_runtime_c__String * str = &ros_message->gga_fix_code;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: gga_fix_name
  {
    const rosidl_runtime_c__String * str = &ros_message->gga_fix_name;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: latitude
  {
    cdr << ros_message->latitude;
  }

  // Field name: longitude
  {
    cdr << ros_message->longitude;
  }

  // Field name: altitude_msl
  {
    cdr << ros_message->altitude_msl;
  }

  // Field name: hdop
  {
    const rosidl_runtime_c__String * str = &ros_message->hdop;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: sats_used
  {
    const rosidl_runtime_c__String * str = &ros_message->sats_used;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: sats_in_view
  {
    const rosidl_runtime_c__String * str = &ros_message->sats_in_view;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: speed_kn
  {
    const rosidl_runtime_c__String * str = &ros_message->speed_kn;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: course_true
  {
    const rosidl_runtime_c__String * str = &ros_message->course_true;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: speed_kmh
  {
    const rosidl_runtime_c__String * str = &ros_message->speed_kmh;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: has_position
  {
    cdr << (ros_message->has_position ? true : false);
  }

  // Field name: uart_connected
  {
    cdr << (ros_message->uart_connected ? true : false);
  }

  // Field name: active_port
  {
    const rosidl_runtime_c__String * str = &ros_message->active_port;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: summary_text
  {
    const rosidl_runtime_c__String * str = &ros_message->summary_text;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _GpsReport__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _GpsReport__ros_msg_type * ros_message = static_cast<_GpsReport__ros_msg_type *>(untyped_ros_message);
  // Field name: header
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, std_msgs, msg, Header
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->header))
    {
      return false;
    }
  }

  // Field name: time_utc
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->time_utc.data) {
      rosidl_runtime_c__String__init(&ros_message->time_utc);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->time_utc,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'time_utc'\n");
      return false;
    }
  }

  // Field name: date_ddmmyy
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->date_ddmmyy.data) {
      rosidl_runtime_c__String__init(&ros_message->date_ddmmyy);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->date_ddmmyy,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'date_ddmmyy'\n");
      return false;
    }
  }

  // Field name: rmc_valid
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->rmc_valid = tmp ? true : false;
  }

  // Field name: gga_fix_code
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->gga_fix_code.data) {
      rosidl_runtime_c__String__init(&ros_message->gga_fix_code);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->gga_fix_code,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'gga_fix_code'\n");
      return false;
    }
  }

  // Field name: gga_fix_name
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->gga_fix_name.data) {
      rosidl_runtime_c__String__init(&ros_message->gga_fix_name);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->gga_fix_name,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'gga_fix_name'\n");
      return false;
    }
  }

  // Field name: latitude
  {
    cdr >> ros_message->latitude;
  }

  // Field name: longitude
  {
    cdr >> ros_message->longitude;
  }

  // Field name: altitude_msl
  {
    cdr >> ros_message->altitude_msl;
  }

  // Field name: hdop
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->hdop.data) {
      rosidl_runtime_c__String__init(&ros_message->hdop);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->hdop,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'hdop'\n");
      return false;
    }
  }

  // Field name: sats_used
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->sats_used.data) {
      rosidl_runtime_c__String__init(&ros_message->sats_used);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->sats_used,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'sats_used'\n");
      return false;
    }
  }

  // Field name: sats_in_view
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->sats_in_view.data) {
      rosidl_runtime_c__String__init(&ros_message->sats_in_view);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->sats_in_view,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'sats_in_view'\n");
      return false;
    }
  }

  // Field name: speed_kn
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->speed_kn.data) {
      rosidl_runtime_c__String__init(&ros_message->speed_kn);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->speed_kn,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'speed_kn'\n");
      return false;
    }
  }

  // Field name: course_true
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->course_true.data) {
      rosidl_runtime_c__String__init(&ros_message->course_true);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->course_true,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'course_true'\n");
      return false;
    }
  }

  // Field name: speed_kmh
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->speed_kmh.data) {
      rosidl_runtime_c__String__init(&ros_message->speed_kmh);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->speed_kmh,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'speed_kmh'\n");
      return false;
    }
  }

  // Field name: has_position
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->has_position = tmp ? true : false;
  }

  // Field name: uart_connected
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->uart_connected = tmp ? true : false;
  }

  // Field name: active_port
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->active_port.data) {
      rosidl_runtime_c__String__init(&ros_message->active_port);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->active_port,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'active_port'\n");
      return false;
    }
  }

  // Field name: summary_text
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->summary_text.data) {
      rosidl_runtime_c__String__init(&ros_message->summary_text);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->summary_text,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'summary_text'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_radr_gps_msgs
size_t get_serialized_size_radr_gps_msgs__msg__GpsReport(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _GpsReport__ros_msg_type * ros_message = static_cast<const _GpsReport__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name header

  current_alignment += get_serialized_size_std_msgs__msg__Header(
    &(ros_message->header), current_alignment);
  // field.name time_utc
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->time_utc.size + 1);
  // field.name date_ddmmyy
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->date_ddmmyy.size + 1);
  // field.name rmc_valid
  {
    size_t item_size = sizeof(ros_message->rmc_valid);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name gga_fix_code
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->gga_fix_code.size + 1);
  // field.name gga_fix_name
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->gga_fix_name.size + 1);
  // field.name latitude
  {
    size_t item_size = sizeof(ros_message->latitude);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name longitude
  {
    size_t item_size = sizeof(ros_message->longitude);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name altitude_msl
  {
    size_t item_size = sizeof(ros_message->altitude_msl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name hdop
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->hdop.size + 1);
  // field.name sats_used
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->sats_used.size + 1);
  // field.name sats_in_view
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->sats_in_view.size + 1);
  // field.name speed_kn
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->speed_kn.size + 1);
  // field.name course_true
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->course_true.size + 1);
  // field.name speed_kmh
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->speed_kmh.size + 1);
  // field.name has_position
  {
    size_t item_size = sizeof(ros_message->has_position);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name uart_connected
  {
    size_t item_size = sizeof(ros_message->uart_connected);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name active_port
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->active_port.size + 1);
  // field.name summary_text
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->summary_text.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _GpsReport__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_radr_gps_msgs__msg__GpsReport(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_radr_gps_msgs
size_t max_serialized_size_radr_gps_msgs__msg__GpsReport(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: header
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_std_msgs__msg__Header(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: time_utc
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: date_ddmmyy
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: rmc_valid
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: gga_fix_code
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: gga_fix_name
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: latitude
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: longitude
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: altitude_msl
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: hdop
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: sats_used
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: sats_in_view
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: speed_kn
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: course_true
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: speed_kmh
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: has_position
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: uart_connected
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: active_port
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: summary_text
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = radr_gps_msgs__msg__GpsReport;
    is_plain =
      (
      offsetof(DataType, summary_text) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _GpsReport__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_radr_gps_msgs__msg__GpsReport(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_GpsReport = {
  "radr_gps_msgs::msg",
  "GpsReport",
  _GpsReport__cdr_serialize,
  _GpsReport__cdr_deserialize,
  _GpsReport__get_serialized_size,
  _GpsReport__max_serialized_size
};

static rosidl_message_type_support_t _GpsReport__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_GpsReport,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, radr_gps_msgs, msg, GpsReport)() {
  return &_GpsReport__type_support;
}

#if defined(__cplusplus)
}
#endif
