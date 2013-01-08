/*
 *===============================================================================
 *
 *                          HHHHH            HHHHH
 *                           HHH     SSSS     HHH
 *                           HHH   SSSSSSSS   HHH 
 *                           HHH  SSS    SSS  HHH       Hugh Spahr
 *                           HHH SSS      SSS HHH       Utilities
 *                           HHH  SSS         HHH
 *                           HHH    SSSS      HHH
 *                           HHHHHHHHHHHHHHHHHHHH
 *                           HHHHHHHHHHHHHHHHHHHH
 *                           HHH         SSS  HHH
 *                           HHH SSS      SSS HHH
 *                           HHH  SSS    SSS  HHH
 *                           HHH   SSSSSSSS   HHH
 *                           HHH     SSSS     HHH
 *                          HHHHH            HHHHH
 *
 *===============================================================================
 *
 * @file:   CodeDownload.java
 * @author: Hugh Spahr
 * @date:   10/4/2005
 *
 * @note    Copyright© 2005-2012, Hugh Spahr
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
 * Code Download is the main application class that allows downloading new
 * programs using Hugh Spahr's standard bootloader.
 *
 *===============================================================================
 */

import gnu.io.CommPortIdentifier;
import gnu.io.PortInUseException;
import gnu.io.SerialPort;
import gnu.io.SerialPortEvent;
import gnu.io.SerialPortEventListener;
import gnu.io.UnsupportedCommOperationException;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URL;
import java.security.CodeSource;
import java.security.ProtectionDomain;
import java.util.Enumeration;
import java.util.TooManyListenersException;
import java.util.jar.JarFile;

import javax.swing.BorderFactory;
import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JRadioButtonMenuItem;
import javax.swing.JScrollPane;
import javax.swing.JTabbedPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.Timer;
import javax.swing.UIManager;

public class CodeDownload extends JFrame implements SerialPortEventListener
{
   private static final long serialVersionUID = -1L;
   private static final String CODE_VERSION = "CodeDownload rev 0.3";
   private static final String BOOT_VERSION = "Supports Boot0.0";

   /* Enumeration for processor type */
   private static final int PROC_MICROCHIP      = 0;
   private static final int PROC_FREE_BIG       = 1;  /* Frescale, sector size 0x300 */
   private static final int PROC_FREE_SMALL     = 2;  /* Frescale, sector size 0x200 */
   
   private static final int NUM_PROC = 10;
   private static final String[] PROCESSOR = { "18F452", "18F4550", "18F6620",
      "FreeScale60K2K", "FreeScale48K1.5K", "FreeScale32K1K", "FreeScale16K.5K",
      "FreeScale16K0K", "FreeScale8K0K", "FreeScale4K0K",};
   private static final int[] EEPROM_SIZE = { 0x100, 0x100, 0x400,
      0x800, 0x600, 0x400, 0x200, 0x000, 0x000 };
   private static final int[] EEPROM_ADDR = { 0x0000, 0x0000, 0x0000,
      0x1400, 0x1500, 0x1600, 0x1700, 0x0000, 0x0000, 0x0000 };
   private static final int[] PROG_MEM_SIZE = { 0x8000, 0x8000, 0x10000,
      0xe700, 0xc000, 0x8400, 0x4200, 0x4000, 0x2000, 0x1000 };
   private static final int[] PIC_PROC = { PROC_MICROCHIP, PROC_MICROCHIP, PROC_MICROCHIP,
      PROC_FREE_BIG, PROC_FREE_BIG, PROC_FREE_BIG, PROC_FREE_BIG,
      PROC_FREE_SMALL, PROC_FREE_SMALL, PROC_FREE_SMALL };
   /* Note:  For 60K Freescale parts, CodeDownload does not support flash bytes
    *    from 0x1080 to 0x13ff.
    */

   private static final int FREE_SMALL_SECT_SIZE = 0x200;
   
   private boolean firstComm = true;
   private static final byte[] BOOT_MSG = { 'B', 'o', 'o', 't', '0', '.', '0',
         '\r' };
   private static final int BOOT_MSG_SIZE = 8;

   /* Lookup table for a standard CRC8. Generator polynomial is x^8+x^2+x+1.
    *    Initial passed value should be 0xff to conform to the ATM HEC CRC8
    */
   private static final byte[] CRC8_LOOKUP = { 0x00, 0x07, 0x0E, 0x09, 0x1C,
         0x1B, 0x12, 0x15, 0x38, 0x3F, 0x36, 0x31, 0x24, 0x23, 0x2A, 0x2D };

   /* Bits that are 0 are ignored (not implemented) in the PIC processor */
   private static final byte[][] CFG_VALID_BITS = {
         { (byte)0x00, (byte)0x27, (byte)0x0f, (byte)0x0f,
           (byte)0x00, (byte)0x01, (byte)0x85, (byte)0x00, 
           (byte)0xff, (byte)0xc0, (byte)0x0f, (byte)0xe0, 
           (byte)0x0f, (byte)0x40, (byte)0x00, (byte)0x00 },
         { (byte)0x3f, (byte)0xcf, (byte)0x3f, (byte)0x1f,
           (byte)0x00, (byte)0x87, (byte)0xe5, (byte)0x00,
           (byte)0x0f, (byte)0xc0, (byte)0x0f, (byte)0xe0,
           (byte)0x0f, (byte)0x40, (byte)0x00, (byte)0x00 },
         { (byte)0x00, (byte)0x27, (byte)0x0f, (byte)0x0f,
           (byte)0x83, (byte)0x01, (byte)0x85, (byte)0x00,
           (byte)0xff, (byte)0xc0, (byte)0xff, (byte)0xe0,
           (byte)0xff, (byte)0x40, (byte)0x00, (byte)0x00 }, };

   private static final char[] CMD_STAT_TBL = { '|', '/', '-', '\\' };
   private static final int NUM_CMD_STAT_TBL_ENTRIES = 4;

   /* Current state including what command is currently running */
   enum DOWNLOAD_STATE_E
   {
      WRITE_FLASH_RESP,
      READ_FLASH_RESP,
      WRITE_EEPROM_RESP,
      READ_EEPROM_RESP,
      CONNECT_RESP,
      IDLE,
      VERIFY_FLASH_RESP,
      VERSION_RESP
   };
   private DOWNLOAD_STATE_E currentState = DOWNLOAD_STATE_E.IDLE;
   private int bootMsgIndex = 0;

   /* Info on the valid COM ports that can be selected */
   private Enumeration<?> portList;
   private static final int MAX_COMM_PORTS = 32;
   private CommPortIdentifier[] portId = new CommPortIdentifier[MAX_COMM_PORTS];
   private String[] portName = new String[MAX_COMM_PORTS];
   private CommPortIdentifier currPort;

   /* Various flags that indicate changes (passes info from event thread to
    *    common execution thread.
    */
   private boolean commChanged = false;
   private boolean connected = false;
   private boolean msgTabRcvBytes = false;
   private boolean clearRunningCmd = false;
   private boolean clearFlash = false;

   /* Groups of buttons for radio buttons on menus that only one can be selected. */
   private ButtonGroup commGroup;
   private ButtonGroup baudGroup;
   private ButtonGroup procGroup;

   /* Serial port streams. */
   private SerialPort serialPort;
   private InputStream inputStream;
   private OutputStream outputStream;

   /* Current information about the selected processor */
   private int currProcIndex;
   private int eeprom_size = 0;
   private int flash_size = 0;
   private int procType;
   private int eeprom_addr = 0;

   /* EEProm write objects */
   private JPanel writeEEPROMTab;
   private JLabel eepromAddrLabel;
   private JTextField eepromAddr;
   private JLabel eepromDataLabel;
   private JTextField eepromDataInp;

   /* Info needed to rcv msgs */
   private static final int RCV_BUFFER_SIZE = 20;
   byte[] rcvBuffer = new byte[RCV_BUFFER_SIZE];
   private int rcvBufIndex;
   private int progCfgIndex;
   private int readIndex;
   private int respBytes;
   private boolean badMsg;

   /* Info for programming Flash and reading hex files */
   private File hexFile = null;
   private BufferedReader hexReader;
   private int upperProgAddr;
   private int baseAddr;
   private int maxProgAddr;
   private byte[] progDataArray;
   private byte[] cfgDataArray;
   boolean fileDone = false;

   /* Locations that are determined by the boot loader application. */
   private static final int PIC_BOOT_START = 0x00000000;
   private static final int FREESCALE_BOOT_START = 0x0000fd00;
   private static final int BOOT_SIZE = 0x300;
   private static final int FREESCALE_SMALL_BOOT_START = 0x0000fc00;
   private static final int FREESCALE_SMALL_BOOT_SIZE = 0x400;
   private static final int PIC_CODE_SIZE_START = 0x300;
   private static final int CODE_SIZE_FIELD = 4;
   private static final int CFG_BIT_START = 0x300000;
   private static final int CFG_BIT_END = 0x300010;
   private static final int FREESCALE_EEPROM_PAGE_TWO = 0x00008000;

   /* Timeouts for receiving cmds from the unit */
   private int timeOutCount;
   private boolean timeoutRunning = false;
   private static final int MAX_TIMEOUT = 8; /* Allow responses to take 4s */

   /* Enumeration for Labels */
   private static final int COMM_LABEL          = 0;
   private static final int CHECKSUM_LABEL      = 1;
   private static final int CONNECT_LABEL       = 2;
   private static final int PROC_LABEL          = 3;
   private static final int FILE_LABEL          = 4;
   private static final int VERS_LABEL          = 5;
   private static final int MAX_STAT_LABEL      = 6;
   private JLabel[] statLabel = new JLabel[MAX_STAT_LABEL];

   /* Enumeration for log tabs */
   private static final int MAIN_TAB            = 0;
   private static final int MSG_TAB             = 1;
   private static final int PROG_MEM_TAB        = 2;
   private static final int EEPROM_TAB          = 3;
   private static final int MAX_NUM_TABS        = 4;
   private JTextArea[] tabs = new JTextArea[MAX_NUM_TABS];

   /* Use for updating the command state */
   private JLabel cmdStatusLabel;
   private int cmdStatusCount = 0;

