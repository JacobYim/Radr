# generated from rosidl_generator_py/resource/_idl.py.em
# with input from radr_gps_msgs:msg/GpsReport.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_GpsReport(type):
    """Metaclass of message 'GpsReport'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('radr_gps_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'radr_gps_msgs.msg.GpsReport')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__gps_report
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__gps_report
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__gps_report
            cls._TYPE_SUPPORT = module.type_support_msg__msg__gps_report
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__gps_report

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GpsReport(metaclass=Metaclass_GpsReport):
    """Message class 'GpsReport'."""

    __slots__ = [
        '_header',
        '_time_utc',
        '_date_ddmmyy',
        '_rmc_valid',
        '_gga_fix_code',
        '_gga_fix_name',
        '_latitude',
        '_longitude',
        '_altitude_msl',
        '_hdop',
        '_sats_used',
        '_sats_in_view',
        '_speed_kn',
        '_course_true',
        '_speed_kmh',
        '_has_position',
        '_uart_connected',
        '_active_port',
        '_summary_text',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'time_utc': 'string',
        'date_ddmmyy': 'string',
        'rmc_valid': 'boolean',
        'gga_fix_code': 'string',
        'gga_fix_name': 'string',
        'latitude': 'double',
        'longitude': 'double',
        'altitude_msl': 'double',
        'hdop': 'string',
        'sats_used': 'string',
        'sats_in_view': 'string',
        'speed_kn': 'string',
        'course_true': 'string',
        'speed_kmh': 'string',
        'has_position': 'boolean',
        'uart_connected': 'boolean',
        'active_port': 'string',
        'summary_text': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.time_utc = kwargs.get('time_utc', str())
        self.date_ddmmyy = kwargs.get('date_ddmmyy', str())
        self.rmc_valid = kwargs.get('rmc_valid', bool())
        self.gga_fix_code = kwargs.get('gga_fix_code', str())
        self.gga_fix_name = kwargs.get('gga_fix_name', str())
        self.latitude = kwargs.get('latitude', float())
        self.longitude = kwargs.get('longitude', float())
        self.altitude_msl = kwargs.get('altitude_msl', float())
        self.hdop = kwargs.get('hdop', str())
        self.sats_used = kwargs.get('sats_used', str())
        self.sats_in_view = kwargs.get('sats_in_view', str())
        self.speed_kn = kwargs.get('speed_kn', str())
        self.course_true = kwargs.get('course_true', str())
        self.speed_kmh = kwargs.get('speed_kmh', str())
        self.has_position = kwargs.get('has_position', bool())
        self.uart_connected = kwargs.get('uart_connected', bool())
        self.active_port = kwargs.get('active_port', str())
        self.summary_text = kwargs.get('summary_text', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.header != other.header:
            return False
        if self.time_utc != other.time_utc:
            return False
        if self.date_ddmmyy != other.date_ddmmyy:
            return False
        if self.rmc_valid != other.rmc_valid:
            return False
        if self.gga_fix_code != other.gga_fix_code:
            return False
        if self.gga_fix_name != other.gga_fix_name:
            return False
        if self.latitude != other.latitude:
            return False
        if self.longitude != other.longitude:
            return False
        if self.altitude_msl != other.altitude_msl:
            return False
        if self.hdop != other.hdop:
            return False
        if self.sats_used != other.sats_used:
            return False
        if self.sats_in_view != other.sats_in_view:
            return False
        if self.speed_kn != other.speed_kn:
            return False
        if self.course_true != other.course_true:
            return False
        if self.speed_kmh != other.speed_kmh:
            return False
        if self.has_position != other.has_position:
            return False
        if self.uart_connected != other.uart_connected:
            return False
        if self.active_port != other.active_port:
            return False
        if self.summary_text != other.summary_text:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def time_utc(self):
        """Message field 'time_utc'."""
        return self._time_utc

    @time_utc.setter
    def time_utc(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'time_utc' field must be of type 'str'"
        self._time_utc = value

    @builtins.property
    def date_ddmmyy(self):
        """Message field 'date_ddmmyy'."""
        return self._date_ddmmyy

    @date_ddmmyy.setter
    def date_ddmmyy(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'date_ddmmyy' field must be of type 'str'"
        self._date_ddmmyy = value

    @builtins.property
    def rmc_valid(self):
        """Message field 'rmc_valid'."""
        return self._rmc_valid

    @rmc_valid.setter
    def rmc_valid(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'rmc_valid' field must be of type 'bool'"
        self._rmc_valid = value

    @builtins.property
    def gga_fix_code(self):
        """Message field 'gga_fix_code'."""
        return self._gga_fix_code

    @gga_fix_code.setter
    def gga_fix_code(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'gga_fix_code' field must be of type 'str'"
        self._gga_fix_code = value

    @builtins.property
    def gga_fix_name(self):
        """Message field 'gga_fix_name'."""
        return self._gga_fix_name

    @gga_fix_name.setter
    def gga_fix_name(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'gga_fix_name' field must be of type 'str'"
        self._gga_fix_name = value

    @builtins.property
    def latitude(self):
        """Message field 'latitude'."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'latitude' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'latitude' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._latitude = value

    @builtins.property
    def longitude(self):
        """Message field 'longitude'."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'longitude' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'longitude' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._longitude = value

    @builtins.property
    def altitude_msl(self):
        """Message field 'altitude_msl'."""
        return self._altitude_msl

    @altitude_msl.setter
    def altitude_msl(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'altitude_msl' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'altitude_msl' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._altitude_msl = value

    @builtins.property
    def hdop(self):
        """Message field 'hdop'."""
        return self._hdop

    @hdop.setter
    def hdop(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'hdop' field must be of type 'str'"
        self._hdop = value

    @builtins.property
    def sats_used(self):
        """Message field 'sats_used'."""
        return self._sats_used

    @sats_used.setter
    def sats_used(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'sats_used' field must be of type 'str'"
        self._sats_used = value

    @builtins.property
    def sats_in_view(self):
        """Message field 'sats_in_view'."""
        return self._sats_in_view

    @sats_in_view.setter
    def sats_in_view(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'sats_in_view' field must be of type 'str'"
        self._sats_in_view = value

    @builtins.property
    def speed_kn(self):
        """Message field 'speed_kn'."""
        return self._speed_kn

    @speed_kn.setter
    def speed_kn(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'speed_kn' field must be of type 'str'"
        self._speed_kn = value

    @builtins.property
    def course_true(self):
        """Message field 'course_true'."""
        return self._course_true

    @course_true.setter
    def course_true(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'course_true' field must be of type 'str'"
        self._course_true = value

    @builtins.property
    def speed_kmh(self):
        """Message field 'speed_kmh'."""
        return self._speed_kmh

    @speed_kmh.setter
    def speed_kmh(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'speed_kmh' field must be of type 'str'"
        self._speed_kmh = value

    @builtins.property
    def has_position(self):
        """Message field 'has_position'."""
        return self._has_position

    @has_position.setter
    def has_position(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'has_position' field must be of type 'bool'"
        self._has_position = value

    @builtins.property
    def uart_connected(self):
        """Message field 'uart_connected'."""
        return self._uart_connected

    @uart_connected.setter
    def uart_connected(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'uart_connected' field must be of type 'bool'"
        self._uart_connected = value

    @builtins.property
    def active_port(self):
        """Message field 'active_port'."""
        return self._active_port

    @active_port.setter
    def active_port(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'active_port' field must be of type 'str'"
        self._active_port = value

    @builtins.property
    def summary_text(self):
        """Message field 'summary_text'."""
        return self._summary_text

    @summary_text.setter
    def summary_text(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'summary_text' field must be of type 'str'"
        self._summary_text = value
