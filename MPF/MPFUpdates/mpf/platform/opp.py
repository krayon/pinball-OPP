"""Contains the hardware interface and drivers for the Open Pinball Project
platform hardware, including the solenoid, input, incandescent, and neopixel
boards.

"""

# opp.py
# Mission Pinball Framework
# Written by Hugh Spahr
# Released under the MIT License. (See license info at the end of this file.)

# Documentation and more info at http://missionpinball.com/mpf

import logging
import time
import sys
import threading
import Queue
import traceback
import io
from copy import deepcopy

from mpf.system.platform import Platform
from mpf.system.config import Config
from mpf.system.utility_functions import Util

try:
    import serial
    serial_imported = True
except:
    serial_imported = False

# Minimum firmware versions needed for this module
MIN_FW = 0x00000100
BAD_FW_VERSION = 0x01020304

class OppRs232Intf:
    GET_SER_NUM_CMD     = '\x00'
    GET_PROD_ID_CMD     = '\x01'
    GET_GET_VERS_CMD    = '\x02'
    GET_SET_SER_NUM_CMD = '\x03'
    RESET_CMD           = '\x04'
    GO_BOOT_CMD         = '\x05'
    CFG_SOL_CMD         = '\x06'
    KICK_SOL_CMD        = '\x07'
    READ_GEN2_INP_CMD   = '\x08'
    CFG_INP_CMD         = '\x09'
    SAVE_CFG_CMD        = '\x0b'
    ERASE_CFG_CMD       = '\x0c'
    GET_GEN2_CFG        = '\x0d'
    SET_GEN2_CFG        = '\x0e'
    CHNG_NEO_CMD        = '\x0f'
    CHNG_NEO_COLOR      = '\x10'
    CHNG_NEO_COLOR_TBL  = '\x11'
    SET_NEO_COLOR_TBL   = '\x12'
    INCAND_CMD          = '\x13'

    INV_CMD             = '\xf0'
    ILLEGAL_CMD         = '\xfe'
    EOM_CMD             = '\xff'

    CARD_ID_TYPE_MASK   = '\xf0'
    CARD_ID_SOL_CARD    = '\x00'
    CARD_ID_INP_CARD    = '\x10'
    CARD_ID_GEN2_CARD   = '\x20'

    NUM_G2_WING_PER_BRD = 4
    WING_SOL            = '\x01'
    WING_INP            = '\x02'
    WING_INCAND         = '\x03'
    WING_SW_MATRIX_OUT  = '\x04'
    WING_SW_MATRIX_IN   = '\x05'
    WING_NEO            = '\x06'

    NUM_G2_INP_PER_BRD  = 32
    CFG_INP_STATE       = '\x00'
    CFG_INP_FALL_EDGE   = '\x01'
    CFG_INP_RISE_EDGE   = '\x02'

    NUM_G2_SOL_PER_BRD  = 16
    CFG_SOL_USE_SWITCH  = '\x01'
    CFG_SOL_AUTO_CLR    = '\x02'

    NUM_COLOR_TBL       = 32

    INCAND_ROT_LEFT     = '\x00'
    INCAND_ROT_RIGHT    = '\x01'
    INCAND_LED_ON       = '\x02'
    INCAND_LED_OFF      = '\x03'
    INCAND_BLINK_SLOW   = '\x04'
    INCAND_BLINK_FAST   = '\x05'
    INCAND_BLINK_OFF    = '\x06'

    INCAND_SET_CMD          = '\x80'
    INCAND_SET_ON           = '\x01'
    INCAND_SET_BLINK_SLOW   = '\x02'
    INCAND_SET_BLINK_FAST   = '\x04'

    # Solenoid configuration constants
    CFG_BYTES_PER_SOL   = 3
    INIT_KICK_OFFSET    = 1
    DUTY_CYCLE_OFFSET   = 2
    CFG_SOL_USE_SWITCH  = '\x01'
    CFG_SOL_AUTO_CLR    = '\x02'
    CFG_SOL_DISABLE     = '\x00'

    CRC8_LOOKUP = \
        [ 0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15, 0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d, \
          0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65, 0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d, \
          0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5, 0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd, \
          0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85, 0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd, \
          0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2, 0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea, \
          0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2, 0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a, \
          0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32, 0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a, \
          0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42, 0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a, \
          0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c, 0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4, \
          0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec, 0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4, \
          0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c, 0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44, \
          0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c, 0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34, \
          0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b, 0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63, \
          0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b, 0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13, \
          0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb, 0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83, \
          0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb, 0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3 ]
    
    @staticmethod
    def calc_crc8_whole_msg(msgChars):
        crc8Byte = 0xff
        for indChar in msgChars:
            indInt = ord(indChar)
            crc8Byte = OppRs232Intf.CRC8_LOOKUP[crc8Byte ^ indInt];
        return (chr(crc8Byte))

    @staticmethod
    def calc_crc8_part_msg(msgChars, startIndex, numChars):
        crc8Byte = 0xff
        index = 0
        while index < numChars:
            indInt = ord(msgChars[startIndex + index])
            crc8Byte = OppRs232Intf.CRC8_LOOKUP[crc8Byte ^ indInt];
            index += 1
        return (chr(crc8Byte))