   // Enumeration for Buttons
   private static final int CONNECT_BUTTON      = 0;
   private static final int DOWNLOAD_BUTTON     = 1;
   private static final int VERIFY_BUTTON       = 2;
   private static final int READ_FLASH_BUTTON   = 3;
   private static final int READ_EEPROM_BUTTON  = 4;
   private static final int BOOT_BUTTON         = 5;
   private static final int VERSION_BUTTON      = 6;
   private static final int WRITE_EEPROM_BUTTON = 7;
   private static final int MAX_BUTTONS         = 8;
   private JButton[] buttons = new JButton[MAX_BUTTONS];
   private int buttonPressed = 0;

   /* Transmit and rcv info */
   private static final byte STX                = 0x5a;
   private static final byte WRITE_FLASH_CMD    = 0x00;
   private static final byte READ_FLASH_CMD     = 0x01;
   private static final byte WRITE_EEPROM_CMD   = 0x02;
   private static final byte READ_EEPROM_CMD    = 0x03;
   private static final byte WRITE_CFG_CMD      = 0x04;
   private static final byte GET_BOOT_REV_CMD   = 0x05;
   private static final byte BOOT_CMD           = (byte)0x80;
   private static final byte VERSION_CMD        = (byte)'?';
   
   /*
    * ===============================================================================
    * 
    * Name: main
    * 
    * ===============================================================================
    */
   /**
    * Main Java entrance function to the application.
    * 
    * Interface with an attached device via a serial port. Create the dll files
    * from the application jar and save them to the local directory. Then create
    * an instance of CodeDownload to start the Code Download GUI.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre None 
    * \note None
    * 
    * ===============================================================================
    */
   public static void main(final String args[])
   {
      try
      {
         UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
      } 
      catch (Exception e)
      {
         System.out.println("Error setting native LAF: " + e);
      }

      /* Create a dummy class to figure out the current path. This is needed so
       * we can extract the .dll from the application jar. Needed so application
       * can be deployed as two small files (CodeDownload.exe and
       * CodeDownload.jar).
       */
      HexFilter app = new HexFilter();
      Class<?> cls = app.getClass();
      ProtectionDomain pDomain = cls.getProtectionDomain();
      CodeSource cSource = pDomain.getCodeSource();
      URL loc = cSource.getLocation();

      /* Check if we are running in development or end application mode. This is
       * so the project can be run within Eclipse, or as an end app. If we are
       * runnning as an application, "CodeDownload.jar!" will be in the path.
       * This also accounts for running as java -jar CodeDownload.jar
       */
      System.out.println("Loc:\t" + loc.toString());
      if (loc.toString().contains("main/main.jar"))
      {
         try
         {
            String tmpStr = new String();
            
            /* outFile contains the name of the .dll that we are creating */
            tmpStr = loc.toString().replaceAll("CodeDownload.jar!/main/main.jar",
               "rxtxSerial.dll").replaceAll("main/main.jar",
               "rxtxSerial.dll").replaceAll("file:", "").replaceAll(
               "jar:", "").replaceAll("%20", " ");
            System.out.println("Create New File: " + tmpStr);
            File outFile = new File(tmpStr);
            if (!outFile.exists())
            {
               /* The .dll doesn't exist, so create it. */
               System.out.println("Creating File");
               outFile.deleteOnExit();
               tmpStr = loc.toString().replaceAll("CodeDownload.jar!/main/main.jar",
                  "CodeDownload.jar").replaceAll("main/main.jar",
                  "CodeDownload.jar").replaceAll("file:", "").replaceAll(
                  "jar:", "").replaceAll("%20", " ");
               System.out.println("Opening File: " + tmpStr);
               
               /* The inFile is the name of the jar that contains the .dll */
               File inFile = new File(tmpStr);
               FileOutputStream out = new FileOutputStream(outFile);
               JarFile jar = new JarFile(inFile);
               InputStream dllFile = jar.getInputStream(jar.getEntry(
                  "lib/rxtxSerial.dll"));
               
               /* Copy the file to a real file on the file system so it can be
                *    linked at runtime.
                */
               int c;
               while ((c = dllFile.read()) != -1)
               {
                  out.write(c);
               }
               out.close();
               dllFile.close();
            }
         } 
         catch (IOException e)
         {
            e.printStackTrace();
         }
      } 
      else
      {
         System.out.println("Driver file not created.");
      }

      /* Create the Code Download GUI */
      new CodeDownload();
   }

   /*
    * ===============================================================================
    * 
    * Name: codeDownload
    * 
    * ===============================================================================
    */
   /**
    * Main class to create the Code Download GUI.
    * 
    * Call createWindow to create the windows that make up the pretty GUI interface,
    * and start a 500 ms timer.  This timer services button presses and menu
    * selections, so only a single cmd can be running at a time. 
    * 
    * \param   None 
    * \return  None
    * 
    * \pre None 
    * \note None
    * 
    * ===============================================================================
    */
   public CodeDownload()
   {
      createWindow();

      Timer timer = new Timer(500, new ActionListener()
      {
         public void actionPerformed(ActionEvent evt)
         {
            if (commChanged)
            {
               /* Update the status label and write msg that COM port changed */
               commChanged = false;
               tabs[MAIN_TAB].append("Comm = " + portName[Integer.parseInt(
                  commGroup.getSelection().getActionCommand())] + "\n");
               statLabel[COMM_LABEL].setText(portName[Integer.parseInt(
                  commGroup.getSelection().getActionCommand())] + ", 19200, 8, N, 1");

               /* Check if we were using a serial port, if so, close it out */
               if (currPort != null)
               {
                  /* Close out the open serial port resources */
                  try
                  {
                     inputStream.close();
                     outputStream.close();
                  } 
                  catch (IOException e)
                  {
                     /* Closing down, so nothing to do if it fails. */
                  }
                  serialPort.close();
               }
               
               /* Try connecting to the new serial port */
               connectSerPort();
               sendConnectMsg();
            }
            else if (buttonPressed != 0)
            {
               /* Find out what button has been pressed, only allow one to be
                * pressed at a time.
                */
               if ((buttonPressed & (1 << CONNECT_BUTTON)) != 0)
               {
                  /* The connect button is also the stop currently running
                   * command button.  Treat a press appropriately. 
                   */
                  if (currentState == DOWNLOAD_STATE_E.IDLE)
                  {
                     sendConnectMsg();
                  } 
                  else
                  {
                     clearRunningCmd = true;
                  }
                  buttonPressed = 0;
               }
               if ((buttonPressed & (1 << DOWNLOAD_BUTTON)) != 0)
               {
                  progFlash();
                  buttonPressed = 0;
               }
               if ((buttonPressed & (1 << VERIFY_BUTTON)) != 0)
               {
                  verifyCode();
                  buttonPressed = 0;
               }
               if ((buttonPressed & (1 << READ_FLASH_BUTTON)) != 0)
               {
                  readFlash();
                  buttonPressed = 0;
               }
               if ((buttonPressed & (1 << READ_EEPROM_BUTTON)) != 0)
               {
                  readEEProm();
                  buttonPressed = 0;
               }
               if ((buttonPressed & (1 << BOOT_BUTTON)) != 0)
               {
                  sendBoot();
                  buttonPressed = 0;
               }
               if ((buttonPressed & (1 << VERSION_BUTTON)) != 0)
               {
                  sendVersion();
                  buttonPressed = 0;
               }
               if ((buttonPressed & (1 << WRITE_EEPROM_BUTTON)) != 0)
               {
                  writeEEProm();
                  buttonPressed = 0;
               }

               /* If not in the idle state, disable all buttons but the
                * end command button.
                */
               if (currentState != DOWNLOAD_STATE_E.IDLE)
               {
                  int index;

                  /* Grey out all the buttons except Connect button which is
                   * renamed to End Cmd.  Note: Button 0 is the connect button.
                   */
                  for (index = 1; index < MAX_BUTTONS; index++)
                  {
                     buttons[index].setEnabled(false);
                  }
                  buttons[CONNECT_BUTTON].setText("End Cmd");
               }
            }
            
            /* If a timeout is running, check if a gross timout happened */
            if (timeoutRunning)
            {
               timeOutCount++;
               if (timeOutCount > MAX_TIMEOUT)
               {
                  tabs[MAIN_TAB].append("TIMEOUT:  Resp not rcv'd in time.\n");
                  goToIdleState();
               }
            }
         }
      });
      timer.start();
   }

