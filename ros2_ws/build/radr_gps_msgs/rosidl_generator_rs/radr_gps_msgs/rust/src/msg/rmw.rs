#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "radr_gps_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__radr_gps_msgs__msg__GpsReport() -> *const std::ffi::c_void;
}

#[link(name = "radr_gps_msgs__rosidl_generator_c")]
extern "C" {
    fn radr_gps_msgs__msg__GpsReport__init(msg: *mut GpsReport) -> bool;
    fn radr_gps_msgs__msg__GpsReport__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GpsReport>, size: usize) -> bool;
    fn radr_gps_msgs__msg__GpsReport__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GpsReport>);
    fn radr_gps_msgs__msg__GpsReport__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GpsReport>, out_seq: *mut rosidl_runtime_rs::Sequence<GpsReport>) -> bool;
}

// Corresponds to radr_gps_msgs__msg__GpsReport
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Parsed GPS summary (aligned with gps_parsed_live GpsDisplayState / as_lines).

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GpsReport {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub time_utc: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub date_ddmmyy: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rmc_valid: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gga_fix_code: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gga_fix_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub latitude: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub longitude: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub altitude_msl: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub hdop: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sats_used: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sats_in_view: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub speed_kn: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub course_true: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub speed_kmh: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub has_position: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub uart_connected: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub active_port: rosidl_runtime_rs::String,

    /// Multi-line human-readable block (same shape as gps_parsed_live as_lines)
    pub summary_text: rosidl_runtime_rs::String,

}



impl Default for GpsReport {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !radr_gps_msgs__msg__GpsReport__init(&mut msg as *mut _) {
        panic!("Call to radr_gps_msgs__msg__GpsReport__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GpsReport {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { radr_gps_msgs__msg__GpsReport__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { radr_gps_msgs__msg__GpsReport__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { radr_gps_msgs__msg__GpsReport__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GpsReport {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GpsReport where Self: Sized {
  const TYPE_NAME: &'static str = "radr_gps_msgs/msg/GpsReport";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__radr_gps_msgs__msg__GpsReport() }
  }
}


