/*
 *===============================================================================
 *
 *                         OOOO
 *                       OOOOOOOO
 *      PPPPPPPPPPPPP   OOO    OOO   PPPPPPPPPPPPP
 *    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
 *   PPP         PPP   OOO      OOO   PPP         PPP
 *  PPP          PPP   OOO      OOO   PPP          PPP
 *  PPP          PPP   OOO      OOO   PPP          PPP
 *  PPP          PPP   OOO      OOO   PPP          PPP
 *   PPP         PPP   OOO      OOO   PPP         PPP
 *    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
 *     PPPPPPPPPPPPP   OOO      OOO   PPP
 *               PPP   OOO      OOO   PPP
 *               PPP   OOO      OOO   PPP
 *               PPP   OOO      OOO   PPP
 *               PPP    OOO    OOO    PPP
 *               PPP     OOOOOOOO     PPP
 *              PPPPP      OOOO      PPPPP
 *
 * @file:   SerIntf.java
 * @author: Hugh Spahr
 * @date:   1/09/2013
 *
 * @note:   Open Pinball Project
 *          Copyright© 2013, Hugh Spahr
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 *===============================================================================
 */
/**
 * This is the serial interface file.  Returns 100 level errors.
 *
 *===============================================================================
 */

import java.awt.BorderLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.util.Enumeration;
import java.util.TooManyListenersException;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.Timer;

import gnu.io.*;

public class SerIntf implements SerialPortEventListener
{
   public static final int       INCORRECT_JVM_INSTALLED    = 100;
   public static final int       CANT_FIND_COMM_PORT        = 101;
   public static final int       PORT_IN_USE_ERROR          = 102;
   public static final int       CANT_SET_COMM_PARAMS       = 103;
   public static final int       CANT_CREATE_STREAMS        = 104;
   public static final int       TOO_MANY_LISTENERS         = 105;
   
   private CommPortIdentifier    currPort;
   private SerialPort            serialPort;
   private InputStream           serInpStream;
   private OutputStream          serOutStream;
   private boolean               rcvResp;
   private boolean               printTimerMisses = true;
   private int                   missed = 0;
   private int                   received = 0;

   private static final int      MAX_READ_BUF_SIZE          = 64;
   private byte[]                readBuffer = new byte[MAX_READ_BUF_SIZE];
   private int                   currBufIndex;
   
   private static final int      RCV_IDLE                   = 0;
   private static final int      RCV_ADDR                   = 1;
   private static final int      RCV_CMD                    = 2;
   private static final int      WAIT_FOR_EOM               = 3;
   private int                   rcvState;
   private int                   rcvDataCtr;
   
   private boolean               foundCards;
   private int[]                 periodicTxMsg = new int[64];
   private int                   periodicTxLen;

   /* Commands are cardAddr, then cmd */
   public static final byte      RS232I_GET_SER_NUM         = 0x00;
   public static final byte      RS232I_GET_PROD_ID         = 0x01;
   public static final byte      RS232I_GET_VERS            = 0x02;
   public static final byte      RS232I_SET_SER_NUM         = 0x03;
   public static final byte      RS232I_RESET               = 0x04;
   public static final byte      RS232I_GO_BOOT             = 0x05;
   public static final byte      RS232I_CONFIG_SOL          = 0x06;
   public static final byte      RS232I_KICK_SOL            = 0x07;
   public static final byte      RS232I_READ_SOL_INP        = 0x08;
   public static final byte      RS232I_CONFIG_INP          = 0x09;
   public static final byte      RS232I_READ_INP_BRD        = 0x0a;
   
   private static final byte     RS232I_INV                 = (byte)0xf0;
   private static final byte     RS232I_EOM                 = (byte)0xff;