   /*
    * ===============================================================================
    * 
    * Name: createWindow
    * 
    * ===============================================================================
    */
   /**
    * Create window method to create the GUI Window.
    * 
    * Create the frame, and set it's size.  Call createMenus to create the menu
    * toolbar.  Create the status bar and all of it's labels.  Next create the button
    * bar with all of it's buttons.  Finally create the logging tabs which take
    * up the remainder of the frame. 
    * 
    * \param   None 
    * \return  None
    * 
    * \pre None 
    * \note None
    * 
    * ===============================================================================
    */
   private void createWindow()
   {
      final String[]                STAT_LABEL = {"      19200, 8, N, 1", 
                                       "Checksum:       ", "Connected: No ",
                                       "Proc: None   ", "File: None",
                                       "Vers: Unknown"};
      final String[]                BUTTON_LABEL = {"Connect", "Download", 
                                       "Verify", "Read Flash", "Read EEPROM",
                                       "Boot", "Version", "Write" };
      final String[]                LOG_TAB = { "Main", "Msgs", "Prog Mem", "EEPROM" };

      int index;

      /* Create the main window */
      setTitle("Code Download Manager");
      setSize(720, 400);
      setResizable(false);
      addWindowListener(new WindowAdapter()
      {
         public void windowClosing(WindowEvent winEvt)
         {
            System.exit(0);
         }
      });

      /* Create the menu bar */
      createMenus();

      JPanel mainPanel = new JPanel();
      mainPanel.setLayout(new BorderLayout());

      JPanel statActionPanel = new JPanel();
      statActionPanel.setLayout(new GridLayout(2, 0));

      /* Create the status bar */
      JPanel statusPanel = new JPanel();
      statusPanel.setLayout(new FlowLayout(FlowLayout.LEFT));
      JLabel status = new JLabel("Status:");
      status.setFont(status.getFont().deriveFont(
            status.getFont().getStyle() ^ Font.BOLD));
      statusPanel.add(status);
      for (index = 0; index < MAX_STAT_LABEL; index++)
      {
         statLabel[index] = new JLabel(STAT_LABEL[index]);
         statLabel[index].setBorder(BorderFactory.createCompoundBorder(
               BorderFactory.createLoweredBevelBorder(), BorderFactory
                     .createEmptyBorder(0, 5, 0, 5)));
         statusPanel.add(statLabel[index]);
      }

      /* Create the button bar which is just below the status bar */
      JPanel buttonPanel = new JPanel();
      buttonPanel.setLayout(new FlowLayout(FlowLayout.LEFT));
      for (index = 0; index < MAX_BUTTONS; index++)
      {
         buttons[index] = new JButton(BUTTON_LABEL[index]);
         buttons[index].setActionCommand(Integer.toString(index));
         buttons[index].addActionListener(new ActionListener()
         {
            public void actionPerformed(ActionEvent e)
            {
               /* Buttons use the index into the button array to identify
                *    themselves and set the correct buttonPressed bitfield.
                */
               buttonPressed |= (1 << (Integer.parseInt(e.getActionCommand())));
            }
         });
         /* The write EEPROM button is on the EEPROM write tab */
         if (index != WRITE_EEPROM_BUTTON)
         {
            buttonPanel.add(buttons[index]);
         }
         buttons[index].setEnabled(false);
      }

      /* Command status label is at the end of the button bar to allow plenty
       *    of space for the name of the hex file.
       */
      cmdStatusLabel = new JLabel("Cmd Stat Idle");
      cmdStatusLabel.setBorder(BorderFactory.createCompoundBorder(BorderFactory
            .createLoweredBevelBorder(), BorderFactory.createEmptyBorder(0, 5,
            0, 5)));
      buttonPanel.add(cmdStatusLabel);

      /* Put the two status and button bars on the main frame */
      statActionPanel.add(statusPanel);
      statActionPanel.add(buttonPanel);
      mainPanel.add(statActionPanel, BorderLayout.NORTH);

      JTabbedPane tabPane = new JTabbedPane();

      /* Create the logging tabs: One for general messages, one for xmt/rcv
       *    msgs from the box, one for displaying program memory, and the
       *    last displays EEPROM memory.
       */
      for (index = 0; index < MAX_NUM_TABS; index++)
      {
         tabs[index] = new JTextArea(13, 48);
         tabs[index].setEditable(false);
         tabPane.addTab(LOG_TAB[index], new JScrollPane(tabs[index]));
      }

      /* Create the write EEPROM tab which isn't a logging tab, but
       * allows a user to write a byte to the EEPROM.
       */
      writeEEPROMTab = new JPanel();
      eepromAddrLabel = new JLabel("EEPROM Addr: ");
      eepromAddr = new JTextField("0x00", 5);
      eepromDataLabel = new JLabel("Data: ");
      eepromDataInp = new JTextField("0x00", 4);
      writeEEPROMTab.add(eepromAddrLabel);
      writeEEPROMTab.add(eepromAddr);
      writeEEPROMTab.add(eepromDataLabel);
      writeEEPROMTab.add(eepromDataInp);
      writeEEPROMTab.add(buttons[WRITE_EEPROM_BUTTON]);
      tabPane.addTab("EEPROM Write", writeEEPROMTab);

      mainPanel.add(tabPane, BorderLayout.CENTER);
      add(mainPanel);

      /* Make the window visible */
      setVisible(true);
   }

   /*
    * ===============================================================================
    * 
    * Name: createMenus
    * 
    * ===============================================================================
    */
   /**
    * Create the menu bar at the top of the window.
    * 
    * Create the menubar.  This allows the user to pick single items using radio
    * buttons.  They can pick COM port, processor, and a file open menu to get
    * a hex file to be downloaded.  If a file is opened the readHexFile method
    * is called to verify that the hex file is valid for the processor.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre None 
    * \note None
    * 
    * ===============================================================================
    */
   private void createMenus()
   {
      int                           portNum;
      int                           procIndex;

      JMenuBar menuBar = new JMenuBar();

      /* The file open allows the user to choose a hex file to read into memory.
       *    If a file is chosen, call readHexFile to insure the processor can
       *    support it.
       */
      JMenu fileMenu = new JMenu("File");
      JMenuItem openFile = new JMenuItem("Open");
      openFile.addActionListener(new ActionListener()
      {
         public void actionPerformed(ActionEvent e)
         {
            if (flash_size == 0)
            {
               tabs[MAIN_TAB].append("Proc must be chosen before hex file.\n");
            } 
            else
            {
               JFileChooser fileChoice = new JFileChooser();
               
               /* Only allow hex/s-record files to be chosen. */
               fileChoice.setFileFilter(new HexFilter());
               int retVal = fileChoice.showOpenDialog(CodeDownload.this);
               if (retVal == JFileChooser.APPROVE_OPTION)
               {
                  hexFile = fileChoice.getSelectedFile();
                  statLabel[FILE_LABEL].setText("File: " + hexFile.getName());
                  tabs[MAIN_TAB].append("File " + hexFile.getName() + " Selected\n");
                  
                  /* Verify the file is valid */
                  if (readHexFile())
                  {
                     /* If not, set handle to null to indicate no valid hex file */
                     hexFile = null;
                     statLabel[FILE_LABEL].setText("File:");
                     tabs[MAIN_TAB].append("Hex file incorrect format\n");
                     statLabel[CHECKSUM_LABEL].setText("Checksum:       ");
                  }
               }
            }
         }
      });
      fileMenu.add(openFile);

      /* Create the Comm menu which lists all of the valid COM ports. */
      JMenu commMenu = new JMenu("Comm");
      commGroup = new ButtonGroup();

      /* Walk through the port list looking for serial ports */
      portList = CommPortIdentifier.getPortIdentifiers();
      for (portNum = 0; portList.hasMoreElements()
            && (portNum < MAX_COMM_PORTS); portNum++)
      {
         currPort = (CommPortIdentifier) portList.nextElement();
         portId[portNum] = currPort;
         if (currPort.getPortType() == CommPortIdentifier.PORT_SERIAL)
         {
            /* If so, add an item to the comm menu with the name of the port */
            JRadioButtonMenuItem commPort = new JRadioButtonMenuItem(currPort
                  .getName());
            
            /* Fill out the portName array used to connect to the port */
            portName[portNum] = currPort.getName();
            commPort.setActionCommand(Integer.toString(portNum));
            commPort.addActionListener(new ActionListener()
            {
               public void actionPerformed(ActionEvent e)
               {
                  commChanged = true;
               }
            });
            
            /* Since only 1 comm port can be selected, use create a group
             * of buttons.
             */
            commMenu.add(commPort);
            commGroup.add(commPort);
         }
      }

      /* No current port, as soon as user selects, this will be filled out */
      currPort = null;
      if (portNum == MAX_COMM_PORTS)
      {
         /* Can't support this many serial ports */
         System.exit(1);
      }

      /* Only support 19.2 kbps.  Probably won't support more speeds but
       *    set up the framework for later.
       */
      JMenu baudMenu = new JMenu("Baud");
      baudGroup = new ButtonGroup();
      JRadioButtonMenuItem baudRate = new JRadioButtonMenuItem("19200");
      baudRate.setActionCommand("19200");
      baudRate.setSelected(true);
      baudRate.addActionListener(new ActionListener()
      {
         public void actionPerformed(ActionEvent e)
         {
            tabs[MAIN_TAB].append("Curr Baud: "
                  + baudGroup.getSelection().getActionCommand() + "\n");
         }
      });
      baudMenu.add(baudRate);
      baudGroup.add(baudRate);

      /* Set up all the currently used processors.  Each processor
       *    needs an entry listing the EEPROM size and the program
       *    mem size.
       */
      JMenu procMenu = new JMenu("Processor");
      procGroup = new ButtonGroup();
      for (procIndex = 0; procIndex < NUM_PROC; procIndex++)
      {
         JRadioButtonMenuItem proc = new JRadioButtonMenuItem(
               PROCESSOR[procIndex]);
         proc.setActionCommand(Integer.toString(procIndex));
         proc.addActionListener(new ActionListener()
         {
            /* If a processor is selected, fill out EEPROM and
             *    program mem size.
             */
            public void actionPerformed(ActionEvent e)
            {
               statLabel[PROC_LABEL].setText("Proc: "
                     + PROCESSOR[Integer.parseInt(procGroup.getSelection()
                           .getActionCommand())]);
               eeprom_size = EEPROM_SIZE[Integer.parseInt(procGroup
                     .getSelection().getActionCommand())];
               currProcIndex = Integer.parseInt(procGroup.getSelection()
                     .getActionCommand());
               flash_size = PROG_MEM_SIZE[currProcIndex];
               procType = PIC_PROC[currProcIndex];
               eeprom_addr = EEPROM_ADDR[currProcIndex];
               tabs[MAIN_TAB].append("Processor: " + PROCESSOR[currProcIndex] + "\n");
               if ((procType == PROC_FREE_BIG) || (procType == PROC_FREE_SMALL))
               {
                  baseAddr = 0x10000 - flash_size;
                  tabs[MAIN_TAB].append("Base Flash Addr:" + String.format(" 0x%04x", baseAddr) + "\n");
                  if (procType == PROC_FREE_BIG)
                  {
                     tabs[MAIN_TAB].append("Base EEPROM Addr:" + String.format(" 0x%04x", eeprom_addr) + "\n\n");
                  }
               }
               else if (procType == PROC_MICROCHIP)
               {
                  baseAddr = 0x0000;
               }
               if (hexFile != null)
               {
                  /* Reverify that the hex file works for this processor */
                  if (readHexFile())
                  {
                     hexFile = null;
                     statLabel[FILE_LABEL].setText("File:");
                     tabs[MAIN_TAB].append("Hex file incorrect format\n");
                     statLabel[CHECKSUM_LABEL].setText("Checksum:       ");
                  }
               }
            }
         });
         procMenu.add(proc);
         procGroup.add(proc);
      }

      /* Create the about menu which lists Code Download rev and supported
       *    bootcode revisions.
       */
      JMenu aboutMenu = new JMenu("About");
      JMenuItem revision = new JMenuItem(CODE_VERSION);
      JMenuItem boot_rev = new JMenuItem(BOOT_VERSION);
      aboutMenu.add(revision);
      aboutMenu.add(boot_rev);

      /* Create the help menu which is a simple how to download code. */
      JMenu helpMenu = new JMenu("Help");
      helpMenu.add(new JMenuItem("Updating code on a box"));
      helpMenu.add(new JMenuItem("1: Choose COM port from Comm menu"));
      helpMenu.add(new JMenuItem("2: Choose processor from Proc menu"));
      helpMenu.add(new JMenuItem("3: Choose hex file from File->Open menu"));
      helpMenu.add(new JMenuItem("4: Press download button"));
      
      menuBar.add(fileMenu);
      menuBar.add(commMenu);
      menuBar.add(baudMenu);
      menuBar.add(procMenu);
      menuBar.add(aboutMenu);
      menuBar.add(helpMenu);
      setJMenuBar(menuBar);
   }

