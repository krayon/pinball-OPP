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

import java.io.*;
import java.util.Enumeration;
import java.util.TooManyListenersException;

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

   private static final int      MAX_READ_BUF_SIZE          = 64;
   private byte[]                readBuffer = new byte[MAX_READ_BUF_SIZE];
   private int                   currBufIndex;
   
   private static final int      RCV_IDLE                   = 0;
   private static final int      RCV_ADDR                   = 1;
   private static final int      RCV_CMD                    = 2;
   private static final int      WAIT_FOR_EOM               = 3;
   private int                   rcvState;
   private int                   rcvDataCtr;

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
   public static final int       CARD_ID_INP_CARD           = 0x00;

   public void SerIntf()
   {
      if (GlobInfo.debug)
      {
         /* Create frame for card rcv data */
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
   public int connectSerPort(String portName)
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
         System.out.println("Configuration not supported.  Default JVM is 32 Bit on 64 Bit OS.");
         return(INCORRECT_JVM_INSTALLED);
      }
      if (!found)
      {
         System.out.println("Can't re-attach to COM port.");
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
         System.exit(PORT_IN_USE_ERROR);
      }

      /* Set the serial port parameters */
      try
      {
         serialPort.setSerialPortParams(9600, SerialPort.DATABITS_8,
               SerialPort.STOPBITS_1, SerialPort.PARITY_NONE);
      } 
      catch (UnsupportedCommOperationException e)
      {
         serialPort.close();
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
         return(TOO_MANY_LISTENERS);
      }

      rcvState = RCV_IDLE;
      currBufIndex = 0;
      serialPort.notifyOnDataAvailable(true);
      serialPort.notifyOnCarrierDetect(true);
      System.out.println("SerIntf: Opened " + portName);
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
            if (GlobInfo.commGood)
            {
               try
               {
                  serInpStream.close();
                  serOutStream.close();
               } 
               catch (IOException except)
               {
               }
               /* serialPort.close(); Removed since it locks the program */
               System.exit(300);
            }
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
                     GlobInfo.chngFlag |= ChangeFlag.CF_RCV_DATA;
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
                     GlobInfo.chngFlag |= ChangeFlag.CF_RCV_DATA;
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
                  GlobInfo.solCardAddr[GlobInfo.numSolCards] =  readBuffer[++index];
                  GlobInfo.numSolCards++;
               }
               else if (((int)currData & CARD_ID_TYPE_MASK) == CARD_ID_INP_CARD)
               {
                  GlobInfo.inpCardAddr[GlobInfo.numInpCards] =  readBuffer[++index];
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
            if (((int)currData & CARD_ID_TYPE_MASK) == CARD_ID_SOL_CARD)
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
                        GlobInfo.inpCardData[cardIndex] = tmpData;
                        break;
                     }
                     default:
                     {
                        /* HRS: Illegal cmd/addr combination received */
                     }
                  }
               }
            }
            else if (((int)currData & CARD_ID_TYPE_MASK) == CARD_ID_INP_CARD)
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
      System.out.println("Close COM port");
   } /* end closeSerPort */
} /* End SerIntf */
