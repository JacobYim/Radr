// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from radr_gps_msgs:msg/GpsReport.idl
// generated code does not contain a copyright notice

#ifndef RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__TRAITS_HPP_
#define RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "radr_gps_msgs/msg/detail/gps_report__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace radr_gps_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const GpsReport & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: time_utc
  {
    out << "time_utc: ";
    rosidl_generator_traits::value_to_yaml(msg.time_utc, out);
    out << ", ";
  }

  // member: date_ddmmyy
  {
    out << "date_ddmmyy: ";
    rosidl_generator_traits::value_to_yaml(msg.date_ddmmyy, out);
    out << ", ";
  }

  // member: rmc_valid
  {
    out << "rmc_valid: ";
    rosidl_generator_traits::value_to_yaml(msg.rmc_valid, out);
    out << ", ";
  }

  // member: gga_fix_code
  {
    out << "gga_fix_code: ";
    rosidl_generator_traits::value_to_yaml(msg.gga_fix_code, out);
    out << ", ";
  }

  // member: gga_fix_name
  {
    out << "gga_fix_name: ";
    rosidl_generator_traits::value_to_yaml(msg.gga_fix_name, out);
    out << ", ";
  }

  // member: latitude
  {
    out << "latitude: ";
    rosidl_generator_traits::value_to_yaml(msg.latitude, out);
    out << ", ";
  }

  // member: longitude
  {
    out << "longitude: ";
    rosidl_generator_traits::value_to_yaml(msg.longitude, out);
    out << ", ";
  }

  // member: altitude_msl
  {
    out << "altitude_msl: ";
    rosidl_generator_traits::value_to_yaml(msg.altitude_msl, out);
    out << ", ";
  }

  // member: hdop
  {
    out << "hdop: ";
    rosidl_generator_traits::value_to_yaml(msg.hdop, out);
    out << ", ";
  }

  // member: sats_used
  {
    out << "sats_used: ";
    rosidl_generator_traits::value_to_yaml(msg.sats_used, out);
    out << ", ";
  }

  // member: sats_in_view
  {
    out << "sats_in_view: ";
    rosidl_generator_traits::value_to_yaml(msg.sats_in_view, out);
    out << ", ";
  }

  // member: speed_kn
  {
    out << "speed_kn: ";
    rosidl_generator_traits::value_to_yaml(msg.speed_kn, out);
    out << ", ";
  }

  // member: course_true
  {
    out << "course_true: ";
    rosidl_generator_traits::value_to_yaml(msg.course_true, out);
    out << ", ";
  }

  // member: speed_kmh
  {
    out << "speed_kmh: ";
    rosidl_generator_traits::value_to_yaml(msg.speed_kmh, out);
    out << ", ";
  }

  // member: has_position
  {
    out << "has_position: ";
    rosidl_generator_traits::value_to_yaml(msg.has_position, out);
    out << ", ";
  }

  // member: uart_connected
  {
    out << "uart_connected: ";
    rosidl_generator_traits::value_to_yaml(msg.uart_connected, out);
    out << ", ";
  }

  // member: active_port
  {
    out << "active_port: ";
    rosidl_generator_traits::value_to_yaml(msg.active_port, out);
    out << ", ";
  }

  // member: summary_text
  {
    out << "summary_text: ";
    rosidl_generator_traits::value_to_yaml(msg.summary_text, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GpsReport & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: time_utc
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "time_utc: ";
    rosidl_generator_traits::value_to_yaml(msg.time_utc, out);
    out << "\n";
  }

  // member: date_ddmmyy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "date_ddmmyy: ";
    rosidl_generator_traits::value_to_yaml(msg.date_ddmmyy, out);
    out << "\n";
  }

  // member: rmc_valid
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "rmc_valid: ";
    rosidl_generator_traits::value_to_yaml(msg.rmc_valid, out);
    out << "\n";
  }

  // member: gga_fix_code
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gga_fix_code: ";
    rosidl_generator_traits::value_to_yaml(msg.gga_fix_code, out);
    out << "\n";
  }

  // member: gga_fix_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gga_fix_name: ";
    rosidl_generator_traits::value_to_yaml(msg.gga_fix_name, out);
    out << "\n";
  }

  // member: latitude
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "latitude: ";
    rosidl_generator_traits::value_to_yaml(msg.latitude, out);
    out << "\n";
  }

  // member: longitude
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "longitude: ";
    rosidl_generator_traits::value_to_yaml(msg.longitude, out);
    out << "\n";
  }

  // member: altitude_msl
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "altitude_msl: ";
    rosidl_generator_traits::value_to_yaml(msg.altitude_msl, out);
    out << "\n";
  }

  // member: hdop
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "hdop: ";
    rosidl_generator_traits::value_to_yaml(msg.hdop, out);
    out << "\n";
  }

  // member: sats_used
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sats_used: ";
    rosidl_generator_traits::value_to_yaml(msg.sats_used, out);
    out << "\n";
  }

  // member: sats_in_view
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sats_in_view: ";
    rosidl_generator_traits::value_to_yaml(msg.sats_in_view, out);
    out << "\n";
  }

  // member: speed_kn
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "speed_kn: ";
    rosidl_generator_traits::value_to_yaml(msg.speed_kn, out);
    out << "\n";
  }

  // member: course_true
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "course_true: ";
    rosidl_generator_traits::value_to_yaml(msg.course_true, out);
    out << "\n";
  }

  // member: speed_kmh
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "speed_kmh: ";
    rosidl_generator_traits::value_to_yaml(msg.speed_kmh, out);
    out << "\n";
  }

  // member: has_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "has_position: ";
    rosidl_generator_traits::value_to_yaml(msg.has_position, out);
    out << "\n";
  }

  // member: uart_connected
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "uart_connected: ";
    rosidl_generator_traits::value_to_yaml(msg.uart_connected, out);
    out << "\n";
  }

  // member: active_port
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "active_port: ";
    rosidl_generator_traits::value_to_yaml(msg.active_port, out);
    out << "\n";
  }

  // member: summary_text
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "summary_text: ";
    rosidl_generator_traits::value_to_yaml(msg.summary_text, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GpsReport & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace radr_gps_msgs

namespace rosidl_generator_traits
{

[[deprecated("use radr_gps_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const radr_gps_msgs::msg::GpsReport & msg,
  std::ostream & out, size_t indentation = 0)
{
  radr_gps_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use radr_gps_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const radr_gps_msgs::msg::GpsReport & msg)
{
  return radr_gps_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<radr_gps_msgs::msg::GpsReport>()
{
  return "radr_gps_msgs::msg::GpsReport";
}

template<>
inline const char * name<radr_gps_msgs::msg::GpsReport>()
{
  return "radr_gps_msgs/msg/GpsReport";
}

template<>
struct has_fixed_size<radr_gps_msgs::msg::GpsReport>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<radr_gps_msgs::msg::GpsReport>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<radr_gps_msgs::msg::GpsReport>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__TRAITS_HPP_