   /*
    * ===============================================================================
    * 
    * Name: sendMsg
    * 
    * ===============================================================================
    */
   /**
    * Send a message out the serial port.
    * 
    * Send message sends a message on the serial port.  It checks if the clear cmd
    * flag is set, and cancels the current command by calling goToIdleState. 
    * Otherwise it updates the current state to the passed next state.
    * 
    * \param   byteArray [in] array of bytes to be sent 
    * \param   numBytes  [in] number of bytes to be sent 
    * \param   nextState [in] next command state 
    * \return  None
    * 
    * \pre None 
    * \note None
    * 
    * ===============================================================================
    */
   private void sendMsg(
      byte[]                        byteArray,  /* data to be sent */
      int                           numBytes,   /* number of bytes to be sent */
      DOWNLOAD_STATE_E              nextState)  /* next command state */
   {
      int                           index;

      if (clearRunningCmd)
      {
         tabs[MAIN_TAB].append("Cmd cancelled.\n");
         clearRunningCmd = false;
         goToIdleState();
      } 
      else
      {
         currentState = nextState;
         
         /* Increment the command status count so that the status spinner works */
         cmdStatusCount = (cmdStatusCount + 1) & (NUM_CMD_STAT_TBL_ENTRIES - 1);
         
         /* Update status label */
         switch (currentState)
         {
            case WRITE_FLASH_RESP:
            {
               cmdStatusLabel.setText("Prog Flash:  " +
                  CMD_STAT_TBL[cmdStatusCount]);
               break;
            }
            case READ_FLASH_RESP:
            {
               cmdStatusLabel.setText("Read Flash:  " +
                  CMD_STAT_TBL[cmdStatusCount]);
               break;
            }
            case READ_EEPROM_RESP:
            {
               cmdStatusLabel.setText("Read EEPROM: " +
                  CMD_STAT_TBL[cmdStatusCount]);
               break;
            }
            case VERIFY_FLASH_RESP:
            {
               cmdStatusLabel.setText("Verify Code: " +
                  CMD_STAT_TBL[cmdStatusCount]);
               break;
            }
         }
         
         /* Start rcving next msg at start of rcv buffer */
         rcvBufIndex = 0;
         if (msgTabRcvBytes)
         {
            tabs[MSG_TAB].append("\n");
            msgTabRcvBytes = false;
         }
         tabs[MSG_TAB].append("Xmt:");
         
         /* Write the bytes to the serial port, and log them.  If
          *    an error occurs, exit.
          */
         for (index = 0; index < numBytes; index++)
         {
            tabs[MSG_TAB].append(String.format(" 0x%02x", byteArray[index]));
            try
            {
               outputStream.write((int) byteArray[index]);
            } 
            catch (IOException e)
            {
               try
               {
                  inputStream.close();
                  outputStream.close();
               } 
               catch (IOException event)
               {
               }
               serialPort.close();
               System.exit(6);
            }
         }
         tabs[MSG_TAB].append("\n");
         
         /* Set the timeout running if expect a response */
         if (nextState != DOWNLOAD_STATE_E.IDLE)
         {
            timeoutRunning = true;
            timeOutCount = 0;
         } 
         else
         {
            /* This is the boot cmd, can't guarantee app response */
            timeoutRunning = false;
            currentState = DOWNLOAD_STATE_E.IDLE;
            cmdStatusLabel.setText("Cmd Stat Idle");
            buttons[CONNECT_BUTTON].setText("Connect");
         }
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
    * \param   None 
    * \return  None
    * 
    * \pre None 
    * \note None
    * 
    * ===============================================================================
    */
   private void connectSerPort()
   {
      currPort = portId[Integer.parseInt(commGroup.getSelection().getActionCommand())];
      try
      {
         /* Grab port and wait up to 2 seconds to acquire it. */
         serialPort = (SerialPort) currPort.open("CodeDownloadApp", 2000);
      } 
      catch (PortInUseException e)
      {
         /* Couldn't open serial port */
         System.exit(2);
      }

      /* Set the serial port parameters */
      try
      {
         serialPort.setSerialPortParams(Integer.parseInt(baudGroup.getSelection().getActionCommand()),
            SerialPort.DATABITS_8, SerialPort.STOPBITS_1, SerialPort.PARITY_NONE);
      } 
      catch (UnsupportedCommOperationException e)
      {
         serialPort.close();
         System.exit(3);
      }

      try
      {
         inputStream = serialPort.getInputStream();
         outputStream = serialPort.getOutputStream();
      } 
      catch (IOException e)
      {
         /* Couldn't get input or output stream */
         serialPort.close();
         System.exit(4);
      }

      /* Notify us when a byte is received */
      try
      {
         serialPort.addEventListener(CodeDownload.this);
      } 
      catch (TooManyListenersException e)
      {
         try
         {
            inputStream.close();
            outputStream.close();
         } 
         catch (IOException event)
         {
         }
         serialPort.close();
         System.exit(5);
      }

      serialPort.notifyOnDataAvailable(true);
   }

   /*
    * ===============================================================================
    * 
    * Name: sendConnectMsg
    * 
    * ===============================================================================
    */
   /**
    * Send connect message.
    * 
    * Send a message to get the boot loader rev.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre None 
    * \note We send 13 STX characters first to make sure that any command that is
    *    in process is flushed.  The maximum length of a cmd is 13 bytes, so worst
    *    case, we need to send 12 bytes to flush it.  Then all msgs must start with
    *    an STX (hence 13 bytes).
    * 
    * ===============================================================================
    */
   private void sendConnectMsg()
   {
      /* Send a hello handshake */
      byte                          getBootRev[] = { STX, GET_BOOT_REV_CMD };
      byte                          helloArray[] = { STX };
      int                           loop;

      if (currPort != null)
      {
         statLabel[CONNECT_LABEL].setText("Connected: No ");
         connected = false;
         for (loop = 0; loop < MAX_BUTTONS; loop++)
         {
            if ((loop != CONNECT_BUTTON) && (loop != VERSION_BUTTON))
            {
               buttons[loop].setEnabled(false);
            }
         }
         for (loop = 0; loop < 13; loop++)
         {
            sendMsg(helloArray, 1, DOWNLOAD_STATE_E.CONNECT_RESP);
            timeoutRunning = false;
            try 
            {
               Thread.sleep(100);
            }
            catch (InterruptedException e) { }
         }
         sendMsg(getBootRev, 2, DOWNLOAD_STATE_E.CONNECT_RESP);
      } 
      else
      {
         tabs[MAIN_TAB].append("No serial port chosen.  Can't connect.\n");
      }
   }

   /*
    * ===============================================================================
    * 
    * Name: readFlash
    * 
    * ===============================================================================
    */
   /**
    * Read Flash command.
    * 
    * Start to read the flash/program memory from the PIC processor.  This sends the
    * first command and the rest of the commands are sent from processRcvData method.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre     None 
    * \note    None
    * 
    * ===============================================================================
    */
   private void readFlash()
   {
      byte                          readFlashCmd[] = { STX, READ_FLASH_CMD, 0x00,
                                       0x00, 0x00 };

      if (connected && (flash_size > 0))
      {
         readIndex = baseAddr;
         readFlashCmd[2] = (byte)((baseAddr >> 16) & 0xff);
         readFlashCmd[3] = (byte)((baseAddr >> 8) & 0xff);
         readFlashCmd[4] = (byte)(baseAddr & 0xff);
         respBytes = 14;
         badMsg = false;
         sendMsg(readFlashCmd, 5, DOWNLOAD_STATE_E.READ_FLASH_RESP);
      } 
      else
      {
         tabs[MAIN_TAB].append("Serial port not connected or no processor chosen."
               + " Can't read Flash.\n");
      }
   }

   /*
    * ===============================================================================
    * 
    * Name: readEEProm
    * 
    * ===============================================================================
    */
   /**
    * Read EEPROM command.
    * 
    * Start to read the EEPROM from the PIC processor.  This sends the
    * first command and the rest of the commands are sent from processRcvData method.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre     None 
    * \note    None
    * 
    * ===============================================================================
    */
   private void readEEProm()
   {
      byte                          eepromData[] = { STX, READ_EEPROM_CMD, 0x00, 0x00 };

      if (connected && (eeprom_size > 0))
      {
         readIndex = eeprom_addr;
         eepromData[2] = (byte)((readIndex >> 8) & 0xff);
         eepromData[3] = (byte)(readIndex & 0xff);
         respBytes = 6;
         badMsg = false;
         sendMsg(eepromData, 4, DOWNLOAD_STATE_E.READ_EEPROM_RESP);
      } 
      else
      {
         tabs[MAIN_TAB].append("Serial port not connected or no processor chosen." +
            "  Can't read EEPROM.\n");
      }
   }

   /*
    * ===============================================================================
    * 
    * Name: progFlash
    * 
    * ===============================================================================
    */
   /**
    * Write the program memory from the hex image that was loaded.
    * 
    * Start writing the program memory.  The hex image has already been loaded into
    * a local byte array.  After the program memory is written, the config bits are
    * written.  This method only sends the first command, the rest are sent from
    * processRcvData method.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre     None 
    * \note    None
    * 
    * ===============================================================================
    */
   private void progFlash()
   {
      byte                          writeFlash[] = { STX, WRITE_FLASH_CMD,
                                       0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x00 };
      int                           copyIndex;

      /* Verify that the file is OK, and we are configured */
      if ((hexFile != null) && connected)
      {
         if (procType == PROC_MICROCHIP)
         {
            readIndex = BOOT_SIZE;
            progCfgIndex = 0;
         }
         else
         {
            /* No configuration data for Freescale processors */
            readIndex = baseAddr;
            progCfgIndex = 16;
            clearFlash = false;
         }
         for (copyIndex = 0; copyIndex < 3; copyIndex++)
         {
            writeFlash[copyIndex + 2] = (byte) ((readIndex >> (16 - (copyIndex * 8))) & 0xff);
         }
         for (copyIndex = 0; copyIndex < 8; copyIndex++)
         {
            writeFlash[copyIndex + 5] = progDataArray[readIndex - baseAddr + copyIndex];
         }
         writeFlash[13] = calculateCrc8(12, writeFlash, 1);
         respBytes = 5;
         badMsg = false;
         sendMsg(writeFlash, 14, DOWNLOAD_STATE_E.WRITE_FLASH_RESP);
      } 
      else
      {
         tabs[MAIN_TAB].append("Serial port not connected or no file chosen." +
            "  Can't program Flash.\n");
      }
   }

   /*
    * ===============================================================================
    * 
    * Name: sendBoot
    * 
    * ===============================================================================
    */
   /**
    * Send the boot command to the target.
    * 
    * The boot command resets the target PIC processor.  The application is started
    * if the application CRC and size are correct.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre     None 
    * \note    None
    * 
    * ===============================================================================
    */
   private void sendBoot()
   {
      byte                          sendBootMsg[] = { STX, BOOT_CMD };
      int                           index;

      /* Verify that the file is OK, and we are configured */
      if (connected)
      {
         readIndex = BOOT_SIZE;
         respBytes = 0;
         badMsg = false;
         connected = false;
         statLabel[CONNECT_LABEL].setText("Connected: No ");
         tabs[MAIN_TAB].append("Boot command sent.\n");
         for (index = 0; index < MAX_BUTTONS; index++)
         {
            if ((index == CONNECT_BUTTON) || (index == VERSION_BUTTON))
            {
               buttons[index].setEnabled(true);
            }
            else
            {
               buttons[index].setEnabled(false);
            }
         }
         sendMsg(sendBootMsg, 2, DOWNLOAD_STATE_E.IDLE);
      } 
      else
      {
         tabs[MAIN_TAB].append("Serial port not connected.  Can't run boot cmd.\n");
      }
   }

   /*
    * ===============================================================================
    * 
    * Name: sendVersion
    * 
    * ===============================================================================
    */
   /**
    * Send the version command to the target.
    * 
    * The version command resets grabs the version of the code.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre     None 
    * \note    None
    * 
    * ===============================================================================
    */
   private void sendVersion()
   {
      byte                          sendVersMsg[] = { VERSION_CMD };

      /* Verify that the file is OK, and we are configured */
      if (!connected)
      {
         respBytes = 10;
         badMsg = false;
         sendMsg(sendVersMsg, 1, DOWNLOAD_STATE_E.VERSION_RESP);
      } 
      else
      {
         tabs[MAIN_TAB].append("In boot mode.  Can't run version cmd.\n");
      }
   }
   
   /*
    * ===============================================================================
    * 
    * Name: verifyCode
    * 
    * ===============================================================================
    */
   /**
    * Verify the program memory and memory image match.
    * 
    * Verify the program memory and the configuration bits.  This method only sends
    * the first command, the rest are sent from processRcvData method.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre     None 
    * \note    This does not verify the EEPROM or the boot program memory (addresses
    *    0x000 to 0x300 in flash memory)
    * 
    * ===============================================================================
    */
   private void verifyCode()
   {
      byte                          readFlashCmd[] = { STX, READ_FLASH_CMD,
                                       0x00, 0x00, 0x00};

      /* Verify that the file is OK, and we are connected */
      if ((hexFile != null) && connected)
      {
         if (procType == PROC_MICROCHIP)
         {
            readIndex = BOOT_SIZE;
         }
         else
         {
            readIndex = baseAddr;
         }
         readFlashCmd[2] = (byte)((readIndex >> 16) & 0xff);
         readFlashCmd[3] = (byte)((readIndex >> 8) & 0xff);
         readFlashCmd[4] = (byte)(readIndex & 0xff);
         respBytes = 14;
         badMsg = false;
         sendMsg(readFlashCmd, 5, DOWNLOAD_STATE_E.VERIFY_FLASH_RESP);
      } 
      else
      {
         tabs[MAIN_TAB].append("Serial port not connected or no file chosen." + 
            "  Can't verify Flash.\n");
      }
   }

   /*
    * ===============================================================================
    * 
    * Name: writeEEProm
    * 
    * ===============================================================================
    */
   /**
    * Write a byte to the EEPROM.
    * 
    * Write a single byte of data to the EEPROM.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre     None 
    * \note    None
    * 
    * ===============================================================================
    */
   private void writeEEProm()
   {
      byte                          eepromData[] = { STX, WRITE_EEPROM_CMD,
                                       0x00, 0x00, 0x00, 0x00 };
      int                           data;

      data = Integer.decode(eepromDataInp.getText());
      eepromData[4] = (byte)(data & 0xff);
      readIndex = Integer.decode(eepromAddr.getText());
      if (connected && 
         ((procType == PROC_MICROCHIP) && ((readIndex & 0xffff) < eeprom_size)) ||
         ((procType == PROC_FREE_BIG) && ((readIndex & 0xffff) >= eeprom_addr) &&
               ((readIndex & 0xffff) < eeprom_addr + eeprom_size/2)) ||
         ((procType == PROC_FREE_BIG) && ((readIndex & 0xffff) >= eeprom_addr + FREESCALE_EEPROM_PAGE_TWO) &&
               ((readIndex & 0xffff) < eeprom_addr + FREESCALE_EEPROM_PAGE_TWO + eeprom_size/2)))
      {
         eepromData[2] = (byte)((readIndex >> 8) & 0xff);
         eepromData[3] = (byte)(readIndex & 0xff);
         eepromData[5] = calculateCrc8(4, eepromData, 1);
         respBytes = 4;
         badMsg = false;
         sendMsg(eepromData, 6, DOWNLOAD_STATE_E.WRITE_EEPROM_RESP);
      } 
      else
      {
         tabs[MAIN_TAB].append("Serial port not connected or no processor chosen." +
            "  Can't write EEPROM.\n");
      }
   }

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
    * \param   None 
    * \return  None
    * 
    * \pre     None 
    * \note    We do not support anything but the tx/rx pins.
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
   }

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
    * Process receive data by putting data into the receive buffer.  If in the
    * idle or receive connect response state, compare incoming charcters with
    * boot rev message.  Each sent message sets up the number of expected read
    * bytes which are copied into the rcvBuffer.  If we get to expected number of
    * bytes, process the receive message.  Otherwise keep waiting for more
    * characters or let the timeout occur which clears the command state.  Perform
    * command specific processing.  This includes verifying the rcv'd message
    * and sending the next message if necessary.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre     None 
    * \note    None
    * 
    * ===============================================================================
    */
   private void processRcvData()
   {
      byte[] readBuffer = new byte[20];
      byte[] tmpBuffer = new byte[20];
      byte crc;
      int numBytes = 0;
      int numReadBufBytes = 0;
      int copyIndex;
      
      /* Grab the input characters.  Copy them into the readBuffer for processing */
      try
      {
         while (inputStream.available() > 0)
         {
            numBytes = inputStream.read(tmpBuffer);
            for (copyIndex = 0; (copyIndex < numBytes)
                  && (numReadBufBytes < 20); copyIndex++, numReadBufBytes++)
            {
               readBuffer[numReadBufBytes] = tmpBuffer[copyIndex];
            }
            if (numReadBufBytes == 20)
            {
               /* If we can't keep up at 19.2 kbps, give up. */
               tabs[MAIN_TAB].append("Rcv buffer overflow! Exiting!\n");
               try
               {
                  inputStream.close();
                  tabs[MAIN_TAB].append("Closed input stream.\n");
                  outputStream.close();
                  tabs[MAIN_TAB].append("Closed output stream.\n");
               } 
               catch (IOException event)
               {
               }
               /* serialPort.close(); Removed since it locks the program */
               tabs[MAIN_TAB].append("Closed serial port.\n");
               System.exit(7);
            }
         }
      } 
      catch (IOException e)
      {
      }

      /* Check if we are looking for the boot connect msg */
      if ((currentState == DOWNLOAD_STATE_E.IDLE)
            || (currentState == DOWNLOAD_STATE_E.CONNECT_RESP))
      {
         /* Check if this is the Boot connect message */
         for (copyIndex = 0; copyIndex < numReadBufBytes; copyIndex++)
         {
            /* If this is the first time that we are talking to the port, the
             * first character can be lost.
             */
            if ((firstComm == true) && (bootMsgIndex == 0) && (copyIndex == 0) &&
                  (readBuffer[copyIndex] == BOOT_MSG[1]))
            {
               bootMsgIndex = 1;
            }
            firstComm = false;
            
            /* Eat any characters that aren't the boot msg */
            if ((bootMsgIndex == 0) && (readBuffer[copyIndex] != BOOT_MSG[0]))
            {
               if (!msgTabRcvBytes)
               {
                  tabs[MSG_TAB].append("Rcv:");
                  msgTabRcvBytes = true;
               }
               tabs[MSG_TAB].append(String.format(" 0x%02x", readBuffer[copyIndex]));
            }
            /* Check if we started receiving the boot msg, these aren't printed
             * as bytes on the rcv tab.
             */
            if (readBuffer[copyIndex] == BOOT_MSG[bootMsgIndex])
            {
               bootMsgIndex++;
               if (bootMsgIndex == BOOT_MSG_SIZE)
               {
                  if (msgTabRcvBytes)
                  {
                     tabs[MSG_TAB].append("\n");
                     msgTabRcvBytes = false;
                  }
                  tabs[MSG_TAB].append("Rcv: Connect Msg\n");
                  connected = true;
                  statLabel[CONNECT_LABEL].setText("Connected: Yes");
                  statLabel[VERS_LABEL].setText("Vers: Unknown");
                  tabs[MAIN_TAB].append("Connected\n");
                  bootMsgIndex = 0;
                  goToIdleState();
               }
            } 
            else
            {
               /* The characters don't match the boot msg. If the boot msg was
                * dropped in the middle, this prints the initial boot characters
                * that matched.
                */
               if (bootMsgIndex != 0)
               {
                  int index;

                  for (index = 0; index < bootMsgIndex; index++)
                  {
                     if (!msgTabRcvBytes)
                     {
                        tabs[MSG_TAB].append("Rcv:");
                        msgTabRcvBytes = true;
                     }
                     tabs[MSG_TAB].append(String.format(" 0x%02x", BOOT_MSG[index]));
                  }
                  bootMsgIndex = 0;
               }
            }
         }
      } 
      else
      {
         /* Any state that isn't IDLE or connect, copy data into rcvBuffer */
         for (copyIndex = 0; copyIndex < numReadBufBytes; copyIndex++)
         {
            if (!msgTabRcvBytes)
            {
               tabs[MSG_TAB].append("Rcv:");
               msgTabRcvBytes = true;
            }
            tabs[MSG_TAB].append(String.format(" 0x%02x", readBuffer[copyIndex]));
            rcvBuffer[copyIndex + rcvBufIndex] = readBuffer[copyIndex];
            if (copyIndex + rcvBufIndex > RCV_BUFFER_SIZE)
            {
               /* We shouldn't overflow at such a slow rate. */
               tabs[MAIN_TAB].append("Rcv buffer overflow! Exiting now!\n");
               try
               {
                  inputStream.close();
                  tabs[MAIN_TAB].append("Closed input stream.\n");
                  outputStream.close();
                  tabs[MAIN_TAB].append("Closed output stream.\n");
               } 
               catch (IOException event)
               {
               }
               serialPort.close();
               tabs[MAIN_TAB].append("Closed serial port.\n");
               System.exit(7);
            }
         }
         rcvBufIndex += numReadBufBytes;
         if (rcvBufIndex >= respBytes)
         {
            /* We've received the whole response */
            switch (currentState)
            {
               case WRITE_FLASH_RESP:
               {
                  if ((readIndex < maxProgAddr) || clearFlash)
                  {
                     /* Verify response address is same as last sent cmd for
                      *    flash memory.
                      */
                     if ((rcvBuffer[0] != STX)
                           || (rcvBuffer[1] != WRITE_FLASH_CMD)
                           || (rcvBuffer[2] != (byte) ((readIndex >> 16) & 0xff))
                           || (rcvBuffer[3] != (byte) ((readIndex >> 8) & 0xff))
                           || (rcvBuffer[4] != (byte) (readIndex & 0xff)))
                     {
                        tabs[MSG_TAB].append(" BadResp");
                        tabs[MAIN_TAB].append("Flash write: Bad resp received\n");
                        badMsg = true;
                     } 
                     else
                     {
                        tabs[MSG_TAB].append(" GoodResp");
                     }
                     if (readIndex < maxProgAddr)
                     {
                        readIndex += 8;
                        if ((readIndex >= maxProgAddr) && (procType == PROC_FREE_SMALL))
                        {
                           readIndex = (readIndex + FREE_SMALL_SECT_SIZE - 1) &
                              ~(FREE_SMALL_SECT_SIZE - 1);
                           if (readIndex < FREESCALE_SMALL_BOOT_START)
                           {
                              clearFlash = true;
                           }
                        }
                     }
                     else if (clearFlash)
                     {
                        readIndex += FREE_SMALL_SECT_SIZE;
                        if (readIndex >= FREESCALE_SMALL_BOOT_START)
                        {
                           clearFlash = false;
                        }
                     }
                  } 
                  else
                  {
                     /* Verify response address is same as last sent cmd for
                      *    config memory.
                      */
                     if ((rcvBuffer[0] != STX) || (rcvBuffer[1] != WRITE_CFG_CMD)
                           || (rcvBuffer[2] != (byte) progCfgIndex))
                     {
                        tabs[MSG_TAB].append(" BadResp");
                        tabs[MAIN_TAB].append("Flash write: Bad cfg resp received\n");
                        badMsg = true;
                     } 
                     else
                     {
                        tabs[MSG_TAB].append(" GoodResp");
                     }
   
                     /* Find the next valid config byte that isn't completely masked
                      *    out.
                      */
                     boolean foundNext = false;
                     while ((progCfgIndex < 16) && !foundNext)
                     {
                        progCfgIndex++;
                        if ((progCfgIndex < 16)
                              && (CFG_VALID_BITS[currProcIndex][progCfgIndex] != 0))
                        {
                           foundNext = true;
                        }
                     }
                  }

                  /* If we need to write more flash, or cfg bytes */
                  if (((readIndex < maxProgAddr) || clearFlash || (progCfgIndex < 16))
                        && !badMsg)
                  {
                     byte writeFlash[] = { STX, WRITE_FLASH_CMD,
                           (byte) ((readIndex >> 16) & 0xff),
                           (byte) ((readIndex >> 8) & 0xff),
                           (byte) (readIndex & 0xff),
                           (byte)0xff, (byte)0xff, (byte)0xff, (byte)0xff,    /* Data */
                           (byte)0xff, (byte)0xff, (byte)0xff, (byte)0xff,
                           (byte)0xff };                                      /* CRC8 */

                     /* Check if programming flash or cfg bytes */
                     if ((readIndex < maxProgAddr) || clearFlash)
                     {
                        /* Programming flash */
                        if (readIndex < maxProgAddr)
                        {
                           for (copyIndex = 0; copyIndex < 8; copyIndex++)
                           {
                              writeFlash[copyIndex + 5] = progDataArray[readIndex - baseAddr
                                    + copyIndex];
                           }
                        }
                        writeFlash[13] = calculateCrc8(12, writeFlash, 1);
                        respBytes = 5;
                        
                        /* Send next write flash cmd */
                        sendMsg(writeFlash, 14, DOWNLOAD_STATE_E.WRITE_FLASH_RESP);
                     } 
                     else
                     {
                        /* Find the next cfg byte that has valid bits */
                        while (CFG_VALID_BITS[currProcIndex][progCfgIndex] == 0)
                        {
                           progCfgIndex++;
                        }
   
                        /* Write config bits */
                        writeFlash[1] = WRITE_CFG_CMD;
                        writeFlash[2] = (byte)progCfgIndex;
                        writeFlash[3] = cfgDataArray[progCfgIndex];
                        writeFlash[4] = calculateCrc8(3, writeFlash, 1);
                        respBytes = 3;

                        /* Send next write cfg cmd */
                        sendMsg(writeFlash, 5, DOWNLOAD_STATE_E.WRITE_FLASH_RESP);
                     }
                  } 
                  else
                  {
                     /* Either done writing flash/cfg, or received a bad msg. */
                     if (badMsg)
                     {
                        tabs[MAIN_TAB].append("Flash write: Bad msgs received\n");
                        goToIdleState();
                     } 
                     else
                     {
                        /* After writing, verify the code */
                        tabs[MAIN_TAB].append("Flash write: Successful\n");
                        verifyCode();
                     }
                  }
                  break;
               }
               case READ_FLASH_RESP:
               {
                  /* Print the data on the program memory tab */
                  if ((readIndex & 0xf) == 0)
                  {
                     tabs[PROG_MEM_TAB].append(String.format("\n0x%05x", readIndex));
                  }
                  
                  /* Verify response is valid */
                  crc = calculateCrc8(12, rcvBuffer, 1);
                  if ((rcvBuffer[0] != STX) || (rcvBuffer[1] != READ_FLASH_CMD)
                        || (rcvBuffer[2] != (byte) ((readIndex >> 16) & 0xff))
                        || (rcvBuffer[3] != (byte) ((readIndex >> 8) & 0xff))
                        || (rcvBuffer[4] != (byte) (readIndex & 0xff))
                        || (rcvBuffer[13] != crc))
                  {
                     tabs[MSG_TAB].append(" BadCRC");
                     tabs[PROG_MEM_TAB].append(" 0xXXXX 0xXXXX 0xXXXX 0xXXXX");
                     badMsg = true;
                  } 
                  else
                  {
                     tabs[MSG_TAB].append(" GoodCRC");
                     tabs[PROG_MEM_TAB].append(String.format(
                        " 0x%04x 0x%04x 0x%04x 0x%04x", ((rcvBuffer[6] << 8) & 0xff00) |
                           (rcvBuffer[5] & 0xff), ((rcvBuffer[8] << 8) & 0xff00) |
                           (rcvBuffer[7] & 0xff), ((rcvBuffer[10] << 8) & 0xff00) |
                           (rcvBuffer[9] & 0xff), ((rcvBuffer[12] << 8) & 0xff00) |
                           (rcvBuffer[11] & 0xff)));
                  }
                  
                  /* Increment index, and check if more data to read */
                  readIndex += 8;
                  if (readIndex < flash_size + baseAddr)
                  {
                     /* Send next flash read request msg */
                     byte           readFlashCmd[] = { STX, READ_FLASH_CMD,
                                       (byte)((readIndex >> 16) & 0xff),
                                       (byte)((readIndex >> 8) & 0xff),
                                       (byte)(readIndex & 0xff) };
                     respBytes = 14;
                     sendMsg(readFlashCmd, 5, DOWNLOAD_STATE_E.READ_FLASH_RESP);
                  } 
                  else
                  {
                     /* We are done reading the the flash, print ending msg */ 
                     tabs[PROG_MEM_TAB].append("\n\n");
                     if (badMsg)
                     {
                        tabs[MAIN_TAB].append("Flash read: Bad msgs received\n");
                     } 
                     else
                     {
                        tabs[MAIN_TAB].append("Flash read: Successful\n");
                     }
                     goToIdleState();
                  }
                  break;
               }
               case WRITE_EEPROM_RESP:
               {
                  /* Verify write eeprom response message */
                  if ((rcvBuffer[0] != STX) || (rcvBuffer[1] != WRITE_EEPROM_CMD) ||
                     (rcvBuffer[2] != (byte) ((readIndex >> 8) & 0xff)) ||
                     (rcvBuffer[3] != (byte) (readIndex & 0xff)))
                  {
                     tabs[MSG_TAB].append(" BadResp");
                     tabs[MAIN_TAB].append("EEPROM write: Bad resp received\n");
                     badMsg = true;
                  } 
                  else
                  {
                     tabs[MAIN_TAB].append("EEPROM write: Successful\n");
                     tabs[MSG_TAB].append(" GoodResp");
                  }
                  goToIdleState();
                  break;
               }
               case READ_EEPROM_RESP:
               {
                  if ((readIndex & 0xf) == 0)
                  {
                     tabs[EEPROM_TAB].append(String.format("\n0x%04x", readIndex));
                  }
                  /* Verify read eeprom response msg */
                  crc = calculateCrc8(4, rcvBuffer, 1);
                  if ((rcvBuffer[0] != STX) || (rcvBuffer[1] != READ_EEPROM_CMD) ||
                        (rcvBuffer[2] != (byte) ((readIndex >> 8) & 0xff)) ||
                        (rcvBuffer[3] != (byte) (readIndex & 0xff)) ||
                        (rcvBuffer[5] != crc))
                  {
                     tabs[MSG_TAB].append(" BadCRC");
                     tabs[EEPROM_TAB].append(" Bad ");
                     badMsg = true;
                  } 
                  else
                  {
                     tabs[MSG_TAB].append(" GoodCRC");
                     tabs[EEPROM_TAB].append(String.format(" 0x%02x", rcvBuffer[4]));
                  }
                  

                  /* EEPROM is only read one byte at a time */
                  readIndex++;

                  /* If a freescale processor, see if on the second page */
                  if ((procType == PROC_FREE_BIG) && (readIndex == (eeprom_size/2) + eeprom_addr))
                  {
                     readIndex = eeprom_addr | FREESCALE_EEPROM_PAGE_TWO;
                  }
                  if (((procType == PROC_MICROCHIP) && (readIndex < eeprom_size + eeprom_addr)) ||
                     ((procType == PROC_FREE_BIG) && (readIndex < FREESCALE_EEPROM_PAGE_TWO +
                           eeprom_size/2 + eeprom_addr)))
                  {
                     /* Send next eeprom read request */
                     byte           eepromData[] = { STX, READ_EEPROM_CMD, 
                                       (byte)((readIndex >> 8) & 0xff),
                                       (byte)(readIndex & 0xff) };
                     respBytes = 6;
                     sendMsg(eepromData, 4, DOWNLOAD_STATE_E.READ_EEPROM_RESP);
                  } 
                  else
                  {
                     /* Done reading the eeprom */
                     tabs[EEPROM_TAB].append("\n\n");
                     if (badMsg)
                     {
                        tabs[MAIN_TAB].append("EEPROM read: Bad msgs received\n");
                     } 
                     else
                     {
                        tabs[MAIN_TAB].append("EEPROM read: Successful\n");
                     }
                     goToIdleState();
                  }
                  break;
               }
               case VERIFY_FLASH_RESP:
               {
                  /* Verify response message from read flash cmd.  This works
                   *    for both flash and cfg bytes.
                   */
                  crc = calculateCrc8(12, rcvBuffer, 1);
                  if ((rcvBuffer[0] != STX) || (rcvBuffer[1] != READ_FLASH_CMD) ||
                        (rcvBuffer[2] != (byte) ((readIndex >> 16) & 0xff)) ||
                        (rcvBuffer[3] != (byte) ((readIndex >> 8) & 0xff)) ||
                        (rcvBuffer[4] != (byte) (readIndex & 0xff)) ||
                        (rcvBuffer[13] != crc))
                  {
                     tabs[MSG_TAB].append(" BadCRC");
                     badMsg = true;
                  } 
                  else
                  {
                     tabs[MSG_TAB].append(" GoodCRC");
   
                     /* Check if next read should be flash or cfg bytes */
                     if (readIndex < maxProgAddr)
                     {
                        /* Reading flash bytes, verify that they are correct */
                        for (copyIndex = 0; (copyIndex < 8) && !badMsg; copyIndex++)
                        {
                           if (progDataArray[readIndex + copyIndex - baseAddr] !=
                              rcvBuffer[copyIndex + 5])
                           {
                              badMsg = true;
                           }
                        }
                     } 
                     else
                     {
                        /* Reading the config bytes, verify they are correct.  Remember
                         *    to mask them with the valid bit mask.
                         */
                        for (copyIndex = 0; (copyIndex < 8) && !badMsg; copyIndex++)
                        {
                           if ((byte)((int)cfgDataArray[readIndex - CFG_BIT_START +
                                 copyIndex] & (int)CFG_VALID_BITS[currProcIndex][
                                 readIndex - CFG_BIT_START + copyIndex]) !=
                                 rcvBuffer[copyIndex + 5])
                           {
                              badMsg = true;
                           }
                        }
                     }
                     
                     /* Increment the index, if we move past the end of the program
                      *    memory, start reading cfg bits.
                      */ 
                     readIndex += 8;
                     if ((readIndex >= maxProgAddr) && (readIndex < CFG_BIT_START))
                     {
                        if (procType == PROC_MICROCHIP)
                        {
                           readIndex = CFG_BIT_START;
                        }
                        else
                        {
                           /* No config bits for Freescale parts */
                           readIndex = CFG_BIT_END;
                        }
                     }
                  }
                  
                  /* Check if we need to send another read request */
                  if (((readIndex < maxProgAddr) || ((readIndex >= CFG_BIT_START) && (readIndex < CFG_BIT_END)))
                        && !badMsg)
                  {
                     /* Send next flash read request */
                     byte readFlashCmd[] = { STX, READ_FLASH_CMD,
                           (byte) ((readIndex >> 16) & 0xff),
                           (byte) ((readIndex >> 8) & 0xff),
                           (byte) (readIndex & 0xff) };
                     respBytes = 14;
                     sendMsg(readFlashCmd, 5, DOWNLOAD_STATE_E.VERIFY_FLASH_RESP);
                  } 
                  else
                  {
                     /* Done verify, write out results */
                     tabs[PROG_MEM_TAB].append("\n\n");
                     if (badMsg)
                     {
                        tabs[MAIN_TAB].append("Verify code: Bad msgs received\n");
                     } 
                     else
                     {
                        tabs[MAIN_TAB].append("Verify code: Successful\n");
                     }
                     goToIdleState();
                  }
                  break;
               }
               case VERSION_RESP:
               {
                  /* Verify response message from read flash cmd.  This works
                   *    for both flash and cfg bytes.
                   */
                  if ((rcvBuffer[0] != 'v') ||
                        (rcvBuffer[1] < '0') || (rcvBuffer[1] > '9') ||
                        (rcvBuffer[2] < '0') || (rcvBuffer[2] > '9') ||
                        (rcvBuffer[3] != '.') ||
                        (rcvBuffer[4] < '0') || (rcvBuffer[4] > '9') ||
                        (rcvBuffer[5] < '0') || (rcvBuffer[5] > '9') ||
                        (rcvBuffer[6] != '.') ||
                        (rcvBuffer[7] < '0') || (rcvBuffer[7] > '9') ||
                        (rcvBuffer[8] < '0') || (rcvBuffer[8] > '9') ||
                        (rcvBuffer[9] != '\r'))
                  {
                     tabs[MSG_TAB].append(" Bad Version String");
                     tabs[MAIN_TAB].append("Version: Bad msg received\n");
                  } 
                  else
                  {
                     String tmpStr = new String(rcvBuffer, 0, 9);
                     tabs[MSG_TAB].append(" Good Version");
                     statLabel[VERS_LABEL].setText("Vers: " + tmpStr); 
                  }
                  timeoutRunning = false;
                  currentState = DOWNLOAD_STATE_E.IDLE;
                  cmdStatusLabel.setText("Cmd Stat Idle");
                  buttons[VERSION_BUTTON].setEnabled(true);
                  buttons[CONNECT_BUTTON].setText("Connect");
                  break;
               }
            }
         }
      }
   }

   /*
    * ===============================================================================
    * 
    * Name: calculateCrc8
    * 
    * ===============================================================================
    */
   /**
    * Calculate CRC8
    * 
    * Calculate the CRC8 for a byte stream.  This uses a lookup table to process
    * 4 bits at a time for speed.  Generator polynomial is x^8+x^2+x+1 with an
    * initial value of 0xff.  This conforms to the CCITT-CRC8.
    * 
    * \param   buffer   [in] array of bytes to calculate CRC8 
    * \param   length   [in] number of bytes in array 
    * \param   offset   [in] offset into array to start calculation 
    * \return  None
    * 
    * \pre     None 
    * \note    None
    * 
    * ===============================================================================
    */
   private byte calculateCrc8(
      int                           length,
      byte[]                        buffer, 
      int                           offset)
   {
      byte currCrc = (byte) 0xff;
      int count;

      for (count = 0; count < length; count++)
      {
         currCrc = (byte) (((currCrc << 4) & 0xf0) ^ CRC8_LOOKUP[(((currCrc) ^ (buffer[count
               + offset])) >> 4) & 0x0f]);
         currCrc = (byte) (((currCrc << 4) & 0xf0) ^ CRC8_LOOKUP[(((currCrc >> 4) & 0x0f) ^ (buffer[count
               + offset])) & 0x0f]);
      }
      return (currCrc);
   }

   /*
    * ===============================================================================
    * 
    * Name: readHexFile
    * 
    * ===============================================================================
    */
   /**
    * Read a hex/s-record object file and store it in memory.
    * 
    * Read the object file and create an array in memory that contains an image
    * for the whole processor.  This includes a separate array for the configuration
    * bytes.  convertHexLine/convertSrecrodLine is called to do the heavy lifting.
    * This method does the wrapper functions such as setting up arrays, opening the
    * file, calling appropriate converter for each line in the file, verifying boot
    * is not overwrriten, filling out code size, and calculating and installing CRC
    * for the code.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre     None 
    * \note    The Microchip checksum includes the configuration bytes which are
    *    anded with the valid mask.  This is so we have a consistent checksum between
    *    Microchip MPLAB IDE and our code. 
    * 
    * ===============================================================================
    */
   private boolean readHexFile()
   {
      int index;
      boolean fileError = false;
      int startAddr;
      int progSize;
      int length;

      /* Open the file and verify it works for this processor */
      upperProgAddr = 0;
      maxProgAddr = 0;
      fileDone = false;
      progDataArray = new byte[flash_size];
      cfgDataArray = new byte[16];
      for (index = 0; index < flash_size; index++)
      {
         progDataArray[index] = (byte) 0xff;
      }
      for (index = 0; index < 16; index++)
      {
         cfgDataArray[index] = (byte) 0xff;
      }

      try
      {
         hexReader = new BufferedReader(new FileReader(hexFile));
         while (!fileDone && !fileError)
         {
            if (procType == PROC_MICROCHIP)
            {
               fileError = convertHexLine(hexReader.readLine());
            }
            else
            {
               fileError = convertSrecordLine(hexReader.readLine());
            }
         }
         hexReader.close();
      } 
      catch (IOException e)
      {
         fileError = true;
         tabs[MAIN_TAB].append("ERROR: Read hex/s-record file error.\n");
      }

      /* Verify that boot load isn't being overwritten */
      if (procType == PROC_MICROCHIP)
      {
         startAddr = PIC_BOOT_START - baseAddr;
         length = BOOT_SIZE;
      }
      else if (procType == PROC_FREE_SMALL)
      {
         startAddr = FREESCALE_SMALL_BOOT_START - baseAddr;
         length = FREESCALE_SMALL_BOOT_SIZE;
      }
      else
      {
         startAddr = FREESCALE_BOOT_START - baseAddr;
         length = BOOT_SIZE;
      }
      for (index = startAddr; (index < startAddr + length) &&
         !fileError; index++)
      {
         if (progDataArray[index] != (byte) 0xff)
         {
            fileError = true;
            tabs[MAIN_TAB].append("ERROR: Hex file contains data in boot area.\n");
         }
      }

      /* Calculate the checksum, currently unimplemented because PIC messed this up
       *   by including configuration words.  Very messy.
       */
      statLabel[CHECKSUM_LABEL].setText("Checksum: Unimpl");

      /* Verify code size is currently unused */
      if (procType == PROC_MICROCHIP)
      {
         startAddr = PIC_CODE_SIZE_START;
         progSize = maxProgAddr - BOOT_SIZE;
      }
      else
      {
         startAddr = 0;
         progSize = maxProgAddr - baseAddr;
      }
      for (index = startAddr; (index < startAddr + CODE_SIZE_FIELD) & !fileError; index++)
      {
         if (progDataArray[index] != (byte) 0xff)
         {
            fileError = true;
            tabs[MAIN_TAB].append("ERROR: Code size location is being used.\n");
         } 
         else
         {
            progDataArray[index] = (byte) ((progSize >>
               ((3 - index - startAddr) * 8)) & 0xff);
         }
      }
      /* Fill out the CRC8 */
      if (!fileError)
      {
         if (procType == PROC_MICROCHIP)
         {
            progDataArray[maxProgAddr] = calculateCrc8(maxProgAddr - BOOT_SIZE,
               progDataArray, BOOT_SIZE);
            progDataArray[maxProgAddr + 1] = (byte) 0xa5; 
         }
         else
         {
            progDataArray[maxProgAddr - baseAddr] = calculateCrc8(maxProgAddr  - baseAddr,
                  progDataArray, 0);
            progDataArray[maxProgAddr - baseAddr + 1] = (byte) 0xa5; 
         }

         /* Throw a marker after the CRC, no reason not to. */
         maxProgAddr += 2;
      }
      return (fileError);
   }

   /*
    * ===============================================================================
    * 
    * Name: convertHexLine
    * 
    * ===============================================================================
    */
   /**
    * Convert a line from a hex file to positions in the byte array.
    * 
    * Extract the length and address from the line.  Verify that the line checksum
    * is correct.  If a data record, write the bytes into the proper array for
    * flash or config bytes.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre     None 
    * \note    We only support data, end and address records.  If the address
    *    is 0x300000 to 0x300010, the bytes are configuration bytes. 
    * 
    * ===============================================================================
    */
   private boolean convertHexLine(String currFileLine)
   {
      int length;
      int addr;
      int index;
      int calcChecksum;
      byte[] data = new byte[20];
      boolean fileFail = false;

      if (currFileLine.length() < 11)
      {
         tabs[MAIN_TAB].append("ERROR: Hex file line incorrect.\n");
         return (true);
      }
      length = Integer.parseInt(currFileLine.substring(1, 3), 16);
      for (index = 0; index < length + 4; index++)
      {
         data[index] = (byte) Integer.parseInt(currFileLine.substring(
               (index * 2) + 3, (index * 2) + 5), 16);
      }
      addr = ((data[0] << 8) & 0xff00) | (data[1] & 0xff);

      /* Verify the checksum is correct */
      for (calcChecksum = length, index = 0; index < length + 3; index++)
      {
         calcChecksum += data[index];
      }
      calcChecksum = (0x100 - (calcChecksum & 0xff)) & 0xff;
      if ((currFileLine.charAt(0) != ':') ||
         ((byte) calcChecksum != data[length + 3]))
      {
         /* Issues with the file format */
         fileFail = true;
         tabs[MAIN_TAB].append("ERROR: Hex file line checksum or start char fail.\n");
      } 
      else
      {
         /* Store info in the array */
         switch (data[2])
         {
            case 0:
            {
               /* Data record */
               for (index = 0; (index < length) && !fileFail; index++)
               {
                  if ((upperProgAddr + addr + index) < flash_size)
                  {
                     progDataArray[upperProgAddr + addr + index] = data[index + 3];
                     if (maxProgAddr < (upperProgAddr + addr + index + 1))
                     {
                        maxProgAddr = (upperProgAddr + addr + index + 1);
                     }
                  }
                  else if (((upperProgAddr + addr + index) >= CFG_BIT_START) &&
                     ((upperProgAddr + addr + index) < CFG_BIT_END))
                  {
                     cfgDataArray[(upperProgAddr + addr + index) - CFG_BIT_START] =
                        data[index + 3];
                  } 
                  else
                  {
                     fileFail = true;
                     tabs[MAIN_TAB].append("ERROR: Hex file addr out of range.\n");
                  }
               }
               break;
            }
            case 1:
            {
               /* End record */
               fileDone = true;
               break;
            }
            case 4:
            {
               /* addr record, update upper 16 bits of address */
               upperProgAddr = ((data[3] << 24) & 0xff000000) |
                  ((data[4] << 16) & 0xff0000);
               break;
            }
         }
      }
      return (fileFail);
   }

   /*
    * ===============================================================================
    * 
    * Name: convertSrecordLine
    * 
    * ===============================================================================
    */
   /**
    * Convert a line from an S-record file to positions in the byte array.
    * 
    * Extract the length and address from the line.  Verify that the line checksum
    * is correct.  If a data record, write the bytes into the flash byte array.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre     None 
    * \note    We only support header, data, and end records. 
    * 
    * ===============================================================================
    */
   private boolean convertSrecordLine(String currFileLine)
   {
      int length;
      int addr;
      int index;
      int calcChecksum;
      byte[] data = new byte[255];
      boolean fileFail = false;

      if (currFileLine.length() < 10)
      {
         tabs[MAIN_TAB].append("ERROR: S-Record file line incorrect.\n");
         return (true);
      }
      length = Integer.parseInt(currFileLine.substring(2, 4), 16);
      for (index = 0; index < length; index++)
      {
         data[index] = (byte) Integer.parseInt(currFileLine.substring(
               (index * 2) + 4, (index * 2) + 6), 16);
      }
      addr = ((data[0] << 8) & 0xff00) | (data[1] & 0xff);

      /* Verify the checksum is correct */
      for (calcChecksum = length, index = 0; index < length - 1; index++)
      {
         calcChecksum += data[index];
      }
      calcChecksum = (0xff - (calcChecksum & 0xff)) & 0xff;
      if ((currFileLine.charAt(0) != 'S') ||
         ((byte) calcChecksum != data[length - 1]))
      {
         /* Issues with the file format */
         fileFail = true;
         tabs[MAIN_TAB].append("ERROR: S-Record file line checksum or start char fail.\n");
      } 
      else
      {
         /* Store info in the array */
         switch (currFileLine.charAt(1))
         {
            case '0':
            {
               /* Header record, just ignore. */
               break;
            }
            case '1':
            {
               /* Data record */
               for (index = 0; (index < length - 3) && !fileFail; index++)
               {
                  if ((upperProgAddr + addr + index - baseAddr) < flash_size)
                  {
                     progDataArray[upperProgAddr + addr + index - baseAddr] = data[index + 2];
                     if (maxProgAddr < (upperProgAddr + addr + index + 1))
                     {
                        maxProgAddr = (upperProgAddr + addr + index + 1);
                     }
                  }
                  else
                  {
                     fileFail = true;
                     tabs[MAIN_TAB].append("ERROR: S-Record file addr out of range.\n");
                  }
               }
               break;
            }
            case '9':
            {
               /* End record */
               fileDone = true;
               break;
            }
         }
      }
      return (fileFail);
   }
   
   /*
    * ===============================================================================
    * 
    * Name: goToIdleState
    * 
    * ===============================================================================
    */
   /**
    * Go to idle state
    * 
    * Turn off the timeout timer, and set the state to idle.  Re-enable all of the
    * buttons and change the Connect/End Cmd button to Connect.
    * 
    * \param   None 
    * \return  None
    * 
    * \pre     None 
    * \note    None 
    * 
    * ===============================================================================
    */
   private void goToIdleState()
   {
      int index;

      timeoutRunning = false;
      currentState = DOWNLOAD_STATE_E.IDLE;
      cmdStatusLabel.setText("Cmd Stat Idle");
      for (index = 0; index < MAX_BUTTONS; index++)
      {
         if (index != VERSION_BUTTON)
         {
            buttons[index].setEnabled(true);
         }
         else
         {
            buttons[index].setEnabled(false);
         }
      }
      buttons[CONNECT_BUTTON].setText("Connect");
   }
}