class HardwarePlatform(Platform):
    """Platform class for the OPP hardware.

    Args:
        machine: The main ``MachineController`` instance.

    """

    def __init__(self, machine):
        super(HardwarePlatform, self).__init__(machine)
        self.log = logging.getLogger('OPP')
        self.log.info("Configuring OPP hardware.")

        if not serial_imported:
            self.log.error('Could not import "pySerial". This is required for '
                           'the OPP platform interface')
            sys.exit()

        # ----------------------------------------------------------------------
        # Platform-specific hardware features. WARNING: Do not edit these. They
        # are based on what the OPP hardware can and cannot do.
        self.features['max_pulse'] = 255  # todo
        self.features['hw_timer'] = False
        self.features['hw_rule_coil_delay'] = False
        self.features['variable_recycle_time'] = False
        self.features['variable_debounce_time'] = False
        # Make the platform features available to everyone
        self.machine.config['platform'] = self.features
        # ----------------------------------------------------------------------

        self.hw_rules = dict()
        self.opp_connection = None
        self.opp_nodes = list()
        self.connection_threads = set()
        self.receive_queue = Queue.Queue()
        self.opp_incands = []
        self.incandDict = dict()
        self.opp_solenoid = []
        self.solDict = dict()
        self.opp_inputs = []
        self.inpDict = dict()
        self.inpAddrDict = dict()
        self.read_input_msg = OppRs232Intf.EOM_CMD
        self.opp_neopixels = []
        self.neoCardDict = dict()
        self.neoDict = dict()
        self.flag_led_tick_registered = False
        self.numGen2Brd = 0
        self.gen2AddrArr = []
        self.currInpData = []
        self.badCRC = 0
        self.oppFirmwareVers = []
        self.minVersion = 0xffffffff

        config_spec = '''
                    ports: list
                    baud: int|115200
                    config_number_format: string|hex
                    debug: boolean|False
                    '''

        self.config = Config.process_config(config_spec=config_spec,
                                            source=self.machine.config['opp'])

        self.machine_type = (
            self.machine.config['hardware']['driverboards'].lower())

        if self.machine_type == 'gen1':
            self.log.info("Configuring the original OPP boards")
            self.log.error("Original OPP boards not currently supported.")
            sys.exit()
        elif self.machine_type == 'gen2':
            self.log.info("Configuring the OPP Gen2 boards")
        else:
            self.log.error('Invalid driverboards type: %s', self.machine_type)
            sys.exit()

        # Only including responses that should be received
        self.opp_commands = {
            OppRs232Intf.INV_CMD: self.inv_resp,
            OppRs232Intf.EOM_CMD: self.eom_resp,
            OppRs232Intf.GET_GEN2_CFG: self.get_gen2_cfg_resp,
            OppRs232Intf.READ_GEN2_INP_CMD: self.read_gen2_inp_resp,
            OppRs232Intf.GET_GET_VERS_CMD: self.vers_resp,
            }

        self._connect_to_hardware()

        if 'config_number_format' not in self.machine.config['opp']:
            self.machine.config['opp']['config_number_format'] = 'int'

    def __repr__(self):
        return '<Platform.OPP>'

    def process_received_message(self, msg):
        """Sends an incoming message from the OPP hardware to the proper
        method for servicing.

        """

        if (len(msg) >= 1):
            if ((ord(msg[0]) >= ord(OppRs232Intf.CARD_ID_GEN2_CARD)) and 
                (ord(msg[0]) < (ord(OppRs232Intf.CARD_ID_GEN2_CARD) + 0x20))):
                if (len(msg) >= 2):
                    cmd = msg[1]
                else:
                    cmd = OppRs232Intf.ILLEGAL_CMD
            # Look for EOM or INV commands
            elif (msg[0] == OppRs232Intf.INV_CMD) or (msg[0] == OppRs232Intf.EOM_CMD):
                cmd = msg[0]
            else:
                cmd = OppRs232Intf.ILLEGAL_CMD
        else:
            # No messages received, fake an EOM
            cmd = OppRs232Intf.EOM_CMD

        # Can't use try since it swallows too many errors for now
        if cmd in self.opp_commands:
            self.opp_commands[cmd](msg)
        else:            
            hex_string = "".join(" 0x%02x" % ord(b) for b in msg)

            self.log.warning("Received unknown serial command?%s. (This is "
                             "very worrisome.)", "".join(" 0x%02x" % ord(b) for b in msg))
            
            # TODO: This means synchronization is lost.  Send EOM characters
            #  until they come back


    def _connect_to_hardware(self):
        # Connect to each port from the config. This procuess will cause the
        # connection threads to figure out which processor they've connected to
        # and to register themselves.
        for port in self.config['ports']:
            self.connection_threads.add(SerialCommunicator(machine=self.machine,
                platform=self, port=port, baud=self.config['baud'],
                send_queue=Queue.Queue(), receive_queue=self.receive_queue))

    def register_processor_connection(self, name, communicator):
        """Once a communication link has been established with one of the
        OPP boards, this method sets the communicator link.

        """

        self.opp_connection = communicator

    def update_incand(self):
        """Updates all the incandescents connected to OPP hardware. This is done
        once per game loop if changes have been made.

        It is currently assumed that the oversampling will guarantee proper communication
        with the boards.  If this does not end up being the case, this will be changed
        to update all the incandescents each loop.
        
        Note:  This could be made much more efficient by supporting a command
        that simply sets the state of all 32 of the LEDs as either on or off.

        """

        wholeMsg = []
        for incand in self.opp_incands:
            # Check if any changes have been made
            changes = incand.oldState ^ incand.newState
            justLit = changes & incand.newState
            if (justLit != 0):                
                # Turn on the bulbs that were just lit
                msg = []
                msg.append(incand.addr)
                msg.append(OppRs232Intf.INCAND_CMD)
                msg.append(OppRs232Intf.INCAND_LED_ON)
                msg.append(chr((justLit >> 24) & 0xff))
                msg.append(chr((justLit >> 16) & 0xff))
                msg.append(chr((justLit >> 8) & 0xff))
                msg.append(chr(justLit & 0xff))
                msg.append(OppRs232Intf.calc_crc8_whole_msg(msg))
                wholeMsg.extend(msg)

            justTurnedOff = changes & ~incand.newState
            if (justTurnedOff != 0):                
                # Turn off the bulbs that just changed to off
                msg = []
                msg.append(incand.addr)
                msg.append(OppRs232Intf.INCAND_CMD)
                msg.append(OppRs232Intf.INCAND_LED_OFF)
                msg.append(chr((justTurnedOff >> 24) & 0xff))
                msg.append(chr((justTurnedOff >> 16) & 0xff))
                msg.append(chr((justTurnedOff >> 8) & 0xff))
                msg.append(chr(justTurnedOff & 0xff))
                msg.append(OppRs232Intf.calc_crc8_whole_msg(msg))
                wholeMsg.extend(msg)

        wholeMsg.append(OppRs232Intf.EOM_CMD)
        sendCmd = ''.join(wholeMsg)

        self.opp_connection.send(sendCmd)

    def get_hw_switch_states(self):
        hw_states = dict()
        for oppInp in self.opp_inputs:
            currBit = 1
            for index in range(0, 32):
                if ((currBit & oppInp.mask) != 0):
                    if ((currBit & oppInp.state) == 0):
                        hw_states[oppInp.cardNum + '-' + str(index)] = 1
                    else:
                        hw_states[oppInp.cardNum + '-' + str(index)] = 0
                currBit <<= 1
        self.hw_switch_data = hw_states
        return self.hw_switch_data
        
    def inv_resp(self, msg):
        self.log.info("Received Inventory Response:%s", "".join(" 0x%02x" % ord(b) for b in msg))

        index = 1
        while (msg[index] != OppRs232Intf.EOM_CMD):
            if ((ord(msg[index]) & ord(OppRs232Intf.CARD_ID_TYPE_MASK)) == ord(OppRs232Intf.CARD_ID_GEN2_CARD)):
                self.numGen2Brd += 1
                self.gen2AddrArr.append(msg[index])
                self.currInpData.append(0)
            index += 1

    def eom_resp(self, msg):
        # An EOM command can be used to resynchronize communications if message synch is lost
        pass

    def get_gen2_cfg_resp(self, msg):
        # Multiple get gen2 cfg responses can be received at once
        self.log.info("Received Gen2 Cfg Response:%s", "".join(" 0x%02x" % ord(b) for b in msg))
        end = False
        currIndex = 0
        wholeMsg = []
        while (not end):
            # Verify the CRC8 is correct
            crc8 = OppRs232Intf.calc_crc8_part_msg(msg, currIndex, 6)
            if (msg[currIndex + 6] != crc8):
                self.badCRC += 1
                hex_string = "".join(" 0x%02x" % ord(b) for b in msg)
                self.log.warning("Msg contains bad CRC:%s.", hex_string)
                end = True
            else:
                hasNeo = False
                wingIndex = 0
                solMask = 0
                inpMask = 0
                incandMask = 0
                while (wingIndex < OppRs232Intf.NUM_G2_WING_PER_BRD):
                    if (msg[currIndex + 2 + wingIndex] == OppRs232Intf.WING_SOL):
                        solMask |= (0x0f << (4 * wingIndex))
                        inpMask |= (0x0f << (8 * wingIndex))
                    elif (msg[currIndex + 2 + wingIndex] == OppRs232Intf.WING_INP):
                        inpMask |= (0xff << (8 * wingIndex))
                    elif (msg[currIndex + 2 + wingIndex] == OppRs232Intf.WING_INCAND):
                        incandMask |= (0xff << (8 * wingIndex))
                    elif (msg[currIndex + 2 + wingIndex] == OppRs232Intf.WING_NEO):
                        hasNeo = True
                    wingIndex += 1
                if (incandMask != 0):
                    self.opp_incands.append(OPPIncand(msg[currIndex], incandMask, self.incandDict))
                if (solMask != 0):
                    self.opp_solenoid.append(OPPSolenoid(msg[currIndex], solMask, self.solDict, self.machine))
                if (inpMask != 0):
                    # Create the input object, and add to the command to read all inputs
                    self.opp_inputs.append(OPPInput(msg[currIndex], inpMask, self.inpDict, self.inpAddrDict))

                    # Add command to read all inputs to read input message
                    inpMsg = []
                    inpMsg.append(msg[currIndex])
                    inpMsg.append(OppRs232Intf.READ_GEN2_INP_CMD)
                    inpMsg.append('\x00')
                    inpMsg.append('\x00')
                    inpMsg.append('\x00')
                    inpMsg.append('\x00')
                    inpMsg.append(OppRs232Intf.calc_crc8_whole_msg(inpMsg))
                    wholeMsg.extend(inpMsg)
            
                if hasNeo:
                    self.opp_neopixels.append(OPPNeopixelCard(msg[currIndex], self.neoCardDict))
            if (not end):
                if (msg[currIndex + 7] == OppRs232Intf.GET_GEN2_CFG):
                    currIndex += 7
                elif (msg[currIndex + 7] == OppRs232Intf.EOM_CMD):
                    end = True
                else:
                    hex_string = "".join(" 0x%02x" % ord(b) for b in msg)
                    self.log.warning("Malformed GET_GEN2_CFG response:%s.", hex_string)
                    end = True

                    # TODO: This means synchronization is lost.  Send EOM characters
                    #  until they come back
                    
        wholeMsg.append(OppRs232Intf.EOM_CMD)
        self.read_input_msg = ''.join(wholeMsg)

    def vers_resp(self, msg):
        # Multiple get version responses can be received at once
        self.log.info("Received Version Response:%s", "".join(" 0x%02x" % ord(b) for b in msg))
        end = False
        currIndex = 0
        while (not end):
            # Verify the CRC8 is correct
            crc8 = OppRs232Intf.calc_crc8_part_msg(msg, currIndex, 6)
            if (msg[currIndex + 6] != crc8):
                self.badCRC += 1
                hex_string = "".join(" 0x%02x" % ord(b) for b in msg)
                self.log.warning("Msg contains bad CRC:%s.", hex_string)
                end = True
            else:
                version = (ord(msg[currIndex + 2]) << 24) | \
                    (ord(msg[currIndex + 3]) << 16) | \
                    (ord(msg[currIndex + 4]) << 8) | \
                    ord(msg[currIndex + 5])
                self.log.info("Firmware version: %d.%d.%d.%d", ord(msg[currIndex + 2]),
                    ord(msg[currIndex + 3]), ord(msg[currIndex + 4]),
                    ord(msg[currIndex + 5]))
                if (version < self.minVersion):
                    self.minVersion = version
                if (version == BAD_FW_VERSION):
                    self.log.error("Original firmware sent only to Brian before adding "
                        "real version numbers.  The firmware must be updated before "
                        "MPF will work.")
                    sys.exit()
                self.oppFirmwareVers.append(version)
            if (not end):
                if (msg[currIndex + 7] == OppRs232Intf.GET_GET_VERS_CMD):
                    currIndex += 7
                elif (msg[currIndex + 7] == OppRs232Intf.EOM_CMD):
                    end = True
                else:
                    hex_string = "".join(" 0x%02x" % ord(b) for b in msg)
                    self.log.warning("Malformed GET_GET_VERS_CMD response:%s.", hex_string)
                    end = True

                    # TODO: This means synchronization is lost.  Send EOM characters
                    #  until they come back


    def read_gen2_inp_resp(self, msg):
        # Multiple read gen2 input responses can be received at once
        #   This function assumes that the inputs are configured so an
        #   active level is only reported once
        self.log.info("Received Input Response:%s", "".join(" 0x%02x" % ord(b) for b in msg))
        end = False
        currIndex = 0
        hw_states = dict()
        while (not end):
            # Verify the CRC8 is correct
            crc8 = OppRs232Intf.calc_crc8_part_msg(msg, currIndex, 6)
            if (msg[currIndex + 6] != crc8):
                self.badCRC += 1
                hex_string = "".join(" 0x%02x" % ord(b) for b in msg)
                self.log.warning("Msg contains bad CRC:%s.", hex_string)
                end = True
            else:
                oppInp = self.inpAddrDict[msg[currIndex]]
                newState = (ord(msg[currIndex + 2]) << 24) | \
                    (ord(msg[currIndex + 3]) << 16) | \
                    (ord(msg[currIndex + 4]) << 8) | \
                    ord(msg[currIndex + 5])

                # Update the state which holds inputs that are active 
                oppInp.state |= newState
            if (not end):
                if (msg[currIndex + 7] == OppRs232Intf.GET_GEN2_CFG):
                    currIndex += 7
                elif (msg[currIndex + 7] == OppRs232Intf.EOM_CMD):
                    end = True
                else:
                    hex_string = "".join(" 0x%02x" % ord(b) for b in msg)
                    self.log.warning("Malformed GET_GEN2_CFG response:%s.", hex_string)
                    end = True

                    # TODO: This means synchronization is lost.  Send EOM characters
                    #  until they come back

    def configure_driver(self, config, device_type='coil'):
        if not self.opp_connection:
            self.log.critical("A request was made to configure an OPP solenoid, "
                              "but no OPP connection is available")
            sys.exit()

        if not config['number'] in self.solDict:
            self.log.critical("A request was made to configure an OPP solenoid "
                              "with number %s which doesn't exist" % config['number'])
            sys.exit()

        opp_sol = self.solDict[config['number']]
        opp_sol.merge_driver_settings(config)
        return (opp_sol, config['number']) 

    def configure_switch(self, config):
        # A switch is termed as an input to OPP
        if not self.opp_connection:
            self.log.critical("A request was made to configure an OPP switch, "
                              "but no OPP connection is available")
            sys.exit()

        if not config['number'] in self.inpDict:
            self.log.critical("A request was made to configure an OPP switch "
                              "with number %s which doesn't exist" % config['number'])
            sys.exit()
            
        return (self.inpDict[config['number']], config['number'])

    def configure_led(self, config):
        if not self.opp_connection:
            self.log.critical("A request was made to configure an OPP LED, "
                              "but no OPP connection is available")
            sys.exit()
        

        card, pixel = config['number'].split('-')
        if not card in self.neoCardDict:
            self.log.critical("A request was made to configure an OPP neopixel "
                              "with card number %s which doesn't exist" % card)
            sys.exit()

        neo = self.neoCardDict[card]
        pixel = neo.add_neopixel(pixel, self.neoDict)
            
        return pixel

    def configure_gi(self, config):
        self.log.critical("OPP hardware does not support configure GI")
        sys.exit()

    def configure_matrixlight(self, config):

        if not self.opp_connection:
            self.log.critical("A request was made to configure an OPP matrix "
                              "light (incand board), but no OPP connection "
                              "is available")
            sys.exit()
        if not config['number'] in self.incandDict:
            self.log.critical("A request was made to configure a OPP matrix "
                              "light (incand board), with number %s "
                              "which doesn't exist" % config['number'])
            sys.exit()
            
        if not self.flag_led_tick_registered:
            self.machine.events.add_handler('timer_tick', self.update_incand)
            self.flag_led_tick_registered = True
            
        return (self.incandDict[config['number']], config['number']) 

    def configure_dmd(self):
        self.log.critical("OPP hardware does not support configure DMD")
        sys.exit()

    def null_dmd_sender(self, *args, **kwargs):
        pass

    def tick(self):
        while not self.receive_queue.empty():
            self.process_received_message(self.receive_queue.get(False))

        self.opp_connection.send(self.read_input_msg)

    def write_hw_rule(self, switch_obj, sw_activity, driver_obj, driver_action,
                      disable_on_release=True, drive_now=True,
                      **driver_settings_overrides):
        """Used to write (or update) a hardware rule to the OPP hardware.

        *Hardware Rules* are used to configure the hardware controller to
        automatically change driver states based on switch changes. These rules
        are completely handled by the hardware (i.e. with no interaction from
        the Python game code). They're used for things that you want to happen
        fast, like firing coils when flipper buttons are pushed, slingshots, pop
        bumpers, etc.

        You can overwrite existing hardware rules at any time to change or
        remove them.

        Args:
            switch_obj: Which switch you're creating this rule for. The
                parameter is a reference to the switch object itself.
                Note:  The OPP firmware currently only supports the using the
                dedicated switch.
            sw_activity: Int which specifies whether this coil should fire when
                the switch becomes active (1) or inactive (0)
                Note:  The OPP firmware currently only supports firing the
                coil when switch becomes active.
            driver_obj: Driver object this rule is being set for.
            driver_action: String 'pulse' or 'hold' which describe what action
                will be applied to this driver
            drive_now: Should the hardware check the state of the switches when
                this rule is first applied, and fire the coils if they should
                be? Typically this is True, especially with flippers because you
                want them to fire if the player is holding in the buttons when
                the machine enables the flippers (which is done via several
                calls to this method.)
                Note:  The OPP firmware always assumes this is True.

        """

        # Verify the switch name is correct for the driver name.
        if (driver_obj.name != switch_obj.name):
            self.log.error('Invalid switch being configured for driver. Driver = %s '
                           'Switch = %s' % (driver_obj.name, switch_obj.name))
            return

        card, solenoid = driver_obj.name.split('-')
            
        driver_settings = deepcopy(driver_obj.hw_driver.driver_settings)

        driver_settings.update(driver_obj.hw_driver.merge_driver_settings(
            **driver_settings_overrides))

        self.log.debug("Setting HW Rule. Driver: %s, Driver settings: %s", 
                      driver_obj.name, driver_settings)

        self.hw_rules[driver_obj] = {'pulse_ms': driver_settings['pulse_ms'],
                               'hold_power': driver_settings['hold_power'],
                               'switch': switch_obj.number}

        pulse_len = int(driver_settings['pulse_ms'])
        hold = int(driver_settings['hold_power'])
        solIndex = int(solenoid) * OppRs232Intf.CFG_BYTES_PER_SOL

        # If hold is 0, set the auto clear bit
        if (hold == 0):
            driver_obj.currCfgLst[solIndex] = chr(ord(OppRs232Intf.CFG_SOL_USE_SWITCH) +
                                                  ord(OppRs232Intf.CFG_SOL_AUTO_CLR))
        else:
            driver_obj.currCfgLst[solIndex] = ord(OppRs232Intf.CFG_SOL_AUTO_CLR)
        driver_obj.currCfgLst[solIndex + OppRs232Intf.INIT_KICK_OFFSET] = chr(pulse_len)
        driver_obj.currCfgLst[solIndex + OppRs232Intf.DUTY_CYCLE_OFFSET] = chr(hold)

        msg = []
        msg.append(driver_obj.addr)
        msg.append(OppRs232Intf.CFG_SOL_CMD)
        for byte in driver_obj.currCfgLst:
            msg.append(byte)
        msg.append(OppRs232Intf.calc_crc8_whole_msg(msg))
        msg.append(OppRs232Intf.EOM_CMD)
        cmd = ''.join(msg)
        
        self.log.debug("Writing hardware rule: %s", "".join(" 0x%02x" % ord(b) for b in cmd))
        self.opp_connection.send(cmd)

    def clear_hw_rule(self, sw_name):
        """Clears a hardware rule.

        This is used if you want to remove the linkage between a switch and
        some driver activity. For example, if you wanted to disable your
        flippers (so that a player pushing the flipper buttons wouldn't cause
        the flippers to flip), you'd call this method with your flipper button
        as the *sw_num*.

        Args:
            sw_name: The string name of the switch whose rule you want to clear.

        """
        sw_num = self.machine.switches[sw_name].number

        # find the rule(s) based on this switch
        coils = [k for k, v in self.hw_rules.iteritems() if v['switch'] == sw_num]

        self.log.debug("Clearing HW Rule for switch: %s %s, coils: %s", sw_name,
                       sw_num, coils)

        for driver_obj in coils:

            del self.hw_rules[driver_obj]

            driver_settings = driver_obj.hw_driver.driver_settings
            driver_settings['pulse_ms'] = '0'
            driver_settings['hold_power'] = '0'

            card, solenoid = driver_obj.name.split('-')
            solIndex = int(solenoid) * OppRs232Intf.CFG_BYTES_PER_SOL
            driver_obj.currCfgLst[solIndex] = '\x00'
            driver_obj.currCfgLst[solIndex + OppRs232Intf.INIT_KICK_OFFSET] = '\x00'
            driver_obj.currCfgLst[solIndex + OppRs232Intf.DUTY_CYCLE_OFFSET] = '\x00'

            msg = []
            msg.append(driver_obj.addr)
            msg.append(OppRs232Intf.CFG_SOL_CMD)
            for byte in driver_obj.currCfgLst:
                msg.append(byte)
            msg.append(OppRs232Intf.calc_crc8_whole_msg(msg))
            msg.append(OppRs232Intf.EOM_CMD)
            cmd = ''.join(msg)
            
            self.log.debug("Clearing hardware rule: %s", "".join(" 0x%02x" % ord(b) for b in cmd))
            self.opp_connection.send(cmd)

