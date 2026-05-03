#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to radr_gps_msgs__msg__GpsReport
/// Parsed GPS summary (aligned with gps_parsed_live GpsDisplayState / as_lines).

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GpsReport {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub time_utc: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub date_ddmmyy: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rmc_valid: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gga_fix_code: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gga_fix_name: std::string::String,


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
    pub hdop: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sats_used: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sats_in_view: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub speed_kn: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub course_true: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub speed_kmh: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub has_position: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub uart_connected: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub active_port: std::string::String,

    /// Multi-line human-readable block (same shape as gps_parsed_live as_lines)
    pub summary_text: std::string::String,

}



impl Default for GpsReport {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::GpsReport::default())
  }
}

impl rosidl_runtime_rs::Message for GpsReport {
  type RmwMsg = super::msg::rmw::GpsReport;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        time_utc: msg.time_utc.as_str().into(),
        date_ddmmyy: msg.date_ddmmyy.as_str().into(),
        rmc_valid: msg.rmc_valid,
        gga_fix_code: msg.gga_fix_code.as_str().into(),
        gga_fix_name: msg.gga_fix_name.as_str().into(),
        latitude: msg.latitude,
        longitude: msg.longitude,
        altitude_msl: msg.altitude_msl,
        hdop: msg.hdop.as_str().into(),
        sats_used: msg.sats_used.as_str().into(),
        sats_in_view: msg.sats_in_view.as_str().into(),
        speed_kn: msg.speed_kn.as_str().into(),
        course_true: msg.course_true.as_str().into(),
        speed_kmh: msg.speed_kmh.as_str().into(),
        has_position: msg.has_position,
        uart_connected: msg.uart_connected,
        active_port: msg.active_port.as_str().into(),
        summary_text: msg.summary_text.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        time_utc: msg.time_utc.as_str().into(),
        date_ddmmyy: msg.date_ddmmyy.as_str().into(),
      rmc_valid: msg.rmc_valid,
        gga_fix_code: msg.gga_fix_code.as_str().into(),
        gga_fix_name: msg.gga_fix_name.as_str().into(),
      latitude: msg.latitude,
      longitude: msg.longitude,
      altitude_msl: msg.altitude_msl,
        hdop: msg.hdop.as_str().into(),
        sats_used: msg.sats_used.as_str().into(),
        sats_in_view: msg.sats_in_view.as_str().into(),
        speed_kn: msg.speed_kn.as_str().into(),
        course_true: msg.course_true.as_str().into(),
        speed_kmh: msg.speed_kmh.as_str().into(),
      has_position: msg.has_position,
      uart_connected: msg.uart_connected,
        active_port: msg.active_port.as_str().into(),
        summary_text: msg.summary_text.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      time_utc: msg.time_utc.to_string(),
      date_ddmmyy: msg.date_ddmmyy.to_string(),
      rmc_valid: msg.rmc_valid,
      gga_fix_code: msg.gga_fix_code.to_string(),
      gga_fix_name: msg.gga_fix_name.to_string(),
      latitude: msg.latitude,
      longitude: msg.longitude,
      altitude_msl: msg.altitude_msl,
      hdop: msg.hdop.to_string(),
      sats_used: msg.sats_used.to_string(),
      sats_in_view: msg.sats_in_view.to_string(),
      speed_kn: msg.speed_kn.to_string(),
      course_true: msg.course_true.to_string(),
      speed_kmh: msg.speed_kmh.to_string(),
      has_position: msg.has_position,
      uart_connected: msg.uart_connected,
      active_port: msg.active_port.to_string(),
      summary_text: msg.summary_text.to_string(),
    }
  }
}


