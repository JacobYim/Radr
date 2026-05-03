// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from radr_gps_msgs:msg/GpsReport.idl
// generated code does not contain a copyright notice

#ifndef RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__STRUCT_HPP_
#define RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__radr_gps_msgs__msg__GpsReport __attribute__((deprecated))
#else
# define DEPRECATED__radr_gps_msgs__msg__GpsReport __declspec(deprecated)
#endif

namespace radr_gps_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct GpsReport_
{
  using Type = GpsReport_<ContainerAllocator>;

  explicit GpsReport_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->time_utc = "";
      this->date_ddmmyy = "";
      this->rmc_valid = false;
      this->gga_fix_code = "";
      this->gga_fix_name = "";
      this->latitude = 0.0;
      this->longitude = 0.0;
      this->altitude_msl = 0.0;
      this->hdop = "";
      this->sats_used = "";
      this->sats_in_view = "";
      this->speed_kn = "";
      this->course_true = "";
      this->speed_kmh = "";
      this->has_position = false;
      this->uart_connected = false;
      this->active_port = "";
      this->summary_text = "";
    }
  }

  explicit GpsReport_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    time_utc(_alloc),
    date_ddmmyy(_alloc),
    gga_fix_code(_alloc),
    gga_fix_name(_alloc),
    hdop(_alloc),
    sats_used(_alloc),
    sats_in_view(_alloc),
    speed_kn(_alloc),
    course_true(_alloc),
    speed_kmh(_alloc),
    active_port(_alloc),
    summary_text(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->time_utc = "";
      this->date_ddmmyy = "";
      this->rmc_valid = false;
      this->gga_fix_code = "";
      this->gga_fix_name = "";
      this->latitude = 0.0;
      this->longitude = 0.0;
      this->altitude_msl = 0.0;
      this->hdop = "";
      this->sats_used = "";
      this->sats_in_view = "";
      this->speed_kn = "";
      this->course_true = "";
      this->speed_kmh = "";
      this->has_position = false;
      this->uart_connected = false;
      this->active_port = "";
      this->summary_text = "";
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _time_utc_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _time_utc_type time_utc;
  using _date_ddmmyy_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _date_ddmmyy_type date_ddmmyy;
  using _rmc_valid_type =
    bool;
  _rmc_valid_type rmc_valid;
  using _gga_fix_code_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _gga_fix_code_type gga_fix_code;
  using _gga_fix_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _gga_fix_name_type gga_fix_name;
  using _latitude_type =
    double;
  _latitude_type latitude;
  using _longitude_type =
    double;
  _longitude_type longitude;
  using _altitude_msl_type =
    double;
  _altitude_msl_type altitude_msl;
  using _hdop_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _hdop_type hdop;
  using _sats_used_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _sats_used_type sats_used;
  using _sats_in_view_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _sats_in_view_type sats_in_view;
  using _speed_kn_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _speed_kn_type speed_kn;
  using _course_true_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _course_true_type course_true;
  using _speed_kmh_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _speed_kmh_type speed_kmh;
  using _has_position_type =
    bool;
  _has_position_type has_position;
  using _uart_connected_type =
    bool;
  _uart_connected_type uart_connected;
  using _active_port_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _active_port_type active_port;
  using _summary_text_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _summary_text_type summary_text;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__time_utc(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->time_utc = _arg;
    return *this;
  }
  Type & set__date_ddmmyy(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->date_ddmmyy = _arg;
    return *this;
  }
  Type & set__rmc_valid(
    const bool & _arg)
  {
    this->rmc_valid = _arg;
    return *this;
  }
  Type & set__gga_fix_code(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->gga_fix_code = _arg;
    return *this;
  }
  Type & set__gga_fix_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->gga_fix_name = _arg;
    return *this;
  }
  Type & set__latitude(
    const double & _arg)
  {
    this->latitude = _arg;
    return *this;
  }
  Type & set__longitude(
    const double & _arg)
  {
    this->longitude = _arg;
    return *this;
  }
  Type & set__altitude_msl(
    const double & _arg)
  {
    this->altitude_msl = _arg;
    return *this;
  }
  Type & set__hdop(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->hdop = _arg;
    return *this;
  }
  Type & set__sats_used(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->sats_used = _arg;
    return *this;
  }
  Type & set__sats_in_view(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->sats_in_view = _arg;
    return *this;
  }
  Type & set__speed_kn(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->speed_kn = _arg;
    return *this;
  }
  Type & set__course_true(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->course_true = _arg;
    return *this;
  }
  Type & set__speed_kmh(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->speed_kmh = _arg;
    return *this;
  }
  Type & set__has_position(
    const bool & _arg)
  {
    this->has_position = _arg;
    return *this;
  }
  Type & set__uart_connected(
    const bool & _arg)
  {
    this->uart_connected = _arg;
    return *this;
  }
  Type & set__active_port(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->active_port = _arg;
    return *this;
  }
  Type & set__summary_text(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->summary_text = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    radr_gps_msgs::msg::GpsReport_<ContainerAllocator> *;
  using ConstRawPtr =
    const radr_gps_msgs::msg::GpsReport_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<radr_gps_msgs::msg::GpsReport_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<radr_gps_msgs::msg::GpsReport_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      radr_gps_msgs::msg::GpsReport_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<radr_gps_msgs::msg::GpsReport_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      radr_gps_msgs::msg::GpsReport_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<radr_gps_msgs::msg::GpsReport_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<radr_gps_msgs::msg::GpsReport_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<radr_gps_msgs::msg::GpsReport_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__radr_gps_msgs__msg__GpsReport
    std::shared_ptr<radr_gps_msgs::msg::GpsReport_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__radr_gps_msgs__msg__GpsReport
    std::shared_ptr<radr_gps_msgs::msg::GpsReport_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GpsReport_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->time_utc != other.time_utc) {
      return false;
    }
    if (this->date_ddmmyy != other.date_ddmmyy) {
      return false;
    }
    if (this->rmc_valid != other.rmc_valid) {
      return false;
    }
    if (this->gga_fix_code != other.gga_fix_code) {
      return false;
    }
    if (this->gga_fix_name != other.gga_fix_name) {
      return false;
    }
    if (this->latitude != other.latitude) {
      return false;
    }
    if (this->longitude != other.longitude) {
      return false;
    }
    if (this->altitude_msl != other.altitude_msl) {
      return false;
    }
    if (this->hdop != other.hdop) {
      return false;
    }
    if (this->sats_used != other.sats_used) {
      return false;
    }
    if (this->sats_in_view != other.sats_in_view) {
      return false;
    }
    if (this->speed_kn != other.speed_kn) {
      return false;
    }
    if (this->course_true != other.course_true) {
      return false;
    }
    if (this->speed_kmh != other.speed_kmh) {
      return false;
    }
    if (this->has_position != other.has_position) {
      return false;
    }
    if (this->uart_connected != other.uart_connected) {
      return false;
    }
    if (this->active_port != other.active_port) {
      return false;
    }
    if (this->summary_text != other.summary_text) {
      return false;
    }
    return true;
  }
  bool operator!=(const GpsReport_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GpsReport_

// alias to use template instance with default allocator
using GpsReport =
  radr_gps_msgs::msg::GpsReport_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace radr_gps_msgs

#endif  // RADR_GPS_MSGS__MSG__DETAIL__GPS_REPORT__STRUCT_HPP_