class OPPIncand(object):

    def __init__(self, addr, mask, incandDict):
        self.log = logging.getLogger('OPPIncand')
        self.addr = addr
        self.oldState = 0
        self.newState = 0
        self.mask = mask

        self.log.debug("Creating OPP Incand at hardware address: 0x%02x",
            ord(addr))
        
        card = str(ord(addr) - ord(OppRs232Intf.CARD_ID_GEN2_CARD))
        for index in range(0, 32):
            if (((1 << index) & mask) != 0):
                incandDict[card + '-' + str(index)] = self
        
    def disable(self):
        #TODO:  Need bit mask of incand to turn off
        currBit
        self.newState &= ~currBit

    def enable(self):
        #TODO:  Need bit mask of incand to turn on
        currBit
        self.newState |= currBit

class OPPSolenoid(object):

    def __init__(self, addr, mask, solDict, machine):
        self.log = logging.getLogger('OPPSolenoid')
        self.addr = addr
        self.state = 0
        self.mask = mask
        self.currCfgLst = ['\x00' for _ in range(OppRs232Intf.NUM_G2_SOL_PER_BRD *
                                            OppRs232Intf.CFG_BYTES_PER_SOL)]

        self.driver_settings = self.create_driver_settings(machine)

        self.log.debug("Creating OPP Solenoid at hardware address: 0x%02x",
            ord(addr))
        
        card = str(ord(addr) - ord(OppRs232Intf.CARD_ID_GEN2_CARD))
        for index in range(0, 16):
            if (((1 << index) & mask) != 0):
                solDict[card + '-' + str(index)] = self

    def create_driver_settings(self, machine):
        return_dict = dict()
        pulse_ms = machine.config['mpf']['default_pulse_ms']
        return_dict['pulse_ms'] = str(pulse_ms)
        return_dict['hold_power'] = '0'
        return return_dict

    def merge_driver_settings(self,
                            pulse_ms=None,
                            pwm_on_ms=None,
                            pwm_off_ms=None,
                            pulse_power=None,
                            hold_power=None,
                            pulse_power32=None,
                            hold_power32=None,
                            pulse_pwm_mask=None,
                            hold_pwm_mask=None,
                            recycle_ms=None,
                            activation_time=None,
                            **kwargs
                            ):

        if pwm_on_ms:
            raise ValueError("The setting 'pwm_on_ms' is not valid with the "
                             "OPP platform. Use hold_power instead.")
        if pwm_off_ms:
            raise ValueError("The setting 'pwm_off_ms' is not valid with the "
                             "OPP platform. Use hold_power instead.")
        if pulse_power:
            raise ValueError("The setting 'pulse_power' is not valid with the "
                             "OPP platform. Use hold_power instead.")
        if pulse_power32:
            raise ValueError("The setting 'pulse_power32' is not valid with the "
                             "OPP platform. Use hold_power instead.")
        if hold_power32:
            raise ValueError("The setting 'hold_power32' is not valid with the "
                             "OPP platform. Use hold_power instead.")
        if pulse_pwm_mask:
            raise ValueError("The setting 'pulse_pwm_mask' is not valid with the "
                             "OPP platform. Use hold_power instead.")
        if hold_pwm_mask:
            raise ValueError("The setting 'hold_pwm_mask' is not valid with the "
                             "OPP platform. Use hold_power instead.")
        if recycle_ms:
            raise ValueError("The setting 'recycle_ms' is not valid with the "
                             "OPP platform.")
        if activation_time:
            raise ValueError("The setting 'activation_time' is not valid with the "
                             "OPP platform.")

        return_dict = dict()

        if pulse_ms is not None:
            return_dict['pulse_ms'] = str(pulse_ms)

        if hold_power is not None:
            return_dict['hold_power'] = str(hold_power)

        return return_dict
        
