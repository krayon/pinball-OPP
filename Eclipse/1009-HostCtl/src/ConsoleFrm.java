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
 * @file:   ConsoleFrm.java
 * @author: Hugh Spahr
 * @date:   1/15/2013
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
 * This is the opens a console frame to write debug information.
 *
 *===============================================================================
 */

import java.awt.Color;
import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Rectangle;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.BorderFactory;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;

public class ConsoleFrm extends JFrame
{
   private static final long     serialVersionUID = -1;

   private JPanel                wholePanel;
   private JTextArea             textArea;
   
   /*
    * ===============================================================================
    * 
    * Name: ConsoleFrm
    * 
    * ===============================================================================
    */
   /**
    * Create console frame
    * 
    * Create a console frame to show debug information
    * 
    * @param   None 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public ConsoleFrm()
   {
      super("Console");
      
      addWindowListener(new WindowAdapter()
      {
         public void windowClosing(WindowEvent winEvt)
         {
           dispose();
         }
      });     

      /* Set up the panel */
      wholePanel = new JPanel(new GridBagLayout());
      wholePanel.setBackground(Color.BLACK);

      /* Set up text field */
      textArea = new JTextArea();
      textArea.setEditable(false);
      JScrollPane areaScrollPane = new JScrollPane(textArea);
      areaScrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
      areaScrollPane.setPreferredSize(new Dimension(300, 250));
      areaScrollPane.setBorder(BorderFactory.createCompoundBorder(
          BorderFactory.createRaisedBevelBorder(), BorderFactory.createLoweredBevelBorder()));
      
      wholePanel.add(areaScrollPane, new GridBagConstraints());

      add(wholePanel);
      setSize(340, 330);
      setResizable(false);
      
      setVisible(true);
   } /* end ConsoleFrm */
   
   /*
    * ===============================================================================
    * 
    * Name: updateText
    * 
    * ===============================================================================
    */
   /**
    * Update the text in the console window
    * 
    * Appends the text to the end of the window.  Sets the viewport appropriately.
    * 
    * @param   text - String with text to display 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public void updateText(
         String                  text)
   {
      textArea.append(text);
      textArea.scrollRectToVisible(new Rectangle(0,textArea.getHeight()-2,1,1));
   } /* end updateText */
} /* End ConsoleFrm */