   private static final int[]    RS232I_DATA_SIZE           =
   { 
      4,  /* RS232I_GET_SER_NUM */     4,  /* RS232I_GET_PROD_ID */
      4,  /* RS232I_GET_VERS */        4,  /* RS232I_SET_SER_NUM */
      0,  /* RS232I_RESET */           0,  /* RS232I_GO_BOOT */
      24, /* RS232I_CONFIG_SOL */      2,  /* RS232I_KICK_SOL */
      1,  /* RS232I_READ_SOL_INP */    16, /* RS232I_CONFIG_INP */
      2,  /* RS232I_READ_INP_BRD */
   };

   public static final int       CARD_ID_TYPE_MASK          = 0xf0;
   public static final int       CARD_ID_SOL_CARD           = 0x00;
   public static final int       CARD_ID_INP_CARD           = 0x10;

   /* Solenoid cfg is flags, initial kick (ms), and duty cycle/off byte.
    *    Min off time is 0-7 times the initial kick time.  If initial kick
    *    is 20 ms and min off is 5, the solenoid will be forced off for 100 ms
    */
   public static final int       SOLCFG_FLG_USE_SWITCH      = 0x01;
   public static final int       SOLCFG_FLG_AUTO_CLR        = 0x02;
   
   public static final int       SOLCFG_TIME_DUTY_CYCLE_MSK = 0x0f;
   public static final int       SOLCFG_TIME_MIN_OFF_MSK    = 0x70;
   
   /* Input cfg is a single byte for each input bit */
   public static final int       INPCFG_STATE_INPUT         = 0x00;
   public static final int       INPCFG_FALL_EDGE           = 0x01;
   public static final int       INPCFG_RISE_EDGE           = 0x02;
   
   private static final int[]    TEST_SOLCFG                =
   {
      /* Flags */                /* intial kick (ms) */     /* min off/duty cycle */
      0x00,                      0xff,                      0x0f,
      0x00,                      0xff,                      0x0f,
      0x00,                      0xff,                      0x0f,
      0x00,                      0xff,                      0x0f,
      0x00,                      0xff,                      0x0f,
      0x00,                      0xff,                      0x0f,
      0x00,                      0xff,                      0x0f,
      0x00,                      0xff,                      0x0f,
   };
   
   private static final int[]    TEST_INPCFG                =
   { 
      INPCFG_STATE_INPUT, INPCFG_STATE_INPUT, INPCFG_STATE_INPUT, INPCFG_STATE_INPUT,
      INPCFG_STATE_INPUT, INPCFG_STATE_INPUT, INPCFG_STATE_INPUT, INPCFG_STATE_INPUT,
      INPCFG_STATE_INPUT, INPCFG_STATE_INPUT, INPCFG_STATE_INPUT, INPCFG_STATE_INPUT,
      INPCFG_STATE_INPUT, INPCFG_STATE_INPUT, INPCFG_STATE_INPUT, INPCFG_STATE_INPUT
   };
   
   /*
    * ===============================================================================
    * 
    * Name: SerIntf
    * 
    * ===============================================================================
    */
   /**
    * Serial interface class
    * 
    * Connect to a serial port and then send an inventory msg to discover
    * cards.  Send the configuration to the cards.  Start a timer thread to
    * periodically get a thread.
    * 
    * @param   None 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public SerIntf(String portName)
   {
      int[]                            msg = new int[384];
      int                              cnt;
      int                              index;
      
      /* Open the serial port and send the inventory cmd */
      rcvResp = false;
      foundCards = false;
      connectSerPort(portName);
      msg[0] = RS232I_INV & 0xff;
      msg[1] = RS232I_EOM & 0xff;
      sendMsg(msg, 2);
      