class OPPInput(object):

    def __init__(self, addr, mask, inpDict, inpAddrDict):
        self.log = logging.getLogger('OPPInput')
        self.addr = addr
        self.state = 0
        self.mask = mask
        self.cardNum = str(ord(addr) - ord(OppRs232Intf.CARD_ID_GEN2_CARD))

        self.log.debug("Creating OPP Input at hardware address: 0x%02x",
            ord(addr))

        inpAddrDict[addr] = self
        for index in range(0, 32):
            if (((1 << index) & mask) != 0):
                inpDict[self.cardNum + '-' + str(index)] = self

class OPPNeopixelCard(object):

    def __init__(self, addr, neoCardDict):
        self.log = logging.getLogger('OPPNeopixel')
        self.addr = addr
        self.card = chr(ord(addr) - ord(OppRs232Intf.CARD_ID_GEN2_CARD))
        self.numPixels = 0
        self.colorTableLst = [0 for _ in range(32)]
        neoCardDict[self.card] = self

        self.log.debug("Creating OPP Neopixel card at hardware address: 0x%02x",
            ord(addr))

    def add_neopixel(self, number, neoDict):
        if number > self.numPixels:
            self.numPixels = number + 1
        pixel_name = self.card + '-' + str(number)
        pixel = OppNeopixel(pixel_name)
        neoDict[pixel_name] = pixel
        return pixel

