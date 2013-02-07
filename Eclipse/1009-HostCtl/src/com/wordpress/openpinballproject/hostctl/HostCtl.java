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
 * @file:   HostCtl.java
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
 * This is the main class file for the Host controller.
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

import java.awt.Color;
import java.awt.Component;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.KeyEventDispatcher;
import java.awt.KeyboardFocusManager;
import java.awt.event.KeyEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.File;

import javax.swing.JDesktopPane;
import javax.swing.JFrame;
import javax.swing.JInternalFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.plaf.basic.BasicInternalFrameTitlePane;
import javax.swing.plaf.basic.BasicInternalFrameUI;

public class HostCtl extends JFrame
{
   private static final long     serialVersionUID = -1;
   
   private static final int      OS_WINDOWS              = 0;
   private static final int      OS_LINUX                = 1;
   private static final int      OS_MAC                  = 2;

   private static final int      HD_WIDTH                = 1920;
   private static final int      HD_HEIGHT               = 1080;
   private static final float    PROT_SCALE_FACT         = (1440.0f)/(1920.0f);
   private static final float    FULLSCR_SCALE_FACT      = 1.0f;
   private static final float    VID_PROT_SCALE_FACT     = 1280.0f/1920.0f;
   private static final float    VID_FULLSCR_SCALE_FACT  = 1536.0f/1920.0f;

   private static final int      NUM_PLAYERS                = 4;

   private static boolean        fullScr = false;
   
   private static int            osType;
   private static String         commPortName;
   private static String         rulesFileName;
   public static JPanel          bgndPanel;
   private static JDesktopPane   deskPane = new JDesktopPane();
   
   /* Frames for graphics */
   private static JInternalFrame vidFrame[] = new JInternalFrame[GlobInfo.NUM_VIDEO_CLIPS];
   private static JInternalFrame bgndFrame = new JInternalFrame();

   /* Panels for graphics */
   private static JPanel         leftColPanel = new JPanel();
   private static JPanel         rightColPanel = new JPanel();
   private static JPanel         leftBotPanel = new JPanel();
   private static JPanel         ctrBotPanel = new JPanel();
   private static JPanel         rightBotPanel = new JPanel();
   private static JPanel         vidPanel = new JPanel();
   private static JLabel         plyrScore[] = new JLabel[NUM_PLAYERS];
   
   /*
    * ===============================================================================
    * 
    * Name: main
    * 
    * ===============================================================================
    */
   /**
    * Main call from command line
    * 
    * Look for passed parameters and options.  Find out the OS for serial port
    * interfacing.  Create the HostCtl object.
    * 
    * @param   args  - passed parameters 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public static void main(String[] args)
   {
      int                        index = 0;
      commPortName               = null;
      
      String path = new File(".").getAbsolutePath();
      System.out.println("Current path: " + path);      
      
      while (index < args.length)
      {
         if (args[index].startsWith("-com="))
         {
            commPortName = new String(args[index].replaceAll("-com=", ""));
         }
         else if (args[index].compareTo("-?") == 0)
         {
            System.out.println("java -jar HostCtl.jar");
            System.out.println("\t-?\t\tOptions Help");
            System.out.println("\t-com=xxxx\tCOM port number");
            System.out.println("\t-fullscr\tFull screen window");
            System.out.println("\t-debug\tCreate debug windows");
            System.out.println("\t-rules=xxxxx.txt\tRules file name");
         }
         else if (args[index].compareTo("-fullscr") == 0)
         {
            fullScr = true;
         }
         else if (args[index].compareTo("-debug") == 0)
         {
            GlobInfo.debug = true;
         }
         if (args[index].startsWith("-rules="))
         {
            rulesFileName = new String(args[index].replaceAll("-rules=", ""));
         }
         index++;
      }

      /* Figure out the OS */
      String os = System.getProperty("os.name").toLowerCase();
      if (os.indexOf( "win" ) >= 0)
      {
         osType = OS_WINDOWS;
      }
      else if (os.indexOf( "mac" ) >= 0)
      {
         osType = OS_MAC;
      }
      else if (os.indexOf( "nix") >=0 || os.indexOf( "nux") >=0)
      {
         osType = OS_LINUX;
      }
      else
      {
         System.out.println("Unknown OS - " + os);
         System.exit(1);
      }
      System.out.println("Operating System:  " + os + ": " + osType);
      