      /* Wait for a response from the boards or a timeout */
      cnt = 0;
      while ((cnt < 10) && !rcvResp)
      {
         try
         {
            Thread.sleep(100);
         }
         catch (InterruptedException e)
         {
            /* HRS: Should not happen */
            e.printStackTrace();
         }
         cnt++;
      }
      if (rcvResp)
      {
         rcvResp = false;
         processCmdStr();
         GlobInfo.hostCtl.printMsg("Found cards!! Sol: " + GlobInfo.numSolCards +
               " Inp: "+ GlobInfo.numInpCards);
         
         /* Send the config command to all the cards */
         index = 0;
         for (cnt = 0; cnt < GlobInfo.numInpCards; cnt++)
         {
            msg[index++] = GlobInfo.inpCardAddr[cnt];
            msg[index++] = RS232I_CONFIG_INP;
            System.arraycopy( TEST_INPCFG, 0, msg, index, TEST_INPCFG.length );
            index += TEST_INPCFG.length;
         }
         for (cnt = 0; cnt < GlobInfo.numSolCards; cnt++)
         {
            msg[index++] = GlobInfo.solCardAddr[cnt];
            msg[index++] = RS232I_CONFIG_SOL;
            System.arraycopy( TEST_SOLCFG, 0, msg, index, TEST_SOLCFG.length );
            index += TEST_SOLCFG.length;
         }
         msg[index++] = RS232I_EOM & 0xff;
         sendMsg(msg, index);
         
         /* Wait for the response */
         cnt = 0;
         while ((cnt < 10) && !rcvResp)
         {
            try
            {
               Thread.sleep(100);
            }
            catch (InterruptedException e)
            {
               /* HRS: Should not happen */
               e.printStackTrace();
            }
            cnt++;
         }
         if (rcvResp)
         {
            /* Process the EOM msg */
            rcvResp = false;
            processCmdStr();
            GlobInfo.hostCtl.printMsg("Cfg msg(s) worked.");
            foundCards = true;
            
            /* Create the periodic tx msg */
            periodicTxLen = 0;
            for (cnt = 0; cnt < GlobInfo.numInpCards; cnt++)
            {
               periodicTxMsg[periodicTxLen++] = GlobInfo.inpCardAddr[cnt];
               periodicTxMsg[periodicTxLen++] = RS232I_READ_INP_BRD;
               periodicTxMsg[periodicTxLen++] = 0;
               periodicTxMsg[periodicTxLen++] = 0;
            }
            for (cnt = 0; cnt < GlobInfo.numSolCards; cnt++)
            {
               periodicTxMsg[periodicTxLen++] = GlobInfo.solCardAddr[cnt];
               periodicTxMsg[periodicTxLen++] = RS232I_READ_SOL_INP;
               periodicTxMsg[periodicTxLen++] = 0;
            }
            periodicTxMsg[periodicTxLen++] = RS232I_EOM & 0xff;
            sendMsg(periodicTxMsg, periodicTxLen);
         }
         else
         {
            GlobInfo.hostCtl.printMsg("Cfg message failed!!");
         }
      }
      else
      {
         GlobInfo.hostCtl.printMsg("No cards found!!");
      }
      