class OPPNeopixel(object):

    def __init__(self, number):
        self.log = logging.getLogger('OPPNeopixel')
        self.number = number
        self.color = 0

        self.log.debug("Creating OPP Neopixel: %s",
            number)

class SerialCommunicator(object):

    def __init__(self, machine, platform, port, baud, send_queue, receive_queue):
        self.machine = machine
        self.platform = platform
        self.send_queue = send_queue
        self.receive_queue = receive_queue
        self.debug = False
        self.log = self.platform.log

        self.remote_processor = "OPP Gen2"
        self.remote_model = None
        self.remote_firmware = 0.0

        self.log.info("Connecting to %s at %sbps", port, baud)
        try:
            self.serial_connection = serial.Serial(port=port, baudrate=baud,
                                               timeout=.1, writeTimeout=0)
        except serial.SerialException:
            self.log.error('Could not open port: %s' % port)
            sys.exit()

        self.serial_io = io.BufferedRWPair(
            self.serial_connection, self.serial_connection)

        self.identify_connection()
        self.platform.register_processor_connection(self.remote_processor, self)
        self._start_threads()

    def identify_connection(self):
        """Identifies which processor this serial connection is talking to."""

        # keep looping and wait for an ID response
        count = 0
        while True:
            if ((count % 10) == 0):
                self.log.debug("Sending EOM command to port '%s'",
                                        self.serial_connection.name)
            count += 1
            self.serial_connection.write(OppRs232Intf.EOM_CMD)
            resp = self.serial_io.read()
            if resp.startswith(OppRs232Intf.EOM_CMD):
                break
            if (count == 100):
                self.log.error('No response from OPP hardware: %s' %
                                        self.serial_connection.name)
                sys.exit()

        # Send inventory command to figure out number of cards
        msg = []
        msg.append(OppRs232Intf.INV_CMD)
        msg.append(OppRs232Intf.EOM_CMD)
        cmd = ''.join(msg)
        
        self.log.debug("Sending inventory command: %s", "".join(" 0x%02x" % ord(b) for b in cmd))
        self.serial_connection.write(cmd) # HRS:  Deal with errors
        
        time.sleep(.1)
        resp = self.serial_io.read()
        
        # resp will contain the inventory response.
        self.platform.process_received_message(resp) # HRS:  Deal with errors

        # Now send get gen2 configuration message to find populated wing boards
        self.send_get_gen2_cfg_cmd()

        time.sleep(.1)
        resp = self.serial_io.read()

        # resp will contain the gen2 cfg reponses.  That will end up creating all the
        # correct objects.
        self.platform.process_received_message(resp) # HRS:  Deal with errors

        # get the version of the firmware
        self.send_vers_cmd()
        time.sleep(.1)
        resp = self.serial_io.read()
        self.platform.process_received_message(resp) # HRS:  Deal with errors
        
        # see if version of firmware is new enough
        if (self.platform.minVersion < MIN_FW):
            self.log.critical("Firmware version mismatch. MPF requires"
                " the %s processor to be firmware %s, but yours is %s",
                self.remote_processor, create_vers_str(MIN_FW),
                create_vers_str(self.platform.minVersion))
            sys.exit()
        
    def send_get_gen2_cfg_cmd(self):
        # Now send get gen2 configuration message to find populated wing boards
        wholeMsg = []
        for cardAddr in self.platform.gen2AddrArr:
            # Turn on the bulbs that are non-zero
            msg = []
            msg.append(cardAddr)
            msg.append(OppRs232Intf.GET_GEN2_CFG)
            msg.append('\x00')
            msg.append('\x00')
            msg.append('\x00')
            msg.append('\x00')
            msg.append(OppRs232Intf.calc_crc8_whole_msg(msg))
            wholeMsg.extend(msg)
            
        wholeMsg.append(OppRs232Intf.EOM_CMD)
        cmd = ''.join(wholeMsg)
        self.log.debug("Sending get Gen2 Cfg command: %s", "".join(" 0x%02x" % ord(b) for b in cmd))
        self.serial_connection.write(cmd)
        
    def send_vers_cmd(self):
        # Now send get firmware version message
        wholeMsg = []
        for cardAddr in self.platform.gen2AddrArr:
            # Turn on the bulbs that are non-zero
            msg = []
            msg.append(cardAddr)
            msg.append(OppRs232Intf.GET_GET_VERS_CMD)
            msg.append('\x00')
            msg.append('\x00')
            msg.append('\x00')
            msg.append('\x00')
            msg.append(OppRs232Intf.calc_crc8_whole_msg(msg))
            wholeMsg.extend(msg)
            
        wholeMsg.append(OppRs232Intf.EOM_CMD)
        cmd = ''.join(wholeMsg)
        self.log.debug("Sending get version command: %s", "".join(" 0x%02x" % ord(b) for b in cmd))
        self.serial_connection.write(cmd)
        
    def create_vers_str(self, version_int):
        return ("%02d.%02d.%02d.%02d" % (((version_int >> 24) & 0xff),
            ((version_int >> 16) & 0xff), ((version_int >> 8) & 0xff),
            (version_int & 0xff)))

    def _start_threads(self):

        self.serial_connection.timeout = None

        self.receive_thread = threading.Thread(target=self._receive_loop)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.sending_thread = threading.Thread(target=self._sending_loop)
        self.sending_thread.daemon = True
        self.sending_thread.start()

    def stop(self):
        """Stops and shuts down this serial connection."""
        self.serial_connection.close()
        self.serial_connection = None  # child threads stop when this is None

        # todo clear the hw?

    def send(self, msg):
        """Sends a message to the remote processor over the serial connection.

        Args:
            msg: String of the message you want to send. We don't need no
            steenking line feed character

        """
        self.send_queue.put(msg)

    def _sending_loop(self):

        debug = self.platform.config['debug']

        try:
            while self.serial_connection:
                msg = self.send_queue.get()
                self.serial_connection.write(msg)

                if debug:
                    self.log.info("Sending: %s", msg)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            msg = ''.join(line for line in lines)
            self.machine.crash_queue.put(msg)

    def _receive_loop(self):

        debug = self.platform.config['debug']

        try:
            while self.serial_connection:
                msg = self.serial_io.read()

                if debug:
                    self.log.info("Received: %s", "".join(" 0x%02x" % ord(b) for b in msg))

                self.receive_queue.put(msg)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value,
                                               exc_traceback)
            msg = ''.join(line for line in lines)
            self.machine.crash_queue.put(msg)

# The MIT License (MIT)

# Oringal code on which this module was based:
# Copyright (c) 2009-2011 Adam Preble and Gerry Stellenberg

# Copyright (c) 2016 Hugh Spahr

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
