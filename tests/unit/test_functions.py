import struct

import pytest

try:
    # Mock has been added to stdlib in Python 3.3.
    from unittest.mock import MagicMock, call
except ImportError:
    from mock import MagicMock, call

from umodbus.exceptions import (AcknowledgeError, GatewayPathUnavailableError,
                                GatewayTargetDeviceFailedToRespondError,
                                IllegalDataAddressError, IllegalDataValueError,
                                IllegalFunctionError, MemoryParityError,
                                ServerDeviceBusyError,
                                ServerDeviceFailureError)
from umodbus.functions import (ReadCoils, ReadDiscreteInputs,
                               ReadHoldingRegisters, ReadInputRegisters,
                               WriteMultipleCoils, WriteMultipleRegisters,
                               WriteSingleCoil, WriteSingleRegister,
                               create_function_from_request_pdu,
                               create_function_from_response_pdu,
                               dummy_function)
from umodbus.route import Map


@pytest.fixture
def read_coils():
    instance = ReadCoils()
    instance.starting_address = 100
    instance.quantity = 3

    return instance


@pytest.fixture
def read_discrete_inputs():
    instance = ReadDiscreteInputs()
    instance.starting_address = 0
    instance.quantity = 2

    return instance


@pytest.fixture
def read_holding_registers():
    instance = ReadHoldingRegisters()
    instance.starting_address = 100
    instance.quantity = 4

    return instance


@pytest.fixture
def read_input_registers():
    instance = ReadInputRegisters()
    instance.starting_address = 50
    instance.quantity = 2

    return instance


@pytest.fixture
def write_single_coil():
    instance = WriteSingleCoil()
    instance.address = 100
    instance.value = 1

    return instance


@pytest.fixture
def write_single_register():
    instance = WriteSingleRegister()
    instance.address = 200
    instance.value = 18

    return instance


@pytest.fixture
def write_multiple_coils():
    instance = WriteMultipleCoils()
    instance.starting_address = 100
    instance.values = [1, 0]

    return instance


@pytest.fixture
def write_multiple_registers():
    instance = WriteMultipleRegisters()
    instance.starting_address = 50
    instance.values = [1337, 15, 128]

    return instance


@pytest.fixture
def route_map():
    return Map()


@pytest.mark.parametrize('pdu,cls', [
    (b'\x01\x00d\x00\x03', ReadCoils),
    (b'\x02\x00d\x00\x03', ReadDiscreteInputs),
    (b'\x03\x00d\x00\x03', ReadHoldingRegisters),
    (b'\x04\x00d\x00\x03', ReadInputRegisters),
    (b'\x05\x00d\x00\x00', WriteSingleCoil),
    (b'\x06\x00d\x00\x00', WriteSingleRegister),
])
def test_create_function_from_request_pdu(pdu, cls):
    assert isinstance(create_function_from_request_pdu(pdu), cls)


@pytest.mark.parametrize('error_code, exception_class', [
    (1, IllegalFunctionError),
    (2, IllegalDataAddressError),
    (3, IllegalDataValueError),
    (4, ServerDeviceFailureError),
    (5, AcknowledgeError),
    (6, ServerDeviceBusyError),
    (8, MemoryParityError),
    (10, GatewayPathUnavailableError),
    (11, GatewayTargetDeviceFailedToRespondError),
])
def test_create_from_response_pdu_raising_exception(error_code,
                                                    exception_class):
    """ Test if correct exception is raied when response PDU contains error
    response.
    """
    resp_pdu = struct.pack('>BB', 81, error_code)

    with pytest.raises(exception_class):
        create_function_from_response_pdu(resp_pdu)


def test_read_discrete_inputs_request_pdu(read_discrete_inputs):
    instance = ReadDiscreteInputs.create_from_request_pdu(read_discrete_inputs.request_pdu)  # NOQA
    assert instance.starting_address == 0
    assert instance.quantity == 2


def test_read_discrete_inputs_response_pdu(read_discrete_inputs):
    response_pdu = read_discrete_inputs.create_response_pdu([1, 0])
    instance = ReadDiscreteInputs.create_from_response_pdu(response_pdu, read_discrete_inputs.request_pdu)  # NOQA

    assert instance.data == [1, 0]


def test_read_holding_registers_class_attributes():
    assert ReadHoldingRegisters.function_code == 3
    assert ReadHoldingRegisters.max_quantity == 125


def test_read_holding_registers_with_invalid_attributes(read_holding_registers):  # NOQA
    with pytest.raises(IllegalDataValueError):
        read_holding_registers.quantity = 126


def test_read_holding_registers_request_pdu(read_holding_registers):
    instance = ReadHoldingRegisters.create_from_request_pdu(read_holding_registers.request_pdu)  # NOQA

    assert instance.starting_address == 100
    assert instance.quantity == 4