      new HostCtl();
   } /* end main */
   
   /*
    * ===============================================================================
    * 
    * Name: MyDispatcher
    * 
    * ===============================================================================
    */
   /**
    * My dispatcher looks for 'x' key to close the window since window controls
    * have been removed.
    * 
    * @param   KeyEvent  - reason for the event 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   private class MyDispatcher implements KeyEventDispatcher
   {
      public boolean dispatchKeyEvent(KeyEvent e)
      {
         if (e.getID() == KeyEvent.KEY_TYPED)
         {
            if ((e.getKeyChar() == 'x') ||
                  (e.getKeyCode() == 'X'))
            {
               if (GlobInfo.serIntf != null)
               {
                  GlobInfo.serIntf.closeSerPort();
               }
               System.exit(0);
            }
            if ((e.getKeyChar() == 's') ||
                  (e.getKeyCode() == 'S'))
            {
               GlobInfo.videoServ.SwapVideo();
            }
         }
         return false;
      }
   } /* end MyDispatcher */
   
   /*
    * ===============================================================================
    * 
    * Name: HostCtl
    * 
    * ===============================================================================
    */
   /**
    * HostCtl is the root object for the pinball instance
    * 
    * Figure out the scale factor and size frames appropriately.  Create console
    * window if in debug.  Open the serial port, and start the create/start the
    * video window.
    * 
    * @param   None 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public HostCtl()
   {
      float                   scaleFact;
      int                     index;
      
      if (fullScr)
      {
         scaleFact = FULLSCR_SCALE_FACT;
      }
      else
      {
         scaleFact = PROT_SCALE_FACT;
      }
      setBounds(100, 100, (int)((HD_WIDTH * scaleFact) + 0.5f),
            (int)((HD_HEIGHT * scaleFact) + 0.5f));
      addWindowListener(new WindowAdapter()
      {
         public void windowClosing(WindowEvent e)
         {
            if (GlobInfo.serIntf != null)
            {
               GlobInfo.serIntf.closeSerPort();
            }
            System.exit(0);
         }
      });
      
      /* Set up all the frames/panels */
      sizeFrmPnl();
      
      /* Create player score labels */
      createScoreLbl();
      
      /* Create a console window if debug */
      if (GlobInfo.debug)
      {
         GlobInfo.consFrm = new ConsoleFrm();
      }
      
      /* Add bgndFrame to desktop */
      for (index = 0; index < GlobInfo.NUM_VIDEO_CLIPS; index++)
      {
         deskPane.add(vidFrame[index]);
      }
      this.setUndecorated(true);
      setContentPane(deskPane);
      
      GlobInfo.hostCtl = this;
      
      if (rulesFileName != null)
      {
         GlobInfo.parseRules = new ParseRules(rulesFileName);
      }

      if (commPortName != null)
      {
         GlobInfo.serIntf = new SerIntf(commPortName);
      }

      /* Set up window to accept hot keys to close */
      KeyboardFocusManager manager = KeyboardFocusManager.getCurrentKeyboardFocusManager();
      manager.addKeyEventDispatcher(new MyDispatcher());

      deskPane.add(bgndFrame);
      GlobInfo.videoServ = new VideoServ();
      
      bgndFrame.moveToBack();
      
      setVisible(true);
   } /* end HostCtl */
   
   /*
    * ===============================================================================
    * 
    * Name: sizeFrmPnl
    * 
    * ===============================================================================
    */
   /**
    * Size frame and panels
    * 
    * Size the frame and panels to the correct size for the scale factor.
    * 
    * @param   None 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   private void sizeFrmPnl()
   {
      float                   vidScaleFact;
      float                   bgndScaleFact;
      int                     titlebarHeight = 0;
      int                     vidWidth;
      int                     vidHeight;
      int                     bgndWidth;
      int                     bgndHeight;
      int                     smVidWidth;
      int                     smVidHeight;
      int                     index;
      BasicInternalFrameTitlePane titlePane;
      
      
      if (fullScr)
      {
         vidScaleFact = VID_FULLSCR_SCALE_FACT;
         bgndScaleFact = FULLSCR_SCALE_FACT;
      }
      else
      {
         vidScaleFact = VID_PROT_SCALE_FACT;
         bgndScaleFact = PROT_SCALE_FACT;
      }
      vidWidth = (int)((HD_WIDTH * vidScaleFact) + 0.5f);
      vidHeight = (int)((HD_HEIGHT * vidScaleFact) + 0.5f);
      bgndWidth = (int)((HD_WIDTH * bgndScaleFact) + 0.5f);
      bgndHeight = (int)((HD_HEIGHT * bgndScaleFact) + 0.5f);
      smVidHeight = bgndHeight - vidHeight;
      smVidWidth = (smVidHeight * 16)/9;     /* Scale so 16:9 video works */

      /* First set up the video frame */
      for (index = 0; index < GlobInfo.NUM_VIDEO_CLIPS; index++)
      {
         vidFrame[index] = new JInternalFrame();
         if (index == 0)
         {
            titlebarHeight =((javax.swing.plaf.basic.BasicInternalFrameUI) vidFrame[0].getUI()).getNorthPane().getPreferredSize().height;
         }
         vidFrame[index].setBorder(null);
         vidFrame[index].setSize(vidWidth, vidHeight + titlebarHeight);
         vidFrame[index].setLocation((bgndWidth - vidWidth)/2, -titlebarHeight);
         titlePane = (BasicInternalFrameTitlePane) ((BasicInternalFrameUI) vidFrame[index].getUI()).  
            getNorthPane();  
         vidFrame[index].remove(titlePane);
         vidFrame[index].setVisible(true);
      }
      
      /* Next the background frame that takes up the whole window */
      bgndFrame.setBorder(null);
      bgndFrame.setSize(bgndWidth, bgndHeight + titlebarHeight);
      bgndFrame.setLocation(0, -titlebarHeight);
      bgndFrame.setBackground(Color.RED);
      bgndFrame.setVisible(true);
      titlePane =  
         (BasicInternalFrameTitlePane) ((BasicInternalFrameUI) bgndFrame.getUI()).  
         getNorthPane();  
      bgndFrame.remove(titlePane);
      
      /* Set up JPanels for content */
      leftColPanel.setBounds(0, 0, (bgndWidth - vidWidth)/2, vidHeight);
      leftColPanel.setBackground(Color.BLACK);
      bgndFrame.add(leftColPanel);
      rightColPanel.setBounds((bgndWidth - vidWidth)/2 + vidWidth, 0, (bgndWidth - vidWidth)/2, vidHeight);
      rightColPanel.setBackground(Color.BLACK);
      bgndFrame.add(rightColPanel);
      leftBotPanel.setBounds(0, vidHeight, (bgndWidth - smVidWidth)/2, smVidHeight);
      leftBotPanel.setBackground(Color.BLACK);
      bgndFrame.add(leftBotPanel);
      ctrBotPanel.setBounds((bgndWidth - smVidWidth)/2, vidHeight, smVidWidth, smVidHeight);
      ctrBotPanel.setBackground(Color.BLACK);
      bgndFrame.add(ctrBotPanel);
      rightBotPanel.setBounds((bgndWidth - smVidWidth)/2 + smVidWidth, vidHeight, (bgndWidth - smVidWidth)/2, smVidHeight);
      rightBotPanel.setBackground(Color.BLACK);
      bgndFrame.add(rightBotPanel);
      vidPanel.setBounds((bgndWidth - vidWidth)/2, 0, vidWidth, vidHeight);
      vidPanel.setBackground(Color.ORANGE);
      bgndFrame.add(vidPanel);
   } /* end sizeFrmPnl */
   
   /*
    * ===============================================================================
    * 
    * Name: createScoreLbl
    * 
    * ===============================================================================
    */
   /**
    * Create the score labels
    * 
    * Create and populate score labels.
    * 
    * @param   None 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   private void createScoreLbl()
   {
      int                     index;
      GridBagConstraints      con = new GridBagConstraints();
      Color                   orange = new Color(0xff8300);
      
      for (index = 0; index < NUM_PLAYERS; index++)
      {
         plyrScore[index] = new JLabel("0");
         plyrScore[index].setMinimumSize(new Dimension(400, 35));
         plyrScore[index].setForeground(orange);
         plyrScore[index].setOpaque(true);
         plyrScore[index].setBackground(Color.DARK_GRAY);
         plyrScore[index].setFont(new Font("Verdana", Font.PLAIN, 28));
         plyrScore[index].setHorizontalAlignment(JLabel.RIGHT);
         plyrScore[index].setHorizontalTextPosition(JLabel.RIGHT);
         plyrScore[index].setVerticalTextPosition(JLabel.CENTER);
      }
      con.insets = new Insets(10,10,10,10);
      con.gridheight = 1;
      con.gridwidth = 1;
      con.weightx = 1;
      con.weighty = 1;
      con.gridx = 0;
      con.gridy = 0;
      leftBotPanel.setLayout(new GridBagLayout());
      rightBotPanel.setLayout(new GridBagLayout());
      leftBotPanel.add(plyrScore[0], con);
      rightBotPanel.add(plyrScore[1], con);
      con.gridy = 1;
      leftBotPanel.add(plyrScore[2], con);
      rightBotPanel.add(plyrScore[3], con);
   } /* end createScoreLbl */
   
   /*
    * ===============================================================================
    * 
    * Name: initVideoFrms
    * 
    * ===============================================================================
    */
   /**
    * Initialize video frames
    * 
    * Set the content pane, and make it visible.
    * 
    * @param   video - video component 
    * @param   instance - instance number 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public void initVideoFrms(
         Component                        video,
         int                              instance)
   {
      vidFrame[instance].setContentPane((Container)video);
      vidFrame[instance].setVisible(true);
      /*
      vidFrame[instance].moveToFront(); */
   } /* end setVideoBgnd */

   /*
    * ===============================================================================
    * 
    * Name: playVideo
    * 
    * ===============================================================================
    */
   /**
    * Play a video by moving it to the front
    * 
    * @param   instance - instance number 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public void playVideo(
         int                              instance)
   {
      vidFrame[instance].moveToFront();
   } /* end setVideoBgnd */
   
   /*
    * ===============================================================================
    * 
    * Name: printMsg
    * 
    * ===============================================================================
    */
   /**
    * Print message
    * 
    * Print a message to the console frame, or if not created, to system.out.
    * 
    * @param   text - String with text to print 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public void printMsg(String text)
   {
      if (GlobInfo.consFrm == null)
      {
         System.out.println(text);
      }
      else
      {
         GlobInfo.consFrm.updateText(text + System.getProperty("line.separator"));
      }
   } /* end printMsg */
} /* End HostCtl */