      if (foundCards)
      {
         /* Now create debug frame since we know number of cards */
         if (GlobInfo.debug)
         {
            /* Create frame for card rcv data */
            createDebugFrm();
         }
         
         /* Through looking at received vs missed, my XP machine needs 15 ms to
          * not miss a large number of msgs.  (at 10 ms, I missed approx 20% of the
          * time)
          */
         Timer timer = new Timer(15, new ActionListener()
         {
           public void actionPerformed(ActionEvent evt)
           {
              int                            cnt;
              
              if (rcvResp)
              {
                 rcvResp = false;
                 processCmdStr();
                 received++;
                 if (printTimerMisses)
                 {
                    if (received > 100)
                    {
                       GlobInfo.hostCtl.printMsg("Received 100 msgs!!!");
                       received = 0;
                    }
                 }
                 
                 /* Update debug panel */
                 if (GlobInfo.debug)
                 {
                    for (cnt = 0; cnt < GlobInfo.numInpCards; cnt++)
                    {
                       GlobInfo.inpCardDbgLbl[cnt].setText(String.format("%16s",
                             Integer.toBinaryString(GlobInfo.inpCardData[cnt])).replace(' ', '0'));
                    }
                    for (cnt = 0; cnt < GlobInfo.numSolCards; cnt++)
                    {
                       GlobInfo.solCardDbgLbl[cnt].setText(String.format("%8s",
                             Integer.toBinaryString(GlobInfo.solCardData[cnt])).replace(' ', '0'));
                    }
                    for (cnt = 0; cnt < GlobInfo.numLedCards; cnt++)
                    {
                       GlobInfo.ledCardDbgLbl[cnt].setText(String.format("%8s",
                             Integer.toBinaryString(GlobInfo.ledCardData[cnt])).replace(' ', '0'));
                    }
                 }
                 
                 sendMsg(periodicTxMsg, periodicTxLen);
              }
              else
              {
                 missed++;
                 if (missed > 100)
                 {
                    GlobInfo.hostCtl.printMsg("Missed 100 msgs!!!");
                    missed = 0;
                 }
              }
           }
         });
         timer.start();
      }
   }
   /*
    * ===============================================================================
    * 
    * Name: connectSerPort
    * 
    * ===============================================================================
    */
   /**
    * Connect to a serial port.
    * 
    * Figure out which serial port is selected.  If anything goes wrong, exit the
    * program.  Try to grab the port.  Create input and output streams.  Set up
    * the event listener to get a message when a byte is received.
    * 
    * @param   None 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   private int connectSerPort(String portName)
   {
      CommPortIdentifier        portId = null;
      boolean                   found = false;

      try
      {
         Enumeration<?>            portList = CommPortIdentifier.getPortIdentifiers();
         while (portList.hasMoreElements() && !found)
         {
            portId = (CommPortIdentifier) portList.nextElement();
            if (portName.equals(portId.getName()))
            {
               found = true;
            }
         }
      } 
      catch (UnsatisfiedLinkError e)
      {
         GlobInfo.hostCtl.printMsg("Configuration not supported.  Default JVM is 32 Bit on 64 Bit OS.");
         return(INCORRECT_JVM_INSTALLED);
      }
      if (!found)
      {
         GlobInfo.hostCtl.printMsg("Can't re-attach to COM port.");
         return(CANT_FIND_COMM_PORT);
      }
      currPort = portId;
      try
      {
         /* Grab port and wait up to 2 seconds to acquire it. */
         serialPort = (SerialPort) currPort.open("SerIntf", 2000);
      } 
      catch (PortInUseException e)
      {
         /* Couldn't open serial port */
         currPort = null;
         System.exit(PORT_IN_USE_ERROR);
      }

      /* Set the serial port parameters */
      try
      {
         serialPort.setSerialPortParams(19200, SerialPort.DATABITS_8,
               SerialPort.STOPBITS_1, SerialPort.PARITY_NONE);
      } 
      catch (UnsupportedCommOperationException e)
      {
         serialPort.close();
         currPort = null;
         return(CANT_SET_COMM_PARAMS);
      }
      try
      {
         serInpStream = serialPort.getInputStream();
         serOutStream = serialPort.getOutputStream();
      } 
      catch (IOException e)
      {
         /* Couldn't get input or output stream */
         serialPort.close();
         currPort = null;
         return(CANT_CREATE_STREAMS);
      }

      /* Notify us when a byte is received */
      try
      {
         serialPort.addEventListener(SerIntf.this);
      } 
      catch (TooManyListenersException e)
      {
         try
         {
            serInpStream.close();
            serOutStream.close();
         } 
         catch (IOException event)
         {
         }
         serialPort.close();
         currPort = null;
         return(TOO_MANY_LISTENERS);
      }

      rcvState = RCV_IDLE;
      currBufIndex = 0;
      serialPort.notifyOnDataAvailable(true);
      GlobInfo.hostCtl.printMsg("SerIntf: Opened " + portName);
      return(0);
   } /* end connectSerPort */
   
   /*
    * ===============================================================================
    * 
    * Name: serialEvent
    * 
    * ===============================================================================
    */
   /**
    * Serial event handler
    * 
    * Standard serial event handler.  It calls processRcvData for all of the
    * processing.
    * 
    * @param   None 
    * @return  None
    * 
    * @pre     None 
    * @note    Other pins can be used to cause the serial port to be closed.
    * 
    * ===============================================================================
    */
   public void serialEvent(SerialPortEvent event)
   {
      switch (event.getEventType())
      {
         case SerialPortEvent.BI:
         case SerialPortEvent.OE:
         case SerialPortEvent.FE:
         case SerialPortEvent.PE:
         case SerialPortEvent.CD:
         case SerialPortEvent.CTS:
         case SerialPortEvent.DSR:
         case SerialPortEvent.RI:
         case SerialPortEvent.OUTPUT_BUFFER_EMPTY:
         {
            break;
         }
         case SerialPortEvent.DATA_AVAILABLE:
         {
            processRcvData();
            break;
         }
      }
   } /* end serialEvent */

   /*
    * ===============================================================================
    * 
    * Name: processRcvData
    * 
    * ===============================================================================
    */
   /**
    * Process receive data
    * 
    * Process receive data by putting data into the receive buffer.  A state is used
    * to figure out the commands, and data for each command.  A flag is set when an
    * EOM byte is received.
    * 
    * @param   None 
    * @return  None
    * 
    * @pre     None 
    * @note    None
    * 
    * ===============================================================================
    */
   private void processRcvData()
   {
      byte[]                        tmpBuffer = new byte[64];
      byte                          currData;
      int                           numBytes = 0;
      int                           index;
      
      /* Grab the input characters.  Copy them into the readBuffer for processing */
      try
      {
         while (serInpStream.available() > 0)
         {
            numBytes = serInpStream.read(tmpBuffer);
            for (index = 0; (index < numBytes) && (currBufIndex < MAX_READ_BUF_SIZE);
               index++, currBufIndex++)
            {
               currData = tmpBuffer[index];
               if (rcvState == RCV_IDLE)
               {
                  if (currData == RS232I_INV)
                  {
                     rcvState = WAIT_FOR_EOM;
                     readBuffer[currBufIndex] = currData;
                  }
                  else if (currData == RS232I_EOM)
                  {
                     /* If in idle state, ignore all EOMs, set data rcv flag */
                     currBufIndex--;
                     rcvResp = true;
                  }
                  else
                  {
                     rcvState = RCV_ADDR;
                     readBuffer[currBufIndex] = currData;
                  }
               }
               else if (rcvState == RCV_ADDR)
               {
                  /* Look up the cmd to find number of data bytes */
                  readBuffer[currBufIndex] = currData;
                  rcvDataCtr = RS232I_DATA_SIZE[currData];
                  rcvState = RCV_CMD;
               }
               else if (rcvState == RCV_CMD)
               {
                  /* Wait for cmd data */
                  readBuffer[currBufIndex] = currData;
                  rcvDataCtr--;
                  if (rcvDataCtr == 0)
                  {
                     rcvState = RCV_IDLE;
                  }
               }
               else if (rcvState == WAIT_FOR_EOM)
               {
                  readBuffer[currBufIndex] = currData;
                  if (currData == RS232I_EOM)
                  {
                     rcvState = RCV_IDLE;
                     rcvResp = true;
                  }
               }
               else
               {
                  /* HRS: Invalid rcv state */ 
               }
            }
         }
      }
      catch (IOException e)
      {
      }
   } /* end processRcvData */
   
   /*
    * ===============================================================================
    * 
    * Name: processCmdStr
    * 
    * ===============================================================================
    */
   /**
    * Process command string
    * 
    * Walk through the cmd string processing each cmd response.  Store the data
    * if necessary.
    * 
    * @param   None 
    * @return  None
    * 
    * @pre     None 
    * @note    None
    * 
    * ===============================================================================
    */
   private void processCmdStr()
   {
      int                           index;
      byte                          currData;
      int                           cardIndex;
      int                           tmpData;
      
      for (index = 0; index < currBufIndex; index++)
      {
         currData = readBuffer[index];
         if (currData == RS232I_INV)
         {
            currData = readBuffer[++index];
            while (currData != RS232I_EOM)
            {
               if (((int)currData & CARD_ID_TYPE_MASK) == CARD_ID_SOL_CARD)
               {
                  GlobInfo.solCardAddr[GlobInfo.numSolCards] =  currData;
                  GlobInfo.numSolCards++;
               }
               else if (((int)currData & CARD_ID_TYPE_MASK) == CARD_ID_INP_CARD)
               {
                  GlobInfo.inpCardAddr[GlobInfo.numInpCards] =  currData;
                  GlobInfo.numInpCards++;
               }
               else
               {
                  /* HRS: Illegal addr */ 
               }
               currData = readBuffer[++index];
            }
         }
         else if (currData == RS232I_EOM)
         {
            /* EOMs can be found within messages, so swallow them. */
         }
         else
         {
            if (((int)currData & CARD_ID_TYPE_MASK) == CARD_ID_INP_CARD)
            {
               cardIndex = (int)currData & ~CARD_ID_TYPE_MASK;
               if (cardIndex < GlobInfo.numSolCards)
               {
                  /* Next byte is the command */
                  currData = readBuffer[++index];
                  switch (currData)
                  {
                     case RS232I_GET_SER_NUM:
                     {
                        tmpData = (((int)readBuffer[index + 1] & 0xff) << 24) |
                           (((int)readBuffer[index + 2] & 0xff) << 16) |
                           (((int)readBuffer[index + 3] & 0xff) << 8) |
                           ((int)readBuffer[index + 4] & 0xff);
                        index += 4;
                        GlobInfo.inpCardSerNum[cardIndex] = tmpData;
                        break;
                     }
                     case RS232I_GET_PROD_ID:
                     {
                        tmpData = (((int)readBuffer[index + 1] & 0xff) << 24) |
                           (((int)readBuffer[index + 2] & 0xff) << 16) |
                           (((int)readBuffer[index + 3] & 0xff) << 8) |
                           ((int)readBuffer[index + 4] & 0xff);
                        index += 4;
                        GlobInfo.inpCardProdId[cardIndex] = tmpData;
                        break;
                     }
                     case RS232I_GET_VERS:
                     {
                        tmpData = (((int)readBuffer[index + 1] & 0xff) << 24) |
                           (((int)readBuffer[index + 2] & 0xff) << 16) |
                           (((int)readBuffer[index + 3] & 0xff) << 8) |
                           ((int)readBuffer[index + 4] & 0xff);
                        index += 4;
                        GlobInfo.inpCardVers[cardIndex] = tmpData;
                        break;
                     }
                     case RS232I_READ_INP_BRD:
                     {
                        tmpData = (((int)readBuffer[index + 1] & 0xff) << 8) |
                           ((int)readBuffer[index + 2] & 0xff);
                        index += 2;
                        GlobInfo.inpCardData[cardIndex] = tmpData; /* HRS */
                        break;
                     }
                     default:
                     {
                        /* HRS: Illegal cmd/addr combination received */
                     }
                  }
               }
            }
            else if (((int)currData & CARD_ID_TYPE_MASK) == CARD_ID_SOL_CARD)
            {
               cardIndex = (int)currData & ~CARD_ID_TYPE_MASK;
               if (cardIndex < GlobInfo.numInpCards)
               {
                  /* Next byte is the command */
                  currData = readBuffer[++index];
                  switch (currData)
                  {
                     case RS232I_GET_SER_NUM:
                     {
                        tmpData = (((int)readBuffer[index + 1] & 0xff) << 24) |
                           (((int)readBuffer[index + 2] & 0xff) << 16) |
                           (((int)readBuffer[index + 3] & 0xff) << 8) |
                           ((int)readBuffer[index + 4] & 0xff);
                        index += 4;
                        GlobInfo.solCardSerNum[cardIndex] = tmpData;
                        break;
                     }
                     case RS232I_GET_PROD_ID:
                     {
                        tmpData = (((int)readBuffer[index + 1] & 0xff) << 24) |
                           (((int)readBuffer[index + 2] & 0xff) << 16) |
                           (((int)readBuffer[index + 3] & 0xff) << 8) |
                           ((int)readBuffer[index + 4] & 0xff);
                        index += 4;
                        GlobInfo.solCardProdId[cardIndex] = tmpData;
                        break;
                     }
                     case RS232I_GET_VERS:
                     {
                        tmpData = (((int)readBuffer[index + 1] & 0xff) << 24) |
                           (((int)readBuffer[index + 2] & 0xff) << 16) |
                           (((int)readBuffer[index + 3] & 0xff) << 8) |
                           ((int)readBuffer[index + 4] & 0xff);
                        index += 4;
                        GlobInfo.solCardVers[cardIndex] = tmpData;
                        break;
                     }
                     case RS232I_READ_SOL_INP:
                     {
                        tmpData = (int)readBuffer[index + 1] & 0xff;
                        index += 1;
                        GlobInfo.solCardData[cardIndex] = tmpData;
                        break;
                     }
                     default:
                     {
                        /* HRS: Illegal cmd/addr combination received */
                     }
                  }
               }
            }
         }
      }
      currBufIndex = 0;
   } /* end processCmdStr */
   
   /*
    * ===============================================================================
    * 
    * Name: closeSerPort
    * 
    * ===============================================================================
    */
   /**
    * Close serial port.
    * 
    * Close the serial port and release its resources.
    * 
    * @param   None 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public void closeSerPort()
   {
      if (currPort != null)
      {
         /* Close out the open serial port resources */
         try
         {
           serInpStream.close();
           serOutStream.close();
         } 
         catch (IOException e)
         {
           /* Closing down, so nothing to do if it fails. */
         }
         serialPort.close();
         GlobInfo.hostCtl.printMsg("Close COM port");
      }
   } /* end closeSerPort */
   
   /*
    * ===============================================================================
    * 
    * Name: createDebugFrm
    * 
    * ===============================================================================
    */
   /**
    * Create debug frame
    * 
    * Create the debug frame that lists all the received 
    * 
    * @param   None 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   private void createDebugFrm()
   {
      JFrame                        cardFrame = new JFrame("Card State");
      JPanel                        cardPanel = new JPanel(new BorderLayout());
      int                           cnt;
      GridBagConstraints            con = new GridBagConstraints();
      
      /* Initialize constraints */
      con.insets = new Insets(5,5,5,5);
      con.gridheight = 1;
      con.gridwidth = 1;
      con.weightx = 1;
      con.weighty = 1;
      con.gridx = 0;
      con.gridy = 0;
      
      if (GlobInfo.numInpCards != 0)
      {
         JPanel                        inpPanel = new JPanel(new GridBagLayout());
         JLabel                        tmpLabel = new JLabel("Input Card(s)");
         
         /* Add the title label */
         con.gridwidth = 5;
         con.gridx = 0;
         con.gridy = 0;
         inpPanel.add(tmpLabel, con);
         
         /* Add heading labels */
         tmpLabel = new JLabel("Addr");
         con.gridwidth = 1;
         con.gridy = 1;
         inpPanel.add(tmpLabel, con);
         tmpLabel = new JLabel("Inputs");
         con.gridwidth = 4;
         con.gridy = 1;
         con.gridx = 1;
         inpPanel.add(tmpLabel, con);
         
         for (cnt = 0; cnt < GlobInfo.numInpCards; cnt++)
         {
            con.gridwidth = 1;
            con.gridy = 2 + cnt;
            con.gridx = 0;
            tmpLabel = new JLabel(String.format("0x%02x:",  GlobInfo.inpCardAddr[cnt]));
            inpPanel.add(tmpLabel, con);

            con.gridwidth = 4;
            con.gridx = 1;
            GlobInfo.inpCardDbgLbl[cnt] = new JLabel(String.format("%16s",
                  Integer.toBinaryString(GlobInfo.inpCardData[cnt])).replace(' ', '0'));

            inpPanel.add(GlobInfo.inpCardDbgLbl[cnt], con);
         }
         cardPanel.add(inpPanel, BorderLayout.NORTH);
      }
      if (GlobInfo.numSolCards != 0)
      {
         JPanel                        solPanel = new JPanel(new GridBagLayout());
         JLabel                        tmpLabel = new JLabel("Solenoid Card(s)");
         
         /* Add the title label */
         con.gridwidth = 5;
         con.gridx = 0;
         con.gridy = 0;
         solPanel.add(tmpLabel, con);
         
         /* Add heading labels */
         tmpLabel = new JLabel("Addr");
         con.gridwidth = 1;
         con.gridy = 1;
         solPanel.add(tmpLabel, con);
         tmpLabel = new JLabel("Inputs");
         con.gridwidth = 4;
         con.gridy = 1;
         con.gridx = 1;
         solPanel.add(tmpLabel, con);
         
         for (cnt = 0; cnt < GlobInfo.numSolCards; cnt++)
         {
            con.gridwidth = 1;
            con.gridy = 2 + cnt;
            con.gridx = 0;
            tmpLabel = new JLabel(String.format("0x%02x:",  GlobInfo.solCardAddr[cnt]));
            solPanel.add(tmpLabel, con);

            con.gridwidth = 4;
            con.gridx = 1;
            GlobInfo.solCardDbgLbl[cnt] = new JLabel(String.format("%8s",
                  Integer.toBinaryString(GlobInfo.solCardAddr[cnt])).replace(' ', '0'));
            solPanel.add(GlobInfo.solCardDbgLbl[cnt], con);
         }
         cardPanel.add(solPanel, BorderLayout.CENTER);
      }
      if (GlobInfo.numLedCards != 0)
      {
         JPanel                        ledPanel = new JPanel(new GridBagLayout());
         JLabel                        tmpLabel = new JLabel("LED Lighting Card(s)");
         
         /* Add the title label */
         con.gridwidth = 5;
         con.gridx = 0;
         con.gridy = 0;
         ledPanel.add(tmpLabel, con);
         
         for (cnt = 0; cnt < GlobInfo.numLedCards; cnt++)
         {
            con.gridwidth = 1;
            con.gridy = 1 + cnt;
            con.gridx = 0;
            tmpLabel = new JLabel(String.format("Card %d:",  cnt + 1));
            ledPanel.add(tmpLabel, con);

            con.gridwidth = 4;
            con.gridx = 1;
            GlobInfo.ledCardDbgLbl[cnt] = new JLabel(String.format("%8s",
                  Integer.toBinaryString(GlobInfo.ledCardData[cnt])).replace(' ', '0'));
            ledPanel.add(GlobInfo.ledCardDbgLbl[cnt], con);
         }
         cardPanel.add(ledPanel, BorderLayout.SOUTH);
      }
      cardFrame.add(cardPanel);
      cardFrame.pack();
      cardFrame.setVisible(true);
      
   } /* end createDebugFrm */
   
   /*
    * ===============================================================================
    * 
    * Name: sendMsg
    * 
    * ===============================================================================
    */
   /**
    * Send message
    * 
    * Send a message
    * 
    * @param   buffer  - Message
    * @param   msgLen  - Message Length
    * @return  None
    * 
    * @pre     None 
    * @note    None
    * 
    * ===============================================================================
    */
   private void sendMsg(
      int[]                            buffer, 
      int                              msgLen)
   {
      int                              cnt;
      
      if (currPort != null)
      {
         try
         {
            for (cnt = 0; cnt < msgLen; cnt++)
            {
              serOutStream.write(buffer[cnt]);
            }
         } 
         catch (IOException e)
         {
            try
            {
              serInpStream.close();
              serOutStream.close();
            } 
            catch (IOException event)
            {
            }
            serialPort.close();
            System.exit(501);
         }
      }
   } /* end sendMsg */

} /* End SerIntf */