def test_read_holding_registers_response_pdu(read_holding_registers):
    response_pdu =\
        read_holding_registers.create_response_pdu([1337, 17, 21, 18])

    instance = ReadHoldingRegisters.create_from_response_pdu(response_pdu, read_holding_registers.request_pdu)  # NOQA

    assert instance.data == [1337, 17, 21, 18]


def test_read_input_registers_class_attributes():
    assert ReadInputRegisters.function_code == 4
    assert ReadInputRegisters.max_quantity == 125


def test_read_input_registers_with_invalid_attributes(read_input_registers):  # NOQA
    with pytest.raises(IllegalDataValueError):
        read_input_registers.quantity = 126


def test_read_input_registers_request_pdu(read_input_registers):
    instance = ReadInputRegisters.create_from_request_pdu(read_input_registers.request_pdu)  # NOQA

    assert instance.starting_address == 50
    assert instance.quantity == 2


def test_read_input_registers_response_pdu(read_input_registers):
    response_pdu = read_input_registers.create_response_pdu([994, 1100])
    instance = ReadInputRegisters.create_from_response_pdu(response_pdu, read_input_registers.request_pdu)  # NOQA

    assert instance.data == [994, 1100]


def test_write_single_coil_class_attributes():
    assert WriteSingleCoil.function_code == 5


def test_write_single_coil_with_invalid_attributes(write_single_coil):
    with pytest.raises(IllegalDataValueError):
        write_single_coil.value = 5


def test_write_single_coil_request_pdu(write_single_coil):
    instance = WriteSingleCoil.create_from_request_pdu(write_single_coil.request_pdu)  # NOQA

    assert instance.address == 100
    assert instance.value == 1


def test_write_single_coil_response_pdu(write_single_coil):
    response_pdu = write_single_coil.create_response_pdu()
    instance = WriteSingleCoil.create_from_response_pdu(response_pdu)

    assert instance.address == 100
    assert instance.data == 1


def test_write_single_registers_class_attributes():
    assert WriteSingleRegister.function_code == 6


def test_write_single_register_with_invalid_attributes(write_single_register):
    with pytest.raises(IllegalDataValueError):
        write_single_register.value = -1


def test_write_single_register_request_pdu(write_single_register):
    instance = WriteSingleRegister.create_from_request_pdu(write_single_register.request_pdu)  # NOQA

    assert instance.address == 200
    assert instance.value == 18


def test_write_single_register_response_pdu(write_single_register):
    response_pdu = write_single_register.create_response_pdu()
    instance = WriteSingleRegister.create_from_response_pdu(response_pdu)

    assert instance.address == 200
    assert instance.data == 18


def test_write_multiple_coils_class_attributes():
    WriteMultipleCoils.function_code == 15


def test_write_multiple_coils_invalid_attributes(write_multiple_coils):
    with pytest.raises(IllegalDataValueError):
        write_multiple_coils.values = []

    with pytest.raises(IllegalDataValueError):
        write_multiple_coils.values = [5]


def test_write_multiple_coils_request_pdu(write_multiple_coils):
    instance = WriteMultipleCoils.create_from_request_pdu(write_multiple_coils.request_pdu)  # NOQA

    assert instance.starting_address == 100
    assert instance.values == [1, 0]


def test_write_multiple_coils_response_pdu(write_multiple_coils):
    response_pdu = write_multiple_coils.create_response_pdu()
    instance = WriteMultipleCoils.create_from_response_pdu(response_pdu)

    assert instance.starting_address == 100
    assert instance.data == 2


def test_write_multiple_registers_class_attributes():
    WriteMultipleRegisters.function_code == 16


def test_write_multiple_registers_invalid_attributes(write_multiple_registers):
    with pytest.raises(IllegalDataValueError):
        write_multiple_registers.values = []

    with pytest.raises(IllegalDataValueError):
        write_multiple_registers.values = [-1]


def test_write_multiple_registers_request_pdu(write_multiple_registers):
    instance = WriteMultipleRegisters.create_from_request_pdu(write_multiple_registers.request_pdu)  # NOQA

    assert instance.starting_address == 50
    assert instance.values == [1337, 15, 128]


def test_write_multiple_registers_response_pdu(write_multiple_registers):
    response_pdu = write_multiple_registers.create_response_pdu()
    instance = WriteMultipleRegisters.create_from_response_pdu(response_pdu)

    assert instance.starting_address == 50
    assert instance.data == 3


def test_create_function_from_response_pdu():
    read_coils = ReadCoils()
    read_coils.starting_address = 1
    read_coils.quantity = 9

    req_pdu = read_coils.request_pdu
    resp_pdu = struct.pack('>BBB', 1, 1, 3)

    assert isinstance(create_function_from_response_pdu(resp_pdu, req_pdu),
                      ReadCoils)


def test_dumy():
    assert dummy_function(1)