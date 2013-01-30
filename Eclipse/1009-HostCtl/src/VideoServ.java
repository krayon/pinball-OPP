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
 * @file:   VideoServ.java
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
 * This class contains the video server.
 *
 *===============================================================================
 */

import javax.swing.SwingUtilities;

import uk.co.caprica.vlcj.binding.LibVlc;
import uk.co.caprica.vlcj.component.EmbeddedMediaPlayerComponent;
import uk.co.caprica.vlcj.runtime.RuntimeUtil;
import com.sun.jna.NativeLibrary;


public class VideoServ
{
   private EmbeddedMediaPlayerComponent   mediaComp[] = new EmbeddedMediaPlayerComponent[GlobInfo.NUM_VIDEO_CLIPS];
   private int                            currVideo = 0;
   private int                            createInst = 0;

   /*
    * ===============================================================================
    * 
    * Name: VideoWin
    * 
    * ===============================================================================
    */
   /**
    * Create a runnable video background.
    * 
    * Create the media player and start it running
    * 
    * @param   None 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public VideoServ() 
   {
      int                           index;
      
      for (index = 0; index < GlobInfo.NUM_VIDEO_CLIPS; index++)
      {
         SwingUtilities.invokeLater(new Runnable()
         {
            @Override
            public void run() 
            {
               this.CreateWin(createInst);
            }

            private void CreateWin(int instance)
            {
               mediaComp[instance] = new EmbeddedMediaPlayerComponent();
               if (instance == 0)
               {
                  mediaComp[instance].getMediaPlayer().prepareMedia("images\\DefconTest.mp4"); /* DefconTest.mp4 */
               }
               else
               {
                  mediaComp[instance].getMediaPlayer().prepareMedia("images\\Defcon17Loop.mp4");
               }
               GlobInfo.hostCtl.initVideoFrms(mediaComp[instance], instance);
               if (instance == 0)
               {
                  GlobInfo.hostCtl.playVideo(currVideo);
                  mediaComp[currVideo].getMediaPlayer().play();
               }
               createInst++;
            }
         });
      }
   }
   
   /*
    * ===============================================================================
    * 
    * Name: SwapVideo
    * 
    * ===============================================================================
    */
   /**
    * Swap video between the two video clips
    * 
    * Switch to the other video clip and start it playing.
    * 
    * @param   None 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public void SwapVideo()
   {
      mediaComp[currVideo].getMediaPlayer().stop();
      if (currVideo == 0)
      {
         currVideo = 1;
      }
      else
      {
         currVideo = 0;
      }
      GlobInfo.hostCtl.playVideo(currVideo);
      mediaComp[currVideo].getMediaPlayer().play();
   }
}
