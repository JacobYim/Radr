// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from radr_gps_msgs:msg/GpsReport.idl
// generated code does not contain a copyright notice

#ifndef RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__BUILDER_HPP_
#define RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "radr_gps_msgs/msg/detail/gps_report__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace radr_gps_msgs
{

namespace msg
{

namespace builder
{

class Init_GpsReport_summary_text
{
public:
  explicit Init_GpsReport_summary_text(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  ::radr_gps_msgs::msg::GpsReport summary_text(::radr_gps_msgs::msg::GpsReport::_summary_text_type arg)
  {
    msg_.summary_text = std::move(arg);
    return std::move(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_active_port
{
public:
  explicit Init_GpsReport_active_port(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_summary_text active_port(::radr_gps_msgs::msg::GpsReport::_active_port_type arg)
  {
    msg_.active_port = std::move(arg);
    return Init_GpsReport_summary_text(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_uart_connected
{
public:
  explicit Init_GpsReport_uart_connected(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_active_port uart_connected(::radr_gps_msgs::msg::GpsReport::_uart_connected_type arg)
  {
    msg_.uart_connected = std::move(arg);
    return Init_GpsReport_active_port(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_has_position
{
public:
  explicit Init_GpsReport_has_position(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_uart_connected has_position(::radr_gps_msgs::msg::GpsReport::_has_position_type arg)
  {
    msg_.has_position = std::move(arg);
    return Init_GpsReport_uart_connected(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_speed_kmh
{
public:
  explicit Init_GpsReport_speed_kmh(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_has_position speed_kmh(::radr_gps_msgs::msg::GpsReport::_speed_kmh_type arg)
  {
    msg_.speed_kmh = std::move(arg);
    return Init_GpsReport_has_position(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_course_true
{
public:
  explicit Init_GpsReport_course_true(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_speed_kmh course_true(::radr_gps_msgs::msg::GpsReport::_course_true_type arg)
  {
    msg_.course_true = std::move(arg);
    return Init_GpsReport_speed_kmh(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_speed_kn
{
public:
  explicit Init_GpsReport_speed_kn(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_course_true speed_kn(::radr_gps_msgs::msg::GpsReport::_speed_kn_type arg)
  {
    msg_.speed_kn = std::move(arg);
    return Init_GpsReport_course_true(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_sats_in_view
{
public:
  explicit Init_GpsReport_sats_in_view(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_speed_kn sats_in_view(::radr_gps_msgs::msg::GpsReport::_sats_in_view_type arg)
  {
    msg_.sats_in_view = std::move(arg);
    return Init_GpsReport_speed_kn(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_sats_used
{
public:
  explicit Init_GpsReport_sats_used(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_sats_in_view sats_used(::radr_gps_msgs::msg::GpsReport::_sats_used_type arg)
  {
    msg_.sats_used = std::move(arg);
    return Init_GpsReport_sats_in_view(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_hdop
{
public:
  explicit Init_GpsReport_hdop(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_sats_used hdop(::radr_gps_msgs::msg::GpsReport::_hdop_type arg)
  {
    msg_.hdop = std::move(arg);
    return Init_GpsReport_sats_used(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_altitude_msl
{
public:
  explicit Init_GpsReport_altitude_msl(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_hdop altitude_msl(::radr_gps_msgs::msg::GpsReport::_altitude_msl_type arg)
  {
    msg_.altitude_msl = std::move(arg);
    return Init_GpsReport_hdop(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_longitude
{
public:
  explicit Init_GpsReport_longitude(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_altitude_msl longitude(::radr_gps_msgs::msg::GpsReport::_longitude_type arg)
  {
    msg_.longitude = std::move(arg);
    return Init_GpsReport_altitude_msl(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_latitude
{
public:
  explicit Init_GpsReport_latitude(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_longitude latitude(::radr_gps_msgs::msg::GpsReport::_latitude_type arg)
  {
    msg_.latitude = std::move(arg);
    return Init_GpsReport_longitude(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_gga_fix_name
{
public:
  explicit Init_GpsReport_gga_fix_name(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_latitude gga_fix_name(::radr_gps_msgs::msg::GpsReport::_gga_fix_name_type arg)
  {
    msg_.gga_fix_name = std::move(arg);
    return Init_GpsReport_latitude(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_gga_fix_code
{
public:
  explicit Init_GpsReport_gga_fix_code(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_gga_fix_name gga_fix_code(::radr_gps_msgs::msg::GpsReport::_gga_fix_code_type arg)
  {
    msg_.gga_fix_code = std::move(arg);
    return Init_GpsReport_gga_fix_name(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_rmc_valid
{
public:
  explicit Init_GpsReport_rmc_valid(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_gga_fix_code rmc_valid(::radr_gps_msgs::msg::GpsReport::_rmc_valid_type arg)
  {
    msg_.rmc_valid = std::move(arg);
    return Init_GpsReport_gga_fix_code(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_date_ddmmyy
{
public:
  explicit Init_GpsReport_date_ddmmyy(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_rmc_valid date_ddmmyy(::radr_gps_msgs::msg::GpsReport::_date_ddmmyy_type arg)
  {
    msg_.date_ddmmyy = std::move(arg);
    return Init_GpsReport_rmc_valid(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_time_utc
{
public:
  explicit Init_GpsReport_time_utc(::radr_gps_msgs::msg::GpsReport & msg)
  : msg_(msg)
  {}
  Init_GpsReport_date_ddmmyy time_utc(::radr_gps_msgs::msg::GpsReport::_time_utc_type arg)
  {
    msg_.time_utc = std::move(arg);
    return Init_GpsReport_date_ddmmyy(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

class Init_GpsReport_header
{
public:
  Init_GpsReport_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GpsReport_time_utc header(::radr_gps_msgs::msg::GpsReport::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_GpsReport_time_utc(msg_);
  }

private:
  ::radr_gps_msgs::msg::GpsReport msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::radr_gps_msgs::msg::GpsReport>()
{
  return radr_gps_msgs::msg::builder::Init_GpsReport_header();
}

}  // namespace radr_gps_msgs

#endif  // RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__BUILDER_HPP_
