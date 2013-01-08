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
 * @date:   10/14/2005
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
 * File filter that only chooses *.hex, *.HEX, *.sx, *.SX files.  It is called  
 * when open file is used to import object files.
 *
 *===============================================================================
 */

import java.io.File;

import javax.swing.filechooser.FileFilter;

public class HexFilter extends FileFilter
{
   public boolean accept(File f)
   {
      /* Directories are cool */
      if (f.isDirectory())
      {
         return true;
      }

      String extension = getExtension(f);
      if (extension.equals("hex") || extension.equals("sx"))
      {
         return true;
      }
      return false;
   }

   public String getDescription()
   {
      return "Hex/S-Record files";
   }

   private String getExtension(File f)
   {
      String s = f.getName();
      int i = s.lastIndexOf('.');
      if (i > 0 && i < s.length() - 1)
      {
         return (s.substring(i + 1).toLowerCase());
      }
      return "";
   }
}
